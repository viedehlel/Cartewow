import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remplacer updateEnergyForYear + loadEnergyData par une version qui alimente COUNTRY_HISTORY
OLD_FUNC = """\
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
}"""

NEW_FUNC = """\
function loadEnergyData() {
  fetch('data/energy.json')
    .then(function(r){ return r.json(); })
    .then(function(json){
      var owid = json.data || {};
      // Construire un index ISO3 -> cle M49 depuis ENERGY_DATA
      var iso3ToM49 = {};
      Object.entries(ENERGY_DATA).forEach(function(e){
        if (e[1].iso3) iso3ToM49[e[1].iso3] = e[0];
      });
      // Conversions unites OWID (TWh) -> unites app
      // oil: TWh/620 = mbd | gas: TWh/10.55 = bcm | coal: TWh/8.14 = Mt
      // nuclear/renew/solar/wind: TWh direct | co2: Mt direct
      var conv = {
        oil_twh:        function(v){ return {key:'oil_prod_mbd',   val: Math.round(v/620*100)/100}; },
        gas_twh:        function(v){ return {key:'gas_prod_bcm',   val: Math.round(v/10.55)}; },
        coal_twh:       function(v){ return {key:'coal_mt',        val: Math.round(v/8.14)}; },
        nuclear_twh:    function(v){ return {key:'nuclear_twh',    val: Math.round(v)}; },
        renewables_twh: function(v){ return {key:'renewables_gw',  val: Math.round(v/2.19)}; },
        co2_mt:         function(v){ return {key:'co2_mt',         val: Math.round(v*10)/10}; },
        solar_twh:      function(v){ return {key:'solar_twh',      val: Math.round(v)}; },
        wind_twh:       function(v){ return {key:'wind_twh',       val: Math.round(v)}; },
        primary_twh:    function(v){ return {key:'primary_twh',    val: Math.round(v)}; },
        energy_per_capita_kwh: function(v){ return {key:'energy_per_capita_kwh', val: Math.round(v)}; }
      };
      var enriched = 0;
      Object.entries(owid).forEach(function(e){
        var iso3 = e[0]; var metrics = e[1];
        var m49 = iso3ToM49[iso3];
        if (!m49) return;
        if (!COUNTRY_HISTORY[m49]) COUNTRY_HISTORY[m49] = {};
        Object.entries(metrics).forEach(function(me){
          var owid_metric = me[0]; var byYear = me[1];
          var c = conv[owid_metric];
          if (!c) return;
          var converted = {};
          Object.entries(byYear).forEach(function(ye){
            var r = c(parseFloat(ye[1]));
            converted[ye[0]] = r.val;
            if (!COUNTRY_HISTORY[m49][r.key]) COUNTRY_HISTORY[m49][r.key] = {};
            COUNTRY_HISTORY[m49][r.key][ye[0]] = r.val;
          });
        });
        enriched++;
      });
      console.log('OWID energy: ' + enriched + ' pays injectes dans COUNTRY_HISTORY (' + json.updated + ')');
      updateCountriesStyle();
    })
    .catch(function(e){ console.warn('Could not load energy.json:', e); });
}"""

if OLD_FUNC in content:
    content = content.replace(OLD_FUNC, NEW_FUNC)
    print("OK: loadEnergyData reecrite pour alimenter COUNTRY_HISTORY")
else:
    print("ERROR: ancien bloc non trouve")

# 2. Supprimer le hook updateEnergyForYear dans updateFlowsForYear (plus necessaire)
OLD_HOOK = "  if (typeof updateEnergyForYear === 'function') updateEnergyForYear(year);\n"
if OLD_HOOK in content:
    content = content.replace(OLD_HOOK, "")
    print("OK: hook updateEnergyForYear supprime de updateFlowsForYear")
else:
    print("WARN: hook updateEnergyForYear non trouve (deja absent?)")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
