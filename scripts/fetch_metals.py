"""
Télécharge les flux commerciaux de métaux critiques depuis l'API UN Comtrade v1.
Génère data/metals.json avec séries historiques 2015–2023 par paire pays.

Fonctionnement :
  - Charge metals.json existant au démarrage
  - Ne fetche QUE les combinaisons (exporteur, métal, année) manquantes
  - Retry automatique sur 429 (attente exponentielle : 60s, 120s, 180s)

Métaux couverts (codes HS chapitre 26) :
  2601 — Minerai de fer   (iron_ore)
  2603 — Cuivre           (copper)
  2604 — Nickel           (nickel)
  2605 — Cobalt           (cobalt)
  2530 — Lithium/spodumène(lithium)

Source : https://comtradeapi.un.org  (nécessite COMTRADE_KEY)
"""
import json, os, time, urllib.request, urllib.error
from datetime import datetime
from collections import defaultdict

YEARS = list(range(2015, 2024))   # 2015 → 2023

M49_TO_FR = {
    # Exportateurs minerais
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
    # Exportateurs raffinés supplémentaires
    "578": "Norvège",        "784": "Émirats Arabes Unis",
    "792": "Turquie",
    # Importateurs / destinations
    "156": "Chine",          "392": "Japon",
    "410": "Corée du Sud",   "528": "Pays-Bas",
    "246": "Finlande",       "56":  "Belgique",
    "276": "Allemagne",      "250": "France",
    "826": "Royaume-Uni",    "380": "Italie",
    "724": "Espagne",        "764": "Thaïlande",
    "704": "Vietnam",        "458": "Malaisie",
    "840": "États-Unis",
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
}

EXPORTERS = {
    # ── Minerais bruts ──────────────────────────────────────────
    "iron_ore":   ["36","76","710","356","643","804","124"],
    #               AUS  BRA  ZAF  IND  RUS  UKR  CAN
    "copper":     ["152","604","180","36","894","643","484","616","398"],
    #               CHL  PER  COD  AUS  ZMB  RUS  MEX  POL  KAZ
    "nickel":     ["360","608","643","124","36","598"],
    #               IDN  PHL  RUS  CAN  AUS  PNG
    "cobalt":     ["180","643","36","608","124"],
    #               COD  RUS  AUS  PHL  CAN
    "lithium":    ["36","152","32","716"],
    #               AUS  CHL  ARG  ZWE
    # ── Métaux raffinés ─────────────────────────────────────────
    "copper_ref": ["156","276","392","152","410","643","616"],
    #               CHN  DEU  JPN  CHL  KOR  RUS  POL
    "steel":      ["156","392","410","276","643","804","356","792"],
    #               CHN  JPN  KOR  DEU  RUS  UKR  IND  TUR
    "aluminum":   ["156","643","124","578","784","36"],
    #               CHN  RUS  CAN  NOR  UAE  AUS
    "nickel_ref": ["643","124","578","246","36"],
    #               RUS  CAN  NOR  FIN  AUS
}

HS_CODES = {
    "iron_ore":   "2601",
    "copper":     "2603",
    "nickel":     "2604",
    "cobalt":     "2605",
    "lithium":    "2530",
    "copper_ref": "7403",   # cuivre affiné non allié
    "steel":      "7208",   # produits laminés plats fer/acier
    "aluminum":   "7601",   # aluminium non allié
    "nickel_ref": "7502",   # nickel non allié
}
TYPE_COLORS = {
    "iron_ore":   "#b45309",
    "copper":     "#ea580c",
    "nickel":     "#64748b",
    "cobalt":     "#3b82f6",
    "lithium":    "#0ea5e9",
    "copper_ref": "#dc2626",   # rouge — distingue du minerai
    "steel":      "#6b7280",   # gris acier
    "aluminum":   "#93c5fd",   # bleu pâle / argent
    "nickel_ref": "#334155",   # gris foncé
}
UNITS = {
    "iron_ore":   "Mt",
    "copper":     "kt",
    "nickel":     "kt",
    "cobalt":     "kt",
    "lithium":    "kt",
    "copper_ref": "kt",
    "steel":      "Mt",
    "aluminum":   "kt",
    "nickel_ref": "kt",
}
THRESHOLDS = {
    "iron_ore":   5_000_000_000,
    "copper":     50_000_000,
    "nickel":     5_000_000,
    "cobalt":     500_000,
    "lithium":    500_000,
    "copper_ref": 50_000_000,    # 50 kt
    "steel":      1_000_000_000, # 1 Mt
    "aluminum":   100_000_000,   # 100 kt
    "nickel_ref": 5_000_000,     # 5 kt
}
DIVISORS = {
    "iron_ore":   1_000_000_000,
    "copper":     1_000_000,
    "nickel":     1_000_000,
    "cobalt":     1_000_000,
    "lithium":    1_000_000,
    "copper_ref": 1_000_000,
    "steel":      1_000_000_000,
    "aluminum":   1_000_000,
    "nickel_ref": 1_000_000,
}


def load_existing():
    """Charge metals.json existant.
    Retourne :
      agg   : {(from, to, type): {year_int: val}}
      meta  : {(from, to, type): {fromC, toC, unit, color}}
      done  : set de (from_name, metal_type, year_int) déjà tentés (avec ou sans résultat)
    """
    try:
        with open("data/metals.json", encoding="utf-8") as f:
            d = json.load(f)
        agg = {}
        meta = {}
        for fl in d.get("flows", []):
            key = (fl["from"], fl["to"], fl["type"])
            agg[key] = {int(y): v for y, v in fl.get("hist", {}).items()}
            meta[key] = {"fromC": fl["fromC"], "toC": fl["toC"],
                         "unit": fl["unit"], "color": fl.get("color", "")}
        # Combinaisons déjà tentées (stockées explicitement pour éviter les re-fetch inutiles)
        done = set()
        for entry in d.get("attempted", []):
            done.add((entry[0], entry[1], int(entry[2])))
        # Toute paire avec données = aussi "tentée"
        for (frm, to, typ), hist in agg.items():
            for yr in hist:
                done.add((frm, typ, yr))
        total = sum(len(v) for v in agg.values())
        print(f"Existant : {len(agg)} paires, {total} points, {len(done)} combinaisons déjà tentées")
        return agg, meta, done
    except FileNotFoundError:
        print("Pas de metals.json existant — fetch complet")
        return {}, {}, set()
    except Exception as e:
        print(f"Erreur lecture metals.json : {e} — fetch complet")
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
    new_done = set(done)   # sera enrichi au fil du fetch

    # Calcul des combinaisons manquantes
    todo = []
    for metal_type, reporters in EXPORTERS.items():
        for rep_code in reporters:
            from_name = M49_TO_FR.get(rep_code)
            if not from_name or from_name not in COORDS:
                continue
            for year in YEARS:
                if (from_name, metal_type, year) not in done:
                    todo.append((metal_type, rep_code, from_name, year))

    total = len(todo)
    print(f"\n{total} combinaisons manquantes à fetcher\n")

    for i, (metal_type, rep_code, from_name, year) in enumerate(todo, 1):
        cmd_code  = HS_CODES[metal_type]
        threshold = THRESHOLDS[metal_type]
        divisor   = DIVISORS[metal_type]

        print(f"  [{i}/{total}] {metal_type} {from_name} {year}...", end=" ", flush=True)
        time.sleep(1.2)
        records = fetch_one(rep_code, cmd_code, api_key, year)
        print(f"{len(records)} partenaires")
        new_done.add((from_name, metal_type, year))   # marque comme tenté même si 0 résultats

        for rec in records:
            partner = str(rec.get("partnerCode", ""))
            net_wgt = rec.get("netWgt") or 0
            try:
                raw_val = float(net_wgt)
            except (TypeError, ValueError):
                continue
            if raw_val < threshold:
                continue
            to_name = M49_TO_FR.get(partner)
            if not to_name or to_name not in COORDS or to_name == from_name:
                continue
            val = round(raw_val / divisor, 1)
            if val <= 0:
                continue
            key = (from_name, to_name, metal_type)
            agg[key][year] = val
            if key not in meta:
                meta[key] = {
                    "fromC":  COORDS[from_name],
                    "toC":    COORDS[to_name],
                    "unit":   UNITS[metal_type],
                    "color":  TYPE_COLORS[metal_type],
                }

    # Convertir en liste de flows
    flows = []
    for (from_name, to_name, metal_type), hist in agg.items():
        if not hist:
            continue
        m = meta.get((from_name, to_name, metal_type), {})
        if not m:
            continue
        flows.append({
            "from":  from_name,
            "fromC": m["fromC"],
            "to":    to_name,
            "toC":   m["toC"],
            "type":  metal_type,
            "unit":  m["unit"],
            "color": m["color"],
            "hist":  {str(y): v for y, v in sorted(hist.items())},
        })

    return flows, new_done


def main():
    api_key = os.environ.get("COMTRADE_KEY", "")
    if not api_key:
        print("Pas de COMTRADE_KEY — skip fetch_metals.")
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
        # Combinaisons tentées (avec ou sans résultat) — évite les re-fetch inutiles
        "attempted": [[f, t, y] for f, t, y in sorted(new_done)],
    }
    with open("data/metals.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    total_points = sum(len(fl["hist"]) for fl in flows)
    size_kb = os.path.getsize("data/metals.json") // 1024
    print(f"\nSauvegardé {len(flows)} flux, {total_points} points dans data/metals.json ({size_kb} KB)")


if __name__ == "__main__":
    main()
