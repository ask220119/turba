---
name: turba-foundations
description: Conception et vérification des fondations superficielles, radiers, fondations semi-profondes et profondes (pieux, barrettes, groupes) selon l'Eurocode 7 et les NF P94-261/262 - portance depuis le pressiomètre, le CPT ou c-phi, tassements (Ménard, élasticité, œdomètre), portance et loi t-z des pieux, frottement négatif, efforts transversaux et raideurs pour le BE structure. Pour tout calcul ou contrôle de fondation.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: foundations
  standards: "EN 1997-1, NF P94-261, NF P94-262"
  tests: "PMT, CPT, SPT, oedometer"
  language: fr
---

# Fondations et interaction sol-structure statique

Charger `turba-core` d'abord. Version anglaise : `SKILL.md`. Ce skill part d'un modèle géotechnique interprété (pl*, EM, α, qc, c', φ', cu). Pour l'interprétation des essais bruts, utiliser `turba-site-investigation`.

## 1. Démarche

1. **Descente de charges** : tableau des torseurs par appui (N, Hx, Hy, Mx, My) pour chaque combinaison (ELS quasi permanent, ELS caractéristique, ELU fondamental, ELU accidentel / sismique).
2. **Type de fondation** selon l'encastrement D et la largeur B :
   - sous charge axiale : superficielle D/B < 1,5 à 2,5, semi-profonde jusqu'à 5, profonde au-delà (définitions NF P94-261 / 262) ;
   - sous charge transversale : comportement de semelle D/B < 5, de pieu D/B > 10.
3. **Portance (ELU et ELS)**, puis **tassements** (absolus et différentiels), puis **interaction** (raideurs, redistribution), puis **effets parasites** (groupe, frottement négatif, poussées latérales, ouvrages voisins).

Les règles de portance sont une manière déguisée de limiter le tassement : ne jamais s'arrêter à la portance.

## 2. Choisir le module

Le module doit correspondre au niveau de déformation de l'ouvrage :

| Déformation | Cas type | E depuis le pressiomètre | E depuis le CPT |
|---|---|---|---|
| ≈ 1 % | semelle proche de la rupture, sol mou sous remblai | 2 à 3 × EM (≈ EM/α) | 2 à 6 × qc |
| ≈ 0,1 % | semelles et radiers courants en service | 3 à 6 × EM | 3 à 10 × qc |
| ≈ 0,01 % | séisme, vibrations | 6 à 12 × EM | 5 à 20 × qc |

- Coefficient de Poisson 0,25 à 0,35 drainé, 0,5 non drainé.
- Le pressiomètre n'est pas adapté aux grandes déformations des sols compressibles : utiliser les paramètres œdométriques (Cc, Cs, σ'p, Cαε) pour les argiles molles et les remblais sur sol mou.

## 3. Fondations superficielles (NF P94-261)

- **Portance au pressiomètre** : q_net = kp · ple*, kp selon les courbes de la norme (classe de sol, De/B, B/L). Réductions pour l'inclinaison de la charge (iδ) et la proximité d'un talus (iβ).
- **Portance c-φ** : q = c'Nc sc ic + q0 Nq sq iq + 0,5 γ' B' Nγ sγ iγ (EN 1997-1 annexe D) ; non drainé Nc = π + 2.
- **Excentrement** : largeur effective B' = B − 2e (Meyerhof). Surface comprimée : 100 % à l'ELS quasi permanent (e ≤ B/6), ≥ 75 % à l'ELS caractéristique (e ≤ B/4), ≥ 10 % à l'ELU (e ≤ 7B/15), semelle rectangulaire.
- **Coefficients ELU (approche 2)** : portance γR;v = 1,4 avec facteur de modèle γR;d;v = 1,2 (pressiomètre) ; glissement γR;h = 1,1.
- **ELS** : q_ref ≤ ple*·kp/(γR;v · γR;d;v) avec γR;v = 2,3 (vérification ELS NF P94-261), plus la vérification des tassements.

### Tassements

Quatre niveaux de méthode, du simple au détaillé :

1. empirique : Ménard (pressiomètre, NF P94-261 annexe H), Schmertmann (CPT) ;
2. élastique : Boussinesq / Steinbrenner multicouche, coefficients de Giroud ;
3. modèles hybrides sol-structure (radier sur ressorts calés sur un multicouche élastique) ;
4. éléments finis.

**Ménard (sol homogène, B > B0 = 0,6 m)** :

```
s = sc + sd
sc = (α / (9 Ec)) · (q − σv0) · λc · B
sd = (2 / (9 Ed)) · (q − σv0) · B0 · (λd · B / B0)^α
```

| L/B | cercle | 1 (carré) | 2 | 3 | 5 | 20 |
|---|---|---|---|---|---|---|
| λc | 1,00 | 1,10 | 1,20 | 1,30 | 1,40 | 1,50 |
| λd | 1,00 | 1,12 | 1,53 | 1,78 | 2,14 | 2,65 |

Sol hétérogène : Ec = E1 (première tranche B/2), Ed = moyenne harmonique des tranches de B/2 jusqu'à 8B (pondération de l'annexe H). Script : `scripts/menard_settlement.py`.

**Ordres de grandeur** : semelle isolée environ 1 cm ; grand radier 1 à 10 cm ; réservoir environ 10 cm ; remblai sur sol mou 10 à 100 cm.

**Distorsions admissibles** : bâtiments courants 1/500 ; IGH et structures hyperstatiques 1/1000 ; l'annexe H de l'EN 1997-1 donne 1/2000 à 1/300 à l'ELS et environ 1/150 à l'ELU pour les bâtiments.

## 4. Radiers et dallages

- La rigidité relative radier/sol doit être modélisée : un ressort uniforme sous un radier peut même inverser la fibre tendue.
- Coefficients de réaction zonés : K_bord ≈ 2 à 3 × K_centre. Itérer : DDC → modèle géotechnique → K zonés → modèle de structure → nouvelle DDC, jusqu'à stabilisation.
- Aucune traction à l'interface ; pression d'interface inférieure à la pression de fluage.

## 5. Fondations profondes (NF P94-262)

- **Portance** : R = Rb + Rs = Ab · qb + P · Σ qs,i · Δzi.
  - qb = kp · ple* (pressiomètre) ou kc · qce (CPT) ; kp, kc selon la classe de sol et la classe de pieu.
  - qs selon les courbes fsol(pl*) ou fsol(qc) de la norme, plafonné par classe de pieu (qs,max).
- Rupture conventionnelle à un tassement en tête de B/10 ; charge de fluage Rc,cr ≈ 0,7 Rc pour les pieux refoulants, 0,5 Rb + 0,7 Rs pour les pieux forés.
- **Comportement en service** (30 à 50 % de Rc) : tassement en tête ≈ B/150 à B/100 ; frottement mobilisé pour moins de 1 cm.
- **Loi t-z (Frank et Zhao)** : sols fins kτ = 2,0 EM / B, kq = 11 EM / B ; sols granulaires kτ = 0,8 EM / B, kq = 4,8 EM / B ; trilinéaire avec une première pente jusqu'à qs/2 et qb/2.
- **Groupes** : vérifier la rupture en bloc et l'efficacité si l'entraxe < 3B ; tassement du groupe par facteurs d'interaction (Poulos et Davis) ou semelle équivalente.
- **Frottement négatif** (Combarieu) : qsn = K tanδ · σ'v sur la hauteur où le sol tasse plus que le pieu ; il ajoute de la charge et réduit la longueur utile.
- **Efforts transversaux** : EI y'''' + Es y = 0, longueur de transfert l0 = (4 EI / Es)^(1/4) ; Es ≈ 2 EM (sols fins) à 4 EM (granulaires) en ordre de grandeur ; réaction plafonnée par la pression de fluage pf. Pieu court rigide si D ≲ l0, pieu long si D ≳ 3 l0.

## 6. Raideurs pour le BE structure

- Définir les raideurs dans le domaine de service, jamais à la rupture. Ordre de grandeur KV ≈ 100 · V_service / B.
- Semelles : vertical par Ménard / élasticité, horizontal et rotation par formules élastiques (Gazetas).
- Pieux : t-z et p-y calés sur le pressiomètre ; fournir les termes couplés H-M ; la raideur latérale est gouvernée par les 3 à 6 B supérieurs.
- Fournir séparément les raideurs statiques et sismiques (sismiques depuis G0, voir `turba-seismic-liquefaction`).

## 7. Trame de note

1. Objet, mission, références. 2. Ouvrage et tableau des charges. 3. Modèle géotechnique et choix des modules. 4. Choix du type de fondation. 5. Portance ELU / ELS par appui avec taux de travail. 6. Tassements et distorsions vs critères. 7. Raideurs. 8. Effets parasites. 9. Dispositions constructives, essais de chargement, auscultation.

## 8. Pièges fréquents

- Étendre EM/α sur toute la profondeur : surestime le tassement (le module croît au-delà de B/2).
- Un ressort uniforme sous un radier.
- Oublier le frottement négatif sous un remblai neuf ou sur un terrain récemment remblayé.
- Mélanger les classes de pieux NF P94-262 et le plafond qs,max.
- Raideurs sismiques tirées de l'EM statique sans justification.
