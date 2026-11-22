---
name: turba-ground-improvement
description: Choix, dimensionnement, prescription et contrôle des techniques d'amélioration et de renforcement des sols - colonnes ballastées (CFMS 2011), inclusions rigides (ASIRI), drains verticaux et préchargement, remblais sur sols compressibles, compactage dynamique, vibrocompactage, injections et jet grouting, traitement à la chaux ou au ciment, géosynthétiques, traitement contre la liquéfaction. Pour tout choix, calcul ou prescription d'amélioration de sol.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: ground-improvement
  standards: "CFMS recommendations for stone columns (2011), ASIRI national project (2012), EN 14731, EN 12716, EN 15237"
  language: fr
---

# Amélioration des sols

Charger `turba-core` d'abord. Version anglaise : `SKILL.md`.

## 1. Choisir une technique

| Problème | Sol | Techniques |
|---|---|---|
| Tassement sous remblai ou dallage | argile molle, limon | préchargement + drains verticaux, inclusions rigides, remblai léger |
| Tassement sous semelles | remblai hétérogène, argile moyenne | colonnes ballastées, inclusions rigides |
| Faible densité, liquéfaction | sable propre | vibrocompactage, compactage dynamique, colonnes ballastées drainantes |
| Liquéfaction, sable silteux | sable silteux | colonnes ballastées (densification limitée), cellules de jet grouting, drains + densification |
| Cavités, karst | calcaire, gypse | injection solide (compaction grouting), injection de comblement |
| Étanchéité, soutènement provisoire | sable, grave | injection d'imprégnation, jet grouting |
| Traficabilité, terrassements | sol fin humide | traitement à la chaux / au ciment |

Vérifier : profondeur à traiter, eau, avoisinants (vibrations), délai disponible, coût, et ce qui peut être contrôlé sur site.

## 2. Colonnes ballastées (CFMS 2011)

- Taux d'incorporation as = Ac / A (typiquement 10 à 30 %) ; rayon de la cellule unitaire Re = 0,564 s (maille carrée), 0,525 s (maille triangulaire).
- Facteur d'amélioration du tassement (Priebe 1995) n0 = 1 + as · [ (5 − as) / (4 · Kac · (1 − as)) − 1 ], Kac = tan²(45° − φc/2), φc ≈ 38 à 40° ; puis corrections pour la compressibilité de la colonne et le poids des terres.
- Contrainte dans la colonne limitée par le confinement latéral : qr = Kpc · (σ'h0 + étreinte latérale tirée de pl* ou de cu) ; contrainte de calcul usuelle dans la colonne 0,4 à 0,8 MPa ; pas dans les sols très mous (cu < 15 à 20 kPa) sans justification.
- Portance des semelles sur colonnes : sol homogénéisé, règles CFMS ; tassement par le facteur d'amélioration ou un module homogénéisé.
- Contrôles : essais de chargement sur colonne et sur semelle, CPT/PMT entre colonnes (sols densifiables), enregistrements d'exécution (profondeur, énergie, volume de ballast).

## 3. Inclusions rigides (ASIRI)

- Colonnes en béton ou mortier non armé avec une plateforme de transfert de charge (granulaire, 0,4 à 1,0 m) ; les inclusions reprennent 60 à 80 % de la charge, le sol le reste.
- Dimensionnement par la cellule unitaire : frottement négatif au-dessus du plan neutre, positif en dessous ; effet de voûte dans la plateforme (Hewlett et Randolph ou méthode ASIRI). Tassement typiquement 0,2 à 0,4 du tassement sans traitement.
- Vérifications : contrainte en tête d'inclusion, contrainte dans le béton (non armé, γc élevé), poinçonnement de la plateforme, efforts horizontaux (les inclusions ne sont pas des pieux : pas de capacité en flexion sauf si armées).
- Contrôles : essais de chargement statique sur inclusion, contrôles d'intégrité, compactage de la plateforme.

## 4. Drains verticaux et préchargement

- Consolidation radiale (Barron / Hansbo) : Uh = 1 − exp(−8 Th / F(n)), Th = ch t / De², F(n) ≈ ln(De/dw) − 0,75 (+ termes de remaniement et de résistance du drain) ; De = 1,13 s (maille carrée), 1,05 s (triangulaire) ; diamètre équivalent d'un drain plat dw = (a + b)/2.
- ch ≈ 1 à 5 × cv (le mesurer si possible : dissipation CPTu, cellule Rowe).
- Surcharge pour atteindre le tassement visé avant la charge de service ; vérifier la stabilité du remblai par étapes (cu augmente avec la consolidation : Δcu ≈ 0,2 à 0,3 Δσ'v), voir `turba-slope-stability`.
- Suivre tassomètres, piézomètres et inclinomètres ; méthode d'Asaoka pour prévoir le tassement final.

## 5. Densification

- **Vibrocompactage** : sables propres avec fines < 10 à 15 % ; qc ou N60 cible entre les points ; maille de 2,5 à 4 m.
- **Compactage dynamique** : profondeur d'influence D ≈ n · √(W·H) (W en t, H en m, n ≈ 0,3 à 0,6) ; vibrations sur les avoisinants ; contrôle par PMT / CPT après traitement.

## 6. Injections et jet grouting

- L'injection d'imprégnation au ciment demande k > 10⁻⁵ m/s ; les sols plus fins demandent des ciments ultrafins ou des coulis chimiques ; critère d'injectabilité (D15 sol / D85 coulis) > 25.
- Jet grouting : diamètre de colonne tiré de colonnes d'essai (simple, double, triple fluide) ; résistance sur carottes ; maîtrise du soulèvement et des rejets.

## 7. Traitement contre la liquéfaction

- Augmenter la densité (vibrocompactage, compactage dynamique), drainer (colonnes ballastées, drains graveleux), confiner (cellules de jet grouting ou de soil mixing), ou fonder sur pieux en tenant compte du frottement négatif et des déplacements latéraux.
- Contrôler après traitement avec la même méthode que l'analyse de déclenchement (`turba-seismic-liquefaction`) : CPT/SPT entre colonnes ; ne pas compter la réduction de contrainte due à la rigidité des colonnes dans les sables silteux sans justification.

## 8. Prescription et contrôle

- La prescription donne la performance (tassement, portance, FS vis-à-vis de la liquéfaction), les essais qui la démontrent et les critères d'acceptation, plutôt qu'un simple mode opératoire.
- Planche d'essai avant production, enregistrements d'exécution pour chaque élément, essais de réception par lot.

## 9. Pièges fréquents

- Colonnes ballastées dans une argile très molle ou un sol organique sans vérification du confinement.
- Inclusions rigides traitées comme des pieux (ou l'inverse).
- Drains sans tapis drainant assez perméable.
- Densification annoncée dans un sable silteux riche en fines.
- Pas de planche d'essai.
