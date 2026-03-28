"""
Télécharge le dataset Our World in Data (OWID) Energy
et extrait les métriques clés par pays et par année.
Sauvegarde dans data/energy.json

Source : https://github.com/owid/energy-data (CC BY 4.0)
"""
import json, urllib.request, io, csv, os
from datetime import datetime

URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

# Métriques à extraire depuis OWID → nom dans le JSON de sortie
METRICS = {
    "oil_production":        "oil_twh",        # Production pétrole (TWh)
    "gas_production":        "gas_twh",         # Production gaz (TWh)
    "coal_production":       "coal_twh",        # Production charbon (TWh)
    "nuclear_electricity":   "nuclear_twh",     # Electricité nucléaire (TWh)
    "renewables_electricity":"renewables_twh",  # Electricité renouvelable (TWh)
    "solar_electricity":     "solar_twh",       # Solaire (TWh)
    "wind_electricity":      "wind_twh",        # Eolien (TWh)
    "hydro_electricity":     "hydro_twh",       # Hydraulique (TWh)
    "greenhouse_gas_emissions": "co2_mt",        # Emissions GES (Mt CO2eq)
    "energy_per_capita":     "energy_per_capita_kwh",  # Conso par habitant (kWh)
    "electricity_generation":"elec_twh",        # Production électrique totale (TWh)
    "fossil_fuel_consumption":"fossil_twh",     # Conso fossile (TWh)
    "primary_energy_consumption": "primary_twh",# Conso primaire (TWh)
}

# Années à conserver
MIN_YEAR = 1990
MAX_YEAR = 2024

# Codes ISO3 agrégats à exclure (pas des pays souverains)
EXCLUDE_ISO = {
    "OWID_WRL", "OWID_EUR", "OWID_ASI", "OWID_AFR", "OWID_NAM", "OWID_SAM",
    "OWID_OCE", "OWID_KOS", "OWID_CIS", "OWID_USB", "OWID_USS",
}

def is_aggregate(iso, country):
    if not iso or iso.startswith("OWID_"):
        return True
    # Certains agrégats n'ont pas de préfixe OWID_
    aggregates = {
        "World", "Africa", "Asia", "Europe", "North America", "South America",
        "Oceania", "Antarctica", "High-income countries", "Low-income countries",
        "Upper-middle-income countries", "Lower-middle-income countries",
        "European Union (27)", "G20", "G7", "OPEC",
    }
    return country in aggregates

def main():
    print(f"Téléchargement OWID energy data...")
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode("utf-8")
    print(f"Téléchargé ({len(raw)//1024} KB)")

    reader = csv.DictReader(io.StringIO(raw))
    cols = reader.fieldnames
    print(f"Colonnes : {len(cols)}")

    # Vérifie que les métriques demandées existent
    missing = [m for m in METRICS if m not in cols]
    if missing:
        print(f"Colonnes manquantes : {missing}")

    # {iso3: {metric_out: {year: value}}}
    data = {}
    rows_kept = 0

    for row in reader:
        iso = row.get("iso_code", "").strip()
        country = row.get("country", "").strip()
        year_str = row.get("year", "").strip()

        if is_aggregate(iso, country):
            continue
        if not iso or len(iso) != 3:
            continue

        try:
            year = int(year_str)
        except ValueError:
            continue

        if year < MIN_YEAR or year > MAX_YEAR:
            continue

        if iso not in data:
            data[iso] = {out: {} for out in METRICS.values()}

        for col_in, col_out in METRICS.items():
            val = row.get(col_in, "").strip()
            if val == "" or val == "nan":
                continue
            try:
                fval = round(float(val), 2)
                if fval != 0:
                    data[iso][col_out][str(year)] = fval
            except ValueError:
                continue

        rows_kept += 1

    # Supprimer les métriques vides pour chaque pays
    for iso in list(data.keys()):
        data[iso] = {k: v for k, v in data[iso].items() if v}
        if not data[iso]:
            del data[iso]

    print(f"Pays avec données : {len(data)}")
    print(f"Lignes traitées : {rows_kept}")

    # Quelques stats
    sample_iso = ["USA", "CHN", "FRA", "SAU", "DEU"]
    for iso in sample_iso:
        if iso in data:
            metrics_avail = list(data[iso].keys())
            years = []
            for m in metrics_avail:
                years += [int(y) for y in data[iso][m].keys()]
            if years:
                print(f"  {iso}: {len(metrics_avail)} métriques, {min(years)}-{max(years)}")

    os.makedirs("data", exist_ok=True)
    out = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "source": "Our World in Data - Energy Data (CC BY 4.0)",
        "url": "https://github.com/owid/energy-data",
        "metrics": {v: k for k, v in METRICS.items()},
        "data": data
    }
    with open("data/energy.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize("data/energy.json") // 1024
    print(f"Sauvegardé data/energy.json ({size_kb} KB)")

if __name__ == "__main__":
    main()
