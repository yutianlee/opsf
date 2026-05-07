from __future__ import annotations

from certsf import besselj, besselk

from _common import run_cases


if __name__ == "__main__":
    run_cases(
        [
            ("besselj-fast", besselj, ("2.5", "4.0"), {"dps": 15, "mode": "fast"}),
            ("besselj-high-precision", besselj, ("2.5", "4.0"), {"dps": 80, "mode": "high_precision"}),
            ("besselj-certified", besselj, ("2.5", "4.0"), {"dps": 80, "mode": "certified"}),
            ("besselj-near-zero", besselj, ("2", "1e-20"), {"dps": 80, "mode": "high_precision"}),
            ("besselk-branch", besselk, ("1.5", "-2.5+1e-20j"), {"dps": 80, "mode": "high_precision"}),
        ]
    )
