"""
Télécharge les flux bilatéraux d'IDE (Investissements Directs Étrangers)
depuis l'API OECD — dataset DF_FDI_FLOW_CTRY (FDI flows by counterpart area, BMD4).

Génère data/finance.json avec flux outward des grands investisseurs OECD.

Source : https://sdmx.oecd.org/public/rest/data/OECD.DAF.INV
Clé API : aucune requise.
"""
import json, os, csv, io, time, urllib.request, urllib.error
from datetime import datetime
from collections import defaultdict

YEARS = list(range(2018, 2023))  # 2018–2022

# Reporters OECD (grands pays investisseurs couverts)
REPORTERS_ISO3 = [
    "USA", "JPN", "DEU", "GBR", "FRA", "NLD",
    "CHE", "KOR", "CAN", "AUS", "ITA", "ESP", "BEL",
]

# Mapping ISO3 → nom français (doit correspondre à COORDS ci-dessous)
ISO3_TO_FR = {
    "USA": "États-Unis",    "JPN": "Japon",          "DEU": "Allemagne",
    "GBR": "Royaume-Uni",   "FRA": "France",          "NLD": "Pays-Bas",
    "CHE": "Suisse",        "KOR": "Corée du Sud",    "CAN": "Canada",
    "AUS": "Australie",     "ITA": "Italie",          "ESP": "Espagne",
    "BEL": "Belgique",      "SWE": "Suède",           "DNK": "Danemark",
    "CHN": "Chine",         "IND": "Inde",            "BRA": "Brésil",
    "SGP": "Singapour",     "MYS": "Malaisie",        "IDN": "Indonésie",
    "MEX": "Mexique",       "THA": "Thaïlande",       "VNM": "Vietnam",
    "SAU": "Arabie Saoudite","ARE": "Émirats Arabes Unis",
    "RUS": "Russie",        "TUR": "Turquie",         "POL": "Pologne",
    "ARG": "Argentine",     "CHL": "Chili",           "PER": "Pérou",
    "ZAF": "Afrique du Sud","NOR": "Norvège",         "IRL": "Irlande",
    "TWN": "Taïwan",        "PHL": "Philippines",     "CZE": "Tchéquie",
    "HUN": "Hongrie",       "PRT": "Portugal",        "GRC": "Grèce",
    "FIN": "Finlande",      "AUT": "Autriche",        "LUX": "Luxembourg",
    "KAZ": "Kazakhstan",    "UKR": "Ukraine",         "SWZ": "Eswatini",
    "NZL": "Nouvelle-Zélande",
}

COORDS = {
    "États-Unis":      [-100, 38],   "Japon":           [138, 37],
    "Allemagne":       [10,  51],    "Royaume-Uni":     [-2,  54],
    "France":          [2,   47],    "Pays-Bas":        [5,   52],
    "Suisse":          [8,   47],    "Corée du Sud":    [127, 37],
    "Canada":          [-96, 56],    "Australie":       [133,-27],
    "Italie":          [12,  43],    "Espagne":         [-4,  40],
    "Belgique":        [4.5,50.5],   "Suède":           [17,  60],
    "Danemark":        [10,  56],
    "Chine":           [104, 35],    "Inde":            [78,  22],
    "Brésil":          [-55,-10],    "Singapour":       [104,  1],
    "Malaisie":        [110,  3],    "Indonésie":       [117, -2],
    "Mexique":         [-102,23],    "Thaïlande":       [101, 15],
    "Vietnam":         [106, 16],    "Arabie Saoudite": [45,  24],
    "Émirats Arabes Unis": [54, 24], "Russie":          [60,  58],
    "Turquie":         [35,  39],    "Pologne":         [20,  52],
    "Argentine":       [-64,-34],    "Chili":           [-71,-35],
    "Pérou":           [-76,-10],    "Afrique du Sud":  [25, -29],
    "Norvège":         [10,  62],    "Irlande":         [-8,  53],
    "Taïwan":          [121, 24],    "Philippines":     [122, 13],
    "Tchéquie":        [15.5,49.8],  "Hongrie":         [19,  47],
    "Portugal":        [-8,  39.5],  "Grèce":           [22,  39],
    "Finlande":        [26,  62],    "Autriche":        [14,  47],
    "Luxembourg":      [6.1, 49.8],  "Kazakhstan":      [67,  48],
    "Ukraine":         [32,  49],    "Nouvelle-Zélande":  [172,-41],
}

THRESHOLD_MD = 2.0       # seuil flux OCDE : 2 Md$ minimum
THRESHOLD_CHN_MD = 0.5   # seuil Chine : 0.5 Md$ (investissements plus diffus)

def fetch_bilateral(reporters, years):
    rep_str = "+".join(reporters)
    # Dimensions: REF_AREA.MEASURE.UNIT_MEASURE.MEASURE_PRINCIPLE.ACCOUNTING_ENTRY
    #             .TYPE_ENTITY.FDI_COMP.SECTOR.COUNTERPART_AREA.LEVEL_COUNTERPART
    #             .ACTIVITY.FREQ.FDI_COLLECTION_ID
    key = f"{rep_str}..USD_EXC.DO...D.S1..IMC._T.A.CTRY_IND"
    url = (
        "https://sdmx.oecd.org/public/rest/data/"
        f"OECD.DAF.INV,DSD_FDI@DF_FDI_FLOW_CTRY,1.0/{key}"
        f"?startPeriod={years[0]}&endPeriod={years[-1]}&format=csvfile"
    )
    print(f"Téléchargement OECD bilateral FDI ({years[0]}-{years[-1]})...")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read().decode("utf-8")
                print(f"  Reçu : {len(data)//1024} KB")
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 30 * (attempt + 1)
                print(f"  429 — attente {wait}s (tentative {attempt+1}/3)...")
                time.sleep(wait)
            else:
                print(f"  HTTP {e.code}")
                return None
        except Exception as e:
            print(f"  Erreur: {e}")
            return None
    return None


def parse_flows(csv_text, years):
    """
    Parse le CSV OECD.
    Retourne dict (from_fr, to_fr) -> {str(year): val_md}.

    Logique de déduplication :
      - Préfère ACCOUNTING_ENTRY=NET_FDI (flux net)
      - Sinon prend A (assets = investissement sortant)
      - Ignore les valeurs négatives par paire/année
    """
    years_set = set(str(y) for y in years)
    # raw[reporter][partner][year][entry] = val_millions
    raw = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        rep     = row.get("REF_AREA", "")
        partner = row.get("COUNTERPART_AREA", "")
        year    = row.get("TIME_PERIOD", "")
        entry   = row.get("ACCOUNTING_ENTRY", "")
        obs     = row.get("OBS_VALUE", "").strip()

        if year not in years_set: continue
        if not obs: continue
        # Garde seulement les codes ISO3 (3 lettres alpha — pas d'agrégats type W, OECD, E...)
        if len(partner) != 3 or not partner.isalpha(): continue
        if partner == rep: continue

        try:
            raw[rep][partner][year][entry] = float(obs)
        except ValueError:
            continue

    # Agrégation : (from_fr, to_fr) -> year -> val_md
    flows = defaultdict(dict)

    for rep, partners in raw.items():
        from_fr = ISO3_TO_FR.get(rep)
        if not from_fr or from_fr not in COORDS:
            continue
        for part, yr_data in partners.items():
            to_fr = ISO3_TO_FR.get(part)
            if not to_fr or to_fr not in COORDS or to_fr == from_fr:
                continue
            for year, entries in yr_data.items():
                # Préférence : NET_FDI > A > premier disponible
                val = (entries.get("NET_FDI")
                       or entries.get("A")
                       or next(iter(entries.values()), None))
                if val is None:
                    continue
                val_md = val / 1000.0  # millions → milliards
                if val_md >= THRESHOLD_MD:
                    flows[(from_fr, to_fr)][year] = round(val_md, 1)

    # Garde seulement les paires avec au moins 1 année valide
    return {k: v for k, v in flows.items() if v}


def fetch_china_outward(years):
    """
    Flux IDE de Chine vers les pays OCDE via les déclarations inward (DI)
    des pays OCDE avec la Chine comme COUNTERPART_AREA.
    """
    key = ".T_FA_F.USD_EXC.DI...D.S1.CHN.IMC._T.A.CTRY_IND"
    url = (
        "https://sdmx.oecd.org/public/rest/data/"
        f"OECD.DAF.INV,DSD_FDI@DF_FDI_FLOW_CTRY,1.0/{key}"
        f"?startPeriod={years[0]}&endPeriod={years[-1]}&format=csvfile"
    )
    print("Telechargement IDE Chine -> pays OCDE...")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read().decode("utf-8")
                print(f"  Reçu : {len(data)//1024} KB")
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(30 * (attempt + 1))
            else:
                print(f"  HTTP {e.code}")
                return None
        except Exception as e:
            print(f"  Erreur: {e}")
            return None
    return None


def parse_china_flows(csv_text, years):
    """
    Parse les flux entrants OCDE depuis Chine.
    REF_AREA = pays destination (OCDE), COUNTERPART_AREA = CHN.
    Retourne dict ("Chine", to_fr) -> {year: val_md}.
    """
    years_set = set(str(y) for y in years)
    raw = defaultdict(lambda: defaultdict(dict))  # [dest_iso][year][entry]

    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        dest    = row.get("REF_AREA", "")
        year    = row.get("TIME_PERIOD", "")
        entry   = row.get("ACCOUNTING_ENTRY", "")
        obs     = row.get("OBS_VALUE", "").strip()

        if year not in years_set or not obs:
            continue
        try:
            raw[dest][year][entry] = float(obs)
        except ValueError:
            continue

    flows = {}
    for dest_iso, yr_data in raw.items():
        to_fr = ISO3_TO_FR.get(dest_iso)
        if not to_fr or to_fr not in COORDS or to_fr == "Chine":
            continue
        hist = {}
        for year, entries in yr_data.items():
            val = (entries.get("NET_FDI")
                   or entries.get("A")
                   or next(iter(entries.values()), None))
            if val is None:
                continue
            val_md = val / 1000.0
            if val_md >= THRESHOLD_CHN_MD:
                hist[year] = round(val_md, 1)
        if hist:
            flows[("Chine", to_fr)] = hist

    return flows


def main():
    # 1. Flux sortants des pays OCDE
    csv_text = fetch_bilateral(REPORTERS_ISO3, YEARS)
    if not csv_text:
        print("Échec du téléchargement OECD.")
        return

    flows_dict = parse_flows(csv_text, YEARS)
    print(f"{len(flows_dict)} paires pays OCDE avec IDE >= {THRESHOLD_MD} Md$/an")

    # 2. Flux sortants de la Chine (via déclarations inward OCDE)
    chn_csv = fetch_china_outward(YEARS)
    if chn_csv:
        chn_flows = parse_china_flows(chn_csv, YEARS)
        print(f"{len(chn_flows)} destinations chinoises avec IDE >= {THRESHOLD_CHN_MD} Md$/an")
        flows_dict.update(chn_flows)

    flows_out = []
    for (from_fr, to_fr), hist in sorted(flows_dict.items()):
        flows_out.append({
            "from":  from_fr,
            "fromC": COORDS[from_fr],
            "to":    to_fr,
            "toC":   COORDS[to_fr],
            "type":  "fdi",
            "unit":  "Md$",
            "color": "#34d399",
            "hist":  hist,
        })

    # Aperçu top 10
    print("\nTop 10 flux par valeur max :")
    for f in sorted(flows_out, key=lambda x: -max(x["hist"].values(), default=0))[:10]:
        best = max(f["hist"].items(), key=lambda x: x[1])
        print(f"  {f['from']:20} -> {f['to']:20}: {best[1]:6.1f} Md$ ({best[0]})")

    os.makedirs("data", exist_ok=True)
    out = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "years":   [YEARS[0], YEARS[-1]],
        "source":  "OECD — FDI flows by counterpart area, BMD4",
        "url":     "https://sdmx.oecd.org/public/rest/data/OECD.DAF.INV,DSD_FDI@DF_FDI_FLOW_CTRY",
        "flows":   flows_out,
    }
    with open("data/finance.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    print(f"\nSauvegardé {len(flows_out)} flux -> data/finance.json")


if __name__ == "__main__":
    main()
