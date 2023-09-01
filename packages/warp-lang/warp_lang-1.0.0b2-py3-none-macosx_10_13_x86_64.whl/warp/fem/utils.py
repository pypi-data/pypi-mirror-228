from typing import Any, Tuple

import warp as wp
from warp.utils import radix_sort_pairs, runlength_encode, array_scan

from .types import vec6


@wp.func
def generalized_outer(x: Any, y: wp.vec2):
    return wp.outer(x, y)


@wp.func
def generalized_outer(x: Any, y: wp.vec3):
    return wp.outer(x, y)


@wp.func
def generalized_outer(x: Any, y: wp.float32):
    return x * y


@wp.func
def unit_element(template_type: wp.float32, coord: int):
    return 1.0


@wp.func
def unit_element(template_type: wp.vec2, coord: int):
    t = wp.vec2(0.0)
    t[coord] = 1.0
    return t


@wp.func
def unit_element(template_type: wp.vec3, coord: int):
    t = wp.vec3(0.0)
    t[coord] = 1.0
    return t


@wp.func
def unit_element(template_type: vec6, coord: int):
    t = vec6(0.0)
    t[coord] = 1.0
    return t


@wp.func
def unit_element(template_type: wp.mat22, coord: int):
    t = wp.mat22(0.0)
    t[coord // 2, coord % 2] = 1.0
    return t


@wp.func
def unit_element(template_type: wp.mat33, coord: int):
    t = wp.mat22(0.0)
    t[coord // 3, coord % 3] = 1.0
    return t


@wp.func
def symmetric_part(x: wp.mat22):
    off_diag = 0.5 * (x[0, 1] + x[1, 0])
    return wp.mat22(x[0, 0], off_diag, off_diag, x[1, 1])


@wp.func
def symmetric_part(x: wp.mat33):
    d = 0.5 * (x[1, 2] + x[2, 1])
    e = 0.5 * (x[2, 0] + x[0, 2])
    f = 0.5 * (x[0, 1] + x[1, 0])
    return wp.mat33(x[0, 0], f, e, f, x[1, 1], d, e, d, x[2, 2])


def compress_node_indices(
    node_count: int, node_indices: wp.array(dtype=int)
) -> Tuple[wp.array, wp.array, int, wp.array]:
    """
    Compress an unsorted list of node indices into:
     - a node_offsets array, giving for each node the start offset of corresponding indices in sorted_array_indices
     - a sorted_array_indices array, listing the indices in the input array corresponding to each node
     - the number of unique node indices
     - a unique_node_indices array containg the sorted list of unique node indices (i.e. the list of indices i for which node_offsets[i] < node_offsets[i+1])
    """

    index_count = node_indices.size
    sorted_node_indices = wp.empty(2 * index_count, dtype=int, device=node_indices.device)
    sorted_array_indices = wp.empty_like(sorted_node_indices)

    wp.copy(dest=sorted_node_indices, src=node_indices, count=index_count)

    indices_per_element = 1 if node_indices.ndim == 1 else node_indices.shape[-1]
    wp.launch(
        kernel=_iota_kernel,
        dim=index_count,
        inputs=[sorted_array_indices, indices_per_element],
        device=sorted_array_indices.device,
    )

    # Sort indices
    radix_sort_pairs(sorted_node_indices, sorted_array_indices, count=index_count)

    # Build prefix sum of number of elements per node
    unique_node_indices = wp.empty(n=index_count, dtype=int, device=node_indices.device)
    node_element_counts = wp.empty(n=index_count, dtype=int, device=node_indices.device)
    unique_node_count = runlength_encode(
        sorted_node_indices, unique_node_indices, node_element_counts, value_count=index_count
    )

    # Scatter seen run counts to global array of element count per node
    node_offsets = wp.zeros(shape=(node_count + 1), device=node_element_counts.device, dtype=int)
    wp.launch(
        kernel=_scatter_node_counts,
        dim=unique_node_count,
        inputs=[node_element_counts, unique_node_indices, node_offsets],
        device=node_offsets.device,
    )

    # Prefix sum of number of elements per node
    array_scan(node_offsets, node_offsets, inclusive=True)

    return node_offsets, sorted_array_indices, unique_node_count, unique_node_indices


_pinned_temp_count_buffer = {}


def _get_pinned_temp_count_buffer(device):
    device = str(device)
    if device not in _pinned_temp_count_buffer:
        _pinned_temp_count_buffer[device] = wp.empty(shape=(1,), dtype=int, pinned=True, device="cpu")

    return _pinned_temp_count_buffer[device]


def masked_indices(mask: wp.array(dtype=int), missing_index=-1) -> Tuple[wp.array, wp.array]:
    """
    From an array of boolean masks (must be either 0 or 1), returns:
      - The list of indices for which the mask is 1
      - A map associating to each element of the input mask array its local index if non-zero, or missing_index if zero.
    """

    offsets = wp.empty_like(mask)

    wp.utils.array_scan(mask, offsets, inclusive=True)

    # Get back total counts on host
    if offsets.device.is_cuda:
        masked_count = _get_pinned_temp_count_buffer(offsets.device)
        wp.copy(dest=masked_count, src=offsets, src_offset=offsets.shape[0] - 1, count=1)
        wp.synchronize_stream(wp.get_stream())
        masked_count = int(masked_count.numpy()[0])
    else:
        masked_count = int(offsets.numpy()[-1])

    # Convert counts to indices
    indices = wp.empty(n=masked_count, device=mask.device, dtype=int)

    wp.launch(
        kernel=_masked_indices_kernel,
        dim=offsets.shape,
        inputs=[missing_index, mask, offsets, indices, offsets],
        device=mask.device,
    )

    return indices, offsets


def array_axpy(x: wp.array, y: wp.array, alpha: float = 1.0, beta: float = 1.0):
    """Performs y = alpha*x + beta*y"""

    dtype = wp.types.type_scalar_type(x.dtype)

    alpha = dtype(alpha)
    beta = dtype(beta)

    if x.dtype != y.dtype or x.shape != y.shape or x.device != y.device:
        raise ValueError("x and y arrays must have same dat atype, shape and device")

    wp.launch(kernel=_array_axpy_kernel, dim=x.shape, device=x.device, inputs=[x, y, alpha, beta])


@wp.kernel
def _iota_kernel(indices: wp.array(dtype=int), divisor: int):
    indices[wp.tid()] = wp.tid() // divisor


@wp.kernel
def _scatter_node_counts(
    unique_counts: wp.array(dtype=int), unique_node_indices: wp.array(dtype=int), node_counts: wp.array(dtype=int)
):
    i = wp.tid()
    node_counts[1 + unique_node_indices[i]] = unique_counts[i]


@wp.kernel
def _masked_indices_kernel(
    missing_index: int,
    mask: wp.array(dtype=int),
    offsets: wp.array(dtype=int),
    masked_to_global: wp.array(dtype=int),
    global_to_masked: wp.array(dtype=int),
):
    i = wp.tid()

    if mask[i] == 0:
        global_to_masked[i] = missing_index
    else:
        masked_idx = offsets[i] - 1
        global_to_masked[i] = masked_idx
        masked_to_global[masked_idx] = i


@wp.kernel
def _array_axpy_kernel(x: wp.array(dtype=Any), y: wp.array(dtype=Any), alpha: Any, beta: Any):
    i = wp.tid()
    y[i] = beta * y[i] + alpha * x[i]
