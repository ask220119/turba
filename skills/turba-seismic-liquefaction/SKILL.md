---
name: turba-seismic-liquefaction
description: Geotechnical earthquake engineering - seismic action to Eurocode 8 (EN 1998-1/-5) and the Moroccan RPS 2000 rev. 2011, site classes and Vs30, liquefaction triggering from SPT and CPT (Boulanger and Idriss 2014) and its consequences, dynamic earth pressure (Mononobe-Okabe), seismic slope checks, dynamic soil stiffness and foundation impedances, construction vibrations. Use for any seismic geotechnical question.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: seismic
  standards: "EN 1998-1, EN 1998-5, RPS 2000 (rev. 2011), NCEER 1997, Boulanger & Idriss 2014"
  tests: "SPT, CPT, MASW, cross-hole"
  language: en
---

# Seismic geotechnics and liquefaction

Load `turba-core` first. French version: `SKILL.fr.md`.

Say which code applies (Eurocode 8 or RPS 2000 rev. 2011 in Morocco) and never mix their spectra or site coefficients. Check every coefficient against the text in force.

## 1. Workflow

1. **Hazard**: seismic zone and reference acceleration (agR for EC8; Za / Zv zones for RPS 2011), importance class of the structure.
2. **Site class** from boreholes and preferably measured Vs (MASW, cross-hole, down-hole):
   - EC8: classes A to E plus S1, S2 by Vs,30, NSPT, cu;
   - RPS 2011: sites S1 to S5 (S5 = specific study).
   - Vs,30 = 30 / Σ (hi / Vs,i).
3. **Site effects**: topography, basins, soft layers → site-specific spectrum (1D equivalent linear analysis) when needed.
4. **Liquefaction** (§2), **slopes under earthquake**, **dynamic earth pressure** (§3), **foundations** (§4).
5. Deliver to the structural engineer: site class, site coefficient, design acceleration at the surface, springs and damping.

## 2. Liquefaction (simplified procedure)

**Susceptibility**: saturated loose sands and silts of low plasticity. For fine soils use Bray and Sancio (2006) or Boulanger and Idriss (2006) criteria (PI < 7 sand-like behaviour).

**Demand**:

```
CSR = 0.65 · (amax / g) · (σv / σ'v) · rd
rd  = exp(α(z) + β(z)·M)          (Idriss 1999)
α(z) = −1.012 − 1.126 sin(z/11.73 + 5.133)
β(z) =  0.106 + 0.118 sin(z/11.28 + 5.142)      (z in m)
```

**Resistance, SPT (Boulanger and Idriss 2014)**:

```
(N1)60 = CN · N60,  CN = (Pa/σ'v)^m ≤ 1.7,  m = 0.784 − 0.0768 √(N1)60cs  (iterate)
Δ(N1)60 = exp(1.63 + 9.7/(FC+0.01) − (15.7/(FC+0.01))²)
(N1)60cs = (N1)60 + Δ(N1)60
CRR(M=7.5, σ'v=1 atm) = exp( N/14.1 + (N/126)² − (N/23.6)³ + (N/25.4)⁴ − 2.8 ),  N = (N1)60cs
MSF = 1 + (MSFmax − 1)(8.64 exp(−M/4) − 1.325),  MSFmax = 1.09 + ((N1)60cs/31.5)² ≤ 2.2
Kσ  = 1 − Cσ ln(σ'v/Pa) ≤ 1.1,  Cσ = 1/(18.9 − 2.55 √(N1)60cs) ≤ 0.3
FS  = CRR · MSF · Kσ / CSR
```

**Resistance, CPT (Boulanger and Idriss 2014)**: qc1Ncs = qc1N + Δqc1N, with the fines correction from Ic; CRR = exp( qc1Ncs/113 + (qc1Ncs/1000)² − (qc1Ncs/140)³ + (qc1Ncs/137)⁴ − 2.80 ).

Script: `scripts/liquefaction_spt.py` (one SPT profile, outputs CSR, CRR, FS per test).

**Criterion**: FS ≥ 1.25 is a common target (EC8 part 5 annex B accepts FS ≥ 1.25 on the simplified method); follow the project's code.

**Consequences, always**: post-liquefaction settlement (Ishihara and Yoshimine 1992, Zhang et al. 2002), lateral spreading, loss of skin friction and down-drag on piles, bearing loss under shallow foundations. Mitigation: see `turba-ground-improvement`.

## 3. Dynamic earth pressure (EN 1998-5 / Mononobe-Okabe)

- Pseudo-static coefficients: kh = α · S / r, kv = ± 0.5 kh (or 0.33 kh depending on the spectrum type), α = ag/g; r = 2 for a wall free to move (up to 300α·S mm), 1.5 for smaller movements, 1 for rigid walls.
- Mononobe-Okabe for active and passive thrust; distinguish pervious and impervious backfill below the water table; Westergaard hydrodynamic pressure for free water.
- Include the dynamic increment in the wall model (see `turba-retaining-walls`).

## 4. Dynamic stiffness and foundations

- G0 = ρ · Vs². Strain-dependent G/G0 and damping curves (Vucetic and Dobry 1991, Darendeli 2001).
- Do not use the pressuremeter EM for dynamics without a justified factor (G0 ≈ 8 to 12 × EM is only an order of magnitude).
- Impedances of footings and pile groups: Gazetas (1991) formulas; give static and seismic springs separately.
- Piles under earthquake: inertial and kinematic effects (bending at interfaces between layers of contrasting stiffness).

## 5. Construction vibrations

Pile driving, dynamic compaction, blasting: peak particle velocity limits from the applicable national rules (e.g. DIN 4150-3, BS 7385-2, French circular of 23 July 1986); monitor sensitive neighbours.

## 6. Common pitfalls

- Mixing EC8 and RPS site classes or spectra.
- Using amax at bedrock instead of at the surface of the site in CSR.
- Applying the SPT correlation with raw N instead of N60 (energy ratio).
- Reporting FS without the consequences (settlement, lateral spread, pile effects).
- Fines content correction applied to clayey soils that are not susceptible.
