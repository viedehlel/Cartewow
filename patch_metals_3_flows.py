import sys
sys.stdout.reconfigure(encoding='utf-8')

METAL_FLOWS_JS = r"""
var METAL_FLOWS = [
  // CUIVRE (kt)
  {from:"Chili",     fromC:[-71,-35], to:"Chine",        toC:[104,35],  type:"copper", unit:"kt", hist:{2000:400,2005:800,2010:1200,2015:1600,2018:2000,2020:2300,2022:2800,2023:2700}},
  {from:"Chili",     fromC:[-71,-35], to:"Japon",         toC:[138,37],  type:"copper", unit:"kt", hist:{2000:400,2005:430,2010:440,2015:450,2022:400,2023:380}},
  {from:"Chili",     fromC:[-71,-35], to:"Corée du Sud",  toC:[127,37],  type:"copper", unit:"kt", hist:{2000:150,2005:200,2010:220,2015:250,2022:250,2023:240}},
  {from:"Pérou",     fromC:[-76,-10], to:"Chine",         toC:[104,35],  type:"copper", unit:"kt", hist:{2000:80,2005:200,2010:500,2015:700,2020:1000,2022:1200,2023:1200}},
  {from:"Pérou",     fromC:[-76,-10], to:"Japon",         toC:[138,37],  type:"copper", unit:"kt", hist:{2000:180,2010:200,2015:220,2022:200,2023:190}},
  {from:"Rép. démocratique du Congo", fromC:[24,-3], to:"Chine", toC:[104,35], type:"copper", unit:"kt", hist:{2000:5,2005:50,2010:300,2015:600,2020:1100,2022:1200,2023:1300}},
  {from:"Australie", fromC:[133,-27], to:"Japon",         toC:[138,37],  type:"copper", unit:"kt", hist:{2000:350,2005:380,2010:400,2015:420,2022:400,2023:390}},
  {from:"Australie", fromC:[133,-27], to:"Corée du Sud",  toC:[127,37],  type:"copper", unit:"kt", hist:{2000:130,2010:190,2015:200,2022:200,2023:195}},
  {from:"Zambie",    fromC:[28,-14],  to:"Chine",         toC:[104,35],  type:"copper", unit:"kt", hist:{2000:30,2005:100,2010:250,2015:300,2022:400,2023:420}},
  // LITHIUM (kt)
  {from:"Australie", fromC:[133,-27], to:"Chine",         toC:[104,35],  type:"lithium", unit:"kt", hist:{2015:5,2017:15,2018:40,2019:30,2020:25,2021:45,2022:60,2023:70}},
  {from:"Australie", fromC:[133,-27], to:"Japon",         toC:[138,37],  type:"lithium", unit:"kt", hist:{2015:4,2018:7,2020:8,2022:10,2023:11}},
  {from:"Australie", fromC:[133,-27], to:"Corée du Sud",  toC:[127,37],  type:"lithium", unit:"kt", hist:{2015:3,2018:5,2020:6,2022:8,2023:9}},
  {from:"Chili",     fromC:[-71,-35], to:"Chine",         toC:[104,35],  type:"lithium", unit:"kt", hist:{2015:5,2018:10,2020:12,2022:20,2023:22}},
  {from:"Chili",     fromC:[-71,-35], to:"Corée du Sud",  toC:[127,37],  type:"lithium", unit:"kt", hist:{2015:4,2018:6,2020:7,2022:8,2023:8}},
  {from:"Argentine", fromC:[-64,-34], to:"Chine",         toC:[104,35],  type:"lithium", unit:"kt", hist:{2018:1,2020:3,2022:5,2023:6}},
  // COBALT (kt)
  {from:"Rép. démocratique du Congo", fromC:[24,-3], to:"Chine",    toC:[104,35],  type:"cobalt", unit:"kt", hist:{2000:9,2005:17,2010:40,2015:57,2020:88,2022:140,2023:150}},
  {from:"Rép. démocratique du Congo", fromC:[24,-3], to:"Finlande", toC:[26,62],   type:"cobalt", unit:"kt", hist:{2010:5,2015:9,2022:15,2023:14}},
  {from:"Rép. démocratique du Congo", fromC:[24,-3], to:"Belgique", toC:[4.5,50.5],type:"cobalt", unit:"kt", hist:{2010:4,2015:7,2022:10,2023:9}},
  {from:"Australie", fromC:[133,-27], to:"Chine",         toC:[104,35],  type:"cobalt", unit:"kt", hist:{2015:3,2022:5,2023:5}},
  {from:"Russie",    fromC:[60,58],   to:"Finlande",      toC:[26,62],   type:"cobalt", unit:"kt", hist:{2015:4,2022:4,2023:3}},
  // NICKEL (kt)
  {from:"Indonésie", fromC:[117,-2],  to:"Chine",         toC:[104,35],  type:"nickel", unit:"kt", hist:{2010:50,2015:80,2017:200,2019:700,2022:800,2023:900}},
  {from:"Philippines",fromC:[122,13], to:"Chine",         toC:[104,35],  type:"nickel", unit:"kt", hist:{2010:80,2015:150,2022:300,2023:310}},
  {from:"Russie",    fromC:[60,58],   to:"Pays-Bas",      toC:[5,52],    type:"nickel", unit:"kt", hist:{2000:60,2010:80,2015:80,2022:80,2023:70}},
  {from:"Canada",    fromC:[-96,56],  to:"États-Unis",    toC:[-95,38],  type:"nickel", unit:"kt", hist:{2000:50,2010:60,2015:70,2022:80,2023:80}},
  // MINERAI DE FER (Mt)
  {from:"Australie", fromC:[133,-27], to:"Chine",         toC:[104,35],  type:"iron_ore", unit:"Mt", hist:{2000:60,2005:130,2010:300,2015:540,2020:680,2022:700,2023:720}},
  {from:"Australie", fromC:[133,-27], to:"Japon",         toC:[138,37],  type:"iron_ore", unit:"Mt", hist:{2000:55,2005:65,2010:70,2015:75,2022:80,2023:78}},
  {from:"Australie", fromC:[133,-27], to:"Corée du Sud",  toC:[127,37],  type:"iron_ore", unit:"Mt", hist:{2000:30,2010:45,2015:50,2022:55,2023:54}},
  {from:"Brésil",    fromC:[-55,-10], to:"Chine",         toC:[104,35],  type:"iron_ore", unit:"Mt", hist:{2000:40,2005:80,2010:150,2015:190,2020:210,2022:220,2023:225}},
  {from:"Brésil",    fromC:[-55,-10], to:"Japon",         toC:[138,37],  type:"iron_ore", unit:"Mt", hist:{2000:20,2010:22,2015:25,2022:25,2023:24}},
  {from:"Afrique du Sud", fromC:[25,-29], to:"Chine",     toC:[104,35],  type:"iron_ore", unit:"Mt", hist:{2000:10,2010:30,2015:45,2022:60,2023:62}},
  {from:"Inde",      fromC:[78,22],   to:"Chine",         toC:[104,35],  type:"iron_ore", unit:"Mt", hist:{2000:5,2010:80,2015:15,2020:20,2022:25,2023:28}}
];

var metalFlowsLayerItems = [];

function getMetalFlowValue(fl, year) {
  if (!fl.hist) return fl.value || 0;
  var keys = Object.keys(fl.hist).map(Number).sort(function(a,b){return a-b;});
  if (year <= keys[0]) return fl.hist[keys[0]];
  if (year >= keys[keys.length-1]) return fl.hist[keys[keys.length-1]];
  for (var i=0; i<keys.length-1; i++) {
    if (year >= keys[i] && year <= keys[i+1]) {
      var t = (year-keys[i])/(keys[i+1]-keys[i]);
      return Math.round(fl.hist[keys[i]]*(1-t) + fl.hist[keys[i+1]]*t);
    }
  }
  return 0;
}

var METAL_THRESHOLD = {copper:50, lithium:0.5, cobalt:0.5, nickel:5, iron_ore:5};

function buildMetalFlowsLayer() {
  if (!layerVis.metal_flows) return;
  var year = typeof currentYear !== 'undefined' ? currentYear : 2022;
  var byType = {};
  METAL_FLOWS.forEach(function(fl) {
    var v = getMetalFlowValue(fl, year);
    if (!byType[fl.type]) byType[fl.type] = [];
    byType[fl.type].push({fl:fl, v:v});
  });
  Object.keys(byType).forEach(function(type) {
    var items = byType[type];
    var thresh = METAL_THRESHOLD[type] || 1;
    var active = items.filter(function(x){return x.v >= thresh;});
    if (!active.length) return;
    var maxV = Math.max.apply(null, active.map(function(x){return x.v;}));
    var col = METAL_COLORS[type] || '#aaa';
    active.forEach(function(item) {
      var fl = item.fl, val = item.v;
      var x1=fl.fromC[0], y1=fl.fromC[1], x2=fl.toC[0], y2=fl.toC[1];
      if (x2-x1>180) x2-=360; else if (x2-x1<-180) x2+=360;
      var weight = 1.5 + (val/maxV)*4.5;
      var mx=(x1+x2)/2, my=(y1+y2)/2;
      var dx=x2-x1, dy=y2-y1, len=Math.sqrt(dx*dx+dy*dy)||1;
      var nx=-dy/len, ny=dx/len;
      var offset=Math.min(len*0.3,22);
      var cx=mx+nx*offset, cy=my+ny*offset;
      var rawPts=[];
      for (var i=0;i<=60;i++) {
        var t=i/60;
        rawPts.push([(1-t)*(1-t)*y1+2*(1-t)*t*cy+t*t*y2,(1-t)*(1-t)*x1+2*(1-t)*t*cx+t*t*x2]);
      }
      var segments=splitArcAtAntimeridian(rawPts);
      var typeLabel = {copper:'Cuivre',lithium:'Lithium',cobalt:'Cobalt',nickel:'Nickel',iron_ore:'Minerai de fer'}[type]||type;
      var tip='<b>'+typeLabel+' : '+fl.from+' \u2192 '+fl.to+'</b><br>'+val+' '+fl.unit+' ('+year+')';
      segments.forEach(function(seg){
        var pl=L.polyline(seg,{color:col,weight:weight,opacity:0.8,className:'flow-anim'});
        pl.bindTooltip(tip,{sticky:true});
        pl._flowFrom=fl.from; pl._flowTo=fl.to;
        pl.addTo(map);
        metalFlowsLayerItems.push(pl);
      });
      var fakeGroup={addLayer:function(item){item.addTo(map);metalFlowsLayerItems.push(item);}};
      addArrowHead(fakeGroup,segments,col,0.85,{from:fl.from,to:fl.to});
    });
  });
}

function toggleMetalFlowsLayer() {
  layerVis.metal_flows = !layerVis.metal_flows;
  metalFlowsLayerItems.forEach(function(item){try{map.removeLayer(item);}catch(e){}});
  metalFlowsLayerItems.length = 0;
  if (layerVis.metal_flows) buildMetalFlowsLayer();
}

function rebuildMetalFlowsLayer() {
  metalFlowsLayerItems.forEach(function(item){try{map.removeLayer(item);}catch(e){}});
  metalFlowsLayerItems.length = 0;
  buildMetalFlowsLayer();
}
"""

METAL_UPDATE_JS = r"""
function updateMetalProdForYear(year) {
  function interp(byYear, y) {
    var keys = Object.keys(byYear).map(Number).sort(function(a,b){return a-b;});
    if (y <= keys[0]) return byYear[keys[0]];
    if (y >= keys[keys.length-1]) return byYear[keys[keys.length-1]];
    for (var i=0;i<keys.length-1;i++) {
      if (y>=keys[i] && y<=keys[i+1]) {
        var t=(y-keys[i])/(keys[i+1]-keys[i]);
        return Math.round(byYear[keys[i]]*(1-t)+byYear[keys[i+1]]*t);
      }
    }
    return byYear[keys[0]];
  }
  Object.keys(METAL_PROD_DATA).forEach(function(metric) {
    var countryData = METAL_PROD_DATA[metric];
    Object.values(ENERGY_DATA).forEach(function(d) {
      var iso3 = d.iso3;
      if (iso3 && countryData[iso3]) d[metric] = interp(countryData[iso3], year);
    });
  });
}
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert METAL_FLOWS before loadCerealProductionData
ANCHOR1 = 'function loadCerealProductionData()'
if ANCHOR1 in content:
    content = content.replace(ANCHOR1, METAL_FLOWS_JS + '\n' + ANCHOR1)
    print("OK: METAL_FLOWS + buildMetalFlowsLayer inserted")
else:
    print("ERROR: anchor 1 not found")

# Insert updateMetalProdForYear before updateCerealProdForYear
ANCHOR2 = 'function updateCerealProdForYear(year)'
if ANCHOR2 in content:
    content = content.replace(ANCHOR2, METAL_UPDATE_JS + '\n' + ANCHOR2)
    print("OK: updateMetalProdForYear inserted")
else:
    print("ERROR: anchor 2 not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done step 3")
