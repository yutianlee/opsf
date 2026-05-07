from __future__ import annotations

from certsf import pbdv, pcfd, pcfu, pcfv, pcfw

from _common import run_cases


if __name__ == "__main__":
    run_cases(
        [
            ("pbdv-high-precision", pbdv, ("2.5", "1.25"), {"dps": 80, "mode": "high_precision"}),
            ("pbdv-certified", pbdv, ("2.5", "1.25"), {"dps": 80, "mode": "certified"}),
            ("pcfd-complex", pcfd, ("2.5", "1.25+0.5j"), {"dps": 80, "mode": "high_precision"}),
            ("pcfu-complex", pcfu, ("2.5", "1.25+0.5j"), {"dps": 80, "mode": "high_precision"}),
            ("pcfv-complex", pcfv, ("2.5", "1.25+0.5j"), {"dps": 80, "mode": "high_precision"}),
            ("pcfw-real", pcfw, ("2.5", "1.25"), {"dps": 80, "mode": "high_precision"}),
        ]
    )
