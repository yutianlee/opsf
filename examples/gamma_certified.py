from __future__ import annotations

import json

from certsf import gamma, loggamma, rgamma


def main() -> None:
    payloads = {
        "gamma": gamma("3.2", dps=80, mode="certified").to_dict(),
        "loggamma": loggamma("3.2", dps=80, mode="certified").to_dict(),
        "rgamma_pole": rgamma("-2", dps=80, mode="certified").to_dict(),
    }
    print(json.dumps(payloads, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
