#!/usr/bin/env python3
"""
Fetch cereal production by type from FAO bulk ZIP.
Produces data/cereal_by_type.json:
  {iso3: {wheat:{year:Mt}, rice:{year:Mt}, maize:{year:Mt}, barley:{year:Mt}, soy:{year:Mt}}}
Source: FAOSTAT QCL Production_Crops_Livestock_E_All_Data_(Normalized).zip
"""
import urllib.request, zipfile, io, csv, json, os, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(BASE_DIR, "data", "cereal_by_type.json")

URL = "https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip"

# FAO item codes for crops
ITEMS = {
    "15":  "wheat",
    "27":  "rice",    # paddy
    "56":  "maize",
    "44":  "barley",
    "236": "soy",
}

# Element code 5510 = Production (tonnes)
ELEMENT_PROD = "5510"

YEARS = list(range(2000, 2024))

# FAO ISO3 country codes mapping (Area Code M49 -> ISO3)
# We use the "Area Code (M49)" column and cross-reference with ISO country codes
# FAO uses its own numeric codes, not M49 consistently — we match on country name instead
# Key: FAO Area name -> ISO3
FAO_NAME_TO_ISO3 = {
    "Afghanistan": "AFG", "Albania": "ALB", "Algeria": "DZA", "Angola": "AGO",
    "Argentina": "ARG", "Armenia": "ARM", "Australia": "AUS", "Austria": "AUT",
    "Azerbaijan": "AZE", "Bangladesh": "BGD", "Belarus": "BLR", "Belgium": "BEL",
    "Belize": "BLZ", "Benin": "BEN", "Bhutan": "BTN", "Bolivia (Plurinational State of)": "BOL",
    "Bosnia and Herzegovina": "BIH", "Brazil": "BRA", "Bulgaria": "BGR",
    "Burkina Faso": "BFA", "Burundi": "BDI", "Cabo Verde": "CPV", "Cambodia": "KHM",
    "Cameroon": "CMR", "Canada": "CAN", "Central African Republic": "CAF", "Chad": "TCD",
    "Chile": "CHL", "China": "CHN", "China, mainland": "CHN",
    "Colombia": "COL", "Congo": "COG", "Costa Rica": "CRI", "Croatia": "HRV",
    "Cuba": "CUB", "Cyprus": "CYP", "Czechia": "CZE", "Czech Republic": "CZE",
    "Denmark": "DNK", "Dominican Republic": "DOM", "Ecuador": "ECU", "Egypt": "EGY",
    "El Salvador": "SLV", "Eritrea": "ERI", "Estonia": "EST", "Eswatini": "SWZ",
    "Ethiopia": "ETH", "Fiji": "FJI", "Finland": "FIN", "France": "FRA",
    "Gabon": "GAB", "Georgia": "GEO", "Germany": "DEU", "Ghana": "GHA",
    "Greece": "GRC", "Guatemala": "GTM", "Guinea": "GIN", "Guinea-Bissau": "GNB",
    "Haiti": "HTI", "Honduras": "HND", "Hungary": "HUN", "India": "IND",
    "Indonesia": "IDN", "Iran (Islamic Republic of)": "IRN", "Iraq": "IRQ",
    "Ireland": "IRL", "Israel": "ISR", "Italy": "ITA", "Japan": "JPN",
    "Jordan": "JOR", "Kazakhstan": "KAZ", "Kenya": "KEN",
    "Korea, Democratic People's Republic of": "PRK", "Korea, Republic of": "KOR",
    "Kyrgyzstan": "KGZ", "Lao People's Democratic Republic": "LAO", "Latvia": "LVA",
    "Lebanon": "LBN", "Liberia": "LBR", "Libya": "LBY", "Lithuania": "LTU",
    "Luxembourg": "LUX", "Madagascar": "MDG", "Malawi": "MWI", "Malaysia": "MYS",
    "Mali": "MLI", "Mauritania": "MRT", "Mexico": "MEX", "Moldova, Republic of": "MDA",
    "Mongolia": "MNG", "Morocco": "MAR", "Mozambique": "MOZ", "Myanmar": "MMR",
    "Namibia": "NAM", "Nepal": "NPL", "Netherlands": "NLD", "Netherlands (Kingdom of the)": "NLD",
    "New Zealand": "NZL", "Nicaragua": "NIC", "Niger": "NER", "Nigeria": "NGA",
    "North Macedonia": "MKD", "Norway": "NOR", "Pakistan": "PAK", "Panama": "PAN",
    "Paraguay": "PRY", "Peru": "PER", "Philippines": "PHL", "Poland": "POL",
    "Portugal": "PRT", "Romania": "ROU", "Russian Federation": "RUS", "Rwanda": "RWA",
    "Saudi Arabia": "SAU", "Senegal": "SEN", "Serbia": "SRB", "Sierra Leone": "SLE",
    "Slovakia": "SVK", "Slovenia": "SVN", "Somalia": "SOM", "South Africa": "ZAF",
    "South Sudan": "SSD", "Spain": "ESP", "Sri Lanka": "LKA", "Sudan": "SDN",
    "Sweden": "SWE", "Switzerland": "CHE", "Syrian Arab Republic": "SYR",
    "Tajikistan": "TJK", "Tanzania, United Republic of": "TZA", "Thailand": "THA",
    "Togo": "TGO", "Tunisia": "TUN", "Turkey": "TUR", "Turkmenistan": "TKM",
    "Uganda": "UGA", "Ukraine": "UKR", "United Arab Emirates": "ARE",
    "United Kingdom of Great Britain and Northern Ireland": "GBR",
    "United States of America": "USA", "Uruguay": "URY", "Uzbekistan": "UZB",
    "Venezuela (Bolivarian Republic of)": "VEN", "Viet Nam": "VNM",
    "Yemen": "YEM", "Zambia": "ZMB", "Zimbabwe": "ZWE",
    "Dem. People's Republic of Korea": "PRK",
    "Democratic Republic of the Congo": "COD",
    "Republic of Korea": "KOR",
    "Taiwan Province of China": "TWN",
    "Bolivia": "BOL", "Iran": "IRN", "Syria": "SYR", "Tanzania": "TZA",
    "Venezuela": "VEN", "Viet Nam": "VNM", "Laos": "LAO",
}


def tonnes_to_mt(t):
    return round(t / 1_000_000, 3)


def download_fao_zip():
    print("Telechargement FAO FAOSTAT QCL...")
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    print(f"  Recu : {len(data)//1024} KB")
    return data


def parse_fao_zip(data):
    """Parse the CSV inside the ZIP, return {iso3: {crop: {year: Mt}}}"""
    result = {}  # iso3 -> {crop -> {year -> Mt}}

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        # Find the normalized CSV file
        csv_name = None
        for name in zf.namelist():
            if "Normalized" in name and name.endswith(".csv"):
                csv_name = name
                break
        if not csv_name:
            # fallback: pick any csv
            for name in zf.namelist():
                if name.endswith(".csv"):
                    csv_name = name
                    break
        print(f"  Fichier CSV: {csv_name}")

        with zf.open(csv_name) as f:
            # FAO CSVs are latin-1 encoded
            reader = csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"))
            rows_read = 0
            rows_matched = 0

            for row in reader:
                rows_read += 1
                item_code = row.get("Item Code", row.get("Item Code (FAO)", "")).strip()
                element_code = row.get("Element Code", "").strip()

                if item_code not in ITEMS:
                    continue
                if element_code != ELEMENT_PROD:
                    continue

                year_str = row.get("Year", "").strip()
                try:
                    year = int(year_str)
                except ValueError:
                    continue
                if year not in YEARS:
                    continue

                val_str = row.get("Value", "").strip()
                if not val_str or val_str == "":
                    continue
                try:
                    val = float(val_str)
                except ValueError:
                    continue

                area_name = row.get("Area", "").strip()
                iso3 = FAO_NAME_TO_ISO3.get(area_name)
                if not iso3:
                    continue

                crop = ITEMS[item_code]
                if iso3 not in result:
                    result[iso3] = {}
                if crop not in result[iso3]:
                    result[iso3][crop] = {}

                existing = result[iso3][crop].get(year, 0)
                # Some countries have multiple entries (e.g. China mainland + Hong Kong)
                # For China specifically, take mainland; otherwise sum duplicates conservatively
                if area_name == "China, mainland" or existing == 0:
                    result[iso3][crop][year] = tonnes_to_mt(val)
                rows_matched += 1

    print(f"  Lignes lues: {rows_read:,}, matchees: {rows_matched:,}")
    print(f"  Pays avec donnees: {len(result)}")
    return result


def main():
    data = download_fao_zip()
    result = parse_fao_zip(data)

    # Convert year keys to strings for JSON
    out = {}
    for iso3, crops in result.items():
        out[iso3] = {}
        for crop, years_dict in crops.items():
            out[iso3][crop] = {str(y): v for y, v in sorted(years_dict.items())}

    # Print top producers 2022
    print("\nTop producteurs 2022 par culture:")
    for crop in ["wheat", "rice", "maize", "soy"]:
        top = sorted(
            [(iso3, d[crop].get("2022", d[crop].get("2021", 0))) for iso3, d in out.items() if crop in d],
            key=lambda x: -x[1]
        )[:5]
        print(f"  {crop}: " + ", ".join(f"{iso}={v}Mt" for iso, v in top))

    output = {
        "updated": time.strftime("%Y-%m-%d"),
        "unit": "Mt",
        "source": "FAOSTAT QCL 2024",
        "crops": ["wheat", "rice", "maize", "barley", "soy"],
        "data": out
    }

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, separators=(",", ":"))

    print(f"\nSauvegarde {len(out)} pays -> {OUT_FILE}")


if __name__ == "__main__":
    main()
