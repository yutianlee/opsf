from __future__ import annotations

from certsf import ai, airy

from _common import run_cases


if __name__ == "__main__":
    run_cases(
        [
            ("airy-fast", airy, ("1.0",), {"dps": 15, "mode": "fast"}),
            ("airy-high-precision", airy, ("1.0",), {"dps": 80, "mode": "high_precision"}),
            ("airy-certified", airy, ("1.0",), {"dps": 80, "mode": "certified"}),
            ("ai-large-positive", ai, ("25",), {"dps": 80, "mode": "high_precision"}),
            ("ai-large-negative", ai, ("-25",), {"dps": 80, "mode": "high_precision"}),
        ]
    )
