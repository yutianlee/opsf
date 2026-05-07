from math import isclose, pi

import pytest

from certsf import ai, besselj, besselk, loggamma, rgamma

mp = pytest.importorskip("mpmath")


def test_loggamma_high_precision_tracks_negative_axis_branch_sides():
    upper = _complex_value(loggamma("-2.5+1e-20j", dps=80, mode="high_precision").value)
    lower = _complex_value(loggamma("-2.5-1e-20j", dps=80, mode="high_precision").value)
    assert upper.imag < 0
    assert lower.imag > 0
    assert isclose(abs(upper.imag), 3 * pi, rel_tol=1e-15)
    assert isclose(abs(lower.imag), 3 * pi, rel_tol=1e-15)
    assert isclose(upper.real, lower.real, rel_tol=1e-15)


def test_rgamma_high_precision_is_stable_near_gamma_pole():
    with mp.workdps(90):
        value = mp.mpf(rgamma("1e-30", dps=80, mode="high_precision").value)
        expected = mp.rgamma(mp.mpf("1e-30"))
        assert abs(value - expected) < mp.mpf("1e-100")


def test_besselj_high_precision_near_zero_matches_series_leading_term():
    with mp.workdps(90):
        value = mp.mpf(besselj("2", "1e-20", dps=80, mode="high_precision").value)
        expected = mp.besselj(2, mp.mpf("1e-20"))
        leading = mp.mpf("1.25e-41")
        assert abs(value - expected) < mp.mpf("1e-120")
        assert abs(value - leading) / leading < mp.mpf("1e-40")


def test_besselk_high_precision_tracks_negative_axis_branch_sides():
    upper = _complex_value(besselk("1.5", "-2.5+1e-20j", dps=70, mode="high_precision").value)
    lower = _complex_value(besselk("1.5", "-2.5-1e-20j", dps=70, mode="high_precision").value)
    assert upper.imag < 0
    assert lower.imag > 0
    assert isclose(abs(upper.imag), abs(lower.imag), rel_tol=1e-14)
    assert isclose(upper.real, lower.real, abs_tol=1e-28)


def test_airy_high_precision_large_positive_argument_decays():
    value = mp.mpf(ai("25", dps=70, mode="high_precision").value)
    assert mp.mpf("0") < value < mp.mpf("1e-30")


def _complex_value(value):
    return complex(str(value).strip().strip("()").replace(" ", ""))
