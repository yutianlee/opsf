"""Custom certified methods."""

from .stirling import stirling_loggamma, stirling_loggamma_shifted
from .loggamma_auto import certified_auto_loggamma

__all__ = ["certified_auto_loggamma", "stirling_loggamma", "stirling_loggamma_shifted"]
