---
name: turba-ground-improvement
description: Selection, design, specification and quality control of ground improvement and reinforcement - stone columns (CFMS 2011), rigid inclusions (ASIRI), prefabricated vertical drains and preloading, embankments on soft soil, dynamic compaction, vibro-compaction, grouting and jet grouting, lime or cement treatment, geosynthetics, and liquefaction mitigation. Use for any ground improvement choice, calculation or specification.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: ground-improvement
  standards: "CFMS recommendations for stone columns (2011), ASIRI national project (2012), EN 14731, EN 12716, EN 15237"
  language: en
---

# Ground improvement

Load `turba-core` first. French version: `SKILL.fr.md`.

## 1. Choosing a technique

| Problem | Soil | Techniques |
|---|---|---|
| Settlement under fill or slab | soft clay, silt | preloading + vertical drains, rigid inclusions, lightweight fill |
| Settlement under footings | heterogeneous fill, medium clay | stone columns, rigid inclusions |
| Low density, liquefaction | clean sand | vibro-compaction, dynamic compaction, stone columns with drainage |
| Liquefaction, silty sand | silty sand | stone columns (densification limited), jet grouting cells, drains + densification |
| Cavities, karst | limestone, gypsum | compaction grouting, fill grouting |
| Water cut-off, temporary support | sand, gravel | permeation grouting, jet grouting |
| Trafficability, earthworks | wet fine soil | lime / cement treatment |

Check: depth to treat, water, neighbours (vibrations), time available, cost, and what can be tested on site.

## 2. Stone columns (CFMS 2011)

- Area replacement ratio as = Ac / A (typically 10 to 30 %); unit cell radius Re = 0.564 s (square grid), 0.525 s (triangular).
- Settlement improvement factor (Priebe 1995) n0 = 1 + as · [ (5 − as) / (4 · Kac · (1 − as)) − 1 ], Kac = tan²(45° − φc/2), φc ≈ 38 to 40°; then corrections for column compressibility and overburden.
- Column stress limited by lateral confinement: qr = Kpc · (σ'h0 + pl* or cu-based support); usual design stress in the column 0.4 to 0.8 MPa; not in very soft soils (cu < 15 to 20 kPa) without justification.
- Bearing of footings on columns: homogenised soil, CFMS rules; settlement by the improvement factor or homogenised modulus.
- Tests: load tests on columns and on footings, CPT/PMT between columns (for densifiable soils), execution records (depth, energy, volume of aggregate).

## 3. Rigid inclusions (ASIRI)

- Unreinforced concrete or grout columns with a load transfer platform (granular, 0.4 to 1.0 m); the inclusions take 60 to 80 % of the load, the soil the rest.
- Design with the unit cell: negative friction above the neutral plane, positive below; arching in the platform (Hewlett and Randolph or ASIRI method). Settlement typically 0.2 to 0.4 of the untreated settlement.
- Checks: inclusion head stress, concrete stress (unreinforced, γc high), punching of the platform, horizontal loads (inclusions are not piles: no bending capacity unless reinforced).
- Tests: static load tests on inclusions, integrity tests, platform compaction.

## 4. Vertical drains and preloading

- Consolidation with radial drainage (Barron / Hansbo): Uh = 1 − exp(−8 Th / F(n)), Th = ch t / De², F(n) ≈ ln(De/dw) − 0.75 (+ smear and well resistance terms); De = 1.13 s (square), 1.05 s (triangular); equivalent diameter of a band drain dw = (a + b)/2.
- ch ≈ 1 to 5 × cv (measure if possible: CPTu dissipation, Rowe cell).
- Surcharge to reach the target settlement before the service load; check stability of the embankment in stages (cu increases with consolidation: Δcu ≈ 0.2 to 0.3 Δσ'v), see `turba-slope-stability`.
- Monitor settlement plates, piezometers and inclinometers; use Asaoka to predict final settlement.

## 5. Densification

- **Vibro-compaction**: clean sands with fines < 10 to 15 %; target qc or N60 between points; grid 2.5 to 4 m.
- **Dynamic compaction**: depth of influence D ≈ n · √(W·H) (W in t, H in m, n ≈ 0.3 to 0.6); vibrations to neighbours; check with PMT / CPT after treatment.

## 6. Grouting and jet grouting

- Permeation grouting needs k > 10⁻⁵ m/s for cement, finer soils need micro-fine cement or chemical grouts; groutability ratio (D15 soil / D85 grout) > 25.
- Jet grouting: column diameter from trial columns (single, double, triple fluid); strength from cores; heave and spoil control.

## 7. Liquefaction mitigation

- Increase density (vibro, dynamic compaction), add drainage (stone columns, gravel drains), confine (jet grout or deep soil mixing cells), or design the structure on piles with down-drag and lateral spreading.
- Check after treatment with the same method as the triggering analysis (`turba-seismic-liquefaction`): CPT/SPT between columns; do not count the column stiffness reduction of stress for silty sands without justification.

## 8. Specification and control

- The specification gives the performance (settlement, bearing, FS against liquefaction), the tests to prove it and the acceptance criteria, rather than a method only.
- Trial area before production, execution records for every element, acceptance tests per lot.

## 9. Common pitfalls

- Stone columns in very soft clay or organic soil without confinement check.
- Rigid inclusions treated as piles (or the reverse).
- Drains without a sufficiently permeable drainage blanket.
- Densification claims in silty sand with high fines.
- No trial area.
