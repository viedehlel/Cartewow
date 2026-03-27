
"""
Fetches cereal production data from World Bank API (free, no key)
Indicator: AG.PRD.CREL.MT — Cereal production (metric tons)
"""
import json, urllib.request, os
from datetime import datetime

def fetch_world_bank():
    url = (
        "https://api.worldbank.org/v2/country/all/indicator/AG.PRD.CREL.MT"
        "?format=json&per_page=300&mrv=1"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
        return data[1] if len(data) > 1 else []
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    print("Fetching cereal production from World Bank...")
    records = fetch_world_bank()
    if not records:
        print("No data, skipping.")
        return

    result = {}
    for rec in records:
        iso3 = rec.get("countryiso3code", "")
        val  = rec.get("value")
        if iso3 and val:
            result[iso3] = round(float(val) / 1_000_000, 1)  # tonnes → Mt

    print(f"Got {len(result)} countries")
    os.makedirs("data", exist_ok=True)
    with open("data/cereal_production.json", "w", encoding="utf-8") as f:
        json.dump({
            "updated": datetime.now().strftime("%Y-%m-%d"),
            "unit": "Mt",
            "source": "World Bank — AG.PRD.CREL.MT",
            "data": result
        }, f, ensure_ascii=False, indent=2)
    print("Saved data/cereal_production.json")

if __name__ == "__main__":
    main()
