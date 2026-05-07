from __future__ import annotations

from certsf import airy, besselj, gamma, pbdv


def main() -> None:
    gamma_result = gamma("3.2", dps=50, mode="certified")
    print("gamma value:", gamma_result.value)
    print("gamma certified:", gamma_result.certified)
    print("gamma diagnostics:", gamma_result.diagnostics)

    bessel_result = besselj("2.5", "4.0+1.25j", dps=60, mode="high_precision")
    print("besselj high precision:", bessel_result.value)

    airy_result = airy("1.0", dps=60, mode="high_precision")
    print("Ai(1):", airy_result.component("ai"))

    pbdv_result = pbdv("2.5", "1.25", dps=60, mode="high_precision")
    print("D_v(x):", pbdv_result.component("value"))
    print("D_v'(x):", pbdv_result.component("derivative"))


if __name__ == "__main__":
    main()
