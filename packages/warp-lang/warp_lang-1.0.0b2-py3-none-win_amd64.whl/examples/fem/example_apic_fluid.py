import os
import math
from typing import Any

import warp as wp
import numpy as np

import warp.sim.render
from warp.sim import Model, State

from warp.fem.geometry import Grid3D
from warp.fem.domain import Cells, BoundarySides
from warp.fem.space import make_polynomial_space
from warp.fem.quadrature import PicQuadrature
from warp.fem.field import make_test, make_trial
from warp.fem.types import vec3i, Field, Sample, Domain
from warp.fem.integrate import integrate
from warp.fem.operator import integrand, lookup, normal, grad, at_node, div
from warp.fem.dirichlet import normalize_dirichlet_projector

from warp.sparse import bsr_mv, bsr_copy, bsr_mm, bsr_transposed, BsrMatrix

from bsr_utils import bsr_cg


@integrand
def integrate_fraction(s: Sample, phi: Field):
    return phi(s)


@integrand
def integrate_velocity(
    s: Sample,
    domain: Domain,
    u: Field,
    velocities: wp.array(dtype=wp.vec3),
    velocity_gradients: wp.array(dtype=wp.mat33),
    dt: float,
    gravity: wp.vec3,
):
    """Transfer particle velocities to grid"""
    node_offset = domain(at_node(u, s)) - domain(s)
    vel_apic = velocities[s.qp_index] + velocity_gradients[s.qp_index] * node_offset

    vel_adv = vel_apic + dt * gravity
    return wp.dot(u(s), vel_adv)


@integrand
def update_particles(
    s: Sample,
    domain: Domain,
    grid_vel: Field,
    dt: float,
    pos: wp.array(dtype=wp.vec3),
    pos_prev: wp.array(dtype=wp.vec3),
    vel: wp.array(dtype=wp.vec3),
    vel_grad: wp.array(dtype=wp.mat33),
):
    """Read particle velocity from grid and advect positions"""
    vel[s.qp_index] = grid_vel(s)
    vel_grad[s.qp_index] = grad(grid_vel, s)

    pos_adv = pos_prev[s.qp_index] + dt * vel[s.qp_index]

    # Project onto domain
    pos_proj = domain(lookup(domain, pos_adv))
    pos[s.qp_index] = pos_proj

    return 0.0


@integrand
def velocity_boundary_projector_form(s: Sample, domain: Domain, u: Field, v: Field):
    """Projector for velocity-Dirichlet boundary conditions"""

    n = normal(domain, s)
    if n[1] > 0.0:
        # Neuman  on top
        return 0.0

    # Free-slip on other sides
    return wp.dot(u(s), n) * wp.dot(v(s), n)


@integrand
def divergence_form(s: Sample, u: Field, psi: Field):
    return div(u, s) * psi(s)


@wp.kernel
def invert_volume_kernel(values: wp.array(dtype=float)):
    i = wp.tid()
    m = values[i]
    if m <= 1.0e-8:
        values[i] = 0.0
    else:
        values[i] = 1.0 / m


@wp.kernel
def scalar_vector_multiply(
    alpha: wp.array(dtype=float),
    x: wp.array(dtype=wp.vec3),
    y: wp.array(dtype=wp.vec3),
):
    i = wp.tid()
    y[i] = alpha[i] * x[i]


@wp.kernel
def scale_transposed_divergence_mat(
    tr_divergence_mat_offsets: wp.array(dtype=int),
    tr_divergence_mat_values: wp.array(dtype=wp.mat(shape=(3, 1), dtype=float)),
    inv_fraction_int: wp.array(dtype=float),
):
    u_i = wp.tid()
    block_beg = tr_divergence_mat_offsets[u_i]
    block_end = tr_divergence_mat_offsets[u_i + 1]

    for b in range(block_beg, block_end):
        tr_divergence_mat_values[b] = tr_divergence_mat_values[b] * inv_fraction_int[u_i]


def solve_incompressibility(
    divergence_mat: BsrMatrix,
    inv_volume,
    pressure,
    velocity,
):
    """Solve for divergence-free velocity delta:

    delta_velocity = inv_volume * transpose(divergence_mat) * pressure
    divergence_mat * (velocity + delta_velocity) = 0
    """

    # Build transposed gradient matrix, scale with inverse fraction
    transposed_divergence_mat = bsr_transposed(divergence_mat)
    wp.launch(
        kernel=scale_transposed_divergence_mat,
        dim=inv_volume.shape[0],
        inputs=[
            transposed_divergence_mat.offsets,
            transposed_divergence_mat.values,
            inv_volume,
        ],
    )

    # For simplicity, assemble schur complement and solve with CG
    schur = bsr_mm(divergence_mat, transposed_divergence_mat)

    rhs = wp.zeros_like(pressure)
    bsr_mv(A=divergence_mat, x=velocity, y=rhs, alpha=-1.0, beta=0.0)
    bsr_cg(schur, b=rhs, x=pressure)

    # Apply pressure to velocity
    bsr_mv(A=transposed_divergence_mat, x=pressure, y=velocity, alpha=1.0, beta=1.0)


class Example:
    def __init__(self, stage):
        self.frame_dt = 1.0 / 60
        self.frame_count = 1000

        self.sim_substeps = 1
        self.sim_dt = self.frame_dt / self.sim_substeps
        self.sim_steps = self.frame_count * self.sim_substeps
        self.sim_time = 0.0

        # grid dimensions and particle emission
        grid_res = np.array([32, 64, 16], dtype=int)
        particle_fill_frac = np.array([0.5, 0.5, 1.0])
        grid_lo = wp.vec3(0.0)
        grid_hi = wp.vec3(50, 100, 25)

        grid_cell_size = np.array(grid_hi - grid_lo) / grid_res
        grid_cell_volume = np.prod(grid_cell_size)

        PARTICLES_PER_CELL_DIM = 3
        self.radius = np.max(grid_cell_size) / (2 * PARTICLES_PER_CELL_DIM)

        particle_grid_res = np.array(particle_fill_frac * grid_res * PARTICLES_PER_CELL_DIM, dtype=int)
        particle_grid_offset = self.radius * np.ones(3)

        np.random.seed(0)
        builder = wp.sim.ModelBuilder()
        builder.add_particle_grid(
            dim_x=particle_grid_res[0],
            dim_y=particle_grid_res[1],
            dim_z=particle_grid_res[2],
            cell_x=self.radius * 2.0,
            cell_y=self.radius * 2.0,
            cell_z=self.radius * 2.0,
            pos=(0.0, 0.0, 0.0) + particle_grid_offset,
            rot=wp.quat_identity(),
            vel=(0.0, 0.0, 0.0),
            mass=grid_cell_volume / PARTICLES_PER_CELL_DIM**3,
            jitter=self.radius * 1.0,
            radius_mean=self.radius,
        )

        self.grid = Grid3D(vec3i(grid_res), grid_lo, grid_hi)

        # Function spaces
        self.velocity_space = make_polynomial_space(self.grid, dtype=wp.vec3, degree=1)
        self.fraction_space = make_polynomial_space(self.grid, dtype=float, degree=1)
        self.strain_space = make_polynomial_space(
            self.grid,
            dtype=float,
            degree=0,
        )

        self.pressure_field = self.strain_space.make_field()
        self.velocity_field = self.velocity_space.make_field()

        # Test and trial functions
        self.domain = Cells(self.grid)
        self.velocity_test = make_test(self.velocity_space, domain=self.domain)
        self.velocity_trial = make_trial(self.velocity_space, domain=self.domain)
        self.fraction_test = make_test(self.fraction_space, domain=self.domain)
        self.strain_test = make_test(self.strain_space, domain=self.domain)
        self.strain_trial = make_trial(self.strain_space, domain=self.domain)

        # Enforcing the Dirichlet boundary condition the hard way;
        # build projector for velocity left- and right-hand-sides
        boundary = BoundarySides(self.grid)
        u_bd_test = make_test(space=self.velocity_space, domain=boundary)
        u_bd_trial = make_trial(space=self.velocity_space, domain=boundary)
        u_bd_projector = integrate(
            velocity_boundary_projector_form, fields={"u": u_bd_trial, "v": u_bd_test}, nodal=True, output_dtype=float
        )

        normalize_dirichlet_projector(u_bd_projector)
        self.vel_bd_projector = u_bd_projector

        # Warp.sim model
        self.model: Model = builder.finalize()

        print("Particle count:", self.model.particle_count)

        self.state_0: State = self.model.state()
        self.state_0.particle_qd_grad = wp.zeros(shape=(self.model.particle_count), dtype=wp.mat33)

        self.state_1: State = self.model.state()
        self.state_1.particle_qd_grad = wp.zeros(shape=(self.model.particle_count), dtype=wp.mat33)

        self.renderer = wp.sim.render.SimRenderer(self.model, stage, scaling=20.0)

    def update(self, frame_index):
        with wp.ScopedTimer(f"simulate frame {frame_index}", active=True):
            for s in range(self.sim_substeps):
                # Bin particles to grid cells
                pic = PicQuadrature(
                    domain=Cells(self.grid), positions=self.state_0.particle_q, measures=self.model.particle_mass
                )

                # Inverse volume fraction
                fraction_test = make_test(space=self.fraction_space, domain=pic.domain)
                inv_volume = integrate(
                    integrate_fraction,
                    quadrature=pic,
                    fields={"phi": fraction_test},
                    accumulate_dtype=float,
                )
                wp.launch(kernel=invert_volume_kernel, dim=inv_volume.shape, inputs=[inv_volume])

                # Velocity right-hand side
                velocity_int = integrate(
                    integrate_velocity,
                    quadrature=pic,
                    fields={"u": self.velocity_test},
                    values={
                        "velocities": self.state_0.particle_qd,
                        "velocity_gradients": self.state_0.particle_qd_grad,
                        "dt": self.sim_dt,
                        "gravity": self.model.gravity,
                    },
                    accumulate_dtype=float,
                    output_dtype=wp.vec3,
                )

                # Compute constraint-free velocity
                wp.launch(
                    kernel=scalar_vector_multiply,
                    dim=inv_volume.shape[0],
                    inputs=[inv_volume, velocity_int, self.velocity_field.dof_values],
                )

                # Apply velocity boundary conditions:
                # velocity -= vel_bd_projector * velocity
                wp.copy(src=self.velocity_field.dof_values, dest=velocity_int)
                bsr_mv(A=self.vel_bd_projector, x=velocity_int, y=self.velocity_field.dof_values, alpha=-1.0, beta=1.0)

                # Divergence matrix
                divergence_mat = integrate(
                    divergence_form,
                    quadrature=pic,
                    fields={"u": self.velocity_trial, "psi": self.strain_test},
                    accumulate_dtype=float,
                    output_dtype=float,
                )

                # Project matrix to enforce boundary conditions
                divergence_mat_tmp = bsr_copy(divergence_mat)
                bsr_mm(alpha=-1.0, x=divergence_mat_tmp, y=self.vel_bd_projector, z=divergence_mat, beta=1.0)

                # Solve unilateral incompressibility
                solve_incompressibility(
                    divergence_mat,
                    inv_volume,
                    self.pressure_field.dof_values,
                    self.velocity_field.dof_values,
                )

                # (A)PIC advection
                integrate(
                    update_particles,
                    quadrature=pic,
                    values={
                        "pos": self.state_1.particle_q,
                        "pos_prev": self.state_0.particle_q,
                        "vel": self.state_1.particle_qd,
                        "vel_grad": self.state_1.particle_qd_grad,
                        "dt": self.sim_dt,
                    },
                    fields={"grid_vel": self.velocity_field},
                )

                # swap states
                (self.state_0, self.state_1) = (self.state_1, self.state_0)

    def render(self, is_live=False):
        with wp.ScopedTimer("render", active=True):
            time = 0.0 if is_live else self.sim_time

            self.renderer.begin_frame(time)
            self.renderer.render(self.state_0)
            self.renderer.end_frame()

        self.sim_time += self.frame_dt


if __name__ == "__main__":
    wp.set_module_options({"enable_backward": False})
    wp.init()

    stage_path = os.path.join(os.path.dirname(__file__), "outputs/example_sim_apic.usd")

    example = Example(stage_path)

    for i in range(example.frame_count):
        example.update(i)
        example.render()

    example.renderer.save()
