---
name: turba-retaining-walls
description: Design and check of embedded retaining walls and deep excavations (diaphragm walls, secant or contiguous piles, soldier piles, sheet piles, struts, ground anchors) to Eurocode 7 design approach 2 and NF P94-282 - earth pressure, subgrade reaction method, staged construction, anchor free length (Kranz), hydraulic heave and uplift, base stability, settlement of neighbouring buildings. Use for any excavation support calculation or review.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: retaining-structures
  standards: "EN 1997-1, NF P94-282, EN 1993-5, NF EN 1537, NF EN ISO 22477-5"
  language: en
---

# Embedded retaining walls and deep excavations

Load `turba-core` first. French version: `SKILL.fr.md`.

## 1. Workflow

1. **Geometry and neighbours**: excavation depth H, adjacent buildings (foundation level, distance, sensitivity), roads, networks, surcharges.
2. **Ground and water model**: layers with γ, c', φ', cu, δ/φ, subgrade reaction parameters; water levels on both sides at each stage; permeability for dewatering and seepage.
3. **Wall type**: soldier piles (no water), sheet piles (soft soils, water), secant / contiguous piles, diaphragm walls (deep, water, stiff), soil nailing (no water, see `turba-slope-stability`).
4. **Support**: cantilever, struts, ground anchors, berms, top-down slabs.
5. **Staged analysis**: each excavation level, each support installation, each prestress, final and long-term stages, high water, seismic if required.
6. **Checks** (§3) and **displacements and neighbours** (§5).

## 2. Methods

- **Limit earth pressures**: Ka, Kp from Kérisel-Absi tables or Coulomb / Caquot with δ/φ (active +2/3, passive −2/3 typical for concrete walls; −1/2 or less where the wall can settle).
- **Subgrade reaction method (SRM)**: elastoplastic springs with pressure bounded between active and passive; reaction coefficient kh from Ménard / Balay (PMT) or Schmitt formula: kh = 2.1 · (EM/α)^(4/3) / (EI)^(1/3) (Schmitt 1995, kh in kN/m³ with EM in kPa, EI in kN·m²/m). NF P94-282 annex F describes the method.
- **Finite elements** (PLAXIS etc.): hardening soil model with small-strain stiffness for displacements; check the same ULS as in SRM.
- Construction history matters: the SRM must follow the real stage sequence (unloading-reloading moduli, prestress).

## 3. ULS checks (NF P94-282, DA2)

| Check | Rule |
|---|---|
| Passive resistance mobilised | Bt / γR;e ≥ Bm, γR;e = 1.4 (with γR;d where required) |
| Vertical equilibrium | downward forces (anchor vertical component, self weight, wall friction) vs base and skin resistance (NF P94-262) |
| Structural resistance | bending, shear in the wall (EN 1992 / EN 1993-5), effect factor 1.35 on SRM results |
| Anchors | ULS pull-out resistance from tests (NF EN ISO 22477-5), tendon capacity; ξ factors |
| Struts | buckling, temperature, accidental loss of one strut |
| Overall stability | DA3, deep failure surface behind anchors (Kranz) and global slip |
| Hydraulic | uplift (UPL), heave (HYD), internal erosion and piping |

Reduce the passive resistance for walls without enough embedment below the excavation (minimum embedment for the "free earth" case: passive mobilised ratio check).

### Anchors

- Free length: the bond length must start beyond the active wedge plus a margin, usually d_wedge + 0.15 H, and the Kranz check (deep slip line from anchor bond centre to the theoretical wall point of zero shear) must give Fs ≥ 1.5 (traditional) or the DA2 equivalent.
- Lock-off load P0 from the SRM; check 1.35 P0 ≤ resistance / γ; tendon stress at lock-off ≤ 0.6 fp0.1k.
- Tests: investigation tests (to failure, before works), suitability tests, acceptance tests on every anchor (NF EN ISO 22477-5).

### Hydraulic stability

- Heave: compare the hydraulic gradient at the toe with the critical gradient (i_c ≈ γ'/γw ≈ 1), factor ≥ 1.5 to 2 depending on soil; Terzaghi block method for the prism at the toe.
- Uplift of an impervious layer below the dig: total weight above vs water pressure below, γG,stb = 0.9, γG,dst = 1.0 (UPL).
- Flow into the excavation: flow net or FE seepage, compare with the dewatering capacity.

## 4. SLS

- Wall displacements from SRM or FE, with characteristic parameters.
- Typical maximum lateral movement: 0.1 to 0.2 % H for stiff, well-propped walls in stiff soils; 0.5 to 1 % H for cantilevers or soft clays.

## 5. Neighbouring buildings

- Settlement trough behind the wall: Clough and O'Rourke (1990) envelopes (sands and stiff clays: δv,max ≈ 0.15 % H within 2H; soft clays: up to 0.5 to 1 % H within 2 to 3H); or Hsieh and Ou (1998) shapes. Or transfer FE displacements.
- Damage assessment: Burland and Wroth (1974), Boscardin and Cording (1989): angular distortion and horizontal strain → damage category 0 to 5. Target category ≤ 1 (very slight) for sensitive buildings.
- Add the effect of the neighbours' loads on the wall (surcharge from foundations: Boussinesq or the standard's simplified diffusion).

## 6. Report outline

1. Purpose, phase, references. 2. Site, neighbours (table with distances and foundation levels). 3. Ground and water model. 4. Wall and support choice. 5. Stage sequence (figure). 6. SRM / FE results per stage: moments, shears, support loads, displacements. 7. ULS checks table (ratios). 8. Anchors (P0, free length, tests). 9. Hydraulics. 10. Neighbours: settlement and damage category. 11. Monitoring plan with alert and alarm thresholds.

## 7. Common pitfalls

- Water levels not stated per stage on both sides.
- SRM run without the real stage sequence or with one stiffness value for loading and unloading.
- Forgetting the vertical equilibrium of an anchored wall (inclined anchors push the wall down).
- Anchor bond inside the active wedge or under a neighbour's foundation without the owner's consent.
- Monitoring without thresholds.
