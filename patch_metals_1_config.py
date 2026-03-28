import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add METRIC_CONFIG entries before CO2 section
OLD = '  // \u2500\u2500 CO2 & PRIX \u2500\u2500'
NEW = '''  // -- METAUX --
  copper_prod_kt:   { label:"Production cuivre",         unit:"kt/an",  max:6000,   key:"copper_prod_kt",   baseColor:'#b45309', colors:['#fef3c7','#fde68a','#fbbf24','#d97706','#b45309','#7c2d12'], grad:"linear-gradient(to right,#fef3c7,#fde68a,#fbbf24,#d97706,#b45309,#7c2d12)" },
  lithium_prod_kt:  { label:"Production lithium",         unit:"kt/an",  max:120,    key:"lithium_prod_kt",  baseColor:'#0ea5e9', colors:['#f0f9ff','#bae6fd','#38bdf8','#0ea5e9','#0369a1','#0c4a6e'], grad:"linear-gradient(to right,#f0f9ff,#bae6fd,#38bdf8,#0ea5e9,#0369a1,#0c4a6e)" },
  cobalt_prod_kt:   { label:"Production cobalt",          unit:"kt/an",  max:200,    key:"cobalt_prod_kt",   baseColor:'#3b82f6', colors:['#eff6ff','#bfdbfe','#60a5fa','#3b82f6','#1d4ed8','#1e3a8a'], grad:"linear-gradient(to right,#eff6ff,#bfdbfe,#60a5fa,#3b82f6,#1d4ed8,#1e3a8a)" },
  nickel_prod_kt:   { label:"Production nickel",          unit:"kt/an",  max:2000,   key:"nickel_prod_kt",   baseColor:'#94a3b8', colors:['#f8fafc','#e2e8f0','#94a3b8','#64748b','#334155','#0f172a'], grad:"linear-gradient(to right,#f8fafc,#e2e8f0,#94a3b8,#64748b,#334155,#0f172a)" },
  iron_ore_prod_mt: { label:"Production minerai de fer",  unit:"Mt/an",  max:1000,   key:"iron_ore_prod_mt", baseColor:'#78716c', colors:['#fafaf9','#e7e5e4','#a8a29e','#78716c','#44403c','#1c1917'], grad:"linear-gradient(to right,#fafaf9,#e7e5e4,#a8a29e,#78716c,#44403c,#1c1917)" },
  gold_prod_t:      { label:"Production or",              unit:"t/an",   max:500,    key:"gold_prod_t",      baseColor:'#eab308', colors:['#fefce8','#fef08a','#fde047','#eab308','#a16207','#713f12'], grad:"linear-gradient(to right,#fefce8,#fef08a,#fde047,#eab308,#a16207,#713f12)" },
  // \u2500\u2500 CO2 & PRIX \u2500\u2500'''

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK: METRIC_CONFIG metals added")
else:
    print("ERROR: CO2 anchor not found")

# 2. Add sidebar group after cereals group
OLD2 = '    </div>\n\n    <div id="legend">'
NEW2 = '''      <div class="layer-group">
        <div class="layer-group-header" onclick="toggleGroup('grp-metals')">
          <span class="layer-group-title">&#9935;&#65039; M&eacute;taux &amp; Mines</span>
          <span class="layer-group-arrow" id="arr-grp-metals">&#9658;</span>
        </div>
        <div class="layer-group-body collapsed" id="grp-metals">
          <div style="font-size:10px;color:#8b949e;margin-bottom:6px">Source : USGS Mineral Commodity Summaries</div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#b45309"></span>Cuivre (kt/an)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-copper" value="copper_prod_kt" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#0ea5e9"></span>Lithium (kt/an)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-lithium" value="lithium_prod_kt" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#3b82f6"></span>Cobalt (kt/an)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-cobalt" value="cobalt_prod_kt" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#94a3b8"></span>Nickel (kt/an)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-nickel" value="nickel_prod_kt" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#78716c"></span>Minerai de fer (Mt/an)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-iron" value="iron_ore_prod_mt" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#eab308"></span>Or (t/an)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-gold" value="gold_prod_t" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span style="display:inline-flex;gap:3px;margin-right:4px"><span class="toggle-dot" style="background:#b45309"></span><span class="toggle-dot" style="background:#0ea5e9"></span><span class="toggle-dot" style="background:#3b82f6"></span><span class="toggle-dot" style="background:#eab308"></span></span>Flux m&eacute;taux</span>
            <label class="toggle-switch"><input type="checkbox" id="tog-metal-flows" onchange="toggleMetalFlowsLayer()"><span class="toggle-slider"></span></label>
          </div>
        </div>
      </div>
    </div>

    <div id="legend">'''

if OLD2 in content:
    content = content.replace(OLD2, NEW2)
    print("OK: sidebar metals group added")
else:
    print("ERROR: sidebar anchor not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done step 1")
