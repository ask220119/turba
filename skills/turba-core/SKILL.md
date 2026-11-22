---
name: turba-core
description: Shared rules for any geotechnical engineering task done by an AI agent (foundations, retaining walls, slopes, seismic, site investigation, ground improvement) - ground model, units, Eurocode 7 / French NF P94 safety formats, checks before issuing a result, and routing to the right TURBA skill. Load first for any geotechnical calculation or report.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: general
  standards: "EN 1997-1 (Eurocode 7), NF P94-500, NF P94-261, NF P94-262, NF P94-270, NF P94-282, RPS 2000 (2011)"
  language: en
---

# TURBA core: how to do geotechnical work as an agent

TURBA is an open collection of geotechnical engineering skills (French version: `SKILL.fr.md`; answer in the language the user writes in). This core skill holds the rules every other TURBA skill assumes. It does not replace a qualified geotechnical engineer: every result you produce is a draft that an engineer checks and signs.

## 1. Non-negotiable rules

1. **Never invent soil parameters.** If a value (c', φ', cu, EM, pl*, qc, N60, γ, k, Vs) is not given, say so, propose a range with its source (correlation, typical table, literature), and flag it as an assumption to confirm. Mark every assumed value in the output.
2. **State the standard and the version.** EN 1997-1:2004 and its national annex, the second-generation EN 1997 (2024/2025), NF P94-261/262/270/282, RPS 2000 rev. 2011 (Morocco), or another code. Do not mix partial factor sets from different documents.
3. **Units are SI and explicit**: kPa or MPa for stresses and moduli, kN and kN/m for forces, m for lengths, kN/m³ for unit weights, degrees for angles. Write the unit next to every number.
4. **Water first.** Identify groundwater levels (lowest, highest, design), drainage condition (drained or undrained, short term or long term) before choosing parameters.
5. **Check orders of magnitude** against the ranges in each skill before reporting. A result outside the range is either an error or a finding that needs an explanation.
6. **Show the chain**: inputs, method, formula, intermediate values, result, verification ratio. A bare number is not a deliverable.
7. **Back-analysis before design** whenever something already exists (stable slope, existing wall, measured settlement). Calibrate on it.

## 2. The ground model

Build it before any calculation, as a table:

| Layer | Top / bottom (m) | Description | γ / γ' (kN/m³) | Strength (c', φ' or cu) | Stiffness (EM, α or E', or qc) | Permeability | Source |
|---|---|---|---|---|---|---|---|

- Characteristic values (EN 1997-1 §2.4.5.2): a cautious estimate of the value governing the limit state, not the mean of the tests. For a large volume of soil, close to the mean; for a local mechanism, close to a low fractile. Say which one you used and why.
- Split a thick layer when the tests show a clear trend with depth.
- Keep a column for the source of every value (test number, correlation, assumption).

## 3. Safety formats (summary)

- **Eurocode 7, design approach 2 (France, Morocco by practice)**: factors on actions and on resistances (A1 + M1 + R2). Bearing γR;v = 1.4, sliding γR;h = 1.1 (NF P94-261), plus model factors in the French application standards.
- **Design approach 3**: factors on material strengths, used for overall stability (γφ' = γc' = 1.25, γcu = 1.4).
- **Traditional global factor of safety** (legacy, still asked for by some clients): F ≥ 1.5 permanent, F ≥ 1.3 temporary for slopes.
- Load combinations: ULS fundamental (1.35 G + 1.5 Q), ULS accidental and seismic (1.0 G + ψ2 Q + AE), SLS characteristic and quasi-permanent.

Always write the verification as a ratio Ed / Rd ≤ 1 (or F ≥ Fmin) so a reader sees the margin.

## 4. Before you issue anything

- [ ] Ground model table present, every assumed value flagged.
- [ ] Standard, version and safety format named.
- [ ] All design situations covered (construction stages, long term, high water, seismic if required).
- [ ] Units checked, orders of magnitude checked.
- [ ] Limits of the method stated (what is not covered).
- [ ] A list of points the engineer must confirm.

## 5. Routing

| Task | Skill |
|---|---|
| Plan or interpret a site investigation, characteristic values, G1/G2 reports | `turba-site-investigation` |
| Shallow footings, rafts, piles, settlements, soil springs | `turba-foundations` |
| Embedded walls, deep excavations, anchors, struts | `turba-retaining-walls` |
| Slopes, embankments, soil nailing, stabilising piles | `turba-slope-stability` |
| Seismic action, site class, liquefaction, dynamic earth pressure | `turba-seismic-liquefaction` |
| Stone columns, rigid inclusions, preloading, grouting | `turba-ground-improvement` |

## 6. Mission phases (NF P94-500)

G1 (site study, general principles), G2 AVP / PRO / DCE-ACT (design), G3 (contractor's execution design), G4 (supervision of G3), G5 (diagnosis). Say which phase the output belongs to: the level of detail and the required data differ.
