---
name: turba-slope-stability
description: Slope and embankment stability and slope reinforcement - limit equilibrium (Bishop, Fellenius, non-circular methods), yield design, FE strength reduction, back-analysis of existing slopes and landslides, Eurocode 7 design approach 3 and NF P94-270, soil nailing (Clouterre), anchors and stabilising piles, drainage, pseudo-static seismic checks. Use for any slope, cutting, embankment or nailed wall calculation or review.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: slopes
  standards: "EN 1997-1, NF P94-270, Clouterre recommendations (1991, 2002)"
  language: en
---

# Slope stability and slope reinforcement

Load `turba-core` first. French version: `SKILL.fr.md`.

## 1. Workflow

1. **Recognise the phenomenon**: geomorphology, signs of movement, piezometers, inclinometers (depth of the slip surface), history. Classify: planar, rotational, flow, rockfall.
2. **Ground model**: c', φ' (residual values if the slide is reactivated), cu for short term, γ, water (hydrostatic, ru, pore pressure grid, or seepage analysis).
3. **Initial state / back-analysis, always first**: an existing stable slope must give F ≥ 1.0 to 1.2; an active slide F ≈ 1.0. Calibrate c' and φ' on it.
   - A stable vertical cut of height H gives a lower bound of cohesion: Hc = 3.83 · (c'/γ) · tan(45° + φ'/2) (Taylor). This cohesion is partly apparent (suction): protecting and draining the face are part of the design.
4. **Options**: regrading (unload the crest, load the toe, flatten), drainage (trenches, drainage blankets, sub-horizontal drains), resisting elements (nails, anchors, piles, micropiles, geosynthetics).
5. **Calculations per stage**: each excavation lift, reinforcement, service, seismic, high water.

## 2. Methods and safety format

- **Limit equilibrium, slices**: Fellenius (conservative, circular), simplified Bishop (reference for circles), Morgenstern-Price / Spencer / perturbation methods for non-circular surfaces.
- **Yield design** (kinematic, log-spiral mechanisms): independent check of the slice methods.
- **FE strength reduction** (c-φ reduction): no assumption on the mechanism; check that ΣMsf is stationary.
- **Traditional global factor**: F ≥ 1.5 permanent, F ≥ 1.3 temporary (< 1 year). Existing landslide: improve F by 10 to 20 % over the calibrated initial state.
- **Eurocode 7, design approach 3** (overall stability): γtanφ' = γc' = 1.25, γcu = 1.4, variable actions × 1.3; NF P94-270 adds a model factor γR;d = 1.0 to 1.2 depending on the consequence class.
- **Seismic**: pseudo-static kh, kv (kv = ± 0.5 kh), then Newmark displacement if F < 1 under the design acceleration. See `turba-seismic-liquefaction` for kh.

Script: `scripts/bishop.py` (simplified Bishop on a circle, layered soil, water table) for independent checks.

## 3. Soil nailing (NF P94-270, Clouterre)

- **Field**: cuts in soil above the water table, top-down lifts; density 0.15 to 0.4 nail/m²; drilled diameter 100 to 200 mm; nail capacity 200 to 600 kN.
- **Sequence**: lift → drainage and first mesh → drill, bar, grout → shotcrete → plates and second mesh. Lift height validated by trial panels. Nails do not hold the face during the open lift.
- **ULS mechanisms**:
  1. overall external stability (deep slip around the nailed block), DA3;
  2. local external stability: nailed block as a gravity wall (bearing, sliding), DA2, and two- or three-block mechanisms. Circles through the toe alone are not enough;
  3. mixed stability (surfaces crossing the nails), nail tension only is usually sufficient;
  4. internal: pull-out, bar failure (corrosion allowance), facing and connections.
- **Pull-out qs**: design from Clouterre charts qs = f(pl*); for execution, pull-out tests to failure are mandatory. Correlation factors ξ depend on the number of tests.
- **Facing**: design load at the head T0 = Tmax · [0.5 + (s − 0.5)/5], s = max(sh, sv) in m (Clouterre 2002); punching and bending of the shotcrete.
- **SLS displacements** (δv ≈ δh): rock H/1000, sands 2H/1000, clays 4H/1000.

## 4. Stabilising piles

1. Calibrate the initial state (F ≈ 1). 2. Choose stiff piles crossing the slip surface and socketed below. 3. Shear mobilised per pile = min(soil yield in front of the pile, plastic moment Mp, shear capacity). 4. Search for new surfaces above and below the pile row. 5. Check the pile under the soil displacement g(z) (see `turba-foundations`).

## 5. Other measures

- **Drainage** is often the most effective measure per unit cost; justify it by the computed or measured drawdown and plan maintenance.
- **Lightweight fills** (EPS, foamed glass) to unload a slope or soft ground.
- **Reinforced soil and steepened slopes**: geosynthetics, with factored pull-out and tensile resistance.

## 6. Software checks

- Automatic search grids can overestimate Fmin by 5 to 15 % when the grid is coarse. Refine manually (step ≤ 0.5 m) around the critical centre and test centres at ground level behind the crest (steep circles under surcharges).
- Compare two methods on the same surface before comparing minima, so a search defect is not mistaken for a mechanical difference.
- A layer with no pull-out value defined for nails gets zero friction silently in some programs: check every layer crossed.

## 7. Report outline

1. Purpose, phase, site visit. 2. Geology, hydrogeology, history, monitoring. 3. Ground model and back-analysis. 4. Assumptions (surcharges, water, seismic, design life, consequence class). 5. Methods and safety format. 6. Options. 7. Results per stage (table of Fmin per stage and per factor set). 8. Elements: nails, anchors, facing, drains. 9. Tests and monitoring thresholds. 10. Points to confirm.

## 8. Common pitfalls

- No calibrated initial state: the design F means nothing.
- Water table badly defined.
- Only circles through the toe for a nailed block or heterogeneous ground.
- Temporary stages forgotten (open lift before nailing).
- Design qs without pull-out tests; ignoring the loss of apparent cohesion on saturation.
