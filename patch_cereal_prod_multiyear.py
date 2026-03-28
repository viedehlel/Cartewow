
"""
Patches carte_energie.html to support multi-year cereal production data.
- loadCerealProductionData stores {iso3: {year: value}} in global CEREAL_PROD_DATA
- New updateCerealProdForYear(year) updates ENERGY_DATA entries
- updateFlowsForYear calls updateCerealProdForYear
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace loadCerealProductionData with multi-year version
OLD_LOAD = """function loadCerealProductionData() {
  fetch('data/cereal_production.json')
    .then(function(r){ return r.json(); })
    .then(function(json){
      var prod = json.data || {};
      Object.values(ENERGY_DATA).forEach(function(d){
        var iso3 = d.iso3;
        if (iso3 && prod[iso3] !== undefined) {
          d.cereal_prod_mt = prod[iso3];
        }
      });
      console.log('Loaded cereal production data from World Bank');
    })
    .catch(function(e){ console.warn('Could not load cereal_production.json:', e); });
}"""

NEW_LOAD = """var CEREAL_PROD_DATA = {};  // {iso3: {year: value_mt}}

function updateCerealProdForYear(year) {
  if (!CEREAL_PROD_DATA || Object.keys(CEREAL_PROD_DATA).length === 0) return;
  var y = String(year);
  Object.values(ENERGY_DATA).forEach(function(d) {
    var iso3 = d.iso3;
    if (!iso3 || !CEREAL_PROD_DATA[iso3]) return;
    var byYear = CEREAL_PROD_DATA[iso3];
    // exact year, or nearest available year
    if (byYear[y] !== undefined) {
      d.cereal_prod_mt = byYear[y];
    } else {
      // find nearest year with data
      var years = Object.keys(byYear).map(Number).sort(function(a,b){return a-b;});
      var nearest = years.reduce(function(prev, cur) {
        return Math.abs(cur - year) < Math.abs(prev - year) ? cur : prev;
      }, years[0]);
      d.cereal_prod_mt = byYear[String(nearest)];
    }
  });
}

function loadCerealProductionData() {
  fetch('data/cereal_production.json')
    .then(function(r){ return r.json(); })
    .then(function(json){
      CEREAL_PROD_DATA = json.data || {};
      updateCerealProdForYear(currentYear);
      console.log('Loaded cereal production data from World Bank (' + Object.keys(CEREAL_PROD_DATA).length + ' countries)');
      if (document.getElementById('mc-cereal-prod') && document.getElementById('mc-cereal-prod').checked) {
        updateCountriesStyle();
      }
    })
    .catch(function(e){ console.warn('Could not load cereal_production.json:', e); });
}"""

if OLD_LOAD in content:
    content = content.replace(OLD_LOAD, NEW_LOAD)
    print("Replaced loadCerealProductionData with multi-year version")
else:
    print("ERROR: could not find loadCerealProductionData to replace")

# 2. Add updateCerealProdForYear call in updateFlowsForYear
OLD_UPDATE = """function updateFlowsForYear(year) {
  currentYear = year;
  document.getElementById('year-label').textContent = year;
  buildFlowsLayer();
  buildNuclearLayer();
  buildLngLayer();
  buildPipelinesLayer('gas');
  buildPipelinesLayer('oil');
  updateCountriesStyle();
  if (typeof rebuildArmsFlowsLayer === 'function') rebuildArmsFlowsLayer();
  if (typeof rebuildCerealFlowsLayer === 'function') rebuildCerealFlowsLayer();"""

NEW_UPDATE = """function updateFlowsForYear(year) {
  currentYear = year;
  document.getElementById('year-label').textContent = year;
  buildFlowsLayer();
  buildNuclearLayer();
  buildLngLayer();
  buildPipelinesLayer('gas');
  buildPipelinesLayer('oil');
  if (typeof updateCerealProdForYear === 'function') updateCerealProdForYear(year);
  updateCountriesStyle();
  if (typeof rebuildArmsFlowsLayer === 'function') rebuildArmsFlowsLayer();
  if (typeof rebuildCerealFlowsLayer === 'function') rebuildCerealFlowsLayer();"""

if OLD_UPDATE in content:
    content = content.replace(OLD_UPDATE, NEW_UPDATE)
    print("Added updateCerealProdForYear call in updateFlowsForYear")
else:
    print("ERROR: could not find updateFlowsForYear to patch")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done.")
