
"""
Fetches cereal trade flows from UN Comtrade API v1
Runs weekly via GitHub Actions
"""

import json
import urllib.request
import os
from datetime import datetime

# UN Comtrade M49 code → French name
M49_TO_FR = {
    "4": "Afghanistan", "12": "Algérie", "32": "Argentine",
    "36": "Australie", "50": "Bangladesh", "76": "Brésil",
    "100": "Bulgarie", "124": "Canada", "152": "Chili",
    "156": "Chine", "170": "Colombie", "384": "Côte d'Ivoire",
    "208": "Danemark", "818": "Égypte", "231": "Éthiopie",
    "246": "Finlande", "250": "France", "276": "Allemagne",
    "288": "Ghana", "300": "Grèce", "356": "Inde",
    "360": "Indonésie", "364": "Iran", "368": "Irak",
    "376": "Israël", "380": "Italie", "392": "Japon",
    "400": "Jordanie", "398": "Kazakhstan", "404": "Kenya",
    "410": "Corée du Sud", "414": "Koweït", "434": "Libye",
    "458": "Malaisie", "484": "Mexique", "504": "Maroc",
    "508": "Mozambique", "104": "Myanmar", "528": "Pays-Bas",
    "554": "Nouvelle-Zélande", "566": "Nigeria", "578": "Norvège",
    "586": "Pakistan", "604": "Pérou", "608": "Philippines",
    "616": "Pologne", "620": "Portugal", "634": "Qatar",
    "642": "Roumanie", "643": "Russie", "682": "Arabie Saoudite",
    "686": "Sénégal", "710": "Afrique du Sud", "724": "Espagne",
    "729": "Soudan", "752": "Suède", "756": "Suisse",
    "158": "Taïwan", "764": "Thaïlande", "788": "Tunisie",
    "792": "Turquie", "804": "Ukraine", "784": "Émirats Arabes Unis",
    "826": "Royaume-Uni", "840": "États-Unis", "858": "Uruguay",
    "862": "Venezuela", "704": "Vietnam", "887": "Yémen",
    "894": "Zambie", "716": "Zimbabwe", "218": "Équateur",
    "320": "Guatemala", "204": "Bénin", "144": "Sri Lanka",
    "760": "Syrie", "800": "Ouganda",
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
    "Royaume-Uni": [-2, 54], "Italie": [12, 43], "Espagne": [-4, 40],
    "Pays-Bas": [5, 52], "Colombie": [-74, 4], "Kenya": [37, -1],
    "Éthiopie": [40, 9], "Soudan": [31, 16], "Yémen": [48, 16],
    "Malaisie": [110, 3], "Afrique du Sud": [25, -30],
    "Émirats Arabes Unis": [54, 24], "Qatar": [51, 25],
    "Israël": [35, 31], "Ghana": [-1, 8], "Sénégal": [-14, 14],
    "Nouvelle-Zélande": [170, -42], "Bénin": [2, 9],
    "Myanmar": [96, 17], "Sri Lanka": [81, 8],
}

# HS commodity codes
COMMODITIES = {
    "wheat": "1001",
    "corn":  "1005",
    "rice":  "1006",
    "soy":   "1201",
}

TYPE_COLORS = {
    "wheat": "#f59e0b",
    "corn":  "#eab308",
    "rice":  "#22c55e",
    "soy":   "#84cc16",
}

def fetch_comtrade(cmd_code, api_key, year=2022):
    """Fetch top export flows from UN Comtrade API v1"""
    url = (
        f"https://comtradeapi.un.org/data/v1/get/C/A/HS"
        f"?cmdCode={cmd_code}"
        f"&flowCode=X"
        f"&period={year}"
        f"&reporterCode=0"
        f"&partnerCode=0"
        f"&subscription-key={api_key}"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        return data.get("data", [])
    except Exception as e:
        print(f"  Error: {e}")
        return []

def build_flows(api_key, year=2022):
    flows = []
    for cereal_type, cmd_code in COMMODITIES.items():
        print(f"Fetching {cereal_type} (HS {cmd_code})...")
        records = fetch_comtrade(cmd_code, api_key, year)
        print(f"  Got {len(records)} records")
        for rec in records:
            reporter = str(rec.get("reporterCode", ""))
            partner  = str(rec.get("partnerCode", ""))
            qty_kg   = rec.get("primaryValue") or 0
            try:
                qty_mt = float(qty_kg) / 1_000_000_000  # USD → on utilise netWgt
            except:
                continue
            # Use net weight in tonnes → convert to Mt
            net_wgt = rec.get("netWgt") or 0
            try:
                val_mt = float(net_wgt) / 1_000_000
            except:
                continue
            if val_mt < 0.3:
                continue
            from_name = M49_TO_FR.get(reporter)
            to_name   = M49_TO_FR.get(partner)
            if not from_name or not to_name:
                continue
            if from_name not in COORDS or to_name not in COORDS:
                continue
            flows.append({
                "from":   from_name,
                "fromC":  COORDS[from_name],
                "to":     to_name,
                "toC":    COORDS[to_name],
                "type":   cereal_type,
                "value":  round(val_mt, 1),
                "year":   year,
                "color":  TYPE_COLORS[cereal_type],
            })
    return flows

def main():
    api_key = os.environ.get("COMTRADE_KEY", "")
    if not api_key:
        print("No COMTRADE_KEY env var set, skipping.")
        return

    year = datetime.now().year - 2  # Comtrade data has ~2yr lag
    print(f"Fetching cereal trade data from UN Comtrade (year {year})...")
    flows = build_flows(api_key, year)

    if not flows:
        print("No data fetched, keeping existing data.")
        return

    os.makedirs("data", exist_ok=True)
    out = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "year": year,
        "source": "UN Comtrade API v1 — mise à jour automatique chaque dimanche",
        "flows": flows,
    }
    with open("data/cereals.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(flows)} flows to data/cereals.json")

if __name__ == "__main__":
    main()
