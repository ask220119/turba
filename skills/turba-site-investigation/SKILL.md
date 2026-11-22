---
name: turba-site-investigation
description: Planning, checking and interpreting geotechnical site investigations - boreholes, pressuremeter (PMT, Menard), SPT, CPT/CPTu, laboratory tests (identification, oedometer, triaxial, shear box), geophysics, piezometers - building the ground model and characteristic values to Eurocode 7, and writing G1/G2 reports to NF P94-500. Use whenever test data must be read, checked, correlated or turned into design parameters.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: site-investigation
  standards: "EN 1997-1, EN 1997-2, NF P94-500, NF EN ISO 22476-1/-3/-4, NF EN ISO 14688, NF EN ISO 17892"
  tests: "PMT, SPT, CPT, CPTu, oedometer, triaxial, MASW"
  language: en
---

# Site investigation and ground model

Load `turba-core` first. French version: `SKILL.fr.md`.

## 1. Planning an investigation

- **Depth**: shallow footings at least 1.5 B below founding level (more for rafts: about 1.5 B of the raft or to a stiff layer); piles at least 5 B below the expected toe and 3 m minimum; excavations at least 1.5 H below the dig or to an impervious layer for hydraulics. EN 1997-2 annex B.3 gives guidance.
- **Spacing**: buildings 15 to 40 m grid; linear works 20 to 200 m depending on variability; at least three points per structure.
- **Test mix**: one continuous test type everywhere (CPT in soft to medium soils, PMT in stiff soils and rock-like materials, SPT where neither works) plus cored boreholes for logging and samples, piezometers for water, geophysics for Vs and to interpolate between points.
- **Laboratory**: identification on every layer (grading, Atterberg limits, water content, density), then mechanical tests where the design needs them (oedometer for settlement of fine soils, triaxial CU/CD for c', φ', UU or vane for cu).

## 2. Checking raw data

- **PMT (NF EN ISO 22476-4, Ménard)**: check calibration (membrane, volume loss), the creep curve, that pl is reached or extrapolated within limits (pl ≤ 2 to 3 × pf extrapolation is unreliable), EM/pl ratio. Typical EM/pl*: normally consolidated clay 9 to 16, overconsolidated clay > 16, loose sand 7 to 10, dense sand 12 to 15; α from soil type and EM/pl.
- **SPT (NF EN ISO 22476-3)**: energy ratio Er for N60 = N · Er/60; reject tests with blow counts disturbed by gravel or heave in sands under water.
- **CPT / CPTu (NF EN ISO 22476-1)**: zero drift, inclination, u2 saturation, cone area ratio a for qt = qc + u2(1 − a). Soil behaviour type from Robertson (2009/2010) Ic.
- **Boreholes**: log to NF EN ISO 14688 / 14689; compare logging with tests and reconcile before interpretation.

## 3. Interpreted parameters (orders of magnitude)

| Soil | pl* (MPa) | EM (MPa) | qc (MPa) | N60 | φ' (°) | cu (kPa) |
|---|---|---|---|---|---|---|
| Soft clay | < 0.3 | < 3 | < 0.7 | < 4 | 20 to 25 | 10 to 40 |
| Firm to stiff clay | 0.3 to 1.0 | 3 to 15 | 0.7 to 2.5 | 4 to 15 | 22 to 28 | 40 to 150 |
| Hard clay, marl | 1.0 to 3.0 | 15 to 100 | > 2.5 | > 15 | 25 to 32 | > 150 |
| Loose sand | < 0.5 | < 5 | < 5 | < 10 | 28 to 32 | n/a |
| Medium dense sand | 0.5 to 1.5 | 5 to 20 | 5 to 15 | 10 to 30 | 32 to 36 | n/a |
| Dense sand, gravel | > 1.5 | > 20 | > 15 | > 30 | 36 to 42 | n/a |
| Weathered rock | 2.5 to 4 | 50 to 200 | refusal | refusal | n/a | n/a |

Correlations to use with care (state them every time): cu ≈ (qt − σv0)/Nkt with Nkt 10 to 20 (calibrate); cu ≈ pl*/5.5 (stiff clay, Ménard type) ; φ' from (N1)60 or qc1N (Kulhawy and Mayne 1990, Robertson 2010); E' from EM (see `turba-foundations` §2).

## 4. Characteristic values (EN 1997-1 §2.4.5.2)

- Group data by layer after checking that the layer is homogeneous; plot every parameter against depth.
- If the mechanism involves a large volume (pile shaft over several metres, raft settlement, global slope), take a cautious estimate of the mean: Xk = Xmean · (1 − kn · Vx) with kn from the Student factor for the mean (kn ≈ 0.3 to 0.6 for n = 10 to 5 tests).
- If the mechanism is local (base of a pile, small footing), take a low fractile (5 %): kn ≈ 1.8 to 2.0 for n = 10 to 5.
- With a trend with depth, fit the trend and apply the reduction to the residuals.
- Always state n, mean, standard deviation, Vx, chosen kn and the reason, and compare with judgement and local experience.

## 5. Water

- At least one piezometer per hydrogeological unit, read over time (seasonal variation); record during drilling is not enough.
- Give three levels: lowest (for buoyancy and uplift at stage), normal (service), highest / exceptional (for design and uplift of the final structure).

## 6. Reports (NF P94-500)

- **G1 (ES / PGC)**: geology, hazards, preliminary model, general principles of construction, investigation programme for G2.
- **G2 AVP / PRO**: ground model with characteristic values, design of foundations / retaining structures, options and costs, risks and residual uncertainties.

Report outline: 1. Purpose, mission, documents. 2. Site and project. 3. Geology and hazards. 4. Investigation carried out (plan, table of points). 5. Results per test type. 6. Ground model (table, section) and characteristic values. 7. Water. 8. Geotechnical design or principles. 9. Risks and residual uncertainties, recommended further investigation. Appendices: logs, test sheets.

## 7. Common pitfalls

- Averaging tests across different layers.
- Using pl* where the standard asks for ple* (equivalent limit pressure over the influence zone).
- SPT N used without energy correction.
- Water level taken from a single reading during drilling.
- No column for the source of each parameter.
