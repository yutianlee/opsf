from __future__ import annotations

import json

from certsf.mcp_server import special_airy, special_gamma, special_pbdv


def main() -> None:
    payloads = {
        "special_gamma": special_gamma("3.2", dps=80, mode="certified"),
        "special_airy": special_airy("1.0", dps=80, mode="certified"),
        "special_pbdv": special_pbdv("2.5", "1.25", dps=80, mode="certified"),
    }
    print(json.dumps(payloads, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
