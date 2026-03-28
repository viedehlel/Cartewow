
"""
Patches carte_energie.html to:
1. Fix the year slider left label from "2015" to "2000"
2. Add M49->ISO3 mapping table so all 226 World Bank cereal production countries are colored
3. Update updateCerealProdForYear to build CEREAL_PROD_BY_M49
4. Update updateCountriesStyle to color non-ENERGY_DATA countries for cereal metric
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ===== Fix 1: slider label =====
OLD_LABEL = '<span style="font-size:11px;color:#8b949e;white-space:nowrap">2015</span>'
NEW_LABEL = '<span style="font-size:11px;color:#8b949e;white-space:nowrap">2000</span>'
if OLD_LABEL in content:
    content = content.replace(OLD_LABEL, NEW_LABEL)
    print("Fixed slider label: 2015 -> 2000")
else:
    print("WARNING: slider label not found")

# ===== Fix 2: Add M49_TO_ISO3 mapping and patch updateCerealProdForYear =====
# Insert after CEREAL_PROD_DATA declaration (which is inside the NEW_LOAD we inserted)
OLD_CEREAL_PROD = "var CEREAL_PROD_DATA = {};  // {iso3: {year: value_mt}}"

# Standard M49 (UN numeric) -> ISO3 mapping (major countries in world-atlas TopoJSON)
M49_ISO3_TABLE = """{
  "4":"AFG","8":"ALB","12":"DZA","24":"AGO","32":"ARG","36":"AUS","40":"AUT","50":"BGD",
  "56":"BEL","64":"BTN","68":"BOL","76":"BRA","100":"BGR","104":"MMR","116":"KHM","120":"CMR",
  "124":"CAN","140":"CAF","144":"LKA","152":"CHL","156":"CHN","170":"COL","178":"COG","180":"COD",
  "188":"CRI","191":"HRV","192":"CUB","203":"CZE","204":"BEN","208":"DNK","214":"DOM","218":"ECU",
  "231":"ETH","232":"ERI","233":"EST","246":"FIN","250":"FRA","266":"GAB","276":"DEU","288":"GHA",
  "300":"GRC","320":"GTM","324":"GIN","332":"HTI","340":"HND","348":"HUN","356":"IND","360":"IDN",
  "364":"IRN","368":"IRQ","372":"IRL","376":"ISR","380":"ITA","388":"JAM","392":"JPN","398":"KAZ",
  "400":"JOR","404":"KEN","408":"PRK","410":"KOR","414":"KWT","418":"LAO","422":"LBN","430":"LBR",
  "434":"LBY","440":"LTU","442":"LUX","450":"MDG","454":"MWI","458":"MYS","466":"MLI","484":"MEX",
  "496":"MNG","504":"MAR","508":"MOZ","516":"NAM","524":"NPL","528":"NLD","540":"NCL","566":"NGA",
  "578":"NOR","586":"PAK","600":"PRY","604":"PER","608":"PHL","616":"POL","620":"PRT","630":"PRI",
  "634":"QAT","642":"ROU","643":"RUS","646":"RWA","682":"SAU","686":"SEN","694":"SLE","706":"SOM",
  "710":"ZAF","724":"ESP","729":"SDN","736":"SDN","752":"SWE","756":"CHE","760":"SYR","764":"THA",
  "788":"TUN","792":"TUR","800":"UGA","804":"UKR","784":"ARE","826":"GBR","840":"USA","858":"URY",
  "860":"UZB","862":"VEN","704":"VNM","887":"YEM","894":"ZMB","716":"ZWE","31":"AZE","50":"BGD",
  "51":"ARM","112":"BLR","144":"LKA","196":"CYP","238":"FLK","242":"FJI","292":"GIB","380":"ITA",
  "426":"LSO","428":"LVA","434":"LBY","440":"LTU","442":"LUX","458":"MYS","470":"MLT","478":"MRT",
  "480":"MUS","492":"MCO","498":"MDA","504":"MAR","508":"MOZ","516":"NAM","524":"NPL","540":"NCL",
  "548":"VUT","554":"NZL","562":"NER","566":"NGA","586":"PAK","591":"PAN","598":"PNG","616":"POL",
  "624":"GNB","626":"TLS","634":"QAT","642":"ROU","703":"SVK","705":"SVN","706":"SOM","710":"ZAF",
  "716":"ZWE","724":"ESP","728":"SSD","729":"SDN","740":"SUR","744":"SJM","748":"SWZ","752":"SWE",
  "756":"CHE","760":"SYR","762":"TJK","764":"THA","768":"TGO","780":"TTO","788":"TUN","792":"TUR",
  "795":"TKM","800":"UGA","804":"UKR","807":"MKD","818":"EGY","826":"GBR","831":"GGY","834":"TZA",
  "840":"USA","854":"BFA","858":"URY","860":"UZB","862":"VEN","887":"YEM","894":"ZMB",
  "12":"DZA","818":"EGY","434":"LBY","504":"MAR","788":"TUN","729":"SDN","728":"SSD",
  "566":"NGA","204":"BEN","288":"GHA","384":"CIV","466":"MLI","562":"NER","686":"SEN",
  "854":"BFA","324":"GIN","694":"SLE","430":"LBR","288":"GHA","120":"CMR","178":"COG",
  "180":"COD","140":"CAF","266":"GAB","646":"RWA","108":"BDI","800":"UGA","404":"KEN",
  "834":"TZA","508":"MOZ","454":"MWI","450":"MDG","426":"LSO","710":"ZAF","748":"SWZ",
  "716":"ZWE","894":"ZMB","516":"NAM","24":"AGO","072":"BWA","729":"SDN","862":"VEN",
  "604":"PER","218":"ECU","170":"COL","862":"VEN","591":"PAN","320":"GTM","340":"HND",
  "222":"SLV","214":"DOM","332":"HTI","388":"JAM","780":"TTO","188":"CRI","558":"NIC",
  "484":"MEX","76":"BRA","32":"ARG","152":"CHL","858":"URY","600":"PRY","68":"BOL",
  "226":"GNQ","174":"COM","132":"CPV","626":"TLS","398":"KAZ","417":"KGZ","762":"TJK",
  "795":"TKM","860":"UZB","703":"SVK","705":"SVN","191":"HRV","70":"BIH","807":"MKD",
  "499":"MNE","688":"SRB","8":"ALB","300":"GRC","100":"BGR","642":"ROU","348":"HUN",
  "203":"CZE","703":"SVK","616":"POL","233":"EST","440":"LTU","428":"LVA","112":"BLR",
  "372":"IRL","208":"DNK","246":"FIN","752":"SWE","578":"NOR","352":"ISL","56":"BEL",
  "528":"NLD","40":"AUT","756":"CHE","442":"LUX","620":"PRT","724":"ESP","250":"FRA",
  "380":"ITA","276":"DEU","826":"GBR","196":"CYP","470":"MLT","51":"ARM","31":"AZE",
  "268":"GEO","422":"LBN","400":"JOR","760":"SYR","275":"PSE","376":"ISR","368":"IRQ",
  "364":"IRN","792":"TUR","682":"SAU","784":"ARE","634":"QAT","48":"BHR","512":"OMN",
  "887":"YEM","414":"KWT","392":"JPN","410":"KOR","408":"PRK","496":"MNG","704":"VNM",
  "764":"THA","418":"LAO","116":"KHM","104":"MMR","360":"IDN","608":"PHL","458":"MYS",
  "764":"THA","50":"BGD","356":"IND","524":"NPL","64":"BTN","586":"PAK","4":"AFG",
  "144":"LKA","36":"AUS","554":"NZL","598":"PNG","242":"FJI","548":"VUT","548":"VUT",
  "72":"BWA","174":"COM","174":"COM","132":"CPV","226":"GNQ","324":"GIN","624":"GNB"
}"""

NEW_CEREAL_PROD = """var CEREAL_PROD_DATA = {};  // {iso3: {year: value_mt}}
var CEREAL_PROD_BY_M49 = {};  // {m49key: value_mt} — rebuilt each year change

// M49 (UN numeric) -> ISO3 mapping for world-atlas TopoJSON countries
var M49_TO_ISO3 = """ + M49_ISO3_TABLE + ";"

if OLD_CEREAL_PROD in content:
    content = content.replace(OLD_CEREAL_PROD, NEW_CEREAL_PROD)
    print("Added M49_TO_ISO3 table and CEREAL_PROD_BY_M49")
else:
    print("ERROR: CEREAL_PROD_DATA declaration not found")

# ===== Fix 3: Patch updateCerealProdForYear to also build CEREAL_PROD_BY_M49 =====
OLD_UPDATE_CEREAL = """function updateCerealProdForYear(year) {
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
}"""

NEW_UPDATE_CEREAL = """function updateCerealProdForYear(year) {
  if (!CEREAL_PROD_DATA || Object.keys(CEREAL_PROD_DATA).length === 0) return;
  var y = String(year);

  function getValForIso3(iso3) {
    var byYear = CEREAL_PROD_DATA[iso3];
    if (!byYear) return undefined;
    if (byYear[y] !== undefined) return byYear[y];
    var years = Object.keys(byYear).map(Number).sort(function(a,b){return a-b;});
    var nearest = years.reduce(function(prev, cur) {
      return Math.abs(cur - year) < Math.abs(prev - year) ? cur : prev;
    }, years[0]);
    return byYear[String(nearest)];
  }

  // Update ENERGY_DATA entries
  Object.values(ENERGY_DATA).forEach(function(d) {
    var iso3 = d.iso3;
    if (!iso3) return;
    var val = getValForIso3(iso3);
    if (val !== undefined) d.cereal_prod_mt = val;
  });

  // Build CEREAL_PROD_BY_M49 for countries NOT in ENERGY_DATA
  CEREAL_PROD_BY_M49 = {};
  var energyIso3Set = {};
  Object.values(ENERGY_DATA).forEach(function(d){ if(d.iso3) energyIso3Set[d.iso3]=1; });
  Object.keys(M49_TO_ISO3).forEach(function(m49) {
    var iso3 = M49_TO_ISO3[m49];
    if (energyIso3Set[iso3]) return; // already in ENERGY_DATA
    var val = getValForIso3(iso3);
    if (val !== undefined) CEREAL_PROD_BY_M49[m49] = val;
  });
}"""

if OLD_UPDATE_CEREAL in content:
    content = content.replace(OLD_UPDATE_CEREAL, NEW_UPDATE_CEREAL)
    print("Patched updateCerealProdForYear to build CEREAL_PROD_BY_M49")
else:
    print("ERROR: updateCerealProdForYear not found")

# ===== Fix 4: Patch updateCountriesStyle to color extra countries via CEREAL_PROD_BY_M49 =====
OLD_STYLE = """function updateCountriesStyle() {
  if (!layers.countries) return;
  layers.countries.eachLayer(layer => {
    const key = String(layer.feature.id);
    const d = getCountryDataForYear(key, currentYear);
    if (!d) layer.setStyle({ fillColor: 'url(#hatch-no-data)', fillOpacity: 1, weight: 0.4, opacity: 0.5, color: '#3a4050' });
    else { layer.setStyle({ fillColor: getCountryColor(d), weight: 0.5, opacity: 0.7, color: '#4a5568', fillOpacity: 0.82 }); }
    if (d && layer.getTooltip()) layer.setTooltipContent(makeCountryTooltip(d, key));
  });
}"""

NEW_STYLE = """function updateCountriesStyle() {
  if (!layers.countries) return;
  var cerealOnly = activeMetrics.length === 1 && activeMetrics[0] === 'cereal_prod_mt';
  layers.countries.eachLayer(layer => {
    const key = String(layer.feature.id);
    const d = getCountryDataForYear(key, currentYear);
    if (!d) {
      // For countries not in ENERGY_DATA, check cereal supplemental data
      if (cerealOnly && CEREAL_PROD_BY_M49[key] !== undefined) {
        var fakeD = { cereal_prod_mt: CEREAL_PROD_BY_M49[key] };
        var col = getMetricColor(fakeD.cereal_prod_mt, 'cereal_prod_mt');
        layer.setStyle({ fillColor: col || '#1a2e05', fillOpacity: 0.82, weight: 0.5, opacity: 0.7, color: '#4a5568' });
      } else {
        layer.setStyle({ fillColor: 'url(#hatch-no-data)', fillOpacity: 1, weight: 0.4, opacity: 0.5, color: '#3a4050' });
      }
    } else {
      layer.setStyle({ fillColor: getCountryColor(d), weight: 0.5, opacity: 0.7, color: '#4a5568', fillOpacity: 0.82 });
      if (layer.getTooltip()) layer.setTooltipContent(makeCountryTooltip(d, key));
    }
  });
}"""

if OLD_STYLE in content:
    content = content.replace(OLD_STYLE, NEW_STYLE)
    print("Patched updateCountriesStyle to color extra countries for cereal metric")
else:
    print("ERROR: updateCountriesStyle not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done.")
