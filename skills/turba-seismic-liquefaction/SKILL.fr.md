---
name: turba-seismic-liquefaction
description: Géotechnique sismique - action sismique selon l'Eurocode 8 (EN 1998-1/-5) et le RPS 2000 révisé 2011 (Maroc), classes de sol et Vs30, déclenchement de la liquéfaction par SPT et CPT (Boulanger et Idriss 2014) et ses conséquences, poussées dynamiques (Mononobe-Okabe), stabilité des pentes sous séisme, rigidité dynamique et impédances de fondations, vibrations de chantier. Pour toute question de géotechnique sismique.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: seismic
  standards: "EN 1998-1, EN 1998-5, RPS 2000 (rev. 2011), NCEER 1997, Boulanger & Idriss 2014"
  tests: "SPT, CPT, MASW, cross-hole"
  language: fr
---

# Géotechnique sismique et liquéfaction

Charger `turba-core` d'abord. Version anglaise : `SKILL.md`.

Dire quel règlement s'applique (Eurocode 8 ou RPS 2000 révisé 2011 au Maroc) et ne jamais mélanger leurs spectres ni leurs coefficients de site. Vérifier chaque coefficient dans le texte en vigueur.

## 1. Démarche

1. **Aléa** : zone sismique et accélération de référence (agR pour l'EC8 ; zones Za / Zv pour le RPS 2011), classe d'importance de l'ouvrage.
2. **Classe de site** depuis les sondages et de préférence la Vs mesurée (MASW, cross-hole, down-hole) :
   - EC8 : classes A à E plus S1, S2 selon Vs,30, NSPT, cu ;
   - RPS 2011 : sites S1 à S5 (S5 = étude spécifique).
   - Vs,30 = 30 / Σ (hi / Vs,i).
3. **Effets de site** : topographie, bassins, couches molles → spectre spécifique si nécessaire (analyse 1D linéaire équivalente).
4. **Liquéfaction** (§2), **pentes sous séisme**, **poussées dynamiques** (§3), **fondations** (§4).
5. Fournir au BE structure : classe de site, coefficient de site, accélération de calcul en surface, raideurs et amortissements.

## 2. Liquéfaction (méthode simplifiée)

**Susceptibilité** : sables et silts saturés lâches et peu plastiques. Pour les sols fins, critères de Bray et Sancio (2006) ou Boulanger et Idriss (2006) (IP < 7 : comportement de type sable).

**Sollicitation** :

```
CSR = 0,65 · (amax / g) · (σv / σ'v) · rd
rd  = exp(α(z) + β(z)·M)          (Idriss 1999)
α(z) = −1,012 − 1,126 sin(z/11,73 + 5,133)
β(z) =  0,106 + 0,118 sin(z/11,28 + 5,142)      (z en m)
```

**Résistance, SPT (Boulanger et Idriss 2014)** :

```
(N1)60 = CN · N60,  CN = (Pa/σ'v)^m ≤ 1,7,  m = 0,784 − 0,0768 √(N1)60cs  (itérer)
Δ(N1)60 = exp(1,63 + 9,7/(FC+0,01) − (15,7/(FC+0,01))²)
(N1)60cs = (N1)60 + Δ(N1)60
CRR(M=7,5, σ'v=1 atm) = exp( N/14,1 + (N/126)² − (N/23,6)³ + (N/25,4)⁴ − 2,8 ),  N = (N1)60cs
MSF = 1 + (MSFmax − 1)(8,64 exp(−M/4) − 1,325),  MSFmax = 1,09 + ((N1)60cs/31,5)² ≤ 2,2
Kσ  = 1 − Cσ ln(σ'v/Pa) ≤ 1,1,  Cσ = 1/(18,9 − 2,55 √(N1)60cs) ≤ 0,3
FS  = CRR · MSF · Kσ / CSR
```

**Résistance, CPT (Boulanger et Idriss 2014)** : qc1Ncs = qc1N + Δqc1N, avec la correction de fines depuis Ic ; CRR = exp( qc1Ncs/113 + (qc1Ncs/1000)² − (qc1Ncs/140)³ + (qc1Ncs/137)⁴ − 2,80 ).

Script : `scripts/liquefaction_spt.py` (un profil SPT, donne CSR, CRR, FS par essai).

**Critère** : FS ≥ 1,25 est une cible courante (l'annexe B de l'EC8-5 admet FS ≥ 1,25 avec la méthode simplifiée) ; suivre le règlement du projet.

**Conséquences, toujours** : tassement post-liquéfaction (Ishihara et Yoshimine 1992, Zhang et al. 2002), déplacements latéraux, perte de frottement et frottement négatif sur les pieux, perte de portance des fondations superficielles. Traitement : voir `turba-ground-improvement`.

## 3. Poussées dynamiques (EN 1998-5 / Mononobe-Okabe)

- Coefficients pseudo-statiques : kh = α · S / r, kv = ± 0,5 kh (ou 0,33 kh selon le type de spectre), α = ag/g ; r = 2 pour un mur libre de se déplacer (jusqu'à 300α·S mm), 1,5 pour des déplacements plus faibles, 1 pour un ouvrage rigide.
- Mononobe-Okabe pour la poussée et la butée ; distinguer remblai perméable et imperméable sous la nappe ; pression hydrodynamique de Westergaard pour l'eau libre.
- Intégrer l'incrément dynamique dans le modèle de l'écran (voir `turba-retaining-walls`).

## 4. Rigidité dynamique et fondations

- G0 = ρ · Vs². Courbes G/G0 et amortissement en fonction de la déformation (Vucetic et Dobry 1991, Darendeli 2001).
- Ne pas utiliser l'EM du pressiomètre en dynamique sans facteur justifié (G0 ≈ 8 à 12 × EM n'est qu'un ordre de grandeur).
- Impédances des semelles et groupes de pieux : formules de Gazetas (1991) ; fournir séparément raideurs statiques et sismiques.
- Pieux sous séisme : effets inertiels et cinématiques (flexion aux interfaces entre couches de rigidités contrastées).

## 5. Vibrations de chantier

Battage, compactage dynamique, explosifs : limites de vitesse particulaire selon les règles nationales applicables (par exemple DIN 4150-3, BS 7385-2, circulaire française du 23 juillet 1986) ; surveiller les avoisinants sensibles.

## 6. Pièges fréquents

- Mélanger les classes de sol ou les spectres de l'EC8 et du RPS.
- Utiliser amax au rocher au lieu de l'accélération en surface du site dans le CSR.
- Appliquer la corrélation SPT au N brut au lieu du N60 (rendement énergétique).
- Donner FS sans les conséquences (tassement, déplacement latéral, effets sur les pieux).
- Appliquer la correction de fines à des sols argileux non susceptibles.
