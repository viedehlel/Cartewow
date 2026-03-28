import sys
sys.stdout.reconfigure(encoding='utf-8')

# Conversions d'unites OWID (TWh) vers unites app
# oil_twh / 620 = oil_prod_mbd
# gas_twh / 10.55 = gas_prod_bcm
# coal_twh / 8.14 = coal_mt
# nuclear_twh -> nuclear_twh (meme unite)
# renewables_twh / 2.19 = renewables_gw (facteur capacite ~25%)

LOAD_ENERGY_FUNC = """\
function updateEnergyForYear(year) {
  if (!window._ENERGY_HIST || Object.keys(window._ENERGY_HIST).length === 0) return;
  var y = String(year);
  function getNearestVal(hist, year) {
    var keys = Object.keys(hist).map(Number).sort(function(a,b){return a-b;});
    if (!keys.length) return undefined;
    var nearest = keys.reduce(function(prev,cur){
      return Math.abs(cur-year)<Math.abs(prev-year)?cur:prev;
    });
    return hist[String(nearest)];
  }
  Object.values(ENERGY_DATA).forEach(function(d) {
    var h = d.iso3 ? window._ENERGY_HIST[d.iso3] : null;
    if (!h) return;
    if (h.oil_twh)        { var v=getNearestVal(h.oil_twh,year);        if(v!=null) d.oil_prod_mbd     = Math.round(v/620*100)/100; }
    if (h.gas_twh)        { var v=getNearestVal(h.gas_twh,year);        if(v!=null) d.gas_prod_bcm     = Math.round(v/10.55); }
    if (h.coal_twh)       { var v=getNearestVal(h.coal_twh,year);       if(v!=null) d.coal_mt          = Math.round(v/8.14); }
    if (h.nuclear_twh)    { var v=getNearestVal(h.nuclear_twh,year);    if(v!=null) d.nuclear_twh      = Math.round(v); }
    if (h.renewables_twh) { var v=getNearestVal(h.renewables_twh,year); if(v!=null) d.renewables_gw    = Math.round(v/2.19); }
    if (h.co2_mt)         { var v=getNearestVal(h.co2_mt,year);         if(v!=null) d.co2_mt           = Math.round(v*10)/10; }
    if (h.solar_twh)      { var v=getNearestVal(h.solar_twh,year);      if(v!=null) d.solar_twh        = Math.round(v); }
    if (h.wind_twh)       { var v=getNearestVal(h.wind_twh,year);       if(v!=null) d.wind_twh         = Math.round(v); }
    if (h.primary_twh)    { var v=getNearestVal(h.primary_twh,year);    if(v!=null) d.primary_twh      = Math.round(v); }
    if (h.energy_per_capita_kwh) { var v=getNearestVal(h.energy_per_capita_kwh,year); if(v!=null) d.energy_per_capita_kwh = Math.round(v); }
  });
}

function loadEnergyData() {
  fetch('data/energy.json')
    .then(function(r){ return r.json(); })
    .then(function(json){
      window._ENERGY_HIST = json.data || {};
      console.log('OWID energy: ' + Object.keys(window._ENERGY_HIST).length + ' pays charges (' + json.updated + ')');
      updateEnergyForYear(currentYear || 2022);
      updateCountriesStyle();
    })
    .catch(function(e){ console.warn('Could not load energy.json:', e); });
}
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inserer les fonctions avant loadCerealProductionData
ANCHOR = 'function loadCerealProductionData()'
if ANCHOR in content:
    content = content.replace(ANCHOR, LOAD_ENERGY_FUNC + '\n' + ANCHOR)
    print("OK: loadEnergyData + updateEnergyForYear inseres")
else:
    print("ERROR: anchor loadCerealProductionData not found")

# 2. Hooker loadEnergyData dans initTimeline (apres loadCerealProductionData)
OLD_HOOK = "  if (typeof loadCerealProductionData === 'function') setTimeout(loadCerealProductionData, 700);"
NEW_HOOK = """\
  if (typeof loadCerealProductionData === 'function') setTimeout(loadCerealProductionData, 700);
  if (typeof loadEnergyData === 'function') setTimeout(loadEnergyData, 850);"""
if OLD_HOOK in content:
    content = content.replace(OLD_HOOK, NEW_HOOK)
    print("OK: loadEnergyData hooke dans initTimeline (850ms)")
else:
    print("ERROR: hook anchor not found")

# 3. Appeler updateEnergyForYear dans updateFlowsForYear (avec updateMigrationForYear)
OLD_FLOWS = "  if (typeof updateMigrationForYear === 'function') updateMigrationForYear(year);"
NEW_FLOWS = """\
  if (typeof updateMigrationForYear === 'function') updateMigrationForYear(year);
  if (typeof updateEnergyForYear === 'function') updateEnergyForYear(year);"""
if OLD_FLOWS in content:
    content = content.replace(OLD_FLOWS, NEW_FLOWS)
    print("OK: updateEnergyForYear appele dans updateFlowsForYear")
else:
    print("ERROR: updateMigrationForYear hook not found in updateFlowsForYear")
    # Try to find where year changes happen
    idx = content.find('updateFlowsForYear')
    print(f"  updateFlowsForYear at: {idx}")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
