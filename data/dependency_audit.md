# Rapport d'audit — Dépendances manquantes par pays

Généré le 2026-04-04. Flux f131–f147 déjà appliqués (Japon, Corée du Sud, Turquie, Pakistan, Égypte).

---

## RÉSUMÉ SYNTHÉTIQUE

| Pays | GAP Énergie | GAP Céréales | GAP Armes | GAP Dette | Priorité |
|---|---|---|---|---|---|
| Inde | FAIBLE (5.6 bcm gaz) | NON | NON | NON | FAIBLE |
| Chine | HAUTE (1.7 Mb/j pétrole + 10 bcm gaz) | NON | NON | NON | HAUTE |
| Allemagne | HAUTE (1.55 Mb/j pétrole + 20 bcm gaz) | NON | NON | NON | HAUTE |
| France | CRITIQUE (1.5 Mb/j pétrole = 0 flux pétrole) | NON | NON | NON | HAUTE |
| Royaume-Uni | MOYENNE (0.4 Mb/j pétrole) | NON | NON | NON | MOYENNE |
| Espagne | HAUTE (0.95 Mb/j pétrole non couvert) | NON | NON | NON | HAUTE |
| Italie | HAUTE (0.7 Mb/j pétrole non couvert) | NON | NON | NON | HAUTE |
| Pologne | CRITIQUE (15 bcm gaz + 0.18 Mb/j pétrole) | NON | NON | NON | CRITIQUE |
| Arabie Saoudite | NON (exportateur) | HAUTE (blé ~4 Mt/an) | NON | NON | HAUTE (céréales) |
| Indonésie | CRITIQUE (0.9 Mb/j pétrole = 0 flux) | NON | NON | NON | HAUTE |
| Bangladesh | CRITIQUE (5 bcm GNL + 0.135 Mb/j pétrole) | HAUTE | NON | NON | HAUTE |
| Nigeria | STRUCTUREL (paradoxe raffiné) | FAIBLE | NON | NON | HAUTE |
| Algérie | NON (exportateur) | CRITIQUE (blé ~9 Mt/an) | NON | NON | HAUTE (céréales) |
| Maroc | CRITIQUE (100% énergie absent) | HAUTE | NON | NON | HAUTE |
| Éthiopie | CRITIQUE (pays absent ENERGY_DATA) | CRITIQUE | NON | NON | FAIBLE (volumes) |
| Argentine | FAIBLE (3 bcm gaz bolivien) | NON | NON | NON | FAIBLE |
| Brésil | FAIBLE | NON | NON | NON | FAIBLE |
| Vietnam | HAUTE (0.25 Mb/j pétrole = 0 flux) | HAUTE | NON | NON | HAUTE |
| Philippines | CRITIQUE (0.48 Mb/j pétrole = 0 flux) | HAUTE | NON | NON | HAUTE |
| Afrique du Sud | CRITIQUE (0.6 Mb/j pétrole = 0 flux) | NON | NON | NON | HAUTE |

---

## DÉTAIL PAR PAYS

### Inde (IND)
- Prod : 0.8 Mb/j, conso : 5.2 Mb/j — coverage pétrole correct (flux f015/f018/f031/f077/f098/f101/f107/f111/f113/f128)
- Gap gaz ~5.6 bcm (conso 64 bcm, prod 35, entrants LNG = 23.4 bcm)
- Doublon probable : f037 et f087 (Australie→Inde LNG 8.3 bcm, deux entrées identiques)
- **Flux à ajouter :** f148 Nigeria→Inde LNG 2.8 bcm ; f149 Malaisie→Inde LNG 3.5 bcm

### Chine (CHN)
- Prod : 4.0 Mb/j, conso : 14.5 Mb/j — gap ~1.7 Mb/j pétrole malgré 19 flux existants
- Gaz : prod 220 + entrants 144.6 = 364.6 vs conso 375 → gap 10.4 bcm
- CAGP (Asie centrale→Chine) : Ouzbékistan et Kazakhstan non individualisés
- **Flux à ajouter :** f150 Ouzbékistan→Chine gaz 6 bcm ; f151 Kazakhstan→Chine gaz 5 bcm ; f152 Russie→Chine gaz 7 bcm (Power of Siberia montée 2023) ; f153 Angola→Chine pétrole 0.3 Mb/j

### Allemagne (DEU)
- Druzhba (f074, 0.5 Mb/j) arrêté fin 2022, aucun remplaçant dans FLOWS_DATA
- Gaz : 30+20+9.7=59.7 bcm vs conso 85 → gap 20 bcm
- **Flux à ajouter :** f154 Norvège→Allemagne pétrole 0.25 Mb/j ; f155 Kazakhstan→Allemagne pétrole 0.15 Mb/j ; f156 USA→Allemagne pétrole 0.20 Mb/j ; f157 Qatar→Allemagne LNG 5.0 bcm

### France (FRA)
- **AUCUN flux pétrole entrant** alors que conso = 1.6 Mb/j, prod = 0.1 Mb/j → score énergie complètement faux
- Gaz OK (48.5 bcm entrants vs conso 38 bcm)
- **Flux à ajouter :** f158 SAU→France 0.25 Mb/j ; f159 Irak→France 0.20 Mb/j ; f160 Norvège→France 0.20 Mb/j ; f161 Angola→France 0.10 Mb/j ; f162 Russie→France 0.15 Mb/j (pré-embargo)

### Espagne (ESP)
- Pétrole conso ~1.1 Mb/j, prod ~0.05 → gap ~1.05 Mb/j, peu de flux pétrole existants
- **Flux à ajouter :** f163 SAU→Espagne 0.25 Mb/j ; f164 Irak→Espagne 0.15 Mb/j ; f165 Nigeria→Espagne 0.15 Mb/j ; f166 Angola→Espagne 0.10 Mb/j ; f167 Mexique→Espagne 0.08 Mb/j

### Italie (ITA)
- Pétrole conso ~1.1 Mb/j, prod ~0.05 → gap ~0.7 Mb/j après quelques flux existants
- **Flux à ajouter :** f168 SAU→Italie 0.20 Mb/j ; f169 Irak→Italie 0.15 Mb/j ; f170 Kazakhstan→Italie 0.10 Mb/j ; f171 Azerbaïdjan→Italie pétrole 0.10 Mb/j (Ceyhan-Trieste)

### Royaume-Uni (GBR)
- Prod 1.1 Mb/j (mer du Nord déclin), conso 1.5 → gap ~0.4 Mb/j
- **Flux à ajouter :** f172 Norvège→Royaume-Uni pétrole 0.25 Mb/j ; f173 USA→Royaume-Uni pétrole 0.15 Mb/j

### Pologne (POL)
- **Seul flux existant : f075 Russie→Pologne pétrole 0.4 Mb/j (Druzhba arrêté 2022)**
- Zéro flux gaz alors que conso = 21 bcm, prod = 6 bcm → gap de 15 bcm invisible
- Baltic Pipe (Norvège, opérationnel oct. 2022, 7.5 bcm) absent
- **Flux à ajouter :** f174 Norvège→Pologne gaz 7.5 bcm ; f175 USA→Pologne LNG 4.0 bcm ; f176 Qatar→Pologne LNG 2.0 bcm ; f177 SAU→Pologne pétrole 0.15 Mb/j ; f178 Norvège→Pologne pétrole 0.10 Mb/j

### Arabie Saoudite (SAU)
- Énergie : exportateur, correct
- Céréales : importe ~4 Mt blé/an (UE, USA, Ukraine/Australie) → absent
- **Flux céréales à ajouter dans cereals.json**

### Indonésie (IDN)
- Prod 0.7 Mb/j, conso 1.6 Mb/j → **importateur net depuis 2014**, zéro flux entrant
- **Flux à ajouter :** f179 SAU→Indonésie 0.20 Mb/j ; f180 ARE→Indonésie 0.15 Mb/j ; f181 Malaisie→Indonésie 0.15 Mb/j ; f182 Nigeria→Indonésie 0.10 Mb/j

### Bangladesh (BGD)
- Gaz prod 25 vs conso 30 bcm → 5 bcm GNL importé, zéro capturé
- Pétrole prod 0.005 vs conso 0.14 Mb/j → 0.135 Mb/j absent
- **Flux à ajouter :** f183 Qatar→Bangladesh LNG 2.5 bcm ; f184 Oman→Bangladesh LNG 1.5 bcm ; f185 SAU→Bangladesh pétrole 0.07 Mb/j ; f186 ARE→Bangladesh pétrole 0.04 Mb/j

### Nigeria (NGA)
- Paradoxe : exportateur pétrole brut mais importe ~0.15 Mb/j produits raffinés (raffineries en panne)
- Note structurelle : modèle actuel ne distingue pas brut/raffiné — pas de flux à ajouter sans refonte

### Algérie (DZA)
- Énergie : exportateur, correct
- Céréales : importe ~9 Mt blé/an (France, Ukraine, Argentine) → absent
- **Flux céréales à ajouter dans cereals.json**

### Maroc (MAR)
- Si présent dans ENERGY_DATA : prod ≈ 0, conso ~0.15 Mb/j pétrole + ~1 bcm gaz → 100% import
- **Flux à ajouter si pays présent :** SAU→Maroc 0.05 Mb/j ; Russie→Maroc 0.04 Mb/j

### Vietnam (VNM)
- Prod 0.22 Mb/j, conso 0.47 → gap 0.25 Mb/j pétrole, zéro flux
- **Flux à ajouter :** f191 Malaisie→Vietnam 0.08 Mb/j ; f192 Koweït→Vietnam 0.06 Mb/j ; f193 SAU→Vietnam 0.05 Mb/j

### Philippines (PHL)
- Prod 0.01 Mb/j, conso 0.49 → **dépendance 98% pétrole**, zéro flux entrant
- **Flux à ajouter :** f194 SAU→Philippines 0.10 Mb/j ; f195 ARE→Philippines 0.08 Mb/j ; f196 Koweït→Philippines 0.07 Mb/j ; f197 Australie→Philippines 0.06 Mb/j

### Afrique du Sud (ZAF)
- Prod 0 Mb/j, conso 0.6 Mb/j + 3.9 bcm gaz (ROMPCO depuis Mozambique absent)
- **Flux à ajouter :** f198 SAU→Afrique du Sud 0.15 Mb/j ; f199 Nigeria→Afrique du Sud 0.12 Mb/j ; f200 Angola→Afrique du Sud 0.10 Mb/j ; f201 Mozambique→Afrique du Sud gas_pipeline 3.8 bcm

---

## OBSERVATIONS TRANSVERSALES

- **Doublons :** f037 = f087 (Australie→Inde LNG 8.3 bcm) — à vérifier
- **Flux "Europe" génériques :** f008, f011, f027, f038 vers "Europe" n'alimentent aucun score individuel
- **Éthiopie :** absente de ENERGY_DATA, présente uniquement en SOVEREIGN_DEBT
- **Paradoxe Nigeria :** nécessiterait un type "refined_products" distinct
- **IDs utilisés :** f131–f147 (existants) + f148–f201 (ce rapport). Prochain ID : **f202**

---

# Round 3 — 20 pays supplémentaires (Pays-Bas, Belgique, Grèce, Roumanie, Hongrie, Autriche, Taïwan, Thaïlande, Singapour, Israël, Jordanie, Venezuela, Colombie, Mexique, Rép. tchèque, Finlande, Slovaquie, RDC, Kenya, Tanzanie)

IDs flux : f201–f266. Prochain ID libre : **f267**.

## TABLEAU RÉSUMÉ

| Pays | ISO3 | GAP Pétrole | GAP Gaz | Priorité |
|---|---|---|---|---|
| Pays-Bas | NLD | 0.85 Mb/j | 5.7 bcm | HAUTE |
| Belgique | BEL | 0.60 Mb/j | 0 (transit) | HAUTE |
| Grèce | GRC | 0.27 Mb/j | 3.9 bcm | HAUTE |
| Roumanie | ROU | 0.12 Mb/j | 2.0 bcm | MOYENNE |
| Hongrie | HUN | ~0 (couvert) | 0.5 bcm | MOYENNE |
| Autriche | AUT | 0.28 Mb/j | 2.5 bcm | MOYENNE |
| Taïwan | TWN | 1.10 Mb/j | 7.9 bcm | CRITIQUE |
| Thaïlande | THA | 1.20 Mb/j | pipeline absent | HAUTE |
| Singapour | SGP | 0.78 Mb/j | 9.5 bcm | CRITIQUE |
| Israël | ISR | 0.25 Mb/j | n/a | HAUTE |
| Jordanie | JOR | 0.10 Mb/j | 6.2 bcm | HAUTE |
| Venezuela | VEN | n/a (export) | 0.5 bcm | FAIBLE |
| Colombie | COL | n/a (export) | doublon f094 supprimé | FAIBLE |
| Mexique | MEX | 0.10 Mb/j | f025 corrigé 65→72 bcm | HAUTE |
| Rép. tchèque | CZE | 0.15 Mb/j | 7.0 bcm | HAUTE |
| Finlande | FIN | 0.20 Mb/j | 1.0 bcm | HAUTE |
| Slovaquie | SVK | 0.08 Mb/j | 0 | FAIBLE |
| RDC | COD | ~0 | 0 | FAIBLE |
| Kenya | KEN | 0.06 Mb/j | 0 | MOYENNE |
| Tanzanie | TZA | 0.05 Mb/j | 0 (export gaz) | MOYENNE |

## ACTIONS CORRECTIVES APPLIQUÉES

- **f094 supprimé** — doublon de f126 (Colombia anglais = Colombie français, même flux USA)
- **f025 corrigé** — USA→Mexique gaz 65 → 72 bcm/an (EIA/SENER 2022)

## CAS CRITIQUES

**Taïwan (TWN)** : 98% énergie importée, aucun flux pétrole ni gaz existant avant ce round. 6 flux ajoutés (f225–f230). Vulnérabilité géopolitique extrême (Détroit de Taïwan).

**Singapour (SGP)** : 100% énergie importée, seul f085 (LNG partiel) existait. 5 flux ajoutés (f236–f240) dont pipelines Malaisie et Indonésie critiques.

**Thaïlande (THA)** : Pipeline Yadana (Myanmar→Thaïlande) existait en tant que pipeline (p28) mais absent de FLOWS_DATA. Ajouté comme f231.
