from __future__ import annotations

from typing import Any, List, Tuple

import numpy as np
import pct_tools_ext
from scipy.sparse import csr_matrix


def construct_matrix(
    filename: str,
    row_indexes: np.ndarray[int],
    col_indexes: np.ndarray[int],
    values: np.ndarray[np.float32],
    img_shape: Tuple[int, int],
    verbose_level: int,
) -> None:
    """Construct and store a matrix from a list of indices and values.

    Args:
        filename: The filename of the output file.
        row_indexes: The row indices of the matrix elements.
        col_indexes: The column indices of the matrix elements.
        values: The values of the matrix elements.
        img_shape: The expected shape of the image.
        verbose_level: The verbosity level.
    """
    return pct_tools_ext.construct_matrix(
        filename, row_indexes, col_indexes, values, img_shape, verbose_level
    )


def read_compressed_matrix(arg0: str) -> csr_matrix[np.float32]:
    """
    Read a compressed vector.
    """


def read_compressed_vector(arg0: str) -> np.ndarray[Any, np.float32]:
    """
    Read a compressed vector.
    """


def read_vector(arg0: str) -> np.ndarray[Any, np.float32]:
    """
    Read a vector.
    """


def recompress_matrix(arg0: str, arg1: int) -> None:
    """
    Load a matrix and store it with a given compression level.
    """


def store_compressed_vector(arg0: np.ndarray[Any, np.float32], arg1: str, arg2: int) -> None:
    """
    Compress and store a vector.
    """


def store_vector(x: np.ndarray[Any, np.float32], filename: str) -> None:
    """Store a vector."""
