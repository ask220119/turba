---
name: turba-core
description: Règles communes à toute tâche géotechnique confiée à un agent IA (fondations, soutènements, pentes, séisme, reconnaissances, amélioration des sols) - modèle géotechnique, unités, formats de sécurité Eurocode 7 et normes NF P94, contrôles avant émission, et aiguillage vers le bon skill TURBA. À charger en premier pour tout calcul ou rapport géotechnique.
license: CC-BY-4.0
metadata:
  collection: TURBA
  version: "0.1.0"
  domain: general
  standards: "EN 1997-1 (Eurocode 7), NF P94-500, NF P94-261, NF P94-262, NF P94-270, NF P94-282, RPS 2000 (2011)"
  language: fr
---

# TURBA socle : faire de la géotechnique en tant qu'agent

TURBA est une collection ouverte de skills d'ingénierie géotechnique (version anglaise : `SKILL.md` ; répondre dans la langue de l'utilisateur). Ce skill socle regroupe les règles que tous les autres skills TURBA supposent acquises. Il ne remplace pas un ingénieur géotechnicien qualifié : tout résultat produit est un projet qu'un ingénieur vérifie et signe.

## 1. Règles impératives

1. **Ne jamais inventer de paramètres de sol.** Si une valeur (c', φ', cu, EM, pl*, qc, N60, γ, k, Vs) n'est pas fournie, le dire, proposer une fourchette avec sa source (corrélation, tableau usuel, littérature) et la signaler comme hypothèse à confirmer. Marquer chaque valeur supposée dans le livrable.
2. **Citer la norme et sa version.** EN 1997-1:2004 et son annexe nationale, l'EN 1997 de deuxième génération (2024/2025), NF P94-261/262/270/282, RPS 2000 révisé 2011 (Maroc) ou autre. Ne pas mélanger des jeux de coefficients partiels de documents différents.
3. **Unités SI explicites** : kPa ou MPa pour les contraintes et modules, kN et kN/m pour les efforts, m pour les longueurs, kN/m³ pour les poids volumiques, degrés pour les angles. L'unité à côté de chaque nombre.
4. **L'eau d'abord.** Identifier les niveaux de nappe (bas, haut, de calcul) et les conditions de drainage (drainé ou non drainé, court ou long terme) avant de choisir les paramètres.
5. **Contrôler les ordres de grandeur** avec les fourchettes données dans chaque skill. Un résultat hors fourchette est soit une erreur, soit un constat qui doit être expliqué.
6. **Montrer la chaîne** : données, méthode, formule, valeurs intermédiaires, résultat, taux de travail. Un nombre seul n'est pas un livrable.
7. **Rétro-analyse avant dimensionnement** dès que quelque chose existe déjà (talus stable, mur existant, tassement mesuré). Caler dessus.

## 2. Le modèle géotechnique

Le construire avant tout calcul, sous forme de tableau :

| Couche | Toit / base (m) | Description | γ / γ' (kN/m³) | Résistance (c', φ' ou cu) | Déformabilité (EM, α ou E', ou qc) | Perméabilité | Source |
|---|---|---|---|---|---|---|---|

- Valeurs caractéristiques (EN 1997-1 §2.4.5.2) : estimation prudente de la valeur qui gouverne l'état limite, pas la moyenne des essais. Pour un grand volume de sol, proche de la moyenne ; pour un mécanisme local, proche d'un fractile bas. Dire laquelle et pourquoi.
- Subdiviser une couche épaisse quand les essais montrent une tendance nette avec la profondeur.
- Garder une colonne pour la source de chaque valeur (numéro d'essai, corrélation, hypothèse).

## 3. Formats de sécurité (résumé)

- **Eurocode 7, approche 2 (France, Maroc par usage)** : coefficients sur les actions et sur les résistances (A1 + M1 + R2). Portance γR;v = 1,4, glissement γR;h = 1,1 (NF P94-261), plus les facteurs de modèle des normes d'application françaises.
- **Approche 3** : coefficients sur les paramètres de résistance, utilisée pour la stabilité générale (γφ' = γc' = 1,25, γcu = 1,4).
- **Coefficient de sécurité global traditionnel** (encore demandé par certains maîtres d'ouvrage) : F ≥ 1,5 définitif, F ≥ 1,3 provisoire pour les pentes.
- Combinaisons : ELU fondamental (1,35 G + 1,5 Q), ELU accidentel et sismique (1,0 G + ψ2 Q + AE), ELS caractéristique et quasi permanent.

Toujours écrire la vérification comme un rapport Ed / Rd ≤ 1 (ou F ≥ Fmin) pour que le lecteur voie la marge.

## 4. Avant toute émission

- [ ] Tableau du modèle géotechnique présent, chaque valeur supposée signalée.
- [ ] Norme, version et format de sécurité nommés.
- [ ] Toutes les situations de projet couvertes (phases de travaux, long terme, nappe haute, séisme si exigé).
- [ ] Unités et ordres de grandeur vérifiés.
- [ ] Limites de la méthode indiquées (ce qui n'est pas couvert).
- [ ] Liste des points que l'ingénieur doit confirmer.

## 5. Aiguillage

| Tâche | Skill |
|---|---|
| Programmer ou interpréter une reconnaissance, valeurs caractéristiques, rapports G1/G2 | `turba-site-investigation` |
| Semelles, radiers, pieux, tassements, raideurs | `turba-foundations` |
| Écrans, fouilles profondes, tirants, butons | `turba-retaining-walls` |
| Pentes, remblais, clouage, pieux stabilisateurs | `turba-slope-stability` |
| Action sismique, classe de sol, liquéfaction, poussées dynamiques | `turba-seismic-liquefaction` |
| Colonnes ballastées, inclusions rigides, préchargement, injections | `turba-ground-improvement` |

## 6. Missions (NF P94-500)

G1 (étude de site, principes généraux), G2 AVP / PRO / DCE-ACT (conception), G3 (étude d'exécution de l'entreprise), G4 (supervision de la G3), G5 (diagnostic). Indiquer à quelle mission appartient le livrable : le niveau de détail et les données exigées diffèrent.
