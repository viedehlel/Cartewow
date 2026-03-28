"""
Downloads UN DESA International Migrant Stock 2020 bilateral data
and extracts all corridors > MIN_THRESHOLD persons.
Saves to data/migration_economic.json

Table 1 format (long): each row = one (destination, origin) pair
  col 0: Index
  col 1: Destination country/region name
  col 3: Destination location code (M49)
  col 5: Origin country/region name
  col 6: Origin location code (M49)
  cols 7-13: Total migrants for years 1990, 1995, 2000, 2005, 2010, 2015, 2020
"""
import json, urllib.request, os, tempfile
from datetime import datetime

# UN DESA 2020 bilateral stock file (public domain)
URL = "https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2020_ims_stock_by_sex_destination_and_origin.xlsx"

MIN_THRESHOLD = 150000  # only corridors with 150k+ migrants
YEARS = [1990, 1995, 2000, 2005, 2010, 2015, 2020]

def download_file(url, dest):
    print(f"Downloading {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        with open(dest, 'wb') as f:
            f.write(r.read())
    print(f"Downloaded to {dest}")

def parse_excel(path):
    try:
        import openpyxl
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "-q"])
        import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    # Table 1 = total by sex (both sexes in cols 7-13)
    ws = wb['Table 1']
    rows = list(ws.iter_rows(values_only=True))

    # Header is row index 10 (0-based)
    # Verify: col 7 should be 1990
    header = rows[10]
    year_cols = []
    for y in YEARS:
        try:
            idx = list(header).index(y)
            year_cols.append((y, idx))
        except ValueError:
            pass
    print(f"Year columns found: {[(y, c) for y, c in year_cols]}")

    flows_by_pair = {}  # {(dest_name, orig_name): {year: value_k}}

    def clean_name(s):
        """Strip leading spaces, trailing asterisks/footnote markers"""
        return str(s).strip().lstrip().rstrip('*').rstrip()

    # Skip regions: only process rows where location code is a real country (< 900)
    for row in rows[11:]:
        if not row or row[1] is None:
            continue
        dest_name = clean_name(row[1])
        orig_name = clean_name(row[5]) if row[5] else None
        if not dest_name or not orig_name:
            continue
        dest_code = row[3]
        orig_code = row[6]
        # Skip aggregates (M49 >= 900 or strings)
        try:
            if int(dest_code) >= 900 or int(orig_code) >= 900:
                continue
        except (TypeError, ValueError):
            continue
        if dest_name == orig_name:
            continue

        hist = {}
        for y, col_idx in year_cols:
            val = row[col_idx] if col_idx < len(row) else None
            if val is None:
                continue
            try:
                val_int = int(float(str(val).replace(',', '').replace(' ', '')))
            except:
                continue
            if val_int >= MIN_THRESHOLD:
                hist[str(y)] = round(val_int / 1000, 1)

        if hist:
            key = (dest_name, orig_name)
            flows_by_pair[key] = hist

    wb.close()
    print(f"Total pairs above {MIN_THRESHOLD}: {len(flows_by_pair)}")
    return flows_by_pair

def get_iso3_coords():
    """Load ISO3 codes and coordinates from a minimal built-in table"""
    return {
        "United States of America": ("USA", [-95, 38]),
        "Germany": ("DEU", [10, 51]),
        "France": ("FRA", [2, 47]),
        "United Kingdom": ("GBR", [-2, 54]),
        "Canada": ("CAN", [-96, 56]),
        "Australia": ("AUS", [133, -27]),
        "Saudi Arabia": ("SAU", [45, 24]),
        "United Arab Emirates": ("ARE", [54, 24]),
        "India": ("IND", [78, 22]),
        "China": ("CHN", [104, 35]),
        "Pakistan": ("PAK", [68, 30]),
        "Bangladesh": ("BGD", [90, 23]),
        "Mexico": ("MEX", [-102, 24]),
        "Colombia": ("COL", [-74, 4]),
        "Turkey": ("TUR", [35, 39]),
        "Russian Federation": ("RUS", [60, 58]),
        "Ukraine": ("UKR", [32, 49]),
        "Poland": ("POL", [20, 52]),
        "Romania": ("ROU", [25, 46]),
        "Italy": ("ITA", [12, 43]),
        "Spain": ("ESP", [-4, 40]),
        "Netherlands": ("NLD", [5, 52]),
        "Belgium": ("BEL", [4.5, 50.5]),
        "Sweden": ("SWE", [18, 62]),
        "Switzerland": ("CHE", [8, 47]),
        "Austria": ("AUT", [14, 47]),
        "Norway": ("NOR", [10, 62]),
        "Denmark": ("DNK", [10, 56]),
        "Finland": ("FIN", [26, 64]),
        "Portugal": ("PRT", [-8, 39]),
        "Greece": ("GRC", [22, 39]),
        "Hungary": ("HUN", [19, 47]),
        "Czech Republic": ("CZE", [16, 50]),
        "Czechia": ("CZE", [16, 50]),
        "Malaysia": ("MYS", [109, 3]),
        "Indonesia": ("IDN", [117, -2]),
        "Philippines": ("PHL", [122, 13]),
        "Thailand": ("THA", [101, 15]),
        "Japan": ("JPN", [138, 37]),
        "Republic of Korea": ("KOR", [127, 37]),
        "Singapore": ("SGP", [104, 1]),
        "South Africa": ("ZAF", [25, -29]),
        "Nigeria": ("NGA", [8, 10]),
        "Ghana": ("GHA", [-1, 8]),
        "Kenya": ("KEN", [37, -1]),
        "Ethiopia": ("ETH", [39, 9]),
        "Egypt": ("EGY", [30, 27]),
        "Morocco": ("MAR", [-7, 32]),
        "Algeria": ("DZA", [3, 28]),
        "Tunisia": ("TUN", [9, 34]),
        "Senegal": ("SEN", [-14, 14]),
        "Zimbabwe": ("ZWE", [30, -20]),
        "Mozambique": ("MOZ", [35, -18]),
        "Côte d'Ivoire": ("CIV", [-6, 7]),
        "Cote d'Ivoire": ("CIV", [-6, 7]),
        "Brazil": ("BRA", [-55, -10]),
        "Argentina": ("ARG", [-64, -34]),
        "Peru": ("PER", [-76, -10]),
        "Venezuela (Bolivarian Republic of)": ("VEN", [-65, 7]),
        "Chile": ("CHL", [-71, -35]),
        "Ecuador": ("ECU", [-78, -2]),
        "Bolivia (Plurinational State of)": ("BOL", [-65, -17]),
        "Cuba": ("CUB", [-79.5, 22]),
        "Haiti": ("HTI", [-72, 19]),
        "Guatemala": ("GTM", [-90, 15]),
        "Honduras": ("HND", [-87, 15]),
        "El Salvador": ("SLV", [-89, 13]),
        "Kazakhstan": ("KAZ", [66, 48]),
        "Uzbekistan": ("UZB", [63, 41]),
        "Tajikistan": ("TJK", [71, 39]),
        "Kyrgyzstan": ("KGZ", [74, 41]),
        "Afghanistan": ("AFG", [67, 33]),
        "Syrian Arab Republic": ("SYR", [38, 35]),
        "Iraq": ("IRQ", [44, 33]),
        "Iran (Islamic Republic of)": ("IRN", [53, 33]),
        "Jordan": ("JOR", [36.5, 31]),
        "Lebanon": ("LBN", [35.5, 33.8]),
        "Israel": ("ISR", [35, 31.5]),
        "Myanmar": ("MMR", [96, 20]),
        "Nepal": ("NPL", [84, 28]),
        "Sri Lanka": ("LKA", [80, 7]),
        "Sudan": ("SDN", [31, 16]),
        "Uganda": ("UGA", [32, 1]),
        "Democratic Republic of the Congo": ("COD", [24, -3]),
        "Somalia": ("SOM", [46, 5]),
        "Burkina Faso": ("BFA", [-2, 12]),
        "Mali": ("MLI", [-2, 17]),
        "Niger": ("NER", [8, 17]),
        "Chad": ("TCD", [18, 15]),
        "New Zealand": ("NZL", [172, -42]),
        "Qatar": ("QAT", [51.5, 25]),
        "Kuwait": ("KWT", [47.5, 29]),
        "Bahrain": ("BHR", [50.5, 26]),
        "Oman": ("OMN", [57, 21]),
        "Ireland": ("IRL", [-8, 53]),
        "South Sudan": ("SSD", [31, 7]),
        "Rwanda": ("RWA", [30, -2]),
        "Tanzania, United Republic of": ("TZA", [35, -6]),
        "United Republic of Tanzania": ("TZA", [35, -6]),
        "Zambia": ("ZMB", [28, -15]),
        "Angola": ("AGO", [18, -12]),
        "Cameroon": ("CMR", [12, 6]),
        "Belarus": ("BLR", [28, 53]),
        "Bulgaria": ("BGR", [25, 43]),
        "Serbia": ("SRB", [21, 44]),
        "Croatia": ("HRV", [16, 45]),
        "Bosnia and Herzegovina": ("BIH", [17.5, 44]),
        "Albania": ("ALB", [20, 41]),
        "North Macedonia": ("MKD", [22, 41.6]),
        "Slovakia": ("SVK", [19, 48.7]),
        "Lithuania": ("LTU", [24, 56]),
        "Latvia": ("LVA", [25, 57]),
        "Estonia": ("EST", [25, 59]),
        "Moldova, Republic of": ("MDA", [28.5, 47]),
        "Republic of Moldova": ("MDA", [28.5, 47]),
        "Armenia": ("ARM", [45, 40]),
        "Georgia": ("GEO", [43, 42]),
        "Azerbaijan": ("AZE", [47, 40]),
        # Additional countries found in UN DESA data
        "Viet Nam": ("VNM", [108, 14]),
        "Yemen": ("YEM", [48, 15]),
        "Cambodia": ("KHM", [105, 12]),
        "Lao People's Democratic Republic": ("LAO", [103, 18]),
        "Benin": ("BEN", [2, 9]),
        "Burkina Faso": ("BFA", [-2, 12]),
        "Burundi": ("BDI", [29.9, -3.4]),
        "Central African Republic": ("CAF", [20, 6]),
        "Congo": ("COG", [15, -1]),
        "Costa Rica": ("CRI", [-84, 10]),
        "Dominican Republic": ("DOM", [-70, 19]),
        "Eritrea": ("ERI", [39, 15]),
        "Guinea": ("GIN", [-11, 11]),
        "Guyana": ("GUY", [-59, 5]),
        "Jamaica": ("JAM", [-77.5, 18]),
        "Lesotho": ("LSO", [28.5, -29.5]),
        "Liberia": ("LBR", [-9.5, 6.5]),
        "Libya": ("LBY", [17, 27]),
        "Malawi": ("MWI", [34, -13]),
        "Nicaragua": ("NIC", [-85, 13]),
        "Paraguay": ("PRY", [-58, -23]),
        "Sierra Leone": ("SLE", [-11.5, 8.5]),
        "State of Palestine": ("PSE", [35.3, 31.9]),
        "Suriname": ("SUR", [-56, 4]),
        "Togo": ("TGO", [1.2, 8]),
        "Trinidad and Tobago": ("TTO", [-61, 10.5]),
        "Turkmenistan": ("TKM", [59, 39]),
        "Western Sahara": ("ESH", [-13, 25]),
        "China, Hong Kong SAR": ("HKG", [114.2, 22.3]),
        "China, Macao SAR": ("MAC", [113.5, 22.2]),
        "Puerto Rico": ("PRI", [-66.5, 18.2]),
    }

def main():
    tmp = tempfile.mktemp(suffix=".xlsx")
    try:
        download_file(URL, tmp)
    except Exception as e:
        print(f"Download failed: {e}")
        return

    flows_by_pair = parse_excel(tmp)
    os.unlink(tmp)

    iso_table = get_iso3_coords()

    flows = []
    skipped_names = set()
    for (dest, orig), hist in flows_by_pair.items():
        orig_info = iso_table.get(orig)
        dest_info = iso_table.get(dest)
        if not orig_info or not dest_info:
            if not orig_info:
                skipped_names.add(orig)
            if not dest_info:
                skipped_names.add(dest)
            continue
        max_val = max(hist.values())
        flows.append({
            "from_name": orig, "from_iso": orig_info[0], "from_coords": orig_info[1],
            "to_name":   dest, "to_iso":   dest_info[0], "to_coords":   dest_info[1],
            "hist": hist, "peak_k": max_val
        })

    flows.sort(key=lambda x: -x["peak_k"])
    print(f"Flows with coords: {len(flows)}, skipped (no coords): {len(flows_by_pair) - len(flows)}")
    if skipped_names:
        print("Sample skipped country names (first 20):", sorted(skipped_names)[:20])
    print("Top 15 corridors:")
    for fl in flows[:15]:
        print(f"  {fl['from_name']} -> {fl['to_name']}: {fl['peak_k']}k")

    os.makedirs("data", exist_ok=True)
    out = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "source": "UN DESA International Migrant Stock 2020",
        "threshold_k": MIN_THRESHOLD / 1000,
        "flows": flows
    }
    with open("data/migration_economic.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Saved data/migration_economic.json ({len(flows)} corridors)")

if __name__ == "__main__":
    main()
