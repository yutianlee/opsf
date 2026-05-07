from __future__ import annotations

import json

from certsf import pbdv, pcfd, pcfu, pcfv, pcfw


def main() -> None:
    payloads = {
        "pcfu": pcfu("2.5", "1.25", dps=80, mode="certified").to_dict(),
        "pcfd": pcfd("2.5", "1.25", dps=80, mode="certified").to_dict(),
        "pbdv": pbdv("2.5", "1.25", dps=80, mode="certified").to_dict(),
        "pcfv": pcfv("2.5", "1.25", dps=80, mode="certified").to_dict(),
        "pcfw": pcfw("2.5", "1.25", dps=80, mode="certified").to_dict(),
    }
    print(json.dumps(payloads, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
