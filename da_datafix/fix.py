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


def fix_baseline(vec: np.array, window_size=288, bottom=0, base=400):
    """
    In case the sensors jump baseline value (autocalibration?) this method fixes the baseline value naively.
    It is using median of specified percentile of the specified time window.

    Args:
        vec: vector to change baseline of.
        window_size: number of values to include in window. In case measurements are in 5 min interval and we want 24h window - `int(24*60/5) == 288`
        bottom: percentile what's median value is used for baseline.
        base: The value that is supposed to be the regular baseline.

    """
    def get_baseline(vec, window_size, bottom):
        result = []
        i = len(vec) - window_size
        for j in range(i):
            _slice = vec[j:j+window_size]
            p = np.percentile(_slice, bottom, axis=0)
            med = np.median(p)
            result.append(med)
        return np.concatenate((np.ones(window_size) * result[0], np.array(result)),)
    bl = get_baseline(vec, window_size, bottom)
    vec[...] = vec - bl + base


def get_baseline_using_percentile(co2, wsize=12, percentile=0):

    result = []
    if wsize >= len(co2):
        return np.ones(len(co2)) * np.median(co2)
    else:
        i = len(co2) - wsize
        for _ in range (wsize):
            result.append(np.nan)

        for j in range(i):
            a = 1
            slice = co2[j:j+wsize]
            p = np.percentile(slice, percentile, axis=0)
            med = np.median(p)
            result.append(med)
    return np.array(result)  # , dtype=np.float64)