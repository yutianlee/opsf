from __future__ import annotations

from certsf import gamma, loggamma, rgamma

from _common import run_cases


if __name__ == "__main__":
    run_cases(
        [
            ("gamma-fast", gamma, ("3.2",), {"dps": 15, "mode": "fast"}),
            ("gamma-high-precision", gamma, ("3.2",), {"dps": 80, "mode": "high_precision"}),
            ("gamma-certified", gamma, ("3.2",), {"dps": 80, "mode": "certified"}),
            ("loggamma-branch", loggamma, ("-2.5+1e-20j",), {"dps": 80, "mode": "high_precision"}),
            ("rgamma-near-pole", rgamma, ("1e-30",), {"dps": 80, "mode": "high_precision"}),
        ]
    )
