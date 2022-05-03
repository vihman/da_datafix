import numpy as np

from da_datafix.fix import fix_lastknown


def test_last_known():
    vec = np.array([0, 1, 2, 3, np.nan, np.nan, 6, 7, 8, np.nan])
    fix_lastknown(vec)
    assert vec[5] == 3
    assert vec[9] == 8


def test_last_known_nanstart():
    vec = np.array([np.nan, 1, 2, 3, np.nan, np.nan, 6, 7, 8, np.nan])
    fix_lastknown(vec)
    assert np.isnan(vec[0])
