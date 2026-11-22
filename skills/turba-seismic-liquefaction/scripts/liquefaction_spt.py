#!/usr/bin/env python3
"""Liquefaction triggering from SPT, Boulanger and Idriss (2014) simplified procedure.

Input: a CSV with columns depth_m, N60, FC (fines content, %), gamma (kN/m3, total unit weight of
the layer above that depth, constant per row interval). Example:

    depth_m,N60,FC,gamma
    1.5,8,10,18
    3.0,10,12,19
    ...

Usage:
    python liquefaction_spt.py profile.csv --amax 0.18 --M 6.5 --gwt 1.0

amax in g at the ground surface, M moment magnitude, gwt water table depth in m.
Output: one line per test with sigma_v, sigma'_v, rd, CSR, (N1)60cs, CRR, MSF, K_sigma, FS.
This is a check tool: compare with your own calculation and the source paper.
"""
from __future__ import annotations

import argparse
import csv
import math

PA = 101.325  # kPa
GAMMA_W = 9.81


def rd_idriss(z: float, M: float) -> float:
    a = -1.012 - 1.126 * math.sin(z / 11.73 + 5.133)
    b = 0.106 + 0.118 * math.sin(z / 11.28 + 5.142)
    return math.exp(a + b * M)


def delta_n_fines(FC: float) -> float:
    f = FC + 0.01
    return math.exp(1.63 + 9.7 / f - (15.7 / f) ** 2)


def n1_60cs(N60: float, FC: float, sv_eff: float) -> tuple[float, float]:
    """Iterate on CN because m depends on (N1)60cs. Returns ((N1)60, (N1)60cs)."""
    dn = delta_n_fines(FC)
    n1cs = N60 + dn
    for _ in range(50):
        m = 0.784 - 0.0768 * math.sqrt(min(max(n1cs, 0.0), 46.0))
        cn = min((PA / sv_eff) ** m, 1.7)
        n1 = cn * N60
        new = n1 + dn
        if abs(new - n1cs) < 1e-6:
            n1cs = new
            break
        n1cs = new
    return n1, n1cs


def crr_75(n: float) -> float:
    n = min(n, 46.0)
    return math.exp(n / 14.1 + (n / 126) ** 2 - (n / 23.6) ** 3 + (n / 25.4) ** 4 - 2.8)


def msf(M: float, n: float) -> float:
    msf_max = min(1.09 + (n / 31.5) ** 2, 2.2)
    return 1 + (msf_max - 1) * (8.64 * math.exp(-M / 4) - 1.325)


def k_sigma(sv_eff: float, n: float) -> float:
    c = min(1.0 / (18.9 - 2.55 * math.sqrt(min(n, 37.0))), 0.3)
    return min(1 - c * math.log(sv_eff / PA), 1.1)


def analyse(rows: list[dict[str, float]], amax: float, M: float, gwt: float) -> list[dict[str, float]]:
    out = []
    sv = 0.0
    z_prev = 0.0
    for r in sorted(rows, key=lambda x: x["depth_m"]):
        z = r["depth_m"]
        sv += r["gamma"] * (z - z_prev)
        z_prev = z
        u = GAMMA_W * max(z - gwt, 0.0)
        sv_eff = sv - u
        rd = rd_idriss(z, M)
        csr = 0.65 * amax * (sv / sv_eff) * rd
        n1, n1cs = n1_60cs(r["N60"], r["FC"], sv_eff)
        crr = crr_75(n1cs)
        m = msf(M, n1cs)
        ks = k_sigma(sv_eff, n1cs)
        fs = crr * m * ks / csr if z > gwt else float("inf")
        out.append({"z": z, "sv": sv, "sv_eff": sv_eff, "rd": rd, "CSR": csr, "N1_60": n1,
                    "N1_60cs": n1cs, "CRR75": crr, "MSF": m, "Ksigma": ks, "FS": fs})
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--amax", type=float, required=True)
    p.add_argument("--M", type=float, required=True)
    p.add_argument("--gwt", type=float, required=True)
    a = p.parse_args()
    with open(a.csv, newline="") as f:
        rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]
    print("z(m)  sv(kPa) sv'(kPa)  rd    CSR   (N1)60cs  CRR7.5  MSF   Ks    FS")
    for r in analyse(rows, a.amax, a.M, a.gwt):
        fs = "dry" if math.isinf(r["FS"]) else f"{r['FS']:.2f}"
        print(f"{r['z']:4.1f} {r['sv']:7.1f} {r['sv_eff']:8.1f} {r['rd']:5.3f} {r['CSR']:5.3f} "
              f"{r['N1_60cs']:8.1f} {r['CRR75']:7.3f} {r['MSF']:5.3f} {r['Ksigma']:5.3f} {fs:>5}")


if __name__ == "__main__":
    main()
