"""
Fetches refugee & displacement data from UNHCR Population Statistics API
Endpoint: https://api.unhcr.org/population/v1/population/
No API key required. Runs weekly via GitHub Actions.
"""
import json, urllib.request, os, time
from datetime import datetime

BASE = "https://api.unhcr.org/population/v1/population"

# Top emitting countries (country of origin)
COO_COUNTRIES = [
    "SYR","AFG","VEN","UKR","MMR","SSD","COD","SOM","SDN","ETH",
    "IRQ","NGA","YEM","CAF","MLI","MOZ","BGD","PAK","COL","ERI",
    "BUR","RUS","CUB","HTI","GEO","AZE","SRB","LBR","CMR","TCD"
]

# Top hosting countries (country of asylum)
COA_COUNTRIES = [
    "TUR","DEU","COL","PAK","IRN","UGA","POL","JOR","ETH","BGD",
    "KEN","SUD","LBN","CHN","USA","FRA","GBR","CAN","IND","SWE",
    "AUT","NOR","CHE","NLD","BEL","ESP","ITA","GRC","HUN","AUS"
]

# Major origin->asylum pairs for flow visualization
FLOW_PAIRS = [
    ("SYR","TUR"),("SYR","DEU"),("SYR","LBN"),("SYR","JOR"),("SYR","SWE"),
    ("AFG","PAK"),("AFG","IRN"),("AFG","DEU"),("AFG","TUR"),
    ("VEN","COL"),("VEN","PER"),("VEN","USA"),("VEN","ECU"),
    ("UKR","DEU"),("UKR","POL"),("UKR","RUS"),("UKR","CZE"),
    ("MMR","BGD"),("MMR","THA"),("MMR","IND"),
    ("SSD","UGA"),("SSD","ETH"),("SSD","SDN"),
    ("COD","UGA"),("COD","RWA"),("COD","AGO"),
    ("SOM","ETH"),("SOM","KEN"),
    ("SDN","ETH"),("SDN","EGY"),("SDN","CHD"),
    ("ETH","SOM"),("ETH","KEN"),
    ("AFG","AUS"),("IRQ","DEU"),("NGA","CMR"),
]

def fetch_country(iso3, role="coo"):
    """Fetch all years data for a country (as origin or asylum)"""
    url = f"{BASE}/?{role}={iso3}&limit=200"
    try:
        req = urllib.request.Request(url, headers={"Accept":"application/json","User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode()).get("items", [])
    except Exception as e:
        print(f"  Error {role}={iso3}: {e}")
        return []

def fetch_pair(coo, coa):
    """Fetch all years for a specific origin->asylum pair"""
    url = f"{BASE}/?coo={coo}&coa={coa}&limit=200"
    try:
        req = urllib.request.Request(url, headers={"Accept":"application/json","User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode()).get("items", [])
    except Exception as e:
        print(f"  Error {coo}->{coa}: {e}")
        return []

def safe_int(v):
    try: return int(v)
    except: return 0

def main():
    print("Fetching migration data from UNHCR API...")

    refugees_out = {}   # {iso3: {year: value_k}}
    idp_data     = {}   # {iso3: {year: value_k}}
    refugees_in  = {}   # {iso3: {year: value_k}}

    # Fetch origin countries
    print(f"Fetching {len(COO_COUNTRIES)} origin countries...")
    for iso3 in COO_COUNTRIES:
        items = fetch_country(iso3, "coo")
        for item in items:
            year = str(item.get("year",""))
            ref  = safe_int(item.get("refugees", 0))
            idps = safe_int(item.get("idps", 0))
            if ref > 0:
                if iso3 not in refugees_out: refugees_out[iso3] = {}
                refugees_out[iso3][year] = round(ref / 1000, 1)
            if idps > 0:
                if iso3 not in idp_data: idp_data[iso3] = {}
                idp_data[iso3][year] = round(idps / 1000, 1)
        time.sleep(0.4)

    # Fetch asylum countries
    print(f"Fetching {len(COA_COUNTRIES)} asylum countries...")
    for iso3 in COA_COUNTRIES:
        items = fetch_country(iso3, "coa")
        for item in items:
            year = str(item.get("year",""))
            ref  = safe_int(item.get("refugees", 0))
            if ref > 0:
                if iso3 not in refugees_in: refugees_in[iso3] = {}
                cur = refugees_in[iso3].get(year, 0)
                refugees_in[iso3][year] = round((cur * 1000 + ref) / 1000, 1)
        time.sleep(0.4)

    # Fetch flows
    print(f"Fetching {len(FLOW_PAIRS)} flow pairs...")
    flows = []
    for coo, coa in FLOW_PAIRS:
        items = fetch_pair(coo, coa)
        if not items:
            time.sleep(0.4)
            continue
        hist = {}
        for item in items:
            year = item.get("year")
            ref  = safe_int(item.get("refugees", 0))
            if year and ref > 0:
                hist[str(year)] = round(ref / 1000, 1)
        if hist:
            coo_name = items[0].get("coo_name","")
            coa_name = items[0].get("coa_name","")
            max_val = max(hist.values())
            if max_val >= 10:  # only flows with at least 10k at peak
                flows.append({
                    "from_iso": coo, "from_name": coo_name,
                    "to_iso": coa,   "to_name": coa_name,
                    "hist": hist,    "peak_k": max_val
                })
        time.sleep(0.4)

    print(f"Results: {len(refugees_out)} origins, {len(refugees_in)} asylums, {len(idp_data)} IDP countries, {len(flows)} flows")

    os.makedirs("data", exist_ok=True)
    out = {
        "updated":       datetime.now().strftime("%Y-%m-%d"),
        "source":        "UNHCR Population Statistics API",
        "refugees_out_k": refugees_out,
        "refugees_in_k":  refugees_in,
        "idp_k":          idp_data,
        "flows":          flows
    }
    with open("data/migrations.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("Saved data/migrations.json")

if __name__ == "__main__":
    main()
