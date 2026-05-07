from __future__ import annotations

import json

from certsf import besseli, besselj, besselk, bessely


def main() -> None:
    order = "2.5"
    argument = "4.0+1.25j"
    payloads = {
        "besselj": besselj(order, argument, dps=80, mode="certified").to_dict(),
        "bessely": bessely(order, argument, dps=80, mode="certified").to_dict(),
        "besseli": besseli(order, argument, dps=80, mode="certified").to_dict(),
        "besselk": besselk(order, argument, dps=80, mode="certified").to_dict(),
    }
    print(json.dumps(payloads, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
