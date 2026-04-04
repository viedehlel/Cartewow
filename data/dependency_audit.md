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

---

# Round 4 — Pays restants (~49 pays)

Généré le 2026-04-04. IDs flux : f267–f340+. Couvre tous les pays d'ENERGY_DATA non audités dans les rounds 1-3.

## TABLEAU RÉSUMÉ

| Pays | ISO3 | GAP Pétrole | GAP Gaz | Priorité |
|---|---|---|---|---|
| États-Unis | USA | ~0 (producteur) | ~0 (producteur) | FAIBLE |
| Russie | RUS | ~0 (exportateur) | ~0 (exportateur) | FAIBLE |
| Canada | CAN | ~0 (exportateur) | ~0 (exportateur) | FAIBLE |
| Norvège | NOR | ~0 (exportateur) | ~0 (exportateur) | FAIBLE |
| Qatar | QAT | ~0 (exportateur) | ~0 (exportateur) | FAIBLE |
| Australie | AUS | 0.6 Mb/j | ~0 (exportateur) | MOYENNE |
| Émirats Arabes Unis | ARE | ~0 (exportateur) | 15 bcm | HAUTE |
| Irak | IRQ | ~0 (exportateur) | 2 bcm gaz torché | FAIBLE |
| Iran | IRN | ~0 (exportateur) | ~0 | FAIBLE |
| Koweït | KWT | ~0 (exportateur) | 3 bcm | MOYENNE |
| Kazakhstan | KAZ | ~0 (exportateur) | ~0 | FAIBLE |
| Azerbaïdjan | AZE | ~0 (exportateur) | ~0 | FAIBLE |
| Turkménistan | TKM | ~0 (exportateur) | ~0 | FAIBLE |
| Angola | AGO | ~0 (exportateur) | ~0 | FAIBLE |
| Libye | LBY | ~0 (exportateur) | ~0 | FAIBLE |
| Oman | OMN | ~0 (exportateur) | ~0 | FAIBLE |
| Malaisie | MYS | 0.1 Mb/j | ~0 (exportateur) | MOYENNE |
| Myanmar | MMR | 0.02 Mb/j | ~0 | FAIBLE |
| Biélorussie | BLR | 0.12 Mb/j | 18 bcm | HAUTE |
| Ouzbékistan | UZB | 0.05 Mb/j | ~0 | FAIBLE |
| Danemark | DNK | 0.05 Mb/j | 1 bcm | FAIBLE |
| Suède | SWE | 0.30 Mb/j | 1 bcm | HAUTE |
| Portugal | PRT | 0.24 Mb/j | 5.4 bcm | HAUTE |
| Irlande | IRL | 0.15 Mb/j | 2.5 bcm | HAUTE |
| Bulgarie | BGR | 0.08 Mb/j | 2.7 bcm | HAUTE |
| Croatie | HRV | 0.04 Mb/j | 1.9 bcm | MOYENNE |
| Slovénie | SVN | 0.05 Mb/j | 0.9 bcm | MOYENNE |
| Lituanie | LTU | 0.05 Mb/j | 2.5 bcm | HAUTE |
| Lettonie | LVA | 0.04 Mb/j | 1.5 bcm | HAUTE |
| Estonie | EST | 0.03 Mb/j | 0.6 bcm | MOYENNE |
| Luxembourg | LUX | 0.05 Mb/j | 0.8 bcm | HAUTE |
| Suisse | CHE | 0.25 Mb/j | 3.5 bcm | HAUTE |
| Serbie | SRB | 0.06 Mb/j | 2.5 bcm | HAUTE |
| Macédoine du Nord | MKD | 0.02 Mb/j | 0.1 bcm | FAIBLE |
| Albanie | ALB | 0.01 Mb/j | 0.2 bcm | FAIBLE |
| Bosnie-Herzégovine | BIH | 0.03 Mb/j | 0.5 bcm | FAIBLE |
| Cambodge | KHM | 0.04 Mb/j | 0 | FAIBLE |
| Mongolie | MNG | ~0 | 0 | FAIBLE |
| Pérou | PER | 0.08 Mb/j | ~0 (exportateur) | FAIBLE |
| Équateur | ECU | ~0 (exportateur) | ~0 | FAIBLE |
| Ghana | GHA | ~0 (exportateur) | 1 bcm | FAIBLE |
| Mozambique | MOZ | 0.03 Mb/j | ~0 (exportateur) | FAIBLE |
| Ouganda | UGA | 0.04 Mb/j | 0 | FAIBLE |
| Zimbabwe | ZWE | 0.02 Mb/j | 0 | FAIBLE |
| Zambie | ZMB | 0.02 Mb/j | 0 | FAIBLE |
| Sénégal | SEN | ~0 (nouveau prod.) | ~0 | FAIBLE |
| Cameroun | CMR | ~0 (exportateur) | ~0 | FAIBLE |
| Trinité-et-Tobago | TTO | ~0 (exportateur) | ~0 | FAIBLE |
| Nouvelle-Zélande | NZL | 0.11 Mb/j | 1.0 bcm | MOYENNE |

---

## DÉTAIL PAR PAYS

---

## États-Unis (USA)
**Base :** pétrole prod=17.8 / conso=20.3 Mb/j | gaz prod=934 / conso=840 bcm
**Flux existants :** exportateurs massifs — f011 (LNG→Europe 75.9 bcm), f021 (Canada→USA pétrole), f023/f024 (LNG→Japon/KOR), f025 (gaz→Mexique), f040 (SAU→USA pétrole 0.5), f055-f061 (LNG Europe), f104/f105 (LNG Inde/Chine), nombreux autres
**GAP :** pétrole importé ~2.5 Mb/j (Canada 3.5 + SAU 0.5 + Mexique 0.4 + Venezuela 0.1 — prod 17.8 = excédent). Pays EXPORTATEUR NET.
**Flux à ajouter :** Aucun flux import manquant significatif. USA produit + importe Canada (f021), SAU (f040), MEX (f125), VEN (f121), ECU (f095/f127).
**Observations :** Le gap production/conso (~2.5 Mb/j) est couvert par f021 (Canada 3.5 Mb/j). Export LNG massif bien documenté.
**Priorité :** FAIBLE

---

## Russie (RUS)
**Base :** pétrole prod=11.2 / conso=3.7 Mb/j | gaz prod=618 / conso=420 bcm
**Flux existants :** exportateur — f012 (→Chine gaz 15 bcm), f013 (→Turquie gaz 20 bcm), f017/f018 (pétrole Chine/Inde), f031 (Inde pétrole 1.8 Mb/j), f046 (→Allemagne gaz), f047-f050 (Europe gaz), f074-f076 (Europe pétrole), nombreux autres
**GAP :** Exportateur massif. Consommation intérieure bien couverte par la production domestique.
**Flux à ajouter :** Aucun — pays autosuffisant avec excédents massifs. Import résiduel de biens de consommation non-énergétiques hors périmètre.
**Priorité :** FAIBLE

---

## Canada (CAN)
**Base :** pétrole prod=5.6 / conso=2.4 Mb/j | gaz prod=175 / conso=115 bcm
**Flux existants :** f021 Canada→USA pétrole 3.5 Mb/j, f122 Canada→Chine pétrole 0.1 Mb/j
**GAP :** EXPORTATEUR NET — excédent pétrole ~3.2 Mb/j, excédent gaz ~60 bcm. Pas d'import énergétique structurel.
**Flux à ajouter :** Aucun — quelques imports pétrole léger (~0.3 Mb/j côte Est) trop mineurs pour scoring.
**Observations :** Trans Mountain Pipeline (expansion 2024, +590 kb/j vers côte Pacifique) pourrait justifier un flux Canada→Chine supplémentaire à terme.
**Priorité :** FAIBLE

---

## Norvège (NOR)
**Base :** pétrole prod=2.0 / conso=0.2 Mb/j | gaz prod=122 / conso=6 bcm
**Flux existants :** f001 (→Allemagne gaz 30 bcm), f002 (→RU gaz 17 bcm), f033 (→France gaz 17 bcm), f034 (→Belgique gaz 12 bcm), f052 (→Pays-Bas gaz 15 bcm), f053 (→Italie gaz 5 bcm), f072 (LNG 2.8 bcm), f154/f172/f178/f256 (pétrole)
**GAP :** EXPORTATEUR NET. Export gaz ~100 bcm/an. Export pétrole ~1.8 Mb/j.
**Flux à ajouter :** Flux vers Espagne absent. Gassco indique ~3 bcm/an vers Espagne via Lacq (France) en 2022.
```json
{ id:"f267", from:"Norvège", to:"Espagne", from_centroid:[10,62], to_centroid:[-4,40], type:"gas_pipeline", volume:3.0, unit:"bcm/an", year:2022, source:"Gassco Annual Report 2022 / Enagas" }
```
**Priorité :** FAIBLE (marginal)

---

## Qatar (QAT)
**Base :** pétrole prod=1.8 / conso=0.2 Mb/j | gaz prod=177 / conso=50 bcm
**Flux existants :** f005 (→Japon LNG 27.6), f006 (→KOR LNG 20.7), f007 (→Inde LNG 11), f008 (→Europe LNG 24.8), f036 (→Pakistan LNG 5.5), f062-f066 (Europe détaillé), f088 (→Chine 16.6), f089 (→Turquie 4.1), f157 (→Allemagne 5), f176 (→Pologne 2), f183 (→Bangladesh 2.5), f205 (→Pays-Bas 5.5), f229 (→Taïwan 4.1), f235 (→Thaïlande 3.5), f246 (→Jordanie 2)
**GAP :** EXPORTATEUR NET ~127 bcm/an LNG. Flux vers Singapour absent (~2.5 bcm/an selon GIIGNL 2023).
```json
{ id:"f268", from:"Qatar", to:"Singapour", from_centroid:[51.5,25.3], to_centroid:[103.8,1.35], type:"lng", volume:2.5, unit:"bcm/an", year:2022, source:"QatarEnergy / EMA Singapore / GIIGNL 2023" }
```
**Priorité :** FAIBLE

---

## Australie (AUS)
**Base :** pétrole prod=0.4 / conso=1.0 Mb/j | gaz prod=153 / conso=40 bcm
**Flux existants :** f009 (→Japon LNG 48.3), f010 (→Chine LNG 41.4), f026 (→KOR LNG 24.8), f037/f087 (→Inde LNG 8.3 — doublon à vérifier), f085 (→Singapour LNG 5.5), f086 (→Taïwan LNG 13.8), f129 (→Japon pétrole 0.1), f196 (→Philippines pétrole 0.06)
**GAP :** Pétrole : prod 0.4 / conso 1.0 → import ~0.6 Mb/j. AUCUN flux pétrole entrant documenté.
**Flux à ajouter :**
```json
{ id:"f269", from:"Arabie Saoudite", to:"Australie", from_centroid:[45,24], to_centroid:[133,-27], type:"oil", volume:0.20, unit:"mb/j", year:2022, source:"Kpler / IEA Oil Market Report 2022 (~20% imports pétroliers)" }
{ id:"f270", from:"États-Unis", to:"Australie", from_centroid:[-95,38], to_centroid:[133,-27], type:"oil", volume:0.15, unit:"mb/j", year:2022, source:"Kpler / EIA / DCCEEW 2022 (condensats WTI Midland)" }
{ id:"f271", from:"Malaisie", to:"Australie", from_centroid:[112,4], to_centroid:[133,-27], type:"oil", volume:0.12, unit:"mb/j", year:2022, source:"Kpler / PETRONAS / DCCEEW 2022" }
{ id:"f272", from:"Qatar", to:"Australie", from_centroid:[51.5,25.3], to_centroid:[133,-27], type:"lng", volume:2.5, unit:"bcm/an", year:2022, source:"QatarEnergy / GIIGNL 2023 (réimports GNL côte Est Australie)" }
```
**Observations :** L'Est australien (Victoria, NSW) manque de gaz domestique et réimporte du LNG via FSRU depuis 2023.
**Priorité :** MOYENNE

---

## Émirats Arabes Unis (ARE)
**Base :** pétrole prod=4.0 / conso=1.0 Mb/j | gaz prod=60 / conso=75 bcm
**Flux existants :** f099 (→Japon pétrole 0.8), f100 (→Chine pétrole 0.5), f111 (→Inde pétrole 0.3), f112 (→KOR pétrole 0.2), f142 (→Pakistan LNG 2), f180 (→Indonésie pétrole 0.15), f186 (→Bangladesh pétrole 0.04), nombreux autres
**GAP :** Gaz : prod 60 / conso 75 → **déficit 15 bcm**. Couvert par Dolphin Pipeline (Qatar→UAE, ~20 bcm/an) — absent de FLOWS_DATA.
**Flux à ajouter :**
```json
{ id:"f273", from:"Qatar", to:"Émirats Arabes Unis", from_centroid:[51.5,25.3], to_centroid:[54,24], type:"gas_pipeline", volume:20.0, unit:"bcm/an", year:2022, source:"QatarEnergy / Dolphin Energy / IEA Gas Market Report 2022 (Dolphin Pipeline, 2 bcfd)" }
```
**Priorité :** HAUTE (flux physique majeur absent)

---

## Irak (IRQ)
**Base :** pétrole prod=4.5 / conso=0.8 Mb/j | gaz prod=9 / conso=11 bcm
**Flux existants :** f030 (→Chine pétrole 1.3), f077 (→Inde pétrole 0.5), f078 (→Europe pétrole 0.5), f103 (→Turquie pétrole 0.35), f109 (→Japon pétrole 0.2), f110 (→KOR pétrole 0.2), f146 (→Égypte pétrole 0.05), f169 (→Italie 0.15), f204 (→Pays-Bas 0.12), et al.
**GAP :** Gaz : prod 9 / conso 11 → import 2 bcm. Couverts informellement par gaz iranien (accord partiel). Pétrole EXPORTATEUR NET.
**Flux à ajouter :**
```json
{ id:"f274", from:"Iran", to:"Irak", from_centroid:[53,32], to_centroid:[44,33], type:"gas_pipeline", volume:2.0, unit:"bcm/an", year:2022, source:"NIGC / Ministry of Electricity Iraq / IEA 2022 (gazoduc Khanaqin-Nahr Omar, irrégulier)" }
```
**Priorité :** FAIBLE

---

## Iran (IRN)
**Base :** pétrole prod=3.8 / conso=2.0 Mb/j | gaz prod=260 / conso=240 bcm
**Flux existants :** f032 (→Chine pétrole 0.9), f113 (→Inde pétrole 0.2 estimé), f139 (→Turquie gaz 8 bcm)
**GAP :** EXPORTATEUR NET marginal (pétrole sous sanctions). Autosuffisant gaz.
**Flux à ajouter :** Aucun flux import structurel. Export gaz vers Turquie documenté (f139). Export pétrole clandestin vers Chine documenté (f032).
**Priorité :** FAIBLE

---

## Koweït (KWT)
**Base :** pétrole prod=2.9 / conso=0.5 Mb/j | gaz prod=19 / conso=22 bcm
**Flux existants :** f106 (→Chine pétrole 0.3), f107 (→Inde pétrole 0.2), f108 (→Japon pétrole 0.2), f135 (→KOR pétrole 0.3), f144 (→Pakistan pétrole 0.10), f191 (→Vietnam pétrole 0.06), f195 (→Philippines pétrole 0.07), f227 (→Taïwan pétrole 0.15)
**GAP :** Gaz : prod 19 / conso 22 → déficit 3 bcm. Couvert par imports GNL spot. EXPORTATEUR PÉTROLE NET.
**Flux à ajouter :**
```json
{ id:"f275", from:"États-Unis", to:"Koweït", from_centroid:[-95,38], to_centroid:[47.5,29.3], type:"lng", volume:1.5, unit:"bcm/an", year:2022, source:"DOE / GIIGNL 2023 / Kuwait Integrated Petroleum Industries Co. (KIPIC terminal Al-Zour LNG)" }
```
**Priorité :** FAIBLE

---

## Kazakhstan (KAZ)
**Base :** pétrole prod=1.9 / conso=0.3 Mb/j | gaz prod=28 / conso=18 bcm
**Flux existants :** f041 (→Chine pétrole 0.3), f093 (→Russie pétrole 0.7 transit CPC), f123 (→Europe pétrole 0.3), f133 (→Japon pétrole 0.08), f151 (→Chine gaz 5 bcm), f155 (→Allemagne pétrole 0.15), f170 (→Italie pétrole 0.10), f218 (→Roumanie pétrole 0.07), f223 (→Autriche pétrole 0.05), f244 (→Israël pétrole 0.05)
**GAP :** EXPORTATEUR NET. Autosuffisant.
**Flux à ajouter :** Aucun import structurel.
**Priorité :** FAIBLE

---

## Azerbaïdjan (AZE)
**Base :** pétrole prod=0.7 / conso=0.1 Mb/j | gaz prod=35 / conso=12 bcm
**Flux existants :** f020 (→Italie gaz 10 bcm via TAP), f054 (→Turquie gaz 10 bcm via TANAP), f124 (→Europe pétrole 0.2 BTC), f171 (→Italie pétrole 0.10), f209 (→Belgique pétrole 0.07), f219 (→Roumanie pétrole 0.05), f220 (→Hongrie gaz 1 bcm), f211 (→Grèce gaz 1.1 bcm), f242 (→Israël pétrole 0.12)
**GAP :** EXPORTATEUR NET (gaz Shah Deniz II, pétrole BTC). Autosuffisant.
**Flux à ajouter :** Aucun import structurel.
**Priorité :** FAIBLE

---

## Turkménistan (TKM)
**Base :** pétrole prod=0.2 / conso=0.15 Mb/j | gaz prod=84 / conso=30 bcm
**Flux existants :** f019 (→Chine gaz 40 bcm CAGP)
**GAP :** EXPORTATEUR GAS MAJEUR. Exportations vers Chine quasi-totales. Autosuffisant pétrole/gaz domestique.
**Flux à ajouter :** Aucun import structurel. Export quasi-exclusif Chine bien documenté (f019 + f150 Ouzbékistan, f151 Kazakhstan).
**Priorité :** FAIBLE

---

## Angola (AGO)
**Base :** pétrole prod=1.2 / conso=0.1 Mb/j | gaz prod=12 / conso=2 bcm
**Flux existants :** f042 (→Chine pétrole 0.7), f101 (→Inde pétrole 0.1), f120 (→Europe pétrole 0.2), f153 (→Chine pétrole 0.3 — possible doublon f042), f161 (→France pétrole 0.1), f166 (→Espagne pétrole 0.1), f199 (→Afrique du Sud pétrole 0.10), f260 (→RDC pétrole 0.01)
**GAP :** EXPORTATEUR NET. Export ~1.1 Mb/j. Import résiduel produits raffinés ~0.05 Mb/j (pays sans raffinerie suffisante).
**Observations :** f042 et f153 semblent être des doublons (Angola→Chine pétrole). f042 = 0.7 Mb/j, f153 = 0.3 Mb/j. Ensemble = 1.0 Mb/j ce qui est plausible (Angola = 2e fournisseur Chine). À vérifier mais probablement intentionnel (deux périodes/volumes différents).
**Flux à ajouter :** Aucun import structurel majeur.
**Priorité :** FAIBLE

---

## Libye (LBY)
**Base :** pétrole prod=1.2 / conso=0.2 Mb/j | gaz prod=12 / conso=7 bcm
**Flux existants :** f035 (→Italie gaz 7 bcm GreenStream), f115 (→Italie pétrole 0.2), f116 (→Espagne pétrole 0.1)
**GAP :** EXPORTATEUR NET. Export pétrole ~1.0 Mb/j mais seulement documenté vers Italie et Espagne. Flux vers Chine/Asie absent.
**Flux à ajouter :**
```json
{ id:"f276", from:"Libye", to:"Chine", from_centroid:[17,27], to_centroid:[104,35], type:"oil", volume:0.15, unit:"mb/j", year:2022, source:"Kpler / NOC Libya / IEA 2022 (Esnaim, Mellitah crude)" }
{ id:"f277", from:"Libye", to:"France", from_centroid:[17,27], to_centroid:[2.3,46], type:"oil", volume:0.08, unit:"mb/j", year:2022, source:"Kpler / NOC Libya / IEA 2022 (Total E&P Libya)" }
```
**Priorité :** FAIBLE

---

## Oman (OMN)
**Base :** pétrole prod=1.0 / conso=0.2 Mb/j | gaz prod=39 / conso=24 bcm
**Flux existants :** f097 (→Chine pétrole 0.4), f098 (→Inde pétrole 0.2), f130 (→Japon pétrole 0.1), f138 (→KOR pétrole 0.10), f184 (→Bangladesh LNG 1.5)
**GAP :** EXPORTATEUR NET. Export LNG ~30 bcm/an non documenté vers Corée/Japon (hors f138/f130).
**Flux à ajouter :**
```json
{ id:"f278", from:"Oman", to:"Japon", from_centroid:[57,22], to_centroid:[138,37], type:"lng", volume:8.3, unit:"bcm/an", year:2022, source:"QatarEnergy/OQ / GIIGNL 2023 (Oman LNG plant, contrats long terme Osaka Gas, Tohoku)" }
{ id:"f279", from:"Oman", to:"Corée du Sud", from_centroid:[57,22], to_centroid:[128,36], type:"lng", volume:4.1, unit:"bcm/an", year:2022, source:"OQ / KOGAS / GIIGNL 2023" }
```
**Priorité :** MOYENNE

---

## Malaisie (MYS)
**Base :** pétrole prod=0.6 / conso=0.7 Mb/j | gaz prod=78 / conso=44 bcm
**Flux existants :** f028 (→Japon LNG 19.3), f029 (→Chine LNG 13.8), f085 (→Singapour LNG 5.5 — via pipeline aussi), f090 (→KOR LNG 8.3), f149 (→Inde LNG 3.5), f181 (→Indonésie pétrole 0.15), f190 (→Vietnam pétrole 0.08), f236 (→Singapour gaz pipeline 6.0)
**GAP :** Pétrole : prod 0.6 / conso 0.7 → import **~0.1 Mb/j** non couvert.
**Flux à ajouter :**
```json
{ id:"f280", from:"Arabie Saoudite", to:"Malaisie", from_centroid:[45,24], to_centroid:[112,4], type:"oil", volume:0.08, unit:"mb/j", year:2022, source:"Kpler / Aramco / PETRONAS 2022 (Arab Light→Port Dickson)" }
{ id:"f281", from:"Émirats Arabes Unis", to:"Malaisie", from_centroid:[54,24], to_centroid:[112,4], type:"oil", volume:0.05, unit:"mb/j", year:2022, source:"Kpler / ADNOC / PETRONAS 2022" }
```
**Priorité :** FAIBLE

---

## Myanmar (MMR)
**Base :** pétrole prod=0.03 / conso=0.05 Mb/j | gaz prod=18 / conso=5 bcm
**Flux existants :** f045 (→Chine gaz 4 bcm pipeline), f231 est Myanmar→Thaïlande gaz 6.5 bcm (documenté Round 3)
**GAP :** Pétrole : prod 0.03 / conso 0.05 → import ~0.02 Mb/j. Import pétrole non documenté.
**Flux à ajouter :**
```json
{ id:"f282", from:"Chine", to:"Myanmar", from_centroid:[104,35], to_centroid:[96,20], type:"oil", volume:0.02, unit:"mb/j", year:2022, source:"Kpler / CNPC / IEA 2022 (pipeline Kunming-Kyaukphyu, produits raffinés)" }
```
**Priorité :** FAIBLE

---

## Biélorussie (BLR)
**Base :** pétrole prod=0.03 / conso=0.15 Mb/j | gaz prod=0.2 / conso=18 bcm
**Flux existants :** AUCUN flux entrant documenté dans FLOWS_DATA.
**GAP :** Pétrole : prod 0.03 / conso 0.15 → **import 0.12 Mb/j** (100% Russie). Gaz : prod 0.2 / conso 18 → **import 17.8 bcm** (100% Russie via Gazprom).
**Flux à ajouter :**
```json
{ id:"f283", from:"Russie", to:"Biélorussie", from_centroid:[60,58], to_centroid:[28,53.5], type:"gas_pipeline", volume:17.5, unit:"bcm/an", year:2022, source:"Gazprom / Beltransgaz / IEA 2022 (prix préférentiels accordés; pipeline Yamal-Europe transite aussi)" }
{ id:"f284", from:"Russie", to:"Biélorussie", from_centroid:[60,58], to_centroid:[28,53.5], type:"oil", volume:0.12, unit:"mb/j", year:2022, source:"Transneft / Belneftekhim / IEA 2022 (Druzhba nord, raffineries Mozyr et Novopolotsk)" }
```
**Observations :** Biélorussie = dépendance énergétique TOTALE à la Russie. Score de vulnérabilité devrait être maximal.
**Priorité :** HAUTE

---

## Ouzbékistan (UZB)
**Base :** pétrole prod=0.05 / conso=0.1 Mb/j | gaz prod=50 / conso=44 bcm
**Flux existants :** f150 (→Chine gaz 6 bcm CAGP)
**GAP :** Pétrole : prod 0.05 / conso 0.1 → import ~0.05 Mb/j (produits raffinés de Russie/Kazakhstan).
**Flux à ajouter :**
```json
{ id:"f285", from:"Russie", to:"Ouzbékistan", from_centroid:[60,58], to_centroid:[63,41], type:"oil", volume:0.04, unit:"mb/j", year:2022, source:"Kpler / IEA Central Asia 2022 (produits pétroliers via pipeline Omsk-Pavlodar)" }
```
**Priorité :** FAIBLE

---

## Danemark (DNK)
**Base :** pétrole prod=0.1 / conso=0.15 Mb/j | gaz prod=2 / conso=3 bcm
**Flux existants :** AUCUN flux entrant spécifique (certains flux génériques via "Norvège→Pays-Bas" etc. transitent).
**GAP :** Pétrole : prod 0.1 / conso 0.15 → import ~0.05 Mb/j. Gaz : prod 2 / conso 3 → import ~1 bcm (Norvège via Baltic Pipe hub ou interconnexions).
**Flux à ajouter :**
```json
{ id:"f286", from:"Norvège", to:"Danemark", from_centroid:[10,62], to_centroid:[10,56], type:"gas_pipeline", volume:1.0, unit:"bcm/an", year:2022, source:"Gassco / Energinet Denmark / IEA 2022 (interconnexion Nybro)" }
```
**Priorité :** FAIBLE

---

## Suède (SWE)
**Base :** pétrole prod=0 / conso=0.3 Mb/j | gaz prod=0 / conso=1 bcm
**Flux existants :** AUCUN.
**GAP :** Pétrole : conso 0.3 Mb/j = 100% importé. Gaz : conso 1 bcm = 100% importé (via Danemark).
**Flux à ajouter :**
```json
{ id:"f287", from:"Norvège", to:"Suède", from_centroid:[10,62], to_centroid:[18,62], type:"oil", volume:0.15, unit:"mb/j", year:2022, source:"Kpler / Energimyndigheten / IEA 2022 (tankers côte ouest, raffinerie Preem Lysekil)" }
{ id:"f288", from:"Arabie Saoudite", to:"Suède", from_centroid:[45,24], to_centroid:[18,62], type:"oil", volume:0.08, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (Arab Light→raffineries Preem)" }
{ id:"f289", from:"Russie", to:"Suède", from_centroid:[60,58], to_centroid:[18,62], type:"oil", volume:0.05, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (avant embargo EU déc. 2022, Oural Baltique)" }
{ id:"f290", from:"Danemark", to:"Suède", from_centroid:[10,56], to_centroid:[18,62], type:"gas_pipeline", volume:1.0, unit:"bcm/an", year:2022, source:"Energinet / Energimyndigheten / IEA 2022 (interconnexion Dragør-Klagshamn)" }
```
**Priorité :** HAUTE

---

## Portugal (PRT)
**Base :** pétrole prod=0 / conso=0.24 Mb/j | gaz prod=0.1 / conso=5.5 bcm
**Flux existants :** AUCUN flux entrant documenté.
**GAP :** Pétrole : conso 0.24 Mb/j = 100% importé. Gaz : déficit ~5.4 bcm (terminal GNL Sines = porte d'entrée principale).
**Flux à ajouter :**
```json
{ id:"f291", from:"Arabie Saoudite", to:"Portugal", from_centroid:[45,24], to_centroid:[-8.2,39.4], type:"oil", volume:0.07, unit:"mb/j", year:2022, source:"Kpler / DGEG Portugal / IEA 2022 (raffinerie Matosinhos)" }
{ id:"f292", from:"Nigeria", to:"Portugal", from_centroid:[8,9], to_centroid:[-8.2,39.4], type:"oil", volume:0.05, unit:"mb/j", year:2022, source:"Kpler / NNPC / IEA 2022 (Bonny Light, 2e fournisseur)" }
{ id:"f293", from:"Angola", to:"Portugal", from_centroid:[18,-12], to_centroid:[-8.2,39.4], type:"oil", volume:0.04, unit:"mb/j", year:2022, source:"Kpler / SONANGOL / IEA 2022 (liens historiques)" }
{ id:"f294", from:"États-Unis", to:"Portugal", from_centroid:[-95,38], to_centroid:[-8.2,39.4], type:"lng", volume:2.5, unit:"bcm/an", year:2022, source:"DOE / REN Portugal / GIIGNL 2023 (Sines LNG terminal, 1er fournisseur gaz)" }
{ id:"f295", from:"Algérie", to:"Portugal", from_centroid:[3,28], to_centroid:[-8.2,39.4], type:"lng", volume:1.5, unit:"bcm/an", year:2022, source:"Sonatrach / REN Portugal / GIIGNL 2023" }
{ id:"f296", from:"Nigeria", to:"Portugal", from_centroid:[8,9], to_centroid:[-8.2,39.4], type:"lng", volume:1.2, unit:"bcm/an", year:2022, source:"NNPC / REN Portugal / GIIGNL 2023" }
```
**Priorité :** HAUTE

---

## Irlande (IRL)
**Base :** pétrole prod=0 / conso=0.15 Mb/j | gaz prod=2.5 / conso=5.0 bcm
**Flux existants :** AUCUN flux entrant documenté.
**GAP :** Pétrole : conso 0.15 Mb/j = 100% importé. Gaz : prod 2.5 (Corrib, déclin) / conso 5 → import 2.5 bcm (Interconnecteur Moffat via Royaume-Uni).
**Flux à ajouter :**
```json
{ id:"f297", from:"Norvège", to:"Irlande", from_centroid:[10,62], to_centroid:[-8.0,53.2], type:"oil", volume:0.07, unit:"mb/j", year:2022, source:"Kpler / SEAI Ireland / IEA 2022 (tankers, 1er fournisseur ~45%)" }
{ id:"f298", from:"Royaume-Uni", to:"Irlande", from_centroid:[-2,54], to_centroid:[-8.0,53.2], type:"gas_pipeline", volume:2.5, unit:"bcm/an", year:2022, source:"National Grid UK / GNI Ireland / IEA 2022 (Interconnecteur Moffat-Brighouse Bay)" }
```
**Priorité :** HAUTE

---

## Bulgarie (BGR)
**Base :** pétrole prod=0.02 / conso=0.1 Mb/j | gaz prod=0.3 / conso=3.0 bcm
**Flux existants :** AUCUN flux entrant spécifique.
**GAP :** Pétrole : import ~0.08 Mb/j. Gaz : import ~2.7 bcm (était 100% russe avant 2022, pivot LNG/Azerbaïdjan en cours).
**Flux à ajouter :**
```json
{ id:"f299", from:"Russie", to:"Bulgarie", from_centroid:[60,58], to_centroid:[25.5,42.7], type:"gas_pipeline", volume:2.0, unit:"bcm/an", year:2022, source:"Bulgargaz / IEA 2022 (TurkStream branche nord, Russie a coupé gaz mai 2022, mais transit partiel 2022)" }
{ id:"f300", from:"Azerbaïdjan", to:"Bulgarie", from_centroid:[47.4,40.4], to_centroid:[25.5,42.7], type:"gas_pipeline", volume:1.0, unit:"bcm/an", year:2022, source:"SOCAR / Bulgargaz / IEA 2022 (ICGB interconnecteur, opérationnel oct. 2022)" }
{ id:"f301", from:"Russie", to:"Bulgarie", from_centroid:[60,58], to_centroid:[25.5,42.7], type:"oil", volume:0.08, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (raffinerie Lukoil Neftochim Bourgas, exemption embargo EU)" }
```
**Priorité :** HAUTE

---

## Croatie (HRV)
**Base :** pétrole prod=0.03 / conso=0.07 Mb/j | gaz prod=0.8 / conso=2.7 bcm
**Flux existants :** AUCUN flux entrant spécifique.
**GAP :** Pétrole : import ~0.04 Mb/j. Gaz : import ~1.9 bcm (terminal GNL Krk + interconnexions).
**Flux à ajouter :**
```json
{ id:"f302", from:"États-Unis", to:"Croatie", from_centroid:[-95,38], to_centroid:[16.4,45.1], type:"lng", volume:1.5, unit:"bcm/an", year:2022, source:"DOE / PLINACRO / GIIGNL 2023 (FSRU Krk, île de Krk, opérationnel 2021)" }
{ id:"f303", from:"Arabie Saoudite", to:"Croatie", from_centroid:[45,24], to_centroid:[16.4,45.1], type:"oil", volume:0.04, unit:"mb/j", year:2022, source:"Kpler / INA Croatia / IEA 2022 (JANAF pipeline, port Omišalj)" }
```
**Priorité :** MOYENNE

---

## Slovénie (SVN)
**Base :** pétrole prod=0 / conso=0.05 Mb/j | gaz prod=0 / conso=0.9 bcm
**Flux existants :** AUCUN.
**GAP :** 100% dépendant import pétrole + gaz. Krško NPP (50% Croatie, 50% Slovénie) = électricité domestique.
**Flux à ajouter :**
```json
{ id:"f304", from:"Russie", to:"Slovénie", from_centroid:[60,58], to_centroid:[14.8,46.1], type:"gas_pipeline", volume:0.7, unit:"bcm/an", year:2022, source:"Geoplin / IEA 2022 (via Autriche, résiduel avant pivot LNG)" }
{ id:"f305", from:"Arabie Saoudite", to:"Slovénie", from_centroid:[45,24], to_centroid:[14.8,46.1], type:"oil", volume:0.03, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (JANAF pipeline / terminal Omišalj Croatie)" }
```
**Priorité :** FAIBLE

---

## Lituanie (LTU)
**Base :** pétrole prod=0.01 / conso=0.06 Mb/j | gaz prod=0 / conso=2.5 bcm
**Flux existants :** AUCUN flux entrant.
**GAP :** Pétrole : import ~0.05 Mb/j. Gaz : 100% importé, terminal GNL flottant Klaipėda (FSRU).
**Flux à ajouter :**
```json
{ id:"f306", from:"États-Unis", to:"Lituanie", from_centroid:[-95,38], to_centroid:[24.0,55.9], type:"lng", volume:1.5, unit:"bcm/an", year:2022, source:"DOE / Ignitis Lithuania / GIIGNL 2023 (FSRU Independence Klaipėda, ~60% approvisionnement)" }
{ id:"f307", from:"Norvège", to:"Lituanie", from_centroid:[10,62], to_centroid:[24.0,55.9], type:"lng", volume:0.7, unit:"bcm/an", year:2022, source:"Equinor / Litgas / GIIGNL 2023 (Hammerfest LNG)" }
{ id:"f308", from:"Arabie Saoudite", to:"Lituanie", from_centroid:[45,24], to_centroid:[24.0,55.9], type:"oil", volume:0.04, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (raffinerie Orlen Lietuva Mažeikiai)" }
```
**Observations :** Lituanie a rompu toute dépendance au gaz russe en 2022 (FSRU Klaipėda). Déconnexion réseau électrique BRELL prévue 2025.
**Priorité :** HAUTE

---

## Lettonie (LVA)
**Base :** pétrole prod=0 / conso=0.04 Mb/j | gaz prod=0 / conso=1.5 bcm
**Flux existants :** AUCUN.
**GAP :** 100% dépendant import. Stockage souterrain Inčukalns = hub régional baltique.
**Flux à ajouter :**
```json
{ id:"f309", from:"États-Unis", to:"Lettonie", from_centroid:[-95,38], to_centroid:[25.0,56.9], type:"lng", volume:1.0, unit:"bcm/an", year:2022, source:"DOE / Latvijas Gāze / GIIGNL 2023 (via FSRU Klaipėda Lituanie → interconnexion gazoducs baltiques)" }
{ id:"f310", from:"Norvège", to:"Lettonie", from_centroid:[10,62], to_centroid:[25.0,56.9], type:"oil", volume:0.03, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (tankers Riga, produits légers)" }
```
**Priorité :** HAUTE

---

## Estonie (EST)
**Base :** pétrole prod=0 / conso=0.03 Mb/j | gaz prod=0 / conso=0.6 bcm
**Flux existants :** AUCUN.
**GAP :** Pétrole : 100% importé (~0.03 Mb/j). Gaz : 100% importé (~0.6 bcm). Particularité : électricité produite à partir de schiste bitumineux (oil shale) domestique — pas de flux import pour l'électricité.
**Flux à ajouter :**
```json
{ id:"f311", from:"États-Unis", to:"Estonie", from_centroid:[-95,38], to_centroid:[25.0,58.7], type:"lng", volume:0.4, unit:"bcm/an", year:2022, source:"DOE / Elering / GIIGNL 2023 (via FSRU Klaipėda → Baltic Connector)" }
{ id:"f312", from:"Finlande", to:"Estonie", from_centroid:[26,62], to_centroid:[25.0,58.7], type:"gas_pipeline", volume:0.2, unit:"bcm/an", year:2022, source:"Gasgrid Finland / Elering / IEA 2022 (Balticconnector, bidirectionnel)" }
```
**Observations :** Balticconnector (Finland-Estonia) sabotage octobre 2023 — contexte géopolitique majeur.
**Priorité :** MOYENNE

---

## Luxembourg (LUX)
**Base :** pétrole prod=0 / conso=0.05 Mb/j | gaz prod=0 / conso=0.8 bcm
**Flux existants :** AUCUN.
**GAP :** 100% dépendant import pétrole + gaz. Approvisionnement via réseaux belge et allemand.
**Flux à ajouter :**
```json
{ id:"f313", from:"Belgique", to:"Luxembourg", from_centroid:[4.5,50.5], to_centroid:[6.1,49.8], type:"gas_pipeline", volume:0.6, unit:"bcm/an", year:2022, source:"Fluxys / Creos Luxembourg / Eurostat 2022 (transit via réseau belge)" }
{ id:"f314", from:"Belgique", to:"Luxembourg", from_centroid:[4.5,50.5], to_centroid:[6.1,49.8], type:"oil", volume:0.04, unit:"mb/j", year:2022, source:"Kpler / Eurostat 2022 (produits pétroliers via Anvers)" }
```
**Priorité :** FAIBLE

---

## Suisse (CHE)
**Base :** pétrole prod=0 / conso=0.25 Mb/j | gaz prod=0 / conso=3.5 bcm
**Flux existants :** AUCUN flux entrant spécifique.
**GAP :** Pétrole : 100% importé (0.25 Mb/j via pipeline TAL Trieste→Ingolstadt→Suisse et tankers rhénans). Gaz : 100% importé (3.5 bcm via réseaux allemand, français, autrichien).
**Flux à ajouter :**
```json
{ id:"f315", from:"Arabie Saoudite", to:"Suisse", from_centroid:[45,24], to_centroid:[8.2,46.8], type:"oil", volume:0.08, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (TAL pipeline Gênes/Trieste→raffineries Collombey, Cressier)" }
{ id:"f316", from:"Norvège", to:"Suisse", from_centroid:[10,62], to_centroid:[8.2,46.8], type:"gas_pipeline", volume:1.5, unit:"bcm/an", year:2022, source:"Gassco / Swissgas / IEA 2022 (transit via France/Allemagne, ~40% approvisionnement)" }
{ id:"f317", from:"Russie", to:"Suisse", from_centroid:[60,58], to_centroid:[8.2,46.8], type:"gas_pipeline", volume:1.2, unit:"bcm/an", year:2022, source:"Gazprom / Swissgas / IEA 2022 (via Autriche, avant réduction 2022)" }
{ id:"f318", from:"Algérie", to:"Suisse", from_centroid:[3,28], to_centroid:[8.2,46.8], type:"gas_pipeline", volume:0.5, unit:"bcm/an", year:2022, source:"Sonatrach / Swissgas / IEA 2022 (transit via Italie, TENP)" }
```
**Priorité :** HAUTE

---

## Serbie (SRB)
**Base :** pétrole prod=0.02 / conso=0.08 Mb/j | gaz prod=0.3 / conso=2.8 bcm
**Flux existants :** AUCUN.
**GAP :** Pétrole : import ~0.06 Mb/j. Gaz : import ~2.5 bcm (TurkStream branche nord via Bulgarie, ex-transit Ukraine avant 2022).
**Flux à ajouter :**
```json
{ id:"f319", from:"Russie", to:"Serbie", from_centroid:[60,58], to_centroid:[20.9,44.0], type:"gas_pipeline", volume:2.2, unit:"bcm/an", year:2022, source:"Gazprom / Srbijagas / IEA 2022 (TurkStream branche nord via Bulgarie-Nišabanle)" }
{ id:"f320", from:"Russie", to:"Serbie", from_centroid:[60,58], to_centroid:[20.9,44.0], type:"oil", volume:0.04, unit:"mb/j", year:2022, source:"Kpler / NIS Srbija (Gazprom Neft) / IEA 2022 (raffinerie Pančevo)" }
{ id:"f321", from:"Irak", to:"Serbie", from_centroid:[44,33], to_centroid:[20.9,44.0], type:"oil", volume:0.02, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (Basra Heavy via JANAF pipeline)" }
```
**Observations :** Serbie reste très dépendante Russie gaz (NIS = 56% Gazprom Neft) malgré statut candidat UE.
**Priorité :** HAUTE

---

## Macédoine du Nord (MKD)
**Base :** pétrole prod=0 / conso=0.02 Mb/j | gaz prod=0 / conso=0.1 bcm
**Flux existants :** AUCUN.
**GAP :** Pétrole 100% importé (~0.02 Mb/j). Gaz 100% importé (0.1 bcm, quasi-100% Russie jusqu'en 2022 via Bulgarie).
**Flux à ajouter :**
```json
{ id:"f322", from:"Russie", to:"Macédoine du Nord", from_centroid:[60,58], to_centroid:[21.7,41.6], type:"gas_pipeline", volume:0.1, unit:"bcm/an", year:2022, source:"Bulgargaz / Makpetrol / IEA 2022 (transit via Bulgarie)" }
{ id:"f323", from:"Grèce", to:"Macédoine du Nord", from_centroid:[22,39], to_centroid:[21.7,41.6], type:"oil", volume:0.015, unit:"mb/j", year:2022, source:"Kpler / EVO Macedonia / IEA 2022 (produits raffinés via OKTA Skopje)" }
```
**Priorité :** FAIBLE

---

## Albanie (ALB)
**Base :** pétrole prod=0.02 / conso=0.03 Mb/j | gaz prod=0 / conso=0.2 bcm
**Flux existants :** AUCUN.
**GAP :** Pétrole : import ~0.01 Mb/j (produits raffinés). Gaz : 100% importé (Grèce via TAP, hors service souvent car faible demande).
**Flux à ajouter :**
```json
{ id:"f324", from:"Azerbaïdjan", to:"Albanie", from_centroid:[47.4,40.4], to_centroid:[20.1,41.1], type:"gas_pipeline", volume:0.15, unit:"bcm/an", year:2022, source:"SOCAR / AKBN Albania / IEA 2022 (off-take TAP, terminal Fier)" }
{ id:"f325", from:"Grèce", to:"Albanie", from_centroid:[22,39], to_centroid:[20.1,41.1], type:"oil", volume:0.01, unit:"mb/j", year:2022, source:"Kpler / IEA 2022 (produits raffinés Thessalonique→Tirana)" }
```
**Priorité :** FAIBLE

---

## Bosnie-Herzégovine (BIH)
**Base :** pétrole prod=0 / conso=0.03 Mb/j | gaz prod=0 / conso=0.5 bcm
**Flux existants :** AUCUN.
**GAP :** Pétrole 100% importé (0.03 Mb/j). Gaz 100% importé (0.5 bcm, principalement Russie via Croatie/Serbie).
**Flux à ajouter :**
```json
{ id:"f326", from:"Russie", to:"Bosnie-Herzégovine", from_centroid:[60,58], to_centroid:[17.5,44.2], type:"gas_pipeline", volume:0.4, unit:"bcm/an", year:2022, source:"BH-Gas / IEA 2022 (transit via Serbie/Croatie, Gazprom contrat)" }
{ id:"f327", from:"Croatie", to:"Bosnie-Herzégovine", from_centroid:[16.4,45.1], to_centroid:[17.5,44.2], type:"oil", volume:0.02, unit:"mb/j", year:2022, source:"Kpler / INA / IEA 2022 (pipeline JANAF branche)" }
```
**Priorité :** FAIBLE

---

## Cambodge (KHM)
**Base :** pétrole prod=0 / conso=0.04 Mb/j | gaz prod=0 / conso=0
**Flux existants :** AUCUN.
**GAP :** Pétrole 100% importé (~0.04 Mb/j produits raffinés, principalement Singapour/Thaïlande).
**Flux à ajouter :**
```json
{ id:"f328", from:"Singapour", to:"Cambodge", from_centroid:[103.8,1.35], to_centroid:[104,12], type:"oil", volume:0.02, unit:"mb/j", year:2022, source:"Kpler / EAC Cambodia / IEA 2022 (produits raffinés, port de Sihanoukville)" }
{ id:"f329", from:"Thaïlande", to:"Cambodge", from_centroid:[101,15], to_centroid:[104,12], type:"oil", volume:0.01, unit:"mb/j", year:2022, source:"Kpler / PPCI Cambodia / IEA 2022 (pipeline terrestre produits pétroliers)" }
```
**Priorité :** FAIBLE

---

## Mongolie (MNG)
**Base :** pétrole prod=0.03 / conso=0.03 Mb/j | gaz prod=0 / conso=0
**Flux existants :** AUCUN.
**GAP :** Production et consommation pétrole équilibrées. Pas de gaz. Electricité 90% importée Russie/Chine pour les grandes villes.
**Flux à ajouter :**
```json
{ id:"f330", from:"Russie", to:"Mongolie", from_centroid:[60,58], to_centroid:[103,47], type:"oil", volume:0.02, unit:"mb/j", year:2022, source:"Kpler / IEA Central Asia 2022 (produits pétroliers raffinés, Rosneft via accord bilatéral)" }
```
**Observations :** La Mongolie est en négociation pour le projet Power of Siberia-2 (gazoduc Russie-Chine via Mongolie) — suivi géopolitique important.
**Priorité :** FAIBLE

---

## Pérou (PER)
**Base :** pétrole prod=0.12 / conso=0.20 Mb/j | gaz prod=14 / conso=8 bcm
**Flux existants :** f043 (Peru LNG→Espagne 4.1 bcm)
**GAP :** Pétrole : prod 0.12 / conso 0.20 → import ~0.08 Mb/j. Gaz EXPORTATEUR (Peru LNG). Flux pétrole importé absent.
**Flux à ajouter :**
```json
{ id:"f331", from:"États-Unis", to:"Pérou", from_centroid:[-95,38], to_centroid:[-76,-10], type:"oil", volume:0.05, unit:"mb/j", year:2022, source:"Kpler / EIA / Osinergmin Peru 2022 (produits raffinés, manque raffinerie domestique)" }
{ id:"f332", from:"Équateur", to:"Pérou", from_centroid:[-78,-2], to_centroid:[-76,-10], type:"oil", volume:0.03, unit:"mb/j", year:2022, source:"Kpler / Petroecuador / Osinergmin 2022" }
```
**Priorité :** FAIBLE

---

## Équateur (ECU)
**Base :** pétrole prod=0.5 / conso=0.25 Mb/j | gaz prod=0.4 / conso=0.4 bcm
**Flux existants :** f095 (→USA pétrole 0.2), f127 (→USA pétrole 0.2 — doublon possible)
**GAP :** EXPORTATEUR NET pétrole. Autosuffisant gaz. f095 et f127 semblent être un doublon (même flux Ecuador→USA pétrole).
**Observations :** **Doublon confirmé** — f095 et f127 sont tous deux "Équateur→États-Unis pétrole ~0.2 Mb/j". À nettoyer.
**Flux à ajouter :** Aucun — exportateur net.
**Priorité :** FAIBLE (correction doublon f095/f127 recommandée)

---

## Ghana (GHA)
**Base :** pétrole prod=0.18 / conso=0.08 Mb/j | gaz prod=2 / conso=3 bcm
**Flux existants :** AUCUN.
**GAP :** EXPORTATEUR PÉTROLE NET. Gaz : import ~1 bcm (pipeline régional WAGP de Nigeria ou LNG spot).
**Flux à ajouter :**
```json
{ id:"f333", from:"Nigeria", to:"Ghana", from_centroid:[8,9], to_centroid:[-1,8], type:"gas_pipeline", volume:1.5, unit:"bcm/an", year:2022, source:"NNPC / GNPC Ghana / IEA 2022 (West Africa Gas Pipeline WAGP, 678 km)" }
```
**Observations :** Ghana a aussi développé des LNG imports spot pour compenser les interruptions WAGP.
**Priorité :** FAIBLE

---

## Mozambique (MOZ)
**Base :** pétrole prod=0 / conso=0.03 Mb/j | gaz prod=6 / conso=0.5 bcm
**Flux existants :** f200 (Mozambique→Afrique du Sud gaz 3.8 bcm ROMPCO)
**GAP :** EXPORTATEUR GAS. Pétrole : 100% importé (0.03 Mb/j).
**Flux à ajouter :**
```json
{ id:"f334", from:"Inde", to:"Mozambique", from_centroid:[78,22], to_centroid:[35,-17], type:"oil", volume:0.02, unit:"mb/j", year:2022, source:"Kpler / INP Mozambique / IEA 2022 (produits raffinés Jamnagar→Maputo)" }
```
**Observations :** Coral South FLNG opérationnel 2022 → export LNG vers Europe (ENI/Total). À documenter comme flux export.
**Flux export à ajouter :**
```json
{ id:"f335", from:"Mozambique", to:"Europe", from_centroid:[35,-17], to_centroid:[10,50], type:"lng", volume:3.4, unit:"bcm/an", year:2022, source:"ENI / TotalEnergies / IEA 2022 (Coral South FLNG, 3.4 MT/an soit ~4.6 bcm)" }
```
**Priorité :** FAIBLE

---

## Ouganda (UGA)
**Base :** pétrole prod=0 / conso=0.04 Mb/j | gaz prod=0 / conso=0
**Flux existants :** AUCUN.
**GAP :** Pétrole 100% importé (0.04 Mb/j produits raffinés via Kenya).
**Flux à ajouter :**
```json
{ id:"f336", from:"Kenya", to:"Ouganda", from_centroid:[37.5,0.5], to_centroid:[32.3,1.3], type:"oil", volume:0.03, unit:"mb/j", year:2022, source:"Kpler / EPRA Kenya / ERA Uganda 2022 (pipeline Mombasa-Kampala, produits raffinés)" }
```
**Observations :** EACOP (pipeline brut Tilenga-Tanzanie) en construction — quand opérationnel, flux sortant à documenter.
**Priorité :** FAIBLE

---

## Zimbabwe (ZWE)
**Base :** pétrole prod=0 / conso=0.02 Mb/j | gaz prod=0 / conso=0
**Flux existants :** AUCUN.
**GAP :** Pétrole 100% importé (~0.02 Mb/j), principalement Afrique du Sud (Natref) et pipeline TAZAMA.
**Flux à ajouter :**
```json
{ id:"f337", from:"Afrique du Sud", to:"Zimbabwe", from_centroid:[25,-29], to_centroid:[30,-20], type:"oil", volume:0.015, unit:"mb/j", year:2022, source:"Kpler / ZERA Zimbabwe / IEA Africa 2022 (pipeline Feruka, produits raffinés Durban→Harare)" }
```
**Priorité :** FAIBLE

---

## Zambie (ZMB)
**Base :** pétrole prod=0 / conso=0.02 Mb/j | gaz prod=0 / conso=0
**Flux existants :** AUCUN.
**GAP :** Pétrole 100% importé (~0.02 Mb/j via pipeline TAZAMA depuis Tanzanie).
**Flux à ajouter :**
```json
{ id:"f338", from:"Tanzanie", to:"Zambie", from_centroid:[35,-6], to_centroid:[28,-14], type:"oil", volume:0.02, unit:"mb/j", year:2022, source:"Kpler / TAZAMA Pipelines / ERB Zambia 2022 (TAZAMA pipeline 1 710 km Dar es Salam→Ndola)" }
```
**Priorité :** FAIBLE

---

## Sénégal (SEN)
**Base :** pétrole prod=0.07 / conso=0.05 Mb/j | gaz prod=2.5 / conso=0.3 bcm
**Flux existants :** AUCUN.
**GAP :** NOUVEAU PRODUCTEUR (Sangomar 2024, GTA 2024). En 2022 encore pré-production. Dépendant import pétrole raffiné malgré ressources brutes.
**Flux à ajouter :**
```json
{ id:"f339", from:"Nigeria", to:"Sénégal", from_centroid:[8,9], to_centroid:[-14,14.5], type:"oil", volume:0.03, unit:"mb/j", year:2022, source:"Kpler / NNPC / IEA Africa 2022 (produits raffinés, Dakar principal port importation)" }
```
**Priorité :** FAIBLE

---

## Cameroun (CMR)
**Base :** pétrole prod=0.07 / conso=0.04 Mb/j | gaz prod=0.9 / conso=0.6 bcm
**Flux existants :** AUCUN.
**GAP :** EXPORTATEUR NET pétrole. Autosuffisant gaz (FLNG Kribi ~1.2 MT/an).
**Flux à ajouter :** Aucun import structurel. Export FLNG à documenter.
```json
{ id:"f340", from:"Cameroun", to:"Europe", from_centroid:[12,5], to_centroid:[10,50], type:"lng", volume:1.7, unit:"bcm/an", year:2022, source:"Golar LNG / NewAge / IEA Africa 2022 (Kribi FLNG, 1.2 MT/an → ~1.7 bcm)" }
```
**Priorité :** FAIBLE

---

## Trinité-et-Tobago (TTO)
**Base :** pétrole prod=0.08 / conso=0.04 Mb/j | gaz prod=36 / conso=20 bcm
**Flux existants :** f038 (→Europe LNG 13.8 bcm), f070 (→Espagne LNG 5.5 bcm), f071 (→France LNG 2.8 bcm), f210 (→Belgique LNG 2.8 bcm)
**GAP :** EXPORTATEUR LNG MAJEUR (~15 MT/an Atlantic LNG). Export vers USA et Europe documentés. Flux vers USA absent.
**Flux à ajouter :**
```json
{ id:"f341", from:"Trinité-et-Tobago", to:"États-Unis", from_centroid:[-61.2,10.7], to_centroid:[-95,38], type:"lng", volume:4.1, unit:"bcm/an", year:2022, source:"NGC Trinidad / GIIGNL 2023 / EIA (Atlantic LNG trains 2-4, Lake Charles terminus)" }
```
**Priorité :** FAIBLE

---

## Nouvelle-Zélande (NZL)
**Base :** pétrole prod=0.05 / conso=0.16 Mb/j | gaz prod=4.5 / conso=5.5 bcm
**Flux existants :** AUCUN.
**GAP :** Pétrole : prod 0.05 / conso 0.16 → import ~0.11 Mb/j. Gaz : prod 4.5 / conso 5.5 → import ~1.0 bcm (principalement via LNG imports spot depuis Australie).
**Flux à ajouter :**
```json
{ id:"f342", from:"Australie", to:"Nouvelle-Zélande", from_centroid:[133,-27], to_centroid:[172,-41], type:"oil", volume:0.07, unit:"mb/j", year:2022, source:"Kpler / MBIE New Zealand / IEA 2022 (raffinerie Marsden Point fermée 2022, 100% import après)" }
{ id:"f343", from:"Arabie Saoudite", to:"Nouvelle-Zélande", from_centroid:[45,24], to_centroid:[172,-41], type:"oil", volume:0.04, unit:"mb/j", year:2022, source:"Kpler / MBIE New Zealand / IEA 2022" }
```
**Observations :** Fermeture de la raffinerie Marsden Point en avril 2022 rend la NZ 100% dépendante des produits raffinés importés.
**Priorité :** MOYENNE

---

## OBSERVATIONS TRANSVERSALES ROUND 4

### Doublons confirmés à corriger
- **f095 / f127** : Équateur→États-Unis pétrole, deux entrées pour le même flux (~0.2 Mb/j). Supprimer f095 (doublon de f127).
- **f042 / f153** : Angola→Chine pétrole — volumes différents (0.7 et 0.3 Mb/j). Probablement intentionnel (volumes réels ~1.0 Mb/j Angola = 2e fournisseur Chine). Conserver les deux avec note.

### Flux critiques manquants (impact score)
1. **Dolphin Pipeline Qatar→UAE** (f273) : 20 bcm/an — flux physique majeur complètement absent, fausse le score UAE
2. **Biélorussie** (f283, f284) : 100% dépendance Russie invisible — score vulnérabilité nul alors qu'il devrait être maximal
3. **Serbie** (f319) : TurkStream branche nord absente
4. **Pays baltes** (f306-f312) : Transition post-Russie vers LNG non documentée

### Exportateurs avec flux sortants manquants
- **Oman→Japon/Corée LNG** (f278, f279) : ~12 bcm/an absent
- **Trinité-et-Tobago→USA** (f341) : ~4 bcm/an absent
- **Mozambique→Europe LNG** (f335) : Coral South FLNG absent

### Nouveaux flux (IDs f267–f343)
Total : **77 flux proposés** dans ce Round 4.
Flux haute priorité : f267 (Norvège→Espagne), f268 (Qatar→Singapour), f269-f272 (Australie imports), f273 (Qatar→UAE Dolphin), f274 (Iran→Irak gaz), f278-f279 (Oman LNG), f283-f284 (Biélorussie), f287-f290 (Suède), f291-f296 (Portugal), f297-f298 (Irlande), f299-f301 (Bulgarie), f306-f308 (Lituanie), f309-f310 (Lettonie), f315-f318 (Suisse), f319-f321 (Serbie).

---

## SYNTHÈSE GLOBALE DES 4 ROUNDS

| Métrique | Valeur |
|---|---|
| Pays audités | ~95 (couvre quasi-totalité d'ENERGY_DATA) |
| Flux ajoutés (f131–f266 appliqués + f267–f343 proposés) | ~213 flux au total |
| Pays CRITIQUE sans flux | Biélorussie, Pays baltes (avant ce round) |
| Flux invalides/doublons identifiés | f095≈f127, f037≈f087 (Australie→Inde), f042+f153 (Angola→Chine partiel) |
| Exportateurs sans flux sortant | Oman LNG, Trinidad→USA, Mozambique LNG, Norvège→Espagne |
| Prochain ID libre | **f344** |

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
