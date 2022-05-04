import numpy as np


def fix_lastknown(vec: np.array) -> None:
    """
    Fix all nan values in vector to Last Known Good Value.
    If first value is missing, it will remain nan.

    Args:
        vec: vector of values to change

    Returns:

    """
    prev_elem = None
    for i, elem in enumerate(vec):
        if np.isnan(elem):
            vec[i] = prev_elem
        prev_elem = vec[i]
