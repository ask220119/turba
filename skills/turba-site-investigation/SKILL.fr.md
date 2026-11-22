---
name: turba-site-investigation
description: Programmation, contrôle et interprétation des reconnaissances géotechniques - sondages, pressiomètre (PMT, Ménard), SPT, CPT/CPTu, essais de laboratoire (identification, œdomètre, triaxial, boîte de cisaillement), géophysique, piézomètres - construction du modèle géotechnique et des valeurs caractéristiques selon l'Eurocode 7, rédaction des rapports G1/G2 selon la NF P94-500. Dès que des résultats d'essais doivent être lus, contrôlés, corrélés ou transformés en paramètres de calcul.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: site-investigation
  standards: "EN 1997-1, EN 1997-2, NF P94-500, NF EN ISO 22476-1/-3/-4, NF EN ISO 14688, NF EN ISO 17892"
  tests: "PMT, SPT, CPT, CPTu, oedometer, triaxial, MASW"
  language: fr
---

# Reconnaissances et modèle géotechnique

Charger `turba-core` d'abord. Version anglaise : `SKILL.md`.

## 1. Programmer une reconnaissance

- **Profondeur** : semelles au moins 1,5 B sous le niveau d'assise (plus pour les radiers : environ 1,5 B du radier ou jusqu'à une couche raide) ; pieux au moins 5 B sous la pointe prévue et 3 m minimum ; fouilles au moins 1,5 H sous le fond ou jusqu'à une couche imperméable pour l'hydraulique. L'annexe B.3 de l'EN 1997-2 donne des indications.
- **Maillage** : bâtiments 15 à 40 m ; ouvrages linéaires 20 à 200 m selon la variabilité ; au moins trois points par ouvrage.
- **Panachage** : un type d'essai continu partout (CPT en sols mous à moyens, pressiomètre en sols raides et matériaux rocheux, SPT quand aucun des deux ne convient) plus des sondages carottés pour le log et les prélèvements, des piézomètres pour l'eau, la géophysique pour Vs et pour interpoler entre les points.
- **Laboratoire** : identification sur chaque couche (granulométrie, limites d'Atterberg, teneur en eau, masse volumique), puis essais mécaniques là où le calcul en a besoin (œdomètre pour le tassement des sols fins, triaxial CU/CD pour c', φ', UU ou scissomètre pour cu).

## 2. Contrôler les données brutes

- **Pressiomètre (NF EN ISO 22476-4, Ménard)** : vérifier les étalonnages (membrane, perte de volume), la courbe de fluage, que pl est atteinte ou extrapolée dans les limites (extrapoler au-delà de 2 à 3 × pf n'est pas fiable), le rapport EM/pl. EM/pl* types : argile normalement consolidée 9 à 16, argile surconsolidée > 16, sable lâche 7 à 10, sable dense 12 à 15 ; α selon le type de sol et EM/pl.
- **SPT (NF EN ISO 22476-3)** : rendement énergétique Er pour N60 = N · Er/60 ; écarter les essais perturbés par des graviers ou par la remontée du sable sous l'eau.
- **CPT / CPTu (NF EN ISO 22476-1)** : dérive du zéro, inclinaison, saturation de u2, rapport de surface a pour qt = qc + u2(1 − a). Type de comportement du sol par l'indice Ic de Robertson (2009/2010).
- **Sondages** : description selon NF EN ISO 14688 / 14689 ; confronter le log et les essais et les mettre en cohérence avant interprétation.

## 3. Paramètres interprétés (ordres de grandeur)

| Sol | pl* (MPa) | EM (MPa) | qc (MPa) | N60 | φ' (°) | cu (kPa) |
|---|---|---|---|---|---|---|
| Argile molle | < 0,3 | < 3 | < 0,7 | < 4 | 20 à 25 | 10 à 40 |
| Argile ferme à raide | 0,3 à 1,0 | 3 à 15 | 0,7 à 2,5 | 4 à 15 | 22 à 28 | 40 à 150 |
| Argile dure, marne | 1,0 à 3,0 | 15 à 100 | > 2,5 | > 15 | 25 à 32 | > 150 |
| Sable lâche | < 0,5 | < 5 | < 5 | < 10 | 28 à 32 | sans objet |
| Sable moyennement dense | 0,5 à 1,5 | 5 à 20 | 5 à 15 | 10 à 30 | 32 à 36 | sans objet |
| Sable dense, grave | > 1,5 | > 20 | > 15 | > 30 | 36 à 42 | sans objet |
| Rocher altéré | 2,5 à 4 | 50 à 200 | refus | refus | sans objet | sans objet |

Corrélations à utiliser avec prudence (toujours les citer) : cu ≈ (qt − σv0)/Nkt avec Nkt de 10 à 20 (à caler) ; cu ≈ pl*/5,5 (argile raide, type Ménard) ; φ' depuis (N1)60 ou qc1N (Kulhawy et Mayne 1990, Robertson 2010) ; E' depuis EM (voir `turba-foundations` §2).

## 4. Valeurs caractéristiques (EN 1997-1 §2.4.5.2)

- Regrouper les données par couche après avoir vérifié que la couche est homogène ; tracer chaque paramètre en fonction de la profondeur.
- Si le mécanisme mobilise un grand volume (frottement d'un pieu sur plusieurs mètres, tassement d'un radier, stabilité générale), prendre une estimation prudente de la moyenne : Xk = Xmoy · (1 − kn · Vx) avec kn tiré du facteur de Student pour la moyenne (kn ≈ 0,3 à 0,6 pour n = 10 à 5 essais).
- Si le mécanisme est local (pointe d'un pieu, petite semelle), prendre un fractile bas (5 %) : kn ≈ 1,8 à 2,0 pour n = 10 à 5.
- En présence d'une tendance avec la profondeur, ajuster la tendance et appliquer la réduction aux résidus.
- Toujours donner n, la moyenne, l'écart type, Vx, le kn retenu et sa justification, et confronter au jugement et à l'expérience locale.

## 5. L'eau

- Au moins un piézomètre par unité hydrogéologique, relevé dans le temps (variations saisonnières) ; le niveau noté en cours de forage ne suffit pas.
- Donner trois niveaux : bas (flottabilité et soulèvement en phase travaux), normal (service), haut / exceptionnel (calcul et soulèvement de l'ouvrage définitif).

## 6. Rapports (NF P94-500)

- **G1 (ES / PGC)** : géologie, aléas, modèle préliminaire, principes généraux de construction, programme de reconnaissance pour la G2.
- **G2 AVP / PRO** : modèle géotechnique avec valeurs caractéristiques, conception des fondations / soutènements, variantes et coûts, risques et incertitudes résiduelles.

Trame : 1. Objet, mission, documents. 2. Site et projet. 3. Géologie et aléas. 4. Reconnaissances réalisées (plan, tableau des points). 5. Résultats par type d'essai. 6. Modèle géotechnique (tableau, coupe) et valeurs caractéristiques. 7. Eau. 8. Conception ou principes géotechniques. 9. Risques et incertitudes résiduelles, reconnaissances complémentaires recommandées. Annexes : logs, fiches d'essais.

## 7. Pièges fréquents

- Moyenner des essais de couches différentes.
- Utiliser pl* là où la norme demande ple* (pression limite équivalente sur la zone d'influence).
- N du SPT utilisé sans correction d'énergie.
- Niveau d'eau tiré d'une seule lecture en cours de forage.
- Pas de colonne pour la source de chaque paramètre.
