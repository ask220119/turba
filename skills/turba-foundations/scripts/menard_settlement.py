#!/usr/bin/env python3
"""Ménard settlement of a shallow footing (NF P94-261 annex H), homogeneous or layered soil.

Usage (homogeneous soil):
    python menard_settlement.py --B 2.0 --L 3.0 --q 250 --sv0 20 --EM 8 --alpha 0.5

Layered soil: give EM per slice of B/2 from the footing base, 16 slices max (down to 8B):
    python menard_settlement.py --B 2 --L 2 --q 250 --sv0 20 --alpha 0.5 --EM-slices 6 6 8 10 10 12 12 12 15 15 15 15 15 15 15 15

Units: B, L in m; q and sv0 in kPa; EM in MPa. Output in mm.
This is a check tool: compare with your own calculation and the text of the standard.
"""
from __future__ import annotations

import argparse
import math

B0 = 0.6  # m, reference width

# Shape coefficients (L/B, lambda_c, lambda_d); circle is L/B = 0 by convention here.
_SHAPE = [(1.0, 1.10, 1.12), (2.0, 1.20, 1.53), (3.0, 1.30, 1.78), (5.0, 1.40, 2.14), (20.0, 1.50, 2.65)]


def shape_coefficients(B: float, L: float | None) -> tuple[float, float]:
    """lambda_c, lambda_d. L=None means a circular footing of diameter B."""
    if L is None:
        return 1.0, 1.0
    r = max(L, B) / min(L, B)
    if r >= _SHAPE[-1][0]:
        return _SHAPE[-1][1], _SHAPE[-1][2]
    for (r0, c0, d0), (r1, c1, d1) in zip(_SHAPE, _SHAPE[1:]):
        if r0 <= r <= r1:
            t = (r - r0) / (r1 - r0)
            return c0 + t * (c1 - c0), d0 + t * (d1 - d0)
    return _SHAPE[0][1], _SHAPE[0][2]


def layered_moduli(slices: list[float]) -> tuple[float, float]:
    """Ec and Ed from EM of 16 slices of B/2 (annex H weighting). Missing deep slices repeat the last one."""
    if not slices:
        raise ValueError("at least one slice is needed")
    e = list(slices) + [slices[-1]] * (16 - len(slices))
    e = e[:16]
    hm = lambda vals: len(vals) / sum(1.0 / v for v in vals)  # harmonic mean
    E1 = e[0]
    E2 = e[1]
    E35 = hm(e[2:5])
    E68 = hm(e[5:8])
    E916 = hm(e[8:16])
    Ec = E1
    Ed = 4.0 / (1 / E1 + 1 / (0.85 * E2) + 1 / E35 + 1 / (2.5 * E68) + 1 / (2.5 * E916))
    return Ec, Ed


def menard_settlement(B: float, q: float, sv0: float, alpha: float, Ec: float, Ed: float,
                      L: float | None = None) -> dict[str, float]:
    """Return sc, sd and s in metres. q, sv0 in kPa; Ec, Ed in MPa."""
    if B <= B0:
        raise ValueError("the formula applies to B > B0 = 0.6 m")
    lc, ld = shape_coefficients(B, L)
    dq = (q - sv0) / 1000.0  # MPa
    sc = alpha / (9.0 * Ec) * dq * lc * B
    sd = 2.0 / (9.0 * Ed) * dq * B0 * (ld * B / B0) ** alpha
    return {"sc": sc, "sd": sd, "s": sc + sd, "lambda_c": lc, "lambda_d": ld}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--B", type=float, required=True)
    p.add_argument("--L", type=float, default=None, help="omit for a circular footing")
    p.add_argument("--q", type=float, required=True, help="applied pressure, kPa")
    p.add_argument("--sv0", type=float, default=0.0, help="initial vertical stress at base, kPa")
    p.add_argument("--alpha", type=float, required=True, help="Ménard rheological factor")
    p.add_argument("--EM", type=float, help="homogeneous EM, MPa")
    p.add_argument("--EM-slices", type=float, nargs="+", help="EM of slices of B/2, MPa")
    a = p.parse_args()
    if a.EM_slices:
        Ec, Ed = layered_moduli(a.EM_slices)
    elif a.EM:
        Ec = Ed = a.EM
    else:
        p.error("give --EM or --EM-slices")
    r = menard_settlement(a.B, a.q, a.sv0, a.alpha, Ec, Ed, a.L)
    print(f"Ec = {Ec:.2f} MPa, Ed = {Ed:.2f} MPa, lambda_c = {r['lambda_c']:.3f}, lambda_d = {r['lambda_d']:.3f}")
    print(f"sc = {r['sc']*1000:.1f} mm, sd = {r['sd']*1000:.1f} mm, s = {r['s']*1000:.1f} mm")


if __name__ == "__main__":
    main()
