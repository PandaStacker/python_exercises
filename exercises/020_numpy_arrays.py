"""020 — Vectorized arrays with NumPy

NumPy arrays carry a shape and dtype, and operations normally apply element by
element in compiled code.  An `axis` says which dimension an aggregation
collapses.  Broadcasting aligns compatible trailing dimensions, so a vector of
column statistics can operate on every row without a Python loop.  Boolean and
integer arrays can themselves be indexes.

Implement these functions without Python `for`/`while` loops or list
comprehensions.  Validate shape explicitly, return new arrays, and leave every
input untouched.  The tests inspect the source to reinforce vectorized
thinking rather than accepting a loop that happens to produce the same values.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def standardize_columns(values: ArrayLike) -> NDArray[np.float64]:
    """Return a 2-D float array with zero-mean, unit-variance columns.

    Require a non-empty 2-D input, raising `ValueError("expected a non-empty
    2-D array")` otherwise.  Use population standard deviation (`ddof=0`).
    A constant column standardizes to zeros rather than NaN or infinity.  A
    useful tool is `np.divide(..., out=..., where=...)`.
    """
    raise NotImplementedError


def pairwise_distances(points: ArrayLike) -> NDArray[np.float64]:
    """Return Euclidean distances between every pair of points.

    Input is a non-empty 2-D float-like array shaped `(points, dimensions)`.
    Use broadcasting by inserting singleton axes; return shape `(points,
    points)`.  Raise `ValueError("expected a non-empty 2-D array")` for a bad
    shape.
    """
    raise NotImplementedError


def one_hot(labels: ArrayLike, classes: int) -> NDArray[np.int64]:
    """Turn a 1-D integer label array into a `(labels, classes)` indicator.

    Require positive `classes`, a one-dimensional integer dtype, and labels in
    `[0, classes)`, raising ValueError for violations.  Create zeros and assign
    ones using two integer index arrays; do not build rows in Python.
    """
    raise NotImplementedError


def scale_channels(image: ArrayLike, gains: ArrayLike) -> NDArray[np.float64]:
    """Multiply each channel of an `(height, width, channels)` image by a gain.

    Require a 3-D image and a 1-D gain array with one entry per channel.  Raise
    `ValueError("incompatible image and gains")` otherwise.  Use broadcasting,
    clip values to `[0, 255]`, and return float64 without modifying the image.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing numpy arrays ---")
    try:
        arr = np.array([[1.0, 2.0], [3.0, 4.0]])
        print("Input array:")
        print(arr)
        print("standardize_columns output:")
        print(standardize_columns(arr))
    except Exception as e:
        print(f"Error: {e!r}")
