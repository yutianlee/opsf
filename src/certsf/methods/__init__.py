"""Custom certified methods."""

from .gamma_stirling import gamma_stirling_exp
from .stirling import stirling_loggamma, stirling_loggamma_shifted
from .loggamma_auto import certified_auto_loggamma

__all__ = ["certified_auto_loggamma", "gamma_stirling_exp", "stirling_loggamma", "stirling_loggamma_shifted"]
