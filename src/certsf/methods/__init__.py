"""Custom certified methods."""

from .gamma_stirling import gamma_stirling_exp
from .rgamma_stirling import rgamma_stirling_recip
from .stirling import stirling_loggamma, stirling_loggamma_shifted
from .loggamma_auto import certified_auto_loggamma

__all__ = [
    "certified_auto_loggamma",
    "gamma_stirling_exp",
    "rgamma_stirling_recip",
    "stirling_loggamma",
    "stirling_loggamma_shifted",
]
