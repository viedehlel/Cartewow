import sys
sys.stdout.reconfigure(encoding='utf-8')

# ISO3 -> French name for UN DESA economic migration countries
ISO_ECON_FR_MAP = """\
var ISO_ECON_FR = {
  "USA":"\u00c9tats-Unis","DEU":"Allemagne","FRA":"France","GBR":"Royaume-Uni",
  "CAN":"Canada","AUS":"Australie","SAU":"Arabie Saoudite","ARE":"\u00c9mirats Arabes Unis",
  "IND":"Inde","CHN":"Chine","PAK":"Pakistan","BGD":"Bangladesh",
  "MEX":"Mexique","COL":"Colombie","TUR":"Turquie","RUS":"Russie",
  "UKR":"Ukraine","POL":"Pologne","ROU":"Roumanie","ITA":"Italie",
  "ESP":"Espagne","NLD":"Pays-Bas","BEL":"Belgique","SWE":"Su\u00e8de",
  "CHE":"Suisse","AUT":"Autriche","NOR":"Norv\u00e8ge","DNK":"Danemark",
  "FIN":"Finlande","PRT":"Portugal","GRC":"Gr\u00e8ce","HUN":"Hongrie",
  "CZE":"Tch\u00e9quie","MYS":"Malaisie","IDN":"Indon\u00e9sie","PHL":"Philippines",
  "THA":"Tha\u00eflande","JPN":"Japon","KOR":"Cor\u00e9e du Sud","SGP":"Singapour",
  "ZAF":"Afrique du Sud","NGA":"Nigeria","GHA":"Ghana","KEN":"Kenya",
  "ETH":"\u00c9thiopie","EGY":"\u00c9gypte","MAR":"Maroc","DZA":"Alg\u00e9rie",
  "TUN":"Tunisie","SEN":"S\u00e9n\u00e9gal","ZWE":"Zimbabwe","MOZ":"Mozambique",
  "CIV":"C\u00f4te d'Ivoire","BRA":"Br\u00e9sil","ARG":"Argentine","PER":"P\u00e9rou",
  "VEN":"Venezuela","CHL":"Chili","ECU":"\u00c9quateur","BOL":"Bolivie",
  "CUB":"Cuba","HTI":"Ha\u00efti","GTM":"Guatemala","HND":"Honduras",
  "SLV":"El Salvador","KAZ":"Kazakhstan","UZB":"Ouzb\u00e9kistan",
  "TJK":"Tadjikistan","KGZ":"Kirghizistan","AFG":"Afghanistan",
  "SYR":"Syrie","IRQ":"Irak","IRN":"Iran","JOR":"Jordanie",
  "LBN":"Liban","ISR":"Isra\u00ebl","MMR":"Myanmar","NPL":"N\u00e9pal",
  "LKA":"Sri Lanka","SDN":"Soudan","SSD":"Soudan du Sud","UGA":"Ouganda",
  "COD":"R\u00e9p. d\u00e9m. du Congo","SOM":"Somalie","BFA":"Burkina Faso",
  "MLI":"Mali","NER":"Niger","TCD":"Tchad","NZL":"Nouvelle-Z\u00e9lande",
  "QAT":"Qatar","KWT":"Kowe\u00eft","BHR":"Bahr\u00ebn","OMN":"Oman",
  "IRL":"Irlande","RWA":"Rwanda","TZA":"Tanzanie","ZMB":"Zambie",
  "AGO":"Angola","CMR":"Cameroun","BLR":"Bi\u00e9lorussie","BGR":"Bulgarie",
  "SRB":"Serbie","HRV":"Croatie","BIH":"Bosnie","ALB":"Albanie",
  "MKD":"Mac\u00e9doine","SVK":"Slovaquie","LTU":"Lituanie","LVA":"Lettonie",
  "EST":"Estonie","MDA":"Moldavie","ARM":"Arm\u00e9nie","GEO":"G\u00e9orgie",
  "AZE":"Azerba\u00efdjan","VNM":"Vietnam","YEM":"Y\u00e9men","KHM":"Cambodge",
  "LAO":"Laos","BEN":"B\u00e9nin","BDI":"Burundi","CAF":"Centrafrique",
  "COG":"Congo","CRI":"Costa Rica","DOM":"R\u00e9p. Dominicaine",
  "ERI":"\u00c9rythr\u00e9e","GIN":"Guin\u00e9e","HTI":"Ha\u00efti",
  "JAM":"Jama\u00efque","LSO":"Lesotho","LBR":"Lib\u00e9ria","LBY":"Libye",
  "MWI":"Malawi","NIC":"Nicaragua","PRY":"Paraguay","SLE":"Sierra Leone",
  "PSE":"Palestine","SUR":"Suriname","TGO":"Togo","TTO":"Trinit\u00e9",
  "TKM":"Turkm\u00e9nistan","ESH":"Sahara Occidental",
  "HKG":"Hong Kong","MAC":"Macao","PRI":"Porto Rico"
};
"""

LOAD_ECON_FUNC = """\
function loadMigrationEconomicData() {
  fetch('data/migration_economic.json')
    .then(function(r){ return r.json(); })
    .then(function(json){
      // Remove existing hardcoded economic flows
      for (var i = MIGRATION_FLOWS.length - 1; i >= 0; i--) {
        if (MIGRATION_FLOWS[i].type === 'economic') MIGRATION_FLOWS.splice(i, 1);
      }
      // Add UN DESA corridors
      var flows = json.flows || [];
      flows.forEach(function(fl) {
        MIGRATION_FLOWS.push({
          from_iso: fl.from_iso,
          from: ISO_ECON_FR[fl.from_iso] || fl.from_name,
          fromC: fl.from_coords,
          to_iso: fl.to_iso,
          to: ISO_ECON_FR[fl.to_iso] || fl.to_name,
          toC: fl.to_coords,
          type: 'economic',
          hist: fl.hist
        });
      });
      console.log('UN DESA: ' + flows.length + ' corridors charg\u00e9s (' + json.updated + ')');
      if (layerVis.migration_flows) rebuildMigrationFlowsLayer();
    })
    .catch(function(e){ console.warn('Could not load migration_economic.json:', e); });
}
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert ISO_ECON_FR + loadMigrationEconomicData before loadMigrationsData
ANCHOR = 'function loadMigrationsData()'
if ANCHOR in content:
    content = content.replace(ANCHOR, ISO_ECON_FR_MAP + '\n' + LOAD_ECON_FUNC + '\n' + ANCHOR)
    print("OK: loadMigrationEconomicData inserted")
else:
    print("ERROR: anchor not found")

# 2. Hook loadMigrationEconomicData call after loadMigrationsData call in initTimeline
OLD_HOOK = "  if (typeof loadMigrationsData === 'function') setTimeout(loadMigrationsData, 900);"
NEW_HOOK = """\
  if (typeof loadMigrationsData === 'function') setTimeout(loadMigrationsData, 900);
  if (typeof loadMigrationEconomicData === 'function') setTimeout(loadMigrationEconomicData, 1100);"""
if OLD_HOOK in content:
    content = content.replace(OLD_HOOK, NEW_HOOK)
    print("OK: initTimeline hooks loadMigrationEconomicData at 1100ms")
else:
    print("ERROR: initTimeline hook anchor not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
