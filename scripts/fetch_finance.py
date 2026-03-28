"""
Télécharge les flux d'IDE (Investissements Directs Étrangers) depuis l'API World Bank.
Génère data/finance.json avec séries historiques 2015–2023 par pays.

Indicateur : BX.KLT.DINV.CD.WD — FDI net inflows (BoP, current US$)
Source : https://api.worldbank.org

Aucune clé API requise pour World Bank.
"""
import json, os, time, urllib.request, urllib.error
from datetime import datetime

COUNTRIES = [
    "CN","US","DE","JP","KR","GB","FR","NL","SG","IN",
    "BR","AU","CA","CH","IT","ES","RU","SA","AE","MX"
]

ISO2_TO_FR = {
    "CN": "Chine",          "US": "États-Unis",     "DE": "Allemagne",
    "JP": "Japon",          "KR": "Corée du Sud",   "GB": "Royaume-Uni",
    "FR": "France",         "NL": "Pays-Bas",       "SG": "Singapour",
    "IN": "Inde",           "BR": "Brésil",         "AU": "Australie",
    "CA": "Canada",         "CH": "Suisse",         "IT": "Italie",
    "ES": "Espagne",        "RU": "Russie",         "SA": "Arabie Saoudite",
    "AE": "Émirats Arabes Unis",                    "MX": "Mexique",
}


def fetch_fdi(iso2, max_retries=3):
    """Fetch FDI net inflows for a country from World Bank API."""
    url = (
        f"https://api.worldbank.org/v2/country/{iso2}/indicator/"
        f"BX.KLT.DINV.CD.WD?format=json&date=2015:2023&per_page=100&mrv=9"
    )
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = json.loads(resp.read().decode())
                # World Bank returns [metadata, data_array]
                if not isinstance(raw, list) or len(raw) < 2:
                    return {}
                records = raw[1] or []
                result = {}
                for rec in records:
                    year = str(rec.get("date", ""))
                    value = rec.get("value")
                    if year and value is not None:
                        result[year] = value
                return result
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 30 * (attempt + 1)
                print(f"    429 — attente {wait}s (tentative {attempt+1}/{max_retries})...")
                time.sleep(wait)
            else:
                print(f"    HTTP {e.code}: {e}")
                return {}
        except Exception as e:
            print(f"    Erreur: {e}")
            return {}
    print("    Échec après 3 tentatives — pays ignoré")
    return {}


def main():
    data = {}
    total = len(COUNTRIES)

    for i, iso2 in enumerate(COUNTRIES, 1):
        name = ISO2_TO_FR.get(iso2, iso2)
        print(f"  [{i}/{total}] {name} ({iso2})...", end=" ", flush=True)
        time.sleep(0.5)
        country_data = fetch_fdi(iso2)
        if country_data:
            # Sort by year ascending
            data[iso2] = {yr: country_data[yr] for yr in sorted(country_data.keys())}
            print(f"{len(country_data)} années")
        else:
            print("aucune donnée")

    if not data:
        print("Aucune donnée FDI récupérée.")
        return

    os.makedirs("data", exist_ok=True)
    out = {
        "updated":   datetime.now().strftime("%Y-%m-%d"),
        "source":    "World Bank API — BX.KLT.DINV.CD.WD",
        "indicator": "fdi_inflows_usd",
        "data":      data,
    }
    with open("data/finance.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize("data/finance.json") // 1024
    print(f"\nSauvegardé {len(data)} pays dans data/finance.json ({size_kb} KB)")


if __name__ == "__main__":
    main()
