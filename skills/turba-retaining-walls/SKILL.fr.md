---
name: turba-retaining-walls
description: Conception et vérification des écrans de soutènement et fouilles profondes (parois moulées, pieux sécants ou contigus, berlinoises, palplanches, butons, tirants) selon l'Eurocode 7 approche 2 et la NF P94-282 - poussée et butée, méthode aux coefficients de réaction, phasage, longueur libre des tirants (Kranz), soulèvement hydraulique et renard, stabilité du fond, tassement des avoisinants. Pour tout calcul ou contrôle de soutènement de fouille.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: retaining-structures
  standards: "EN 1997-1, NF P94-282, EN 1993-5, NF EN 1537, NF EN ISO 22477-5"
  language: fr
---

# Écrans de soutènement et fouilles profondes

Charger `turba-core` d'abord. Version anglaise : `SKILL.md`.

## 1. Démarche

1. **Géométrie et avoisinants** : profondeur de fouille H, bâtiments voisins (niveau de fondation, distance, sensibilité), voiries, réseaux, surcharges.
2. **Modèle géotechnique et hydraulique** : couches avec γ, c', φ', cu, δ/φ, paramètres de réaction ; niveaux d'eau des deux côtés à chaque phase ; perméabilités pour le rabattement et les écoulements.
3. **Type d'écran** : berlinoise (hors d'eau), palplanches (sols mous, eau), pieux sécants / contigus, paroi moulée (profond, eau, rigide), paroi clouée (hors d'eau, voir `turba-slope-stability`).
4. **Appuis** : console, butons, tirants, risbermes, planchers en taupe.
5. **Calcul phasé** : chaque niveau de terrassement, chaque mise en place d'appui, chaque mise en tension, phases finale et long terme, nappe haute, séisme si exigé.
6. **Vérifications** (§3) et **déplacements et avoisinants** (§5).

## 2. Méthodes

- **Poussée et butée limites** : Ka, Kp par les tables de Kérisel-Absi ou Coulomb / Caquot avec δ/φ (poussée +2/3, butée −2/3 usuels pour un écran béton ; −1/2 ou moins si l'écran peut tasser).
- **Méthode aux coefficients de réaction (MISS)** : ressorts élastoplastiques bornés entre poussée et butée ; coefficient kh de Ménard / Balay (pressiomètre) ou formule de Schmitt : kh = 2,1 · (EM/α)^(4/3) / (EI)^(1/3) (Schmitt 1995, kh en kN/m³ avec EM en kPa, EI en kN·m²/m). La NF P94-282 annexe F décrit la méthode.
- **Éléments finis** (PLAXIS etc.) : modèle Hardening Soil avec rigidité aux petites déformations pour les déplacements ; vérifier les mêmes ELU qu'en MISS.
- L'historique compte : la MISS doit suivre le phasage réel (modules de déchargement-rechargement, précontrainte).

## 3. Vérifications ELU (NF P94-282, approche 2)

| Vérification | Règle |
|---|---|
| Butée mobilisée | Bt / γR;e ≥ Bm, γR;e = 1,4 (avec γR;d si requis) |
| Équilibre vertical | efforts descendants (composante verticale des tirants, poids propre, frottement) vs résistance de pointe et de frottement (NF P94-262) |
| Résistance structurale | flexion, effort tranchant (EN 1992 / EN 1993-5), facteur 1,35 sur les sollicitations MISS |
| Tirants | résistance à l'arrachement ELU depuis les essais (NF EN ISO 22477-5), capacité de l'armature ; facteurs ξ |
| Butons | flambement, température, perte accidentelle d'un buton |
| Stabilité générale | approche 3, rupture profonde derrière les tirants (Kranz) et grand glissement |
| Hydraulique | soulèvement (UPL), boulance (HYD), érosion interne et renard |

### Tirants

- Longueur libre : le scellement doit commencer au-delà du coin de poussée avec une marge, usuellement d_coin + 0,15 H, et la vérification de Kranz (ligne de rupture profonde du centre du scellement au point d'effort tranchant nul théorique de l'écran) doit donner Fs ≥ 1,5 (traditionnel) ou l'équivalent approche 2.
- Effort de blocage P0 tiré de la MISS ; vérifier 1,35 P0 ≤ résistance / γ ; contrainte de l'armature au blocage ≤ 0,6 fp0,1k.
- Essais : essais préalables (à la rupture, avant travaux), essais de conformité, essais de réception sur chaque tirant (NF EN ISO 22477-5).

### Stabilité hydraulique

- Boulance : comparer le gradient hydraulique en pied au gradient critique (i_c ≈ γ'/γw ≈ 1), coefficient ≥ 1,5 à 2 selon le sol ; méthode du prisme de Terzaghi en pied.
- Soulèvement d'une couche imperméable sous le fond : poids total au-dessus vs pression d'eau en dessous, γG,stb = 0,9, γG,dst = 1,0 (UPL).
- Débit entrant dans la fouille : réseau d'écoulement ou calcul EF, à comparer à la capacité de pompage.

## 4. ELS

- Déplacements de l'écran par MISS ou EF, avec les paramètres caractéristiques.
- Déplacement latéral maximal type : 0,1 à 0,2 % H pour un écran rigide bien appuyé en sol raide ; 0,5 à 1 % H pour une console ou des argiles molles.

## 5. Avoisinants

- Cuvette de tassement derrière l'écran : enveloppes de Clough et O'Rourke (1990) (sables et argiles raides : δv,max ≈ 0,15 % H sur 2H ; argiles molles : jusqu'à 0,5 à 1 % H sur 2 à 3H) ; ou formes de Hsieh et Ou (1998). Ou report des déplacements EF.
- Évaluation des dommages : Burland et Wroth (1974), Boscardin et Cording (1989) : distorsion angulaire et déformation horizontale → catégorie de dommage 0 à 5. Viser la catégorie ≤ 1 (très léger) pour les bâtiments sensibles.
- Ajouter l'effet des charges des avoisinants sur l'écran (surcharge des fondations : Boussinesq ou diffusion simplifiée de la norme).

## 6. Trame de note

1. Objet, mission, références. 2. Site, avoisinants (tableau des distances et niveaux de fondation). 3. Modèle géotechnique et hydraulique. 4. Choix de l'écran et des appuis. 5. Phasage (figure). 6. Résultats MISS / EF par phase : moments, efforts tranchants, efforts dans les appuis, déplacements. 7. Tableau des vérifications ELU (taux). 8. Tirants (P0, longueur libre, essais). 9. Hydraulique. 10. Avoisinants : tassements et catégorie de dommage. 11. Plan d'auscultation avec seuils de vigilance et d'alerte.

## 7. Pièges fréquents

- Niveaux d'eau non précisés par phase des deux côtés.
- MISS lancée sans le phasage réel ou avec une seule raideur en chargement et déchargement.
- Oublier l'équilibre vertical d'un écran tiranté (les tirants inclinés poussent l'écran vers le bas).
- Scellement dans le coin de poussée ou sous la fondation d'un voisin sans son accord.
- Auscultation sans seuils.
