
"""
Fetches cereal trade flows from FAOSTAT API and saves to data/cereals.json
Runs weekly via GitHub Actions
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime
import os

# FAO country code → French name mapping
FAO_TO_FR = {
    "2": "Afghanistan", "4": "Albanie", "8": "Algérie", "12": "Angola",
    "32": "Argentine", "36": "Australie", "40": "Autriche", "50": "Bangladesh",
    "56": "Belgique", "76": "Brésil", "100": "Bulgarie", "116": "Cambodge",
    "124": "Canada", "152": "Chili", "156": "Chine", "170": "Colombie",
    "384": "Côte d'Ivoire", "191": "Croatie", "208": "Danemark",
    "818": "Égypte", "724": "Espagne", "231": "Éthiopie",
    "246": "Finlande", "250": "France", "276": "Allemagne", "288": "Ghana",
    "300": "Grèce", "348": "Hongrie", "356": "Inde", "360": "Indonésie",
    "364": "Iran", "368": "Irak", "372": "Irlande", "376": "Israël",
    "380": "Italie", "392": "Japon", "400": "Jordanie", "398": "Kazakhstan",
    "404": "Kenya", "410": "Corée du Sud", "414": "Koweït", "418": "Laos",
    "422": "Liban", "434": "Libye", "458": "Malaisie", "484": "Mexique",
    "504": "Maroc", "508": "Mozambique", "104": "Myanmar", "524": "Népal",
    "528": "Pays-Bas", "554": "Nouvelle-Zélande", "558": "Nicaragua",
    "566": "Nigeria", "578": "Norvège", "586": "Pakistan", "591": "Panama",
    "604": "Pérou", "608": "Philippines", "616": "Pologne", "620": "Portugal",
    "634": "Qatar", "642": "Roumanie", "643": "Russie", "682": "Arabie Saoudite",
    "686": "Sénégal", "694": "Sierra Leone", "703": "Slovaquie",
    "706": "Somalie", "710": "Afrique du Sud", "724": "Espagne",
    "729": "Soudan", "752": "Suède", "756": "Suisse", "760": "Syrie",
    "158": "Taïwan", "764": "Thaïlande", "768": "Togo", "788": "Tunisie",
    "792": "Turquie", "800": "Ouganda", "804": "Ukraine",
    "784": "Émirats Arabes Unis", "826": "Royaume-Uni",
    "840": "États-Unis", "858": "Uruguay", "862": "Venezuela",
    "704": "Vietnam", "887": "Yémen", "894": "Zambie",
    "716": "Zimbabwe", "218": "Équateur", "320": "Guatemala",
    "340": "Honduras", "388": "Jamaïque", "434": "Libye",
    "466": "Mali", "478": "Mauritanie", "598": "Papouasie-Nouvelle-Guinée",
    "740": "Suriname", "144": "Sri Lanka", "646": "Rwanda",
    "204": "Bénin", "854": "Burkina Faso", "226": "Guinée équatoriale",
}

# FAO coordinates (lon, lat) for each country
COORDS = {
    "Russie": [60, 60], "États-Unis": [-100, 38], "France": [2, 47],
    "Australie": [134, -25], "Canada": [-96, 56], "Ukraine": [32, 49],
    "Argentine": [-64, -34], "Kazakhstan": [67, 48], "Inde": [78, 20],
    "Brésil": [-55, -10], "Paraguay": [-58, -23], "Chine": [104, 35],
    "Égypte": [30, 27], "Turquie": [35, 39], "Nigeria": [8, 10],
    "Indonésie": [117, -2], "Philippines": [122, 13], "Japon": [138, 36],
    "Corée du Sud": [127, 36], "Bangladesh": [90, 24], "Algérie": [3, 28],
    "Maroc": [-7, 32], "Mexique": [-102, 23], "Vietnam": [106, 16],
    "Thaïlande": [101, 15], "Pakistan": [70, 30], "Iran": [53, 33],
    "Arabie Saoudite": [45, 24], "Irak": [44, 33], "Allemagne": [10, 51],
    "Pologne": [20, 52], "Royaume-Uni": [-2, 54], "Italie": [12, 43],
    "Espagne": [-4, 40], "Pays-Bas": [5, 52], "Belgique": [4, 51],
    "Colombie": [-74, 4], "Pérou": [-76, -10], "Kenya": [37, -1],
    "Éthiopie": [40, 9], "Soudan": [31, 16], "Yémen": [48, 16],
    "Malaisie": [110, 3], "Afrique du Sud": [25, -30],
    "Émirats Arabes Unis": [54, 24], "Qatar": [51, 25],
    "Koweït": [47, 29], "Israël": [35, 31], "Jordanie": [36, 31],
    "Syrie": [38, 35], "Tunisie": [9, 34], "Libye": [17, 27],
    "Ghana": [-1, 8], "Sénégal": [-14, 14], "Côte d'Ivoire": [-6, 7],
    "Uruguay": [-56, -33], "Nouvelle-Zélande": [170, -42],
    "Bénin": [2, 9], "Myanmar": [96, 17], "Sri Lanka": [81, 8],
}

# Commodity codes in FAOSTAT
ITEMS = {
    "wheat": "23",    # Wheat and meslin
    "corn": "56",     # Maize (corn)
    "rice": "27",     # Rice
    "soy": "236",     # Soya beans
}

TYPE_COLORS = {
    "wheat": "#f59e0b",
    "corn": "#eab308",
    "rice": "#22c55e",
    "soy": "#84cc16",
}

def fetch_fao_trade(item_code, year=2022, min_quantity=500):
    """Fetch bilateral trade data from FAOSTAT for a given commodity"""
    url = (
        f"https://fenixservices.fao.org/faostat/api/v1/en/data/TCL"
        f"?item_code={item_code}"
        f"&element_code=5910"  # Export Quantity (tonnes)
        f"&year={year}"
        f"&output_type=json"
        f"&limit=500"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("data", [])
    except Exception as e:
        print(f"Error fetching FAO data for item {item_code}: {e}")
        return []

def build_flows_from_fao(year=2022):
    flows = []
    for cereal_type, item_code in ITEMS.items():
        print(f"Fetching {cereal_type} (item {item_code})...")
        records = fetch_fao_trade(item_code, year)
        # Aggregate by reporter (exporter)
        agg = {}
        for rec in records:
            reporter = rec.get("reporter_country_code")
            partner = rec.get("partner_country_code")
            value_str = rec.get("value", "0")
            try:
                value = float(value_str) / 1000  # Convert tonnes → kt → Mt
            except:
                continue
            if value < 0.3:  # Min 300k tonnes
                continue
            reporter_name = FAO_TO_FR.get(str(reporter))
            partner_name = FAO_TO_FR.get(str(partner))
            if not reporter_name or not partner_name:
                continue
            if reporter_name not in COORDS or partner_name not in COORDS:
                continue
            flows.append({
                "from": reporter_name,
                "fromC": COORDS[reporter_name],
                "to": partner_name,
                "toC": COORDS[partner_name],
                "type": cereal_type,
                "value": round(value, 1),
                "year": year,
                "color": TYPE_COLORS[cereal_type],
            })
    return flows

def main():
    print("Fetching cereal trade data from FAOSTAT...")
    year = datetime.now().year - 2  # FAO data has ~2 year lag
    flows = build_flows_from_fao(year)

    if not flows:
        print("No data fetched, keeping existing data.")
        return

    output = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "year": year,
        "source": "FAOSTAT — FAO Trade Crops and Livestock (TCL)",
        "flows": flows,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/cereals.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(flows)} flows to data/cereals.json")

if __name__ == "__main__":
    main()
