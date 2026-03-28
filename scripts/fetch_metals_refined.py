"""
Télécharge les flux de métaux RAFFINÉS depuis l'API UN Comtrade v1.
Complète data/metals.json (même fichier que fetch_metals.py).

Types couverts :
  7403 — Cuivre raffiné   (copper_ref)
  7208 — Acier laminé     (steel)
  7601 — Aluminium        (aluminum)
  7502 — Nickel raffiné   (nickel_ref)

Coût API : ~243 appels max (27 exporteurs × 9 ans), décroissant grâce au gap-filling.
"""
import json, os, time, urllib.request, urllib.error
from datetime import datetime
from collections import defaultdict

YEARS = list(range(2015, 2024))

M49_TO_FR = {
    "156": "Chine",           "276": "Allemagne",
    "392": "Japon",           "152": "Chili",
    "410": "Corée du Sud",    "643": "Russie",
    "616": "Pologne",         "124": "Canada",
    "578": "Norvège",         "784": "Émirats Arabes Unis",
    "356": "Inde",            "792": "Turquie",
    "804": "Ukraine",         "36":  "Australie",
    "246": "Finlande",        "76":  "Brésil",
    # Importateurs
    "840": "États-Unis",      "528": "Pays-Bas",
    "826": "Royaume-Uni",     "380": "Italie",
    "724": "Espagne",         "250": "France",
    "56":  "Belgique",        "764": "Thaïlande",
    "704": "Vietnam",         "458": "Malaisie",
    "360": "Indonésie",       "608": "Philippines",
    "710": "Afrique du Sud",
}

COORDS = {
    "Chine":              [104,  35],  "Allemagne":          [10,   51],
    "Japon":              [138,  37],  "Chili":              [-71, -35],
    "Corée du Sud":       [127,  37],  "Russie":             [60,   58],
    "Pologne":            [20,   52],  "Canada":             [-96,  56],
    "Norvège":            [10,   62],  "Émirats Arabes Unis":[54,   24],
    "Inde":               [78,   22],  "Turquie":            [35,   39],
    "Ukraine":            [32,   49],  "Australie":          [133, -27],
    "Finlande":           [26,   62],  "Brésil":             [-55, -10],
    "États-Unis":         [-100, 38],  "Pays-Bas":           [5,    52],
    "Royaume-Uni":        [-2,   54],  "Italie":             [12,   43],
    "Espagne":            [-4,   40],  "France":             [2,    47],
    "Belgique":           [4.5, 50.5], "Thaïlande":          [101,  15],
    "Vietnam":            [106,  16],  "Malaisie":           [110,   3],
    "Indonésie":          [117,  -2],  "Philippines":        [122,  13],
    "Afrique du Sud":     [25,  -29],
}

EXPORTERS = {
    "copper_ref": ["156","276","392","152","410","643","616"],
    #               CHN  DEU  JPN  CHL  KOR  RUS  POL
    "steel":      ["156","392","410","276","643","804","356","792","76"],
    #               CHN  JPN  KOR  DEU  RUS  UKR  IND  TUR  BRA
    "aluminum":   ["156","643","124","578","784","36"],
    #               CHN  RUS  CAN  NOR  UAE  AUS
    "nickel_ref": ["643","124","578","246","36"],
    #               RUS  CAN  NOR  FIN  AUS
}

HS_CODES    = {"copper_ref":"7403","steel":"7208","aluminum":"7601","nickel_ref":"7502"}
TYPE_COLORS = {"copper_ref":"#dc2626","steel":"#6b7280","aluminum":"#93c5fd","nickel_ref":"#334155"}
UNITS       = {"copper_ref":"kt","steel":"Mt","aluminum":"kt","nickel_ref":"kt"}
THRESHOLDS  = {"copper_ref":50_000_000,"steel":1_000_000_000,"aluminum":100_000_000,"nickel_ref":5_000_000}
DIVISORS    = {"copper_ref":1_000_000,"steel":1_000_000_000,"aluminum":1_000_000,"nickel_ref":1_000_000}


def load_existing():
    try:
        with open("data/metals.json", encoding="utf-8") as f:
            d = json.load(f)
        agg, meta = {}, {}
        for fl in d.get("flows", []):
            key = (fl["from"], fl["to"], fl["type"])
            agg[key]  = {int(y): v for y, v in fl.get("hist", {}).items()}
            meta[key] = {"fromC": fl["fromC"], "toC": fl["toC"],
                         "unit": fl["unit"], "color": fl.get("color", "")}
        done = set()
        for e in d.get("attempted", []):
            done.add((e[0], e[1], int(e[2])))
        for (frm, to, typ), hist in agg.items():
            for yr in hist:
                done.add((frm, typ, yr))
        print(f"Existant : {len(agg)} paires, {len(done)} combinaisons déjà tentées")
        return agg, meta, done, d
    except FileNotFoundError:
        return {}, {}, set(), {}
    except Exception as e:
        print(f"Erreur lecture : {e}")
        return {}, {}, set(), {}


def fetch_one(reporter_code, cmd_code, api_key, year, max_retries=3):
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
                print(f"    429 — attente {wait}s...")
                time.sleep(wait)
            elif e.code == 403:
                print(f"    403 Quota dépassé — arrêt du script")
                raise
            else:
                print(f"    HTTP {e.code}")
                return []
        except Exception as e:
            print(f"    Erreur: {e}")
            return []
    return []


def build_flows(api_key, existing_agg, existing_meta, done):
    agg      = defaultdict(dict, {k: dict(v) for k, v in existing_agg.items()})
    meta     = dict(existing_meta)
    new_done = set(done)

    todo = [
        (metal_type, rep_code, M49_TO_FR[rep_code], year)
        for metal_type, reporters in EXPORTERS.items()
        for rep_code in reporters
        if M49_TO_FR.get(rep_code) and M49_TO_FR[rep_code] in COORDS
        for year in YEARS
        if (M49_TO_FR[rep_code], metal_type, year) not in done
    ]

    print(f"{len(todo)} combinaisons manquantes à fetcher\n")

    for i, (metal_type, rep_code, from_name, year) in enumerate(todo, 1):
        cmd_code  = HS_CODES[metal_type]
        threshold = THRESHOLDS[metal_type]
        divisor   = DIVISORS[metal_type]

        print(f"  [{i}/{len(todo)}] {metal_type} {from_name} {year}...", end=" ", flush=True)
        time.sleep(1.2)

        try:
            records = fetch_one(rep_code, cmd_code, api_key, year)
        except urllib.error.HTTPError:
            print("Quota dépassé, sauvegarde de l'état actuel...")
            break

        print(f"{len(records)} partenaires")
        new_done.add((from_name, metal_type, year))

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
                meta[key] = {"fromC": COORDS[from_name], "toC": COORDS[to_name],
                             "unit": UNITS[metal_type], "color": TYPE_COLORS[metal_type]}

    flows = [
        {"from": frm, "fromC": m["fromC"], "to": to, "toC": m["toC"],
         "type": typ, "unit": m["unit"], "color": m["color"],
         "hist": {str(y): v for y, v in sorted(hist.items())}}
        for (frm, to, typ), hist in agg.items()
        if hist and (m := meta.get((frm, to, typ)))
    ]
    return flows, new_done


def main():
    api_key = os.environ.get("COMTRADE_KEY", "")
    if not api_key:
        print("Pas de COMTRADE_KEY — skip.")
        return

    existing_agg, existing_meta, done, existing_json = load_existing()
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
    with open("data/metals.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    total_pts = sum(len(fl["hist"]) for fl in flows)
    size_kb   = os.path.getsize("data/metals.json") // 1024
    print(f"\nSauvegardé {len(flows)} flux, {total_pts} points ({size_kb} KB)")


if __name__ == "__main__":
    main()
