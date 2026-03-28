import sys
sys.stdout.reconfigure(encoding='utf-8')

# ISO3 -> French name mapping for migration flow countries
# (used to build _flowFrom/_flowTo for filterFlowsByCountry)
ISO_FR_MAP = """
var MIGRATION_ISO_FR = {
  "SYR":"Syrie","AFG":"Afghanistan","VEN":"Venezuela","UKR":"Ukraine",
  "MMR":"Myanmar","SSD":"Soudan du Sud","COD":"R\u00e9p. d\u00e9mocratique du Congo",
  "SOM":"Somalie","SDN":"Soudan","ETH":"\u00c9thiopie","IRQ":"Irak",
  "NGA":"Nigeria","YEM":"Y\u00e9men","COL":"Colombie","BGD":"Bangladesh",
  "TUR":"Turquie","DEU":"Allemagne","LBN":"Liban","JOR":"Jordanie",
  "PAK":"Pakistan","IRN":"Iran","UGA":"Ouganda","POL":"Pologne",
  "KEN":"Kenya","LBR":"Lib\u00e9ria","MLI":"Mali","CAF":"Centrafrique",
  "THA":"Tha\u00eflande","PER":"P\u00e9rou","USA":"\u00c9tats-Unis",
  "RUS":"Russie","SWE":"Su\u00e8de","ECU":"\u00c9quateur","RWA":"Rwanda",
  "AGO":"Angola","EGY":"\u00c9gypte","CHD":"Tchad","CZE":"Tch\u00e9quie",
  "IND":"Inde","AUS":"Australie"
};
"""

LOAD_FUNC = """
function loadMigrationsData() {
  fetch('data/migrations.json')
    .then(function(r){ return r.json(); })
    .then(function(json){
      // 1. Update production metrics in ENERGY_DATA
      var metrics = ['refugees_out_k','refugees_in_k','idp_k'];
      metrics.forEach(function(metric){
        var cd = json[metric] || {};
        Object.values(ENERGY_DATA).forEach(function(d){
          if (!d.iso3 || !cd[d.iso3]) return;
          // store full hist
          d['_hist_' + metric] = cd[d.iso3];
        });
      });

      // 2. Update MIGRATION_FLOWS hist from real API data
      var apiFlows = json.flows || [];
      MIGRATION_FLOWS.forEach(function(fl){
        var match = apiFlows.find(function(af){
          return af.from_iso === fl.from_iso && af.to_iso === fl.to_iso;
        });
        if (match && match.hist && Object.keys(match.hist).length > 0) {
          fl.hist = match.hist;
        }
      });

      console.log('Loaded migrations data from UNHCR API (' + json.updated + ')');
      updateMigrationForYear(currentYear || 2022);
      if (layerVis.migration_flows) rebuildMigrationFlowsLayer();
      var mc = document.getElementById('mc-ref-out');
      if (mc && mc.checked) updateCountriesStyle();
    })
    .catch(function(e){ console.warn('Could not load migrations.json:', e); });
}
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add ISO_FR_MAP + loadMigrationsData before loadCerealProductionData
ANCHOR = 'function loadCerealProductionData()'
if ANCHOR in content:
    content = content.replace(ANCHOR, ISO_FR_MAP + LOAD_FUNC + '\n' + ANCHOR)
    print("OK: loadMigrationsData inserted")
else:
    print("ERROR: anchor not found")

# 2. Add from_iso/to_iso to MIGRATION_FLOWS entries
# Map French names to ISO3 for the flows
flow_map = {
    'from:"Syrie"': 'from_iso:"SYR",from:"Syrie"',
    'from:"Afghanistan"': 'from_iso:"AFG",from:"Afghanistan"',
    'from:"Venezuela"': 'from_iso:"VEN",from:"Venezuela"',
    'from:"Ukraine"': 'from_iso:"UKR",from:"Ukraine"',
    'from:"Myanmar"': 'from_iso:"MMR",from:"Myanmar"',
    'from:"Soudan du Sud"': 'from_iso:"SSD",from:"Soudan du Sud"',
    'from:"Rép. démocratique du Congo"': 'from_iso:"COD",from:"Rép. démocratique du Congo"',
    'from:"Somalie"': 'from_iso:"SOM",from:"Somalie"',
    'from:"Soudan"': 'from_iso:"SDN",from:"Soudan"',
    'to:"Turquie"': 'to_iso:"TUR",to:"Turquie"',
    'to:"Allemagne"': 'to_iso:"DEU",to:"Allemagne"',
    'to:"Liban"': 'to_iso:"LBN",to:"Liban"',
    'to:"Jordanie"': 'to_iso:"JOR",to:"Jordanie"',
    'to:"Pakistan"': 'to_iso:"PAK",to:"Pakistan"',
    'to:"Iran"': 'to_iso:"IRN",to:"Iran"',
    'to:"Ouganda"': 'to_iso:"UGA",to:"Ouganda"',
    'to:"Pologne"': 'to_iso:"POL",to:"Pologne"',
    'to:"Bangladesh"': 'to_iso:"BGD",to:"Bangladesh"',
    'to:"Éthiopie"': 'to_iso:"ETH",to:"Éthiopie"',
    'to:"Thaïlande"': 'to_iso:"THA",to:"Thaïlande"',
    'to:"Pérou"': 'to_iso:"PER",to:"Pérou"',
    'to:"États-Unis"': 'to_iso:"USA",to:"États-Unis"',
    'to:"Russie"': 'to_iso:"RUS",to:"Russie"',
    'to:"Égypte"': 'to_iso:"EGY",to:"Égypte"',
}
count = 0
for old, new in flow_map.items():
    if old in content and new not in content:
        content = content.replace(old, new)
        count += 1
print(f"OK: {count} from_iso/to_iso added to MIGRATION_FLOWS")

# 3. Update updateMigrationForYear to use _hist_ values
OLD_UPDATE = """function updateMigrationForYear(year) {
  function interp(byYear,y){
    var keys=Object.keys(byYear).map(Number).sort(function(a,b){return a-b;});
    if(y<=keys[0])return byYear[keys[0]];
    if(y>=keys[keys.length-1])return byYear[keys[keys.length-1]];
    for(var i=0;i<keys.length-1;i++){if(y>=keys[i]&&y<=keys[i+1]){var t=(y-keys[i])/(keys[i+1]-keys[i]);return Math.round(byYear[keys[i]]*(1-t)+byYear[keys[i+1]]*t);}}
    return byYear[keys[0]];
  }
  Object.keys(MIGRATION_PROD_DATA).forEach(function(metric){
    var cd=MIGRATION_PROD_DATA[metric];
    Object.values(ENERGY_DATA).forEach(function(d){
      if(d.iso3&&cd[d.iso3])d[metric]=interp(cd[d.iso3],year);
    });
  });
}"""

NEW_UPDATE = """function updateMigrationForYear(year) {
  function interp(byYear,y){
    var keys=Object.keys(byYear).map(Number).sort(function(a,b){return a-b;});
    if(y<=keys[0])return byYear[keys[0]];
    if(y>=keys[keys.length-1])return byYear[keys[keys.length-1]];
    for(var i=0;i<keys.length-1;i++){if(y>=keys[i]&&y<=keys[i+1]){var t=(y-keys[i])/(keys[i+1]-keys[i]);return Math.round(byYear[keys[i]]*(1-t)+byYear[keys[i+1]]*t);}}
    return byYear[keys[0]];
  }
  // Use real API data (_hist_*) if available, else fallback to hardcoded
  var metrics = ['refugees_out_k','refugees_in_k','idp_k'];
  Object.values(ENERGY_DATA).forEach(function(d){
    metrics.forEach(function(metric){
      var hist = d['_hist_' + metric] || (MIGRATION_PROD_DATA[metric] && MIGRATION_PROD_DATA[metric][d.iso3]);
      if (hist) d[metric] = interp(hist, year);
    });
  });
}"""

if OLD_UPDATE in content:
    content = content.replace(OLD_UPDATE, NEW_UPDATE)
    print("OK: updateMigrationForYear updated to use API data")
else:
    print("ERROR: updateMigrationForYear not found")

# 4. Hook loadMigrationsData in initTimeline
OLD_INIT = "  if (typeof updateMigrationForYear === 'function') setTimeout(function(){ updateMigrationForYear(currentYear || 2022); }, 900);"
NEW_INIT = """  if (typeof loadMigrationsData === 'function') setTimeout(loadMigrationsData, 900);"""
if OLD_INIT in content:
    content = content.replace(OLD_INIT, NEW_INIT)
    print("OK: initTimeline hooks loadMigrationsData")
else:
    print("ERROR: migration init hook not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
