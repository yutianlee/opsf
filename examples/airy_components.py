from __future__ import annotations

import json

from certsf import ai, airy, bi


def main() -> None:
    payloads = {
        "airy": airy("1.0", dps=80, mode="certified").to_dict(),
        "ai_derivative": ai("1.0", derivative=1, dps=80, mode="certified").to_dict(),
        "bi": bi("1.0", dps=80, mode="certified").to_dict(),
    }
    print(json.dumps(payloads, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
