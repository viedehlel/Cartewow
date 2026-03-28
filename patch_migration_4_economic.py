import sys
sys.stdout.reconfigure(encoding='utf-8')

ECONOMIC_FLOWS = r"""
  // MIGRATION ECONOMIQUE / TRAVAIL (UN DESA International Migrant Stock, milliers)
  {from_iso:"MEX",from:"Mexique",      fromC:[-102,24], to_iso:"USA",to:"États-Unis",   toC:[-95,38],   type:"economic", hist:{"2000":9300,"2005":11000,"2010":11700,"2015":12000,"2020":11000,"2023":10800}},
  {from_iso:"IND",from:"Inde",         fromC:[78,22],   to_iso:"ARE",to:"Émirats Arabes Unis", toC:[54,24], type:"economic", hist:{"2000":1000,"2005":1800,"2010":2500,"2015":3000,"2020":3500,"2023":3600}},
  {from_iso:"IND",from:"Inde",         fromC:[78,22],   to_iso:"SAU",to:"Arabie Saoudite",toC:[45,24],  type:"economic", hist:{"2000":1200,"2005":1700,"2010":2000,"2015":2500,"2020":2500,"2023":2600}},
  {from_iso:"BGD",from:"Bangladesh",   fromC:[90,23.5], to_iso:"IND",to:"Inde",          toC:[78,22],   type:"economic", hist:{"2000":3000,"2005":3400,"2010":3600,"2015":3900,"2020":3900,"2023":4000}},
  {from_iso:"PAK",from:"Pakistan",     fromC:[68,30],   to_iso:"SAU",to:"Arabie Saoudite",toC:[45,24],  type:"economic", hist:{"2000":900,"2005":1200,"2010":1500,"2015":2000,"2020":2200,"2023":2300}},
  {from_iso:"PHL",from:"Philippines",  fromC:[122,13],  to_iso:"SAU",to:"Arabie Saoudite",toC:[45,24],  type:"economic", hist:{"2000:":500,"2005":700,"2010":1000,"2015":1200,"2020":1100,"2023":1000}},
  {from_iso:"PHL",from:"Philippines",  fromC:[122,13],  to_iso:"ARE",to:"Émirats Arabes Unis", toC:[54,24], type:"economic", hist:{"2000":400,"2005":600,"2010":700,"2015":800,"2020":800,"2023":800}},
  {from_iso:"IDN",from:"Indonésie",    fromC:[117,-2],  to_iso:"MYS",to:"Malaisie",      toC:[109,3],   type:"economic", hist:{"2000":1500,"2005":1800,"2010":2100,"2015":2000,"2020":2000,"2023":2100}},
  {from_iso:"NPL",from:"Népal",        fromC:[84,28],   to_iso:"IND",to:"Inde",          toC:[78,22],   type:"economic", hist:{"2000":1000,"2005":1400,"2010":1700,"2015":2000,"2020":2000,"2023":2100}},
  {from_iso:"MAR",from:"Maroc",        fromC:[-7,32],   to_iso:"FRA",to:"France",        toC:[2,47],    type:"economic", hist:{"2000":1000,"2005":1200,"2010":1350,"2015":1500,"2020":1600,"2023":1700}},
  {from_iso:"DZA",from:"Algérie",      fromC:[3,28],    to_iso:"FRA",to:"France",        toC:[2,47],    type:"economic", hist:{"2000":1400,"2005":1550,"2010":1650,"2015":1700,"2020":1800,"2023":1850}},
  {from_iso:"MAR",from:"Maroc",        fromC:[-7,32],   to_iso:"ESP",to:"Espagne",       toC:[-4,40],   type:"economic", hist:{"2000":300,"2005":600,"2010":750,"2015":800,"2020":850,"2023":900}},
  {from_iso:"TUR",from:"Turquie",      fromC:[35,39],   to_iso:"DEU",to:"Allemagne",     toC:[10,51],   type:"economic", hist:{"2000":1600,"2005":1650,"2010":1650,"2015":1700,"2020":1500,"2023":1450}},
  {from_iso:"POL",from:"Pologne",      fromC:[20,52],   to_iso:"DEU",to:"Allemagne",     toC:[10,51],   type:"economic", hist:{"2000":300,"2005":500,"2010":700,"2015":800,"2020":900,"2023":950}},
  {from_iso:"ROU",from:"Roumanie",     fromC:[25,46],   to_iso:"ITA",to:"Italie",        toC:[12,43],   type:"economic", hist:{"2000":100,"2005":400,"2010":900,"2015":1000,"2020":1100,"2023":1100}},
  {from_iso:"ROU",from:"Roumanie",     fromC:[25,46],   to_iso:"DEU",to:"Allemagne",     toC:[10,51],   type:"economic", hist:{"2000":100,"2005":300,"2010":500,"2015":700,"2020":800,"2023":850}},
  {from_iso:"CHN",from:"Chine",        fromC:[104,35],  to_iso:"USA",to:"États-Unis",    toC:[-95,38],  type:"economic", hist:{"2000":1500,"2005":1800,"2010":2000,"2015":2300,"2020":2400,"2023":2400}},
  {from_iso:"IND",from:"Inde",         fromC:[78,22],   to_iso:"USA",to:"États-Unis",    toC:[-95,38],  type:"economic", hist:{"2000":1000,"2005":1500,"2010":2000,"2015":2400,"2020":2700,"2023":3000}},
  {from_iso:"IND",from:"Inde",         fromC:[78,22],   to_iso:"CAN",to:"Canada",        toC:[-96,56],  type:"economic", hist:{"2000":400,"2005":600,"2010":700,"2015":900,"2020":1000,"2023":1500}},
  {from_iso:"SEN",from:"Sénégal",      fromC:[-14,14],  to_iso:"FRA",to:"France",        toC:[2,47],    type:"economic", hist:{"2000":150,"2010":200,"2015":230,"2020":270,"2023":290}},
  {from_iso:"GHA",from:"Ghana",        fromC:[-1,8],    to_iso:"GBR",to:"Royaume-Uni",   toC:[-2,54],   type:"economic", hist:{"2000":100,"2010":150,"2015":170,"2020":200,"2023":220}},
  {from_iso:"KOR",from:"Corée du Sud", fromC:[127,37],  to_iso:"USA",to:"États-Unis",    toC:[-95,38],  type:"economic", hist:{"2000":850,"2005":900,"2010":1100,"2015":1100,"2020":1000,"2023":1000}},
"""

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find end of MIGRATION_FLOWS array and insert economic flows before closing ];
# The array ends with the last flow entry followed by ];
OLD = """  {from:"Soudan",      fromC:[31,16],   to:"Égypte",      toC:[30,27],   type:"migration", hist:{2020:50,2022:50,2023:500}}
];"""

NEW = """  {from_iso:"SDN",from:"Soudan",      fromC:[31,16],   to_iso:"EGY",to:"Égypte",      toC:[30,27],   type:"migration", hist:{2020:50,2022:50,2023:500}},
""" + ECONOMIC_FLOWS + """
];"""

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK: economic flows added to MIGRATION_FLOWS")
else:
    print("ERROR: MIGRATION_FLOWS end not found")
    # debug
    idx = content.find('to:"Égypte",      toC:[30,27]')
    print(f"Soudan->Egypte found at: {idx}")

# 2. Update buildMigrationFlowsLayer to handle 'economic' type with different color
OLD_COLOR = "    var tip='<b>'+fl.from+' \\u2192 '+fl.to+'</b><br>'+val+' 000 personnes ('+year+')';"
NEW_COLOR = """    var flowColor = fl.type === 'economic' ? '#22d3ee' : '#f97316';
    var tip='<b>'+(fl.type==='economic'?'Migration\u00a0\u00e9conomique':'R\u00e9fugi\u00e9s')+' : '+fl.from+' \u2192 '+fl.to+'</b><br>'+val+' 000 personnes ('+year+')'+(fl.type==='economic'?' (UN DESA)':' (UNHCR)');"""

if OLD_COLOR in content:
    content = content.replace(OLD_COLOR, NEW_COLOR)
    # Also replace the hardcoded color in the polyline
    content = content.replace(
        "var pl=L.polyline(seg,{color:'#f97316',weight:weight,opacity:0.75,className:'flow-anim'});",
        "var pl=L.polyline(seg,{color:flowColor,weight:weight,opacity:0.75,className:'flow-anim'});"
    )
    content = content.replace(
        "addArrowHead(fg,segments,'#f97316',0.85,{from:fl.from,to:fl.to});",
        "addArrowHead(fg,segments,flowColor,0.85,{from:fl.from,to:fl.to});"
    )
    print("OK: economic flows colored differently (cyan vs orange)")
else:
    print("ERROR: color anchor not found")

# 3. Update sidebar to mention economic migration
OLD_SRC = '<div style="font-size:10px;color:#8b949e;margin-bottom:6px">Source : UNHCR</div>'
NEW_SRC = '<div style="font-size:10px;color:#8b949e;margin-bottom:6px">&#128994; UNHCR (r&eacute;fugi&eacute;s) &nbsp; &#128309; UN DESA (&eacute;conomique)</div>'
if OLD_SRC in content:
    content = content.replace(OLD_SRC, NEW_SRC)
    print("OK: sidebar legend updated")
else:
    print("ERROR: sidebar source not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
