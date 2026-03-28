
"""
Fetches cereal trade flows from UN Comtrade API v1
Runs weekly via GitHub Actions
"""

import json
import urllib.request
import os
import time
from datetime import datetime

M49_TO_FR = {
    "4": "Afghanistan", "12": "Algérie", "32": "Argentine",
    "36": "Australie", "50": "Bangladesh", "76": "Brésil",
    "124": "Canada", "156": "Chine", "170": "Colombie",
    "818": "Égypte", "231": "Éthiopie", "250": "France",
    "276": "Allemagne", "356": "Inde", "360": "Indonésie",
    "364": "Iran", "368": "Irak", "376": "Israël",
    "392": "Japon", "398": "Kazakhstan", "404": "Kenya",
    "410": "Corée du Sud", "434": "Libye", "458": "Malaisie",
    "484": "Mexique", "504": "Maroc", "104": "Myanmar",
    "528": "Pays-Bas", "566": "Nigeria", "586": "Pakistan",
    "608": "Philippines", "616": "Pologne", "634": "Qatar",
    "643": "Russie", "682": "Arabie Saoudite", "710": "Afrique du Sud",
    "724": "Espagne", "729": "Soudan", "764": "Thaïlande",
    "792": "Turquie", "804": "Ukraine", "784": "Émirats Arabes Unis",
    "826": "Royaume-Uni", "840": "États-Unis", "704": "Vietnam",
    "887": "Yémen", "600": "Paraguay",
}

COORDS = {
    "Russie": [60, 60], "États-Unis": [-100, 38], "France": [2, 47],
    "Australie": [134, -25], "Canada": [-96, 56], "Ukraine": [32, 49],
    "Argentine": [-64, -34], "Kazakhstan": [67, 48], "Inde": [78, 20],
    "Brésil": [-55, -10], "Chine": [104, 35], "Égypte": [30, 27],
    "Turquie": [35, 39], "Nigeria": [8, 10], "Indonésie": [117, -2],
    "Philippines": [122, 13], "Japon": [138, 36], "Corée du Sud": [127, 36],
    "Bangladesh": [90, 24], "Algérie": [3, 28], "Maroc": [-7, 32],
    "Mexique": [-102, 23], "Vietnam": [106, 16], "Thaïlande": [101, 15],
    "Pakistan": [70, 30], "Iran": [53, 33], "Arabie Saoudite": [45, 24],
    "Irak": [44, 33], "Allemagne": [10, 51], "Pologne": [20, 52],
    "Royaume-Uni": [-2, 54], "Colombie": [-74, 4], "Kenya": [37, -1],
    "Soudan": [31, 16], "Yémen": [48, 16], "Malaisie": [110, 3],
    "Émirats Arabes Unis": [54, 24], "Qatar": [51, 25],
    "Israël": [35, 31], "Paraguay": [-58, -23],
}

# Top exporters per commodity (M49 codes)
EXPORTERS = {
    "wheat": ["643","840","124","36","804","250","32","398"],   # RUS,USA,CAN,AUS,UKR,FRA,ARG,KAZ
    "corn":  ["840","76","32","804","710"],                     # USA,BRA,ARG,UKR,ZAF
    "rice":  ["356","764","704","586","840"],                   # IND,THA,VNM,PAK,USA
    "soy":   ["76","840","32","600"],                          # BRA,USA,ARG,PRY
}

TYPE_COLORS = {
    "wheat": "#f59e0b", "corn": "#eab308",
    "rice": "#22c55e", "soy": "#84cc16",
}

HS_CODES = {"wheat": "1001", "corn": "1005", "rice": "1006", "soy": "1201"}

def fetch_one(reporter_code, cmd_code, api_key, year):
    url = (
        f"https://comtradeapi.un.org/data/v1/get/C/A/HS"
        f"?reporterCode={reporter_code}"
        f"&cmdCode={cmd_code}"
        f"&flowCode=X"
        f"&period={year}"
        f"&subscription-key={api_key}"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("data", [])
    except Exception as e:
        print(f"    Error: {e}")
        return []

def load_existing():
    """Charge cereals.json existant → {(from,to,type): hist_dict}"""
    try:
        with open("data/cereals.json", encoding="utf-8") as f:
            d = json.load(f)
        agg, meta = {}, {}
        for fl in d.get("flows", []):
            key = (fl["from"], fl["to"], fl["type"])
            agg[key] = {int(y): v for y, v in fl.get("hist", {}).items()}
            meta[key] = {"fromC": fl["fromC"], "toC": fl["toC"], "color": fl.get("color", "")}
        print(f"Existant : {len(agg)} paires")
        return agg, meta
    except FileNotFoundError:
        return {}, {}
    except Exception as e:
        print(f"Erreur lecture : {e}")
        return {}, {}


def build_flows(api_key, year, existing_agg, existing_meta):
    from collections import defaultdict
    agg  = defaultdict(dict, {k: dict(v) for k, v in existing_agg.items()})
    meta = dict(existing_meta)

    for cereal_type, reporters in EXPORTERS.items():
        cmd_code = HS_CODES[cereal_type]
        print(f"Fetching {cereal_type} (HS {cmd_code}) année {year}...")
        for rep_code in reporters:
            from_name = M49_TO_FR.get(rep_code)
            if not from_name or from_name not in COORDS:
                continue
            time.sleep(1.5)
            records = fetch_one(rep_code, cmd_code, api_key, year)
            print(f"  {from_name}: {len(records)} partners")
            for rec in records:
                partner = str(rec.get("partnerCode", ""))
                net_wgt = rec.get("netWgt") or 0
                try:
                    val_mt = float(net_wgt) / 1_000_000
                except:
                    continue
                if val_mt < 0.3:
                    continue
                to_name = M49_TO_FR.get(partner)
                if not to_name or to_name not in COORDS or to_name == from_name:
                    continue
                key = (from_name, to_name, cereal_type)
                agg[key][year] = round(val_mt, 1)
                if key not in meta:
                    meta[key] = {"fromC": COORDS[from_name], "toC": COORDS[to_name],
                                 "color": TYPE_COLORS[cereal_type]}

    flows = []
    for (frm, to, typ), hist in agg.items():
        if not hist:
            continue
        m = meta.get((frm, to, typ), {})
        if not m:
            continue
        flows.append({
            "from":  frm, "fromC": m["fromC"],
            "to":    to,  "toC":   m["toC"],
            "type":  typ, "color": m["color"],
            "hist":  {str(y): v for y, v in sorted(hist.items())},
        })
    return flows


def main():
    api_key = os.environ.get("COMTRADE_KEY", "")
    if not api_key:
        print("No COMTRADE_KEY env var set, skipping.")
        return

    year = datetime.now().year - 2
    print(f"Fetching cereal data from UN Comtrade (year {year})...")
    existing_agg, existing_meta = load_existing()
    flows = build_flows(api_key, year, existing_agg, existing_meta)

    if not flows:
        print("No data fetched, keeping existing data.")
        return

    os.makedirs("data", exist_ok=True)
    out = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "source": "UN Comtrade API v1 — mise à jour automatique chaque dimanche",
        "flows": flows,
    }
    with open("data/cereals.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Saved {len(flows)} flows to data/cereals.json")

if __name__ == "__main__":
    main()
