"""Custom certified methods."""

from .gamma_stirling import gamma_stirling_exp
from .loggamma_ratio_stirling import loggamma_ratio_stirling_diff
from .rgamma_stirling import rgamma_stirling_recip
from .stirling import stirling_loggamma, stirling_loggamma_shifted
from .loggamma_auto import certified_auto_loggamma

__all__ = [
    "certified_auto_loggamma",
    "gamma_stirling_exp",
    "loggamma_ratio_stirling_diff",
    "rgamma_stirling_recip",
    "stirling_loggamma",
    "stirling_loggamma_shifted",
]
