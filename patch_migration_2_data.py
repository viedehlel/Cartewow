import sys
sys.stdout.reconfigure(encoding='utf-8')

JS = r"""
// ============================================================
//  MIGRATIONS — UNHCR data (thousands of persons)
// ============================================================
var MIGRATION_PROD_DATA = {
  refugees_out_k: {
    "VEN":{2000:0,2010:0,2015:300,2017:1000,2018:3000,2019:4000,2020:4200,2021:4800,2022:5600,2023:7700},
    "UKR":{2000:0,2010:0,2014:30,2015:30,2021:30,2022:5700,2023:6500},
    "MMR":{2000:100,2005:150,2010:400,2015:500,2016:500,2017:900,2018:1100,2019:1100,2020:1100,2021:1200,2022:1400,2023:1500},
    "COD":{2000:300,2005:450,2010:500,2015:700,2018:800,2020:900,2021:950,2022:1000,2023:1000},
    "ETH":{2015:40,2018:40,2019:50,2020:40,2021:300,2022:600,2023:700},
    "IRQ":{2000:100,2005:400,2010:400,2015:300,2018:300,2022:350,2023:380},
    "NGA":{2000:0,2010:100,2015:200,2018:250,2020:300,2022:350,2023:380},
    "YEM":{2010:0,2015:200,2017:280,2018:300,2020:300,2022:300,2023:320},
    "COL":{2000:0,2005:0,2010:0,2015:0,2018:50,2020:100,2022:150,2023:200},
    "PHL":{2000:0,2010:0,2015:20,2020:30,2022:50,2023:55}
  },
  refugees_in_k: {
    "TUR":{2000:0,2010:100,2013:500,2014:1300,2015:2000,2016:2800,2017:3200,2018:3700,2019:3600,2020:3600,2021:3700,2022:3600,2023:3600},
    "DEU":{2000:900,2005:700,2010:600,2014:700,2015:400,2016:900,2017:970,2018:1100,2019:1100,2020:1200,2021:1300,2022:2100,2023:2400},
    "COL":{2015:50,2017:500,2018:1000,2019:1400,2020:1800,2021:1700,2022:2500,2023:2900},
    "PAK":{2000:2000,2005:1100,2010:1900,2015:1500,2016:1400,2017:1400,2018:1400,2019:1400,2020:1500,2021:1500,2022:1700,2023:1700},
    "IRN":{2000:1900,2005:980,2010:1100,2015:1000,2017:980,2018:980,2019:980,2020:800,2021:800,2022:800,2023:800},
    "UGA":{2010:200,2015:500,2016:600,2017:1000,2018:1200,2019:1400,2020:1400,2021:1500,2022:1500,2023:1600},
    "POL":{2015:0,2021:10,2022:1000,2023:1000},
    "JOR":{2013:300,2014:620,2015:650,2016:660,2017:660,2018:670,2019:660,2020:660,2021:660,2022:660,2023:650},
    "ETH":{2010:500,2015:700,2016:800,2017:900,2018:900,2019:700,2020:800,2021:800,2022:900,2023:900},
    "BGD":{2015:200,2017:700,2018:900,2019:900,2020:900,2021:920,2022:950,2023:980},
    "FRA":{2000:130,2005:150,2010:190,2015:280,2018:340,2020:370,2022:400,2023:450},
    "GBR":{2000:100,2005:120,2010:110,2015:120,2018:130,2022:240,2023:250},
    "PER":{2015:0,2017:100,2018:500,2019:900,2020:1000,2021:1000,2022:1300,2023:1500},
    "IND":{2000:180,2010:180,2015:200,2020:210,2022:210,2023:215},
    "KEN":{2000:200,2005:250,2010:300,2015:470,2018:480,2020:500,2022:580,2023:600}
  },
  idp_k: {
    "COD":{2000:1600,2005:1200,2010:1700,2015:2700,2018:4000,2020:5200,2021:5600,2022:6900,2023:7200},
    "UKR":{2014:600,2015:700,2021:700,2022:5900,2023:3700},
    "ETH":{2015:700,2018:2000,2019:2100,2020:4200,2021:4200,2022:4200,2023:4400},
    "COL":{2000:900,2005:2400,2010:3900,2015:6100,2018:7100,2020:7700,2021:6800,2022:6200,2023:6200},
    "YEM":{2010:350,2015:2500,2016:3000,2017:2900,2018:3500,2019:3600,2020:4000,2021:4300,2022:4500,2023:4500},
    "IRQ":{2010:1600,2013:1200,2014:3000,2015:4000,2016:3600,2017:2600,2018:1900,2019:1400,2020:1200,2022:1200,2023:1100},
    "NGA":{2010:400,2015:1600,2017:2000,2019:2500,2020:3000,2021:3100,2022:3200,2023:3300},
    "MMR":{2010:400,2015:400,2019:500,2020:500,2021:900,2022:1500,2023:1900},
    "MOZ":{2019:700,2020:700,2021:800,2022:700,2023:650},
    "IRN":{2000:0,2010:0,2015:0,2022:0},
    "IND":{2000:500,2010:600,2015:600,2022:630,2023:650},
    "PHL":{2015:300,2018:400,2020:300,2022:300,2023:280},
    "CMR":{2015:200,2018:700,2020:900,2022:1000,2023:1000}
  }
};

var MIGRATION_FLOWS = [
  // Crise syrienne
  {from:"Syrie",       fromC:[38,35],   to:"Turquie",     toC:[35,39],   type:"migration", hist:{2012:100,2013:600,2014:1300,2015:2000,2016:2700,2018:3600,2020:3600,2022:3600,2023:3600}},
  {from:"Syrie",       fromC:[38,35],   to:"Allemagne",   toC:[10,51],   type:"migration", hist:{2013:50,2014:200,2015:500,2016:700,2017:700,2018:700,2022:700,2023:750}},
  {from:"Syrie",       fromC:[38,35],   to:"Liban",       toC:[35.5,33.8],type:"migration",hist:{2012:100,2013:600,2014:1100,2015:1200,2018:950,2020:900,2022:800,2023:800}},
  {from:"Syrie",       fromC:[38,35],   to:"Jordanie",    toC:[36.5,31], type:"migration", hist:{2012:80,2013:400,2014:620,2015:650,2018:670,2022:660,2023:650}},
  // Crise afghane
  {from:"Afghanistan", fromC:[67,33],   to:"Pakistan",    toC:[68,30],   type:"migration", hist:{2000:2000,2005:1100,2010:1900,2015:1500,2020:1500,2021:1500,2022:1700,2023:1700}},
  {from:"Afghanistan", fromC:[67,33],   to:"Iran",        toC:[53,33],   type:"migration", hist:{2000:1500,2005:900,2010:1000,2015:950,2018:950,2020:780,2022:780,2023:780}},
  {from:"Afghanistan", fromC:[67,33],   to:"Allemagne",   toC:[10,51],   type:"migration", hist:{2015:50,2016:200,2018:180,2021:100,2022:300,2023:350}},
  // Crise venezuelienne
  {from:"Venezuela",   fromC:[-65,7],   to:"Colombie",    toC:[-74,4],   type:"migration", hist:{2015:50,2017:500,2018:1000,2019:1400,2020:1800,2021:1700,2022:2500,2023:2900}},
  {from:"Venezuela",   fromC:[-65,7],   to:"Pérou",       toC:[-76,-10], type:"migration", hist:{2017:100,2018:500,2019:900,2020:1000,2021:1000,2022:1300,2023:1500}},
  {from:"Venezuela",   fromC:[-65,7],   to:"États-Unis",  toC:[-95,38],  type:"migration", hist:{2018:50,2020:100,2022:300,2023:500}},
  // Crise ukrainienne
  {from:"Ukraine",     fromC:[32,49],   to:"Allemagne",   toC:[10,51],   type:"migration", hist:{2014:50,2015:50,2016:50,2018:100,2019:100,2020:100,2021:100,2022:1000,2023:1100}},
  {from:"Ukraine",     fromC:[32,49],   to:"Pologne",     toC:[20,52],   type:"migration", hist:{2014:30,2015:30,2020:30,2021:30,2022:1500,2023:970}},
  {from:"Ukraine",     fromC:[32,49],   to:"Russie",      toC:[60,58],   type:"migration", hist:{2022:2900,2023:2600}},
  // Crise birmane / Rohingya
  {from:"Myanmar",     fromC:[96,20],   to:"Bangladesh",  toC:[90,23.5], type:"migration", hist:{2010:200,2015:400,2017:700,2018:900,2019:900,2020:900,2022:950,2023:980}},
  {from:"Myanmar",     fromC:[96,20],   to:"Thaïlande",   toC:[101,15],  type:"migration", hist:{2000:100,2005:150,2010:150,2015:100,2022:100,2023:120}},
  // Afrique sub-saharienne
  {from:"Soudan du Sud",fromC:[31,7],   to:"Ouganda",     toC:[32.3,1.3],type:"migration", hist:{2013:100,2014:400,2015:600,2016:900,2017:1000,2018:900,2020:900,2022:960,2023:1000}},
  {from:"Soudan du Sud",fromC:[31,7],   to:"Éthiopie",    toC:[39,9],    type:"migration", hist:{2013:50,2015:300,2017:400,2018:400,2020:370,2022:400,2023:420}},
  {from:"Rép. démocratique du Congo",fromC:[24,-3],to:"Ouganda",toC:[32.3,1.3],type:"migration",hist:{2010:150,2015:200,2018:350,2020:400,2022:420,2023:450}},
  {from:"Somalie",     fromC:[46,5],    to:"Éthiopie",    toC:[39,9],    type:"migration", hist:{2000:100,2005:150,2010:200,2015:250,2018:280,2020:300,2022:400,2023:430}},
  {from:"Soudan",      fromC:[31,16],   to:"Éthiopie",    toC:[39,9],    type:"migration", hist:{2020:50,2021:60,2022:70,2023:800}},
  {from:"Soudan",      fromC:[31,16],   to:"Égypte",      toC:[30,27],   type:"migration", hist:{2020:50,2022:50,2023:500}}
];

var migrationFlowsLayerItems = [];

function getMigrationFlowValue(fl, year) {
  if (!fl.hist) return 0;
  var keys = Object.keys(fl.hist).map(Number).sort(function(a,b){return a-b;});
  if (year <= keys[0]) return fl.hist[keys[0]];
  if (year >= keys[keys.length-1]) return fl.hist[keys[keys.length-1]];
  for (var i=0;i<keys.length-1;i++) {
    if (year>=keys[i] && year<=keys[i+1]) {
      var t=(year-keys[i])/(keys[i+1]-keys[i]);
      return Math.round(fl.hist[keys[i]]*(1-t)+fl.hist[keys[i+1]]*t);
    }
  }
  return 0;
}

function buildMigrationFlowsLayer() {
  if (!layerVis.migration_flows) return;
  var year = typeof currentYear !== 'undefined' ? currentYear : 2022;
  var vals = MIGRATION_FLOWS.map(function(fl){ return getMigrationFlowValue(fl, year); });
  var active = vals.filter(function(v){ return v >= 50; });
  var maxV = active.length ? Math.max.apply(null, active) : 1;
  MIGRATION_FLOWS.forEach(function(fl, idx) {
    var val = vals[idx];
    if (val < 50) return;
    var x1=fl.fromC[0],y1=fl.fromC[1],x2=fl.toC[0],y2=fl.toC[1];
    if (x2-x1>180) x2-=360; else if (x2-x1<-180) x2+=360;
    var weight=1.5+(val/maxV)*5;
    var mx=(x1+x2)/2,my=(y1+y2)/2,dx=x2-x1,dy=y2-y1,len=Math.sqrt(dx*dx+dy*dy)||1;
    var nx=-dy/len,ny=dx/len,offset=Math.min(len*0.3,22);
    var cx=mx+nx*offset,cy=my+ny*offset;
    var rawPts=[];
    for (var i=0;i<=60;i++){var t=i/60;rawPts.push([(1-t)*(1-t)*y1+2*(1-t)*t*cy+t*t*y2,(1-t)*(1-t)*x1+2*(1-t)*t*cx+t*t*x2]);}
    var segments=splitArcAtAntimeridian(rawPts);
    var tip='<b>'+fl.from+' \u2192 '+fl.to+'</b><br>'+val+' 000 personnes ('+year+')';
    segments.forEach(function(seg){
      var pl=L.polyline(seg,{color:'#f97316',weight:weight,opacity:0.75,className:'flow-anim'});
      pl.bindTooltip(tip,{sticky:true});
      pl._flowFrom=fl.from; pl._flowTo=fl.to;
      pl.addTo(map); migrationFlowsLayerItems.push(pl);
    });
    var fg={addLayer:function(item){item.addTo(map);migrationFlowsLayerItems.push(item);}};
    addArrowHead(fg,segments,'#f97316',0.85,{from:fl.from,to:fl.to});
  });
}

function toggleMigrationFlowsLayer() {
  layerVis.migration_flows=!layerVis.migration_flows;
  migrationFlowsLayerItems.forEach(function(item){try{map.removeLayer(item);}catch(e){}});
  migrationFlowsLayerItems.length=0;
  if (layerVis.migration_flows) buildMigrationFlowsLayer();
}

function rebuildMigrationFlowsLayer() {
  migrationFlowsLayerItems.forEach(function(item){try{map.removeLayer(item);}catch(e){}});
  migrationFlowsLayerItems.length=0;
  buildMigrationFlowsLayer();
}

function updateMigrationForYear(year) {
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
}
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

ANCHOR = 'function loadCerealProductionData()'
if ANCHOR in content:
    content = content.replace(ANCHOR, JS + '\n' + ANCHOR)
    print("OK: migration data + functions inserted")
else:
    print("ERROR: anchor not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done step 2")
