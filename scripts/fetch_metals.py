"""
Télécharge les flux commerciaux de métaux critiques depuis l'API UN Comtrade v1.
Génère data/metals.json — même pattern que fetch_cereals.py.

Métaux couverts (codes HS chapitre 26 — minerais et concentrés) :
  2601 — Minerai de fer     (iron_ore)
  2603 — Minerai de cuivre  (copper)
  2604 — Minerai de nickel  (nickel)
  2605 — Minerai de cobalt  (cobalt)
  2530 — Minéraux divers incl. spodumène/lithium  (lithium)

Source : https://comtradeapi.un.org  (nécessite COMTRADE_KEY)
"""
import json, os, time, urllib.request
from datetime import datetime

# ── Correspondance M49 → nom français ────────────────────────────────────────
M49_TO_FR = {
    # Exportateurs de métaux
    "152": "Chili",
    "604": "Pérou",
    "180": "Congo RDC",
    "36":  "Australie",
    "894": "Zambie",
    "643": "Russie",
    "360": "Indonésie",
    "608": "Philippines",
    "124": "Canada",
    "76":  "Brésil",
    "710": "Afrique du Sud",
    "356": "Inde",
    "32":  "Argentine",
    "398": "Kazakhstan",
    "840": "États-Unis",
    # Importateurs principaux
    "156": "Chine",
    "392": "Japon",
    "410": "Corée du Sud",
    "528": "Pays-Bas",
    "246": "Finlande",
    "56":  "Belgique",
    "276": "Allemagne",
    "250": "France",
    "826": "Royaume-Uni",
    "380": "Italie",
    "724": "Espagne",
    "792": "Turquie",
    "764": "Thaïlande",
    "704": "Vietnam",
    "458": "Malaisie",
}

COORDS = {
    "Chili":         [-71, -35],
    "Pérou":         [-76, -10],
    "Congo RDC":     [24,  -3],
    "Australie":     [133, -27],
    "Zambie":        [28,  -14],
    "Russie":        [60,   58],
    "Indonésie":     [117,  -2],
    "Philippines":   [122,  13],
    "Canada":        [-96,  56],
    "Brésil":        [-55, -10],
    "Afrique du Sud":[25,  -29],
    "Inde":          [78,   22],
    "Argentine":     [-64, -34],
    "Kazakhstan":    [67,   48],
    "États-Unis":    [-100, 38],
    "Chine":         [104,  35],
    "Japon":         [138,  37],
    "Corée du Sud":  [127,  37],
    "Pays-Bas":      [5,    52],
    "Finlande":      [26,   62],
    "Belgique":      [4.5, 50.5],
    "Allemagne":     [10,   51],
    "France":        [2,    47],
    "Royaume-Uni":   [-2,   54],
    "Italie":        [12,   43],
    "Espagne":       [-4,   40],
    "Turquie":       [35,   39],
    "Thaïlande":     [101,  15],
    "Vietnam":       [106,  16],
    "Malaisie":      [110,   3],
}

# ── Principaux exportateurs par métal (M49) ──────────────────────────────────
EXPORTERS = {
    "iron_ore": ["36", "76", "710", "356", "643"],          # AUS, BRA, ZAF, IND, RUS
    "copper":   ["152", "604", "180", "36", "894", "643"],  # CHL, PER, COD, AUS, ZMB, RUS
    "nickel":   ["360", "608", "643", "124", "36"],         # IDN, PHL, RUS, CAN, AUS
    "cobalt":   ["180", "643", "36", "608"],                # COD, RUS, AUS, PHL
    "lithium":  ["36", "152", "32"],                        # AUS, CHL, ARG
}

HS_CODES = {
    "iron_ore": "2601",
    "copper":   "2603",
    "nickel":   "2604",
    "cobalt":   "2605",
    "lithium":  "2530",
}

TYPE_COLORS = {
    "iron_ore": "#b45309",
    "copper":   "#ea580c",
    "nickel":   "#64748b",
    "cobalt":   "#3b82f6",
    "lithium":  "#0ea5e9",
}

# Seuils minimaux (valeur nette en kt ou Mt selon métal)
THRESHOLDS = {
    "iron_ore": 5_000_000,   # 5 Mt → poids en kg dans Comtrade
    "copper":   50_000,      # 50 kt
    "nickel":   5_000,       # 5 kt
    "cobalt":   500,         # 0.5 kt
    "lithium":  500,         # 0.5 kt
}

UNITS = {
    "iron_ore": "Mt",
    "copper":   "kt",
    "nickel":   "kt",
    "cobalt":   "kt",
    "lithium":  "kt",
}

DIVISORS = {
    "iron_ore": 1_000_000_000,  # kg → Mt (÷ 10^9)
    "copper":   1_000_000,      # kg → kt (÷ 10^6)
    "nickel":   1_000_000,
    "cobalt":   1_000_000,
    "lithium":  1_000_000,
}

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
        print(f"    Erreur: {e}")
        return []

def build_flows(api_key, year=2022):
    flows = []
    for metal_type, reporters in EXPORTERS.items():
        cmd_code = HS_CODES[metal_type]
        threshold = THRESHOLDS[metal_type]
        divisor = DIVISORS[metal_type]
        unit = UNITS[metal_type]
        color = TYPE_COLORS[metal_type]
        print(f"Fetching {metal_type} (HS {cmd_code})...")
        for rep_code in reporters:
            from_name = M49_TO_FR.get(rep_code)
            if not from_name or from_name not in COORDS:
                continue
            time.sleep(1.5)
            records = fetch_one(rep_code, cmd_code, api_key, year)
            print(f"  {from_name}: {len(records)} partenaires")
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
                flows.append({
                    "from":  from_name,
                    "fromC": COORDS[from_name],
                    "to":    to_name,
                    "toC":   COORDS[to_name],
                    "type":  metal_type,
                    "unit":  unit,
                    "value": val,
                    "year":  year,
                    "color": color,
                })
    return flows

def main():
    api_key = os.environ.get("COMTRADE_KEY", "")
    if not api_key:
        print("Pas de COMTRADE_KEY — skip fetch_metals.")
        return

    year = datetime.now().year - 2   # données disponibles ~2 ans derrière
    print(f"Récupération métaux UN Comtrade (année {year})...")
    flows = build_flows(api_key, year)

    if not flows:
        print("Aucune donnée — conservation des données existantes.")
        return

    os.makedirs("data", exist_ok=True)
    out = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "year": year,
        "source": "UN Comtrade API v1 — mise à jour automatique hebdomadaire",
        "url": "https://comtradeapi.un.org",
        "flows": flows,
    }
    with open("data/metals.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Sauvegardé {len(flows)} flux dans data/metals.json")

if __name__ == "__main__":
    main()
