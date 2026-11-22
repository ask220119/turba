---
name: turba-slope-stability
description: Stabilité des pentes et remblais et confortements - équilibre limite (Bishop, Fellenius, surfaces non circulaires), calcul à la rupture, réduction c-phi aux éléments finis, rétro-analyse des talus et glissements existants, Eurocode 7 approche 3 et NF P94-270, parois clouées (Clouterre), tirants et pieux stabilisateurs, drainage, vérification sismique pseudo-statique. Pour tout calcul ou contrôle de talus, déblai, remblai ou paroi clouée.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: slopes
  standards: "EN 1997-1, NF P94-270, Clouterre recommendations (1991, 2002)"
  language: fr
---

# Stabilité des pentes et confortements

Charger `turba-core` d'abord. Version anglaise : `SKILL.md`.

## 1. Démarche

1. **Reconnaître le phénomène** : géomorphologie, indices de mouvement, piézomètres, inclinomètres (profondeur de la surface de glissement), historique. Classer : glissement plan, rotationnel, coulée, chute de blocs.
2. **Modèle géotechnique** : c', φ' (valeurs résiduelles si le glissement est réactivé), cu à court terme, γ, eau (hydrostatique, ru, maillage de pressions ou calcul d'écoulement).
3. **État initial / rétro-analyse, toujours en premier** : un talus existant stable doit donner F ≥ 1,0 à 1,2 ; un glissement actif F ≈ 1,0. Caler c' et φ' dessus.
   - Un front vertical stable de hauteur H donne une borne inférieure de la cohésion : Hc = 3,83 · (c'/γ) · tan(45° + φ'/2) (Taylor). Cette cohésion est en partie apparente (succion) : la protection et le drainage du front font partie du projet.
4. **Solutions** : terrassement (allègement en tête, butée en pied, adoucissement), drainage (tranchées, masques, drains subhorizontaux), éléments résistants (clous, tirants, pieux, micropieux, géosynthétiques).
5. **Calculs par phase** : chaque passe de terrassement, renforcement, service, séisme, nappe haute.

## 2. Méthodes et format de sécurité

- **Équilibre limite par tranches** : Fellenius (prudente, circulaire), Bishop simplifié (référence pour les cercles), Morgenstern-Price / Spencer / perturbations pour les surfaces non circulaires.
- **Calcul à la rupture** (mécanismes cinématiques en spirale logarithmique) : contrôle indépendant des méthodes des tranches.
- **Réduction c-φ aux EF** : aucune hypothèse sur le mécanisme ; vérifier la stationnarité de ΣMsf.
- **Coefficient global traditionnel** : F ≥ 1,5 définitif, F ≥ 1,3 provisoire (< 1 an). Glissement existant : améliorer F de 10 à 20 % par rapport à l'état initial calé.
- **Eurocode 7, approche 3** (stabilité générale) : γtanφ' = γc' = 1,25, γcu = 1,4, actions variables × 1,3 ; la NF P94-270 ajoute un facteur de modèle γR;d = 1,0 à 1,2 selon la classe de conséquence.
- **Séisme** : pseudo-statique kh, kv (kv = ± 0,5 kh), puis déplacement de Newmark si F < 1 sous l'accélération de calcul. Voir `turba-seismic-liquefaction` pour kh.

Script : `scripts/bishop.py` (Bishop simplifié sur un cercle, sol multicouche, nappe) pour les contrôles indépendants.

## 3. Parois clouées (NF P94-270, Clouterre)

- **Domaine** : déblais en terrain hors d'eau, passes descendantes ; densité 0,15 à 0,4 clou/m² ; diamètre de forage 100 à 200 mm ; capacité de clou 200 à 600 kN.
- **Séquence** : passe → drainage et premier treillis → forage, armature, scellement → béton projeté → platines et second treillis. Hauteur de passe validée par plots d'essai. Les clous ne tiennent pas le parement pendant la passe ouverte.
- **Mécanismes ELU** :
  1. stabilité externe générale (grand glissement contournant le massif), approche 3 ;
  2. stabilité externe locale : massif cloué comme mur poids (portance, glissement), approche 2, et mécanismes à deux ou trois blocs. Les seuls cercles débouchant en pied ne suffisent pas ;
  3. stabilité mixte (surfaces recoupant les clous), la traction seule suffit généralement ;
  4. stabilité interne : arrachement, rupture de l'armature (surépaisseur de corrosion), parement et liaisons.
- **Frottement qs** : en projet, abaques Clouterre qs = f(pl*) ; en exécution, essais d'arrachement à la rupture obligatoires. Les facteurs ξ dépendent du nombre d'essais.
- **Parement** : effort en tête T0 = Tmax · [0,5 + (s − 0,5)/5], s = max(sh, sv) en m (Clouterre 2002) ; poinçonnement et flexion du béton projeté.
- **Déplacements ELS** (δv ≈ δh) : rocher H/1000, sables 2H/1000, argiles 4H/1000.

## 4. Pieux stabilisateurs

1. Caler l'état initial (F ≈ 1). 2. Choisir des pieux raides traversant la surface de glissement et ancrés en dessous. 3. Effort tranchant mobilisé par pieu = min(plastification du sol en butée, moment plastique Mp, capacité à l'effort tranchant). 4. Rechercher de nouvelles surfaces au-dessus et en dessous de la file de pieux. 5. Vérifier le pieu sous le déplacement du sol g(z) (voir `turba-foundations`).

## 5. Autres confortements

- Le **drainage** est souvent la mesure la plus efficace par euro investi ; le justifier par le rabattement calculé ou mesuré et prévoir l'entretien.
- **Remblais légers** (PSE, verre cellulaire) pour décharger une pente ou un sol mou.
- **Sols renforcés et talus raidis** : géosynthétiques, avec résistances à l'arrachement et à la traction pondérées.

## 6. Contrôle des logiciels

- Les grilles de recherche automatiques peuvent surestimer Fmin de 5 à 15 % quand elles sont grossières. Resserrer manuellement (pas ≤ 0,5 m) autour du centre critique et tester des centres au niveau du terrain derrière la crête (cercles raides sous les surcharges).
- Comparer deux méthodes sur la même surface avant de comparer les minima, pour ne pas confondre un défaut de recherche avec un écart de mécanique.
- Une couche sans frottement défini pour les clous a un frottement nul silencieux dans certains logiciels : vérifier chaque couche traversée.

## 7. Trame de note

1. Objet, mission, visite de site. 2. Géologie, hydrogéologie, historique, auscultation. 3. Modèle géotechnique et rétro-analyse. 4. Hypothèses (surcharges, eau, séisme, durée de vie, classe de conséquence). 5. Méthodes et format de sécurité. 6. Variantes. 7. Résultats par phase (tableau de Fmin par phase et par jeu de coefficients). 8. Éléments : clous, tirants, parement, drains. 9. Essais et seuils d'auscultation. 10. Points à confirmer.

## 8. Pièges fréquents

- Pas d'état initial calé : le F de projet n'a pas de sens.
- Nappe mal définie.
- Seulement des cercles débouchant en pied pour un massif cloué ou un sol hétérogène.
- Phases provisoires oubliées (passe ouverte avant clouage).
- qs de projet sans essais d'arrachement ; ignorer la perte de cohésion apparente à la saturation.
