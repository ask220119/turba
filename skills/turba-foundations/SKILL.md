---
name: turba-foundations
description: Design and check of shallow footings, rafts, semi-deep and deep foundations (piles, barrettes, groups) to Eurocode 7 and NF P94-261/262 - bearing capacity from pressuremeter, CPT or c-phi, settlement (Menard, elastic, oedometer), pile capacity and t-z behaviour, negative skin friction, lateral loading and soil springs for the structural engineer. Use for any foundation calculation or review.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: foundations
  standards: "EN 1997-1, NF P94-261, NF P94-262"
  tests: "PMT, CPT, SPT, oedometer"
  language: en
---

# Foundations and static soil-structure interaction

Load `turba-core` first. French version: `SKILL.fr.md`. This skill starts from an interpreted ground model (pl*, EM, α, qc, c', φ', cu). For the interpretation of raw tests, use `turba-site-investigation`.

## 1. Workflow

1. **Loads**: a table of load effects per support (N, Hx, Hy, Mx, My) for each combination (SLS quasi-permanent, SLS characteristic, ULS fundamental, ULS accidental / seismic).
2. **Foundation type** from embedment D and width B:
   - axial loading: shallow D/B < 1.5 to 2.5, semi-deep up to 5, deep beyond 5 (NF P94-261 / 262 definitions);
   - lateral loading: shallow behaviour D/B < 5, pile behaviour D/B > 10.
3. **Bearing (ULS and SLS)**, then **settlement** (absolute and differential), then **interaction** (springs, redistribution), then **parasitic effects** (group, negative friction, lateral soil movement, neighbours).

Bearing rules are a disguised way of limiting settlement: never stop at bearing.

## 2. Choosing the modulus

The modulus must match the strain level of the structure:

| Strain level | Typical case | E from pressuremeter | E from CPT |
|---|---|---|---|
| ≈ 1 % | footing near failure, soft soil under fill | 2 to 3 × EM (≈ EM/α) | 2 to 6 × qc |
| ≈ 0.1 % | usual footings, rafts in service | 3 to 6 × EM | 3 to 10 × qc |
| ≈ 0.01 % | seismic, vibrations | 6 to 12 × EM | 5 to 20 × qc |

- Poisson's ratio 0.25 to 0.35 drained, 0.5 undrained.
- The pressuremeter is not suited to large strains in compressible soils: use oedometer parameters (Cc, Cs, σ'p, Cαε) for soft clays and fills on soft ground.

## 3. Shallow foundations (NF P94-261)

- **Bearing from PMT**: q_net = kp · ple*, kp from the standard's curves (soil class, De/B, B/L). Reduce for load inclination (iδ) and slope proximity (iβ).
- **Bearing c-φ**: q = c'Nc sc ic + q0 Nq sq iq + 0.5 γ' B' Nγ sγ iγ (EN 1997-1 annex D); undrained Nc = π + 2.
- **Eccentricity**: effective width B' = B − 2e (Meyerhof). Compressed area: 100 % at SLS quasi-permanent (e ≤ B/6), ≥ 75 % at SLS characteristic (e ≤ B/4), ≥ 10 % at ULS (e ≤ 7B/15), rectangular footing.
- **ULS factors (DA2)**: bearing γR;v = 1.4 with model factor γR;d;v = 1.2 (PMT) ; sliding γR;h = 1.1.
- **SLS**: q_ref ≤ ple*·kp/(γR;v · γR;d;v) with γR;v = 2.3 (NF P94-261 SLS check), plus settlement check.

### Settlement

Four levels of method, from simple to detailed:

1. empirical: Ménard (PMT, NF P94-261 annex H), Schmertmann (CPT);
2. elastic: Boussinesq / Steinbrenner multilayer, Giroud coefficients;
3. hybrid soil-structure models (raft on springs calibrated on an elastic multilayer);
4. finite elements.

**Ménard (homogeneous soil, B > B0 = 0.6 m)**:

```
s = sc + sd
sc = (α / (9 Ec)) · (q − σv0) · λc · B
sd = (2 / (9 Ed)) · (q − σv0) · B0 · (λd · B / B0)^α
```

| L/B | circle | 1 (square) | 2 | 3 | 5 | 20 |
|---|---|---|---|---|---|---|
| λc | 1.00 | 1.10 | 1.20 | 1.30 | 1.40 | 1.50 |
| λd | 1.00 | 1.12 | 1.53 | 1.78 | 2.14 | 2.65 |

Layered soil: Ec = E1 (first B/2), Ed = harmonic mean of slices of B/2 down to 8B (annex H weighting). Script: `scripts/menard_settlement.py`.

**Typical magnitudes**: isolated footing about 1 cm; large raft 1 to 10 cm; tank about 10 cm; embankment on soft soil 10 to 100 cm.

**Angular distortion limits**: ordinary buildings 1/500; tall and statically indeterminate structures 1/1000; EN 1997-1 annex H gives 1/2000 to 1/300 at SLS and about 1/150 at ULS for buildings.

## 4. Rafts and slabs

- The relative stiffness raft/soil must be modelled: one uniform spring under a raft can even reverse the tensile face.
- Zoned subgrade reaction: K_edge ≈ 2 to 3 × K_centre. Iterate: loads → ground model → zoned K → structure model → new loads, until stable.
- No tension at the interface; interface pressure below the creep pressure.

## 5. Deep foundations (NF P94-262)

- **Capacity**: R = Rb + Rs = Ab · qb + P · Σ qs,i · Δzi.
  - qb = kp · ple* (PMT) or kc · qce (CPT); kp, kc from the standard by soil class and pile class.
  - qs from the standard's curves fsol(pl*) or fsol(qc), capped by pile class (qs,max).
- Conventional failure at a head settlement of B/10; creep load Rc,cr ≈ 0.7 Rc for displacement piles, 0.5 Rb + 0.7 Rs for bored piles.
- **Service behaviour** (30 to 50 % of Rc): head settlement ≈ B/150 to B/100; skin friction mobilised at less than 1 cm.
- **t-z law (Frank and Zhao)**: fine soils kτ = 2.0 EM / B, kq = 11 EM / B; granular soils kτ = 0.8 EM / B, kq = 4.8 EM / B; tri-linear with a first slope up to qs/2 and qb/2.
- **Groups**: check the block failure and the efficiency when spacing < 3B; group settlement by interaction factors (Poulos and Davis) or equivalent raft.
- **Negative skin friction** (Combarieu): qsn = K tanδ · σ'v over the zone where the soil settles more than the pile; it adds load and reduces the useful length.
- **Lateral loading**: EI y'''' + Es y = 0, transfer length l0 = (4 EI / Es)^(1/4); Es ≈ 2 EM (fine soils) to 4 EM (granular) as an order of magnitude; reaction capped by the creep pressure pf. Short rigid pile if D ≲ l0, long pile if D ≳ 3 l0.

## 6. Springs for the structural engineer

- Define springs in the service range, never at failure. Order of magnitude KV ≈ 100 · V_service / B.
- Footings: vertical from Ménard / elasticity, horizontal and rocking from elastic formulas (Gazetas).
- Piles: t-z and p-y calibrated on PMT; give coupled H-M terms; lateral stiffness is governed by the top 3 to 6 B.
- Give static springs and seismic springs separately (seismic from G0, see `turba-seismic-liquefaction`).

## 7. Report outline

1. Purpose, mission phase, references. 2. Structure and loads table. 3. Ground model and choice of moduli. 4. Choice of foundation type. 5. Bearing ULS / SLS per support with utilisation ratios. 6. Settlements and distortions vs criteria. 7. Springs. 8. Parasitic effects. 9. Construction requirements, load tests, monitoring.

## 8. Common pitfalls

- Using EM/α over the whole depth: overestimates settlement (modulus increases beyond B/2).
- One uniform spring under a raft.
- Forgetting negative friction under new fills or on recently filled ground.
- Mixing NF P94-262 pile classes and the qs,max cap.
- Seismic springs taken from static EM without justification.
