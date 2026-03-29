"""
Télécharge les flux commerciaux de technologie/électronique depuis l'API UN Comtrade v1.
Génère data/tech_flows.json avec séries historiques 2015–2023 par paire pays.

Fonctionnement :
  - Charge tech_flows.json existant au démarrage
  - Ne fetche QUE les combinaisons (exporteur, type, année) manquantes
  - Retry automatique sur 429 (attente exponentielle : 60s, 120s, 180s)

Types couverts (codes HS) :
  8542 — Circuits intégrés / semiconducteurs  (electronics)
  8458+8462+8466 — Tours + Presses + Parties machines-outils (machinery)

Source : https://comtradeapi.un.org  (nécessite COMTRADE_KEY)
"""
import json, os, time, urllib.request, urllib.error
from datetime import datetime
from collections import defaultdict

YEARS = list(range(2015, 2024))   # 2015 → 2023

M49_TO_FR = {
    # Exportateurs / importateurs métaux (repris pour cohérence)
    "152": "Chili",          "604": "Pérou",
    "180": "Congo RDC",      "36":  "Australie",
    "894": "Zambie",         "643": "Russie",
    "360": "Indonésie",      "608": "Philippines",
    "124": "Canada",         "76":  "Brésil",
    "710": "Afrique du Sud", "356": "Inde",
    "32":  "Argentine",      "398": "Kazakhstan",
    "484": "Mexique",        "616": "Pologne",
    "804": "Ukraine",        "716": "Zimbabwe",
    "598": "Papouasie-NG",
    "578": "Norvège",        "784": "Émirats Arabes Unis",
    "792": "Turquie",
    "156": "Chine",          "392": "Japon",
    "410": "Corée du Sud",   "528": "Pays-Bas",
    "246": "Finlande",       "56":  "Belgique",
    "276": "Allemagne",      "250": "France",
    "826": "Royaume-Uni",    "380": "Italie",
    "724": "Espagne",        "764": "Thaïlande",
    "704": "Vietnam",        "458": "Malaisie",
    "840": "États-Unis",
    # Additions spécifiques tech
    "158": "Taïwan",
    "702": "Singapour",
    "756": "Suisse",
}

COORDS = {
    "Chili":              [-71, -35],  "Pérou":          [-76, -10],
    "Congo RDC":          [24,  -3],   "Australie":      [133, -27],
    "Zambie":             [28,  -14],  "Russie":         [60,   58],
    "Indonésie":          [117, -2],   "Philippines":    [122,  13],
    "Canada":             [-96, 56],   "Brésil":         [-55, -10],
    "Afrique du Sud":     [25,  -29],  "Inde":           [78,   22],
    "Argentine":          [-64, -34],  "Kazakhstan":     [67,   48],
    "Mexique":            [-102, 23],  "Pologne":        [20,   52],
    "Ukraine":            [32,  49],   "Zimbabwe":       [30,  -20],
    "Papouasie-NG":       [145, -6],   "Norvège":        [10,   62],
    "Émirats Arabes Unis":[54,  24],   "Turquie":        [35,   39],
    "Chine":              [104,  35],  "Japon":          [138,  37],
    "Corée du Sud":       [127,  37],  "Pays-Bas":       [5,    52],
    "Finlande":           [26,   62],  "Belgique":       [4.5, 50.5],
    "Allemagne":          [10,   51],  "France":         [2,    47],
    "Royaume-Uni":        [-2,   54],  "Italie":         [12,   43],
    "Espagne":            [-4,   40],  "Thaïlande":      [101,  15],
    "Vietnam":            [106,  16],  "Malaisie":       [110,   3],
    "États-Unis":         [-100, 38],
    # Additions spécifiques tech
    "Taïwan":             [121,  24],
    "Singapour":          [104,   1],
    "Suisse":             [8,    47],
}

EXPORTERS = {
    "electronics": ["156","410","158","392","528","276","840","702","458"],
    #                CHN  KOR  TWN  JPN  NLD  DEU  USA  SGP  MYS
    "machinery":   ["276","840","392","156","410","392","380","756"],
    #                DEU  USA  JPN  CHN  KOR  JPN  ITA  CHE
}

HS_CODES = {
    "electronics": "8542",  # circuits intégrés / semiconducteurs
    "machinery":   "8458,8462,8466",  # tours + presses + parties machines-outils
}

TYPE_COLORS = {
    "electronics": "#818cf8",  # indigo
    "machinery":   "#a78bfa",  # violet
}

UNITS = {
    "electronics": "Md$",
    "machinery":   "Md$",
}

THRESHOLD = 500_000_000    # 500 M USD
DIVISOR   = 1_000_000_000  # → milliards USD


def load_existing():
    """Charge tech_flows.json existant.
    Retourne :
      agg   : {(from, to, type): {year_int: val}}
      meta  : {(from, to, type): {fromC, toC, unit, color}}
      done  : set de (from_name, tech_type, year_int) déjà tentés (avec ou sans résultat)
    """
    try:
        with open("data/tech_flows.json", encoding="utf-8") as f:
            d = json.load(f)
        agg = {}
        meta = {}
        for fl in d.get("flows", []):
            key = (fl["from"], fl["to"], fl["type"])
            agg[key] = {int(y): v for y, v in fl.get("hist", {}).items()}
            meta[key] = {"fromC": fl["fromC"], "toC": fl["toC"],
                         "unit": fl["unit"], "color": fl.get("color", "")}
        done = set()
        for entry in d.get("attempted", []):
            done.add((entry[0], entry[1], int(entry[2])))
        for (frm, to, typ), hist in agg.items():
            for yr in hist:
                done.add((frm, typ, yr))
        total = sum(len(v) for v in agg.values())
        print(f"Existant : {len(agg)} paires, {total} points, {len(done)} combinaisons déjà tentées")
        return agg, meta, done
    except FileNotFoundError:
        print("Pas de tech_flows.json existant — fetch complet")
        return {}, {}, set()
    except Exception as e:
        print(f"Erreur lecture tech_flows.json : {e} — fetch complet")
        return {}, {}, set()


def fetch_one(reporter_code, cmd_code, api_key, year, max_retries=3):
    """Fetch avec retry exponentiel sur 429."""
    url = (
        f"https://comtradeapi.un.org/data/v1/get/C/A/HS"
        f"?reporterCode={reporter_code}&cmdCode={cmd_code}"
        f"&flowCode=X&period={year}&subscription-key={api_key}"
    )
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode()).get("data", [])
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 60 * (attempt + 1)
                print(f"    429 — attente {wait}s (tentative {attempt+1}/{max_retries})...")
                time.sleep(wait)
            elif e.code == 403:
                print(f"    403 Quota dépassé — arrêt du script")
                raise
            else:
                print(f"    HTTP {e.code}: {e}")
                return []
        except Exception as e:
            print(f"    Erreur: {e}")
            return []
    print("    Échec après 3 tentatives — point ignoré")
    return []


def build_flows(api_key, existing_agg, existing_meta, done):
    agg      = defaultdict(dict, {k: dict(v) for k, v in existing_agg.items()})
    meta     = dict(existing_meta)
    new_done = set(done)

    # Calcul des combinaisons manquantes
    todo = []
    for tech_type, reporters in EXPORTERS.items():
        seen_reporters = set()
        for rep_code in reporters:
            if rep_code in seen_reporters:
                continue
            seen_reporters.add(rep_code)
            from_name = M49_TO_FR.get(rep_code)
            if not from_name or from_name not in COORDS:
                continue
            for year in YEARS:
                if (from_name, tech_type, year) not in done:
                    todo.append((tech_type, rep_code, from_name, year))

    total = len(todo)
    print(f"\n{total} combinaisons manquantes à fetcher\n")

    for i, (tech_type, rep_code, from_name, year) in enumerate(todo, 1):
        cmd_code = HS_CODES[tech_type]

        print(f"  [{i}/{total}] {tech_type} {from_name} {year}...", end=" ", flush=True)
        time.sleep(1.2)
        try:
            records = fetch_one(rep_code, cmd_code, api_key, year)
        except urllib.error.HTTPError:
            print("Quota dépassé, sauvegarde de l'état actuel...")
            break
        print(f"{len(records)} partenaires")
        new_done.add((from_name, tech_type, year))

        for rec in records:
            partner = str(rec.get("partnerCode", ""))
            primary_value = rec.get("primaryValue") or 0
            try:
                raw_val = float(primary_value)
            except (TypeError, ValueError):
                continue
            if raw_val < THRESHOLD:
                continue
            to_name = M49_TO_FR.get(partner)
            if not to_name or to_name not in COORDS or to_name == from_name:
                continue
            val = round(raw_val / DIVISOR, 1)
            if val <= 0:
                continue
            key = (from_name, to_name, tech_type)
            agg[key][year] = val
            if key not in meta:
                meta[key] = {
                    "fromC":  COORDS[from_name],
                    "toC":    COORDS[to_name],
                    "unit":   UNITS[tech_type],
                    "color":  TYPE_COLORS[tech_type],
                }

    # Convertir en liste de flows
    flows = []
    for (from_name, to_name, tech_type), hist in agg.items():
        if not hist:
            continue
        m = meta.get((from_name, to_name, tech_type), {})
        if not m:
            continue
        flows.append({
            "from":  from_name,
            "fromC": m["fromC"],
            "to":    to_name,
            "toC":   m["toC"],
            "type":  tech_type,
            "unit":  m["unit"],
            "color": m["color"],
            "hist":  {str(y): v for y, v in sorted(hist.items())},
        })

    return flows, new_done


def main():
    api_key = os.environ.get("COMTRADE_KEY", "")
    if not api_key:
        print("Pas de COMTRADE_KEY — skip fetch_tech_flows.")
        return

    existing_agg, existing_meta, done = load_existing()
    flows, new_done = build_flows(api_key, existing_agg, existing_meta, done)

    if not flows:
        print("Aucune donnée.")
        return

    os.makedirs("data", exist_ok=True)
    out = {
        "updated":   datetime.now().strftime("%Y-%m-%d"),
        "years":     [YEARS[0], YEARS[-1]],
        "source":    "UN Comtrade API v1",
        "url":       "https://comtradeapi.un.org",
        "flows":     flows,
        "attempted": [[f, t, y] for f, t, y in sorted(new_done)],
    }
    with open("data/tech_flows.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    total_points = sum(len(fl["hist"]) for fl in flows)
    size_kb = os.path.getsize("data/tech_flows.json") // 1024
    print(f"\nSauvegardé {len(flows)} flux, {total_points} points dans data/tech_flows.json ({size_kb} KB)")


if __name__ == "__main__":
    main()
