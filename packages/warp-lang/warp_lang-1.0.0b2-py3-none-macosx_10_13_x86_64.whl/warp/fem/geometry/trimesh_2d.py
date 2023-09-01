import warp as wp

from warp.fem.types import ElementIndex, Coords, vec2i, Sample
from warp.fem.types import NULL_ELEMENT_INDEX, OUTSIDE, NULL_DOF_INDEX, NULL_QP_INDEX

from .geometry import Geometry
from .element import Triangle, LinearEdge
from .closest_point import project_on_tri_at_origin


@wp.struct
class Trimesh2DArg:
    tri_vertex_indices: wp.array2d(dtype=int)
    positions: wp.array(dtype=wp.vec2)

    vertex_tri_offsets: wp.array(dtype=int)
    vertex_tri_indices: wp.array(dtype=int)

    edge_vertex_indices: wp.array(dtype=vec2i)
    edge_tri_indices: wp.array(dtype=vec2i)


class Trimesh2D(Geometry):
    """Two-dimensional triangular mesh geometry"""

    def __init__(self, tri_vertex_indices: wp.array, positions: wp.array):
        """
        Constructs a two-dimensional triangular mesh.

        Args:
            tri_vertex_indices: warp array of shape (num_tris, 3) containing vertex indices for each tri
            positions: warp array of shape (num_vertices, 2) containing 2d position for each vertex

        """
        self.dimension = 2

        self.tri_vertex_indices = tri_vertex_indices
        self.positions = positions

        self._edge_vertex_indices: wp.array = None
        self._edge_tri_indices: wp.array = None
        self._vertex_tri_offsets: wp.array = None
        self._vertex_tri_indices: wp.array = None

        self._build_topology()

    def cell_count(self):
        return self.tri_vertex_indices.shape[0]

    def vertex_count(self):
        return self.positions.shape[0]

    def side_count(self):
        return self._edge_vertex_indices.shape[0]

    def boundary_side_count(self):
        return self._boundary_edge_indices.shape[0]

    def reference_cell(self) -> Triangle:
        return Triangle()

    def reference_side(self) -> LinearEdge:
        return LinearEdge()

    CellArg = Trimesh2DArg
    SideArg = Trimesh2DArg

    @wp.struct
    class SideIndexArg:
        boundary_edge_indices: wp.array(dtype=int)

    # Geometry device interface

    def cell_arg_value(self, device) -> CellArg:
        args = self.CellArg()

        args.tri_vertex_indices = self.tri_vertex_indices.to(device)
        args.positions = self.positions.to(device)
        args.edge_vertex_indices = self._edge_vertex_indices.to(device)
        args.edge_tri_indices = self._edge_tri_indices.to(device)
        args.vertex_tri_offsets = self._vertex_tri_offsets.to(device)
        args.vertex_tri_indices = self._vertex_tri_indices.to(device)

        return args

    @wp.func
    def cell_position(args: CellArg, s: Sample):
        tri_idx = args.tri_vertex_indices[s.element_index]
        return (
            s.element_coords[0] * args.positions[tri_idx[0]]
            + s.element_coords[1] * args.positions[tri_idx[1]]
            + s.element_coords[2] * args.positions[tri_idx[2]]
        )

    @wp.func
    def _project_on_tri(args: CellArg, pos: wp.vec2, tri_index: int):
        p0 = args.positions[args.tri_vertex_indices[tri_index, 0]]

        q = pos - p0
        e1 = args.positions[args.tri_vertex_indices[tri_index, 1]] - p0
        e2 = args.positions[args.tri_vertex_indices[tri_index, 2]] - p0

        dist, coords = project_on_tri_at_origin(q, e1, e2)
        return dist, coords

    @wp.func
    def cell_lookup(args: CellArg, pos: wp.vec2, guess: Sample):
        closest_tri = int(NULL_ELEMENT_INDEX)
        closest_coords = Coords(OUTSIDE)
        closest_dist = float(1.0e8)

        for v in range(3):
            vtx = args.tri_vertex_indices[guess.element_index, v]
            tri_beg = args.vertex_tri_offsets[vtx]
            tri_end = args.vertex_tri_offsets[vtx + 1]

            for t in range(tri_beg, tri_end):
                tri = args.vertex_tri_indices[t]
                dist, coords = Trimesh2D._project_on_tri(args, pos, tri)
                if dist <= closest_dist:
                    closest_dist = dist
                    closest_tri = tri
                    closest_coords = coords

        return Sample(closest_tri, closest_coords, NULL_QP_INDEX, 0.0, NULL_DOF_INDEX, NULL_DOF_INDEX)

    @wp.func
    def cell_measure(args: CellArg, cell_index: ElementIndex, coords: Coords):
        tri_idx = args.tri_vertex_indices[cell_index]

        v0 = args.positions[tri_idx[0]]
        v1 = args.positions[tri_idx[1]]
        v2 = args.positions[tri_idx[2]]

        e1 = v1 - v0
        e2 = v2 - v0

        return 0.5 * wp.abs(e1[0] * e2[1] - e1[1] * e2[0])

    @wp.func
    def cell_measure(args: CellArg, s: Sample):
        return Trimesh2D.cell_measure(args, s.element_index, s.element_coords)

    @wp.func
    def cell_measure_ratio(args: CellArg, s: Sample):
        return 1.0

    @wp.func
    def cell_normal(args: CellArg, s: Sample):
        return wp.vec2(0.0)

    def side_arg_value(self, device) -> SideArg:
        return self.cell_arg_value(device)

    def side_index_arg_value(self, device) -> SideIndexArg:
        args = self.SideIndexArg()

        args.boundary_edge_indices = self._boundary_edge_indices.to(device)

        return args

    @wp.func
    def boundary_side_index(args: SideIndexArg, boundary_side_index: int):
        """Boundary side to side index"""

        return args.boundary_edge_indices[boundary_side_index]

    @wp.func
    def side_position(args: SideArg, s: Sample):
        edge_idx = args.edge_vertex_indices[s.element_index]
        return (1.0 - s.element_coords[0]) * args.positions[edge_idx[0]] + s.element_coords[0] * args.positions[
            edge_idx[1]
        ]

    @wp.func
    def side_measure(args: SideArg, side_index: ElementIndex, coords: Coords):
        edge_idx = args.edge_vertex_indices[side_index]
        v0 = args.positions[edge_idx[0]]
        v1 = args.positions[edge_idx[1]]
        return wp.length(v1 - v0)

    @wp.func
    def side_measure(args: SideArg, s: Sample):
        return Trimesh2D.side_measure(args, s.element_index, s.element_coords)

    @wp.func
    def side_measure_ratio(args: SideArg, s: Sample):
        inner = Trimesh2D.side_inner_cell_index(args, s.element_index)
        outer = Trimesh2D.side_outer_cell_index(args, s.element_index)
        return Trimesh2D.side_measure(args, s) / wp.min(
            Trimesh2D.cell_measure(args, inner, Coords()),
            Trimesh2D.cell_measure(args, outer, Coords()),
        )

    @wp.func
    def side_normal(args: SideArg, s: Sample):
        edge_idx = args.edge_vertex_indices[s.element_index]
        v0 = args.positions[edge_idx[0]]
        v1 = args.positions[edge_idx[1]]
        e = v1 - v0

        return wp.normalize(wp.vec2(-e[1], e[0]))

    @wp.func
    def side_inner_cell_index(arg: SideArg, side_index: ElementIndex):
        return arg.edge_tri_indices[side_index][0]

    @wp.func
    def side_outer_cell_index(arg: SideArg, side_index: ElementIndex):
        return arg.edge_tri_indices[side_index][1]

    @wp.func
    def edge_to_tri_coords(args: SideArg, side_index: ElementIndex, tri_index: ElementIndex, side_coords: Coords):
        edge_vidx = args.edge_vertex_indices[side_index]
        tri_vidx = args.tri_vertex_indices[tri_index]

        v0 = tri_vidx[0]
        v1 = tri_vidx[1]

        cx = float(0.0)
        cy = float(0.0)
        cz = float(0.0)

        if edge_vidx[0] == v0:
            cx = 1.0 - side_coords[0]
        elif edge_vidx[0] == v1:
            cy = 1.0 - side_coords[0]
        else:
            cz = 1.0 - side_coords[0]

        if edge_vidx[1] == v0:
            cx = side_coords[0]
        elif edge_vidx[1] == v1:
            cy = side_coords[0]
        else:
            cz = side_coords[0]

        return Coords(cx, cy, cz)

    @wp.func
    def tri_to_edge_coords(args: SideArg, side_index: ElementIndex, tri_index: ElementIndex, tri_coords: Coords):
        edge_vidx = args.edge_vertex_indices[side_index]
        tri_vidx = args.tri_vertex_indices[tri_index]

        start = int(2)
        end = int(2)

        for k in range(2):
            v = tri_vidx[k]
            if edge_vidx[1] == v:
                end = k
            elif edge_vidx[0] == v:
                start = k

        return wp.select(
            tri_coords[start] + tri_coords[end] > 0.999, Coords(OUTSIDE), Coords(tri_coords[end], 0.0, 0.0)
        )

    def _build_topology(self):
        from warp.fem.utils import compress_node_indices, masked_indices, _get_pinned_temp_count_buffer
        from warp.utils import array_scan

        device = self.tri_vertex_indices.device

        self._vertex_tri_offsets, self._vertex_tri_indices, _, __ = compress_node_indices(
            self.vertex_count(), self.tri_vertex_indices
        )

        vertex_start_edge_count = wp.zeros(dtype=int, device=device, shape=self.vertex_count())
        vertex_start_edge_offsets = wp.empty_like(vertex_start_edge_count)

        vertex_edge_ends = wp.empty(dtype=int, device=device, shape=(3 * self.cell_count()))
        vertex_edge_tris = wp.empty(dtype=int, device=device, shape=(3 * self.cell_count(), 2))

        # Count face edges starting at each vertex
        wp.launch(
            kernel=Trimesh2D._count_starting_edges_kernel,
            device=device,
            dim=self.cell_count(),
            inputs=[self.tri_vertex_indices, vertex_start_edge_count],
        )

        array_scan(in_array=vertex_start_edge_count, out_array=vertex_start_edge_offsets, inclusive=False)

        # Count number of unique edges (deduplicate across faces)
        vertex_unique_edge_count = vertex_start_edge_count
        wp.launch(
            kernel=Trimesh2D._count_unique_starting_edges_kernel,
            device=device,
            dim=self.vertex_count(),
            inputs=[
                self._vertex_tri_offsets,
                self._vertex_tri_indices,
                self.tri_vertex_indices,
                vertex_start_edge_offsets,
                vertex_unique_edge_count,
                vertex_edge_ends,
                vertex_edge_tris,
            ],
        )

        vertex_unique_edge_offsets = wp.empty_like(vertex_start_edge_offsets)
        array_scan(in_array=vertex_start_edge_count, out_array=vertex_unique_edge_offsets, inclusive=False)

        # Get back edge count to host
        if device.is_cuda:
            edge_count = _get_pinned_temp_count_buffer(device)
            # Last vertex will not own any edge, so its count will be zero; just fetching last prefix count is ok
            wp.copy(dest=edge_count, src=vertex_unique_edge_offsets, src_offset=self.vertex_count() - 1, count=1)
            wp.synchronize_stream(wp.get_stream())
            edge_count = int(edge_count.numpy()[0])
        else:
            edge_count = int(vertex_unique_edge_offsets.numpy()[self.vertex_count() - 1])

        self._edge_vertex_indices = wp.empty(shape=(edge_count,), dtype=vec2i, device=device)
        self._edge_tri_indices = wp.empty(shape=(edge_count,), dtype=vec2i, device=device)

        boundary_mask = wp.empty(shape=(edge_count,), dtype=int, device=device)

        # Compress edge data
        wp.launch(
            kernel=Trimesh2D._compress_edges_kernel,
            device=device,
            dim=self.vertex_count(),
            inputs=[
                vertex_start_edge_offsets,
                vertex_unique_edge_offsets,
                vertex_unique_edge_count,
                vertex_edge_ends,
                vertex_edge_tris,
                self._edge_vertex_indices,
                self._edge_tri_indices,
                boundary_mask,
            ],
        )

        # Flip normals if necessary
        wp.launch(
            kernel=Trimesh2D._flip_edge_normals,
            device=device,
            dim=self.side_count(),
            inputs=[self._edge_vertex_indices, self._edge_tri_indices, self.tri_vertex_indices, self.positions],
        )

        self._boundary_edge_indices, _ = masked_indices(boundary_mask)

    @wp.kernel
    def _count_starting_edges_kernel(
        tri_vertex_indices: wp.array2d(dtype=int), vertex_start_edge_count: wp.array(dtype=int)
    ):
        t = wp.tid()
        for k in range(3):
            v0 = tri_vertex_indices[t, k]
            v1 = tri_vertex_indices[t, (k + 1) % 3]

            if v0 < v1:
                wp.atomic_add(vertex_start_edge_count, v0, 1)
            else:
                wp.atomic_add(vertex_start_edge_count, v1, 1)

    @wp.func
    def _find(
        needle: int,
        values: wp.array(dtype=int),
        beg: int,
        end: int,
    ):
        for i in range(beg, end):
            if values[i] == needle:
                return i

        return -1

    @wp.kernel
    def _count_unique_starting_edges_kernel(
        vertex_tri_offsets: wp.array(dtype=int),
        vertex_tri_indices: wp.array(dtype=int),
        tri_vertex_indices: wp.array2d(dtype=int),
        vertex_start_edge_offsets: wp.array(dtype=int),
        vertex_start_edge_count: wp.array(dtype=int),
        edge_ends: wp.array(dtype=int),
        edge_tris: wp.array2d(dtype=int),
    ):
        v = wp.tid()

        edge_beg = vertex_start_edge_offsets[v]

        tri_beg = vertex_tri_offsets[v]
        tri_end = vertex_tri_offsets[v + 1]

        edge_cur = edge_beg

        for tri in range(tri_beg, tri_end):
            t = vertex_tri_indices[tri]

            for k in range(3):
                v0 = tri_vertex_indices[t, k]
                v1 = tri_vertex_indices[t, (k + 1) % 3]

                if v == wp.min(v0, v1):
                    other_v = wp.max(v0, v1)

                    # Check if other_v has been seen
                    seen_idx = Trimesh2D._find(other_v, edge_ends, edge_beg, edge_cur)

                    if seen_idx == -1:
                        edge_ends[edge_cur] = other_v
                        edge_tris[edge_cur, 0] = t
                        edge_tris[edge_cur, 1] = t
                        edge_cur += 1
                    else:
                        edge_tris[seen_idx, 1] = t

        vertex_start_edge_count[v] = edge_cur - edge_beg

    @wp.kernel
    def _compress_edges_kernel(
        vertex_start_edge_offsets: wp.array(dtype=int),
        vertex_unique_edge_offsets: wp.array(dtype=int),
        vertex_unique_edge_count: wp.array(dtype=int),
        uncompressed_edge_ends: wp.array(dtype=int),
        uncompressed_edge_tris: wp.array2d(dtype=int),
        edge_vertex_indices: wp.array(dtype=vec2i),
        edge_tri_indices: wp.array(dtype=vec2i),
        boundary_mask: wp.array(dtype=int),
    ):
        v = wp.tid()

        start_beg = vertex_start_edge_offsets[v]
        unique_beg = vertex_unique_edge_offsets[v]
        unique_count = vertex_unique_edge_count[v]

        for e in range(unique_count):
            src_index = start_beg + e
            edge_index = unique_beg + e

            edge_vertex_indices[edge_index] = vec2i(v, uncompressed_edge_ends[src_index])

            t0 = uncompressed_edge_tris[src_index, 0]
            t1 = uncompressed_edge_tris[src_index, 1]
            edge_tri_indices[edge_index] = vec2i(t0, t1)
            if t0 == t1:
                boundary_mask[edge_index] = 1
            else:
                boundary_mask[edge_index] = 0

    @wp.kernel
    def _flip_edge_normals(
        edge_vertex_indices: wp.array(dtype=vec2i),
        edge_tri_indices: wp.array(dtype=vec2i),
        tri_vertex_indices: wp.array2d(dtype=int),
        positions: wp.array(dtype=wp.vec2),
    ):
        e = wp.tid()

        tri = edge_tri_indices[e][0]

        tri_vidx = tri_vertex_indices[tri]
        edge_vidx = edge_vertex_indices[e]

        tri_centroid = (positions[tri_vidx[0]] + positions[tri_vidx[1]] + positions[tri_vidx[2]]) / 3.0

        v0 = positions[edge_vidx[0]]
        v1 = positions[edge_vidx[1]]

        edge_center = 0.5 * (v1 + v0)
        edge_vec = v1 - v0
        edge_normal = wp.vec2(-edge_vec[1], edge_vec[0])

        # if edge normal points toward first triangle centroid, flip indices
        if wp.dot(tri_centroid - edge_center, edge_normal) > 0.0:
            edge_vertex_indices[e] = vec2i(edge_vidx[1], edge_vidx[0])
