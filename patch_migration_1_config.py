import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. METRIC_CONFIG entries
OLD = '  // \u2500\u2500 CO2 & PRIX \u2500\u2500'
NEW = '''  // -- MIGRATIONS --
  refugees_out_k: { label:"R\u00e9fugi\u00e9s quittant le pays", unit:"k pers.", max:8000, key:"refugees_out_k", baseColor:'#ef4444', colors:['#fff1f2','#fecdd3','#fca5a5','#ef4444','#b91c1c','#450a0a'], grad:"linear-gradient(to right,#fff1f2,#fecdd3,#fca5a5,#ef4444,#b91c1c,#450a0a)" },
  refugees_in_k:  { label:"R\u00e9fugi\u00e9s accueillis",       unit:"k pers.", max:4000, key:"refugees_in_k",  baseColor:'#3b82f6', colors:['#eff6ff','#bfdbfe','#60a5fa','#3b82f6','#1d4ed8','#1e3a8a'], grad:"linear-gradient(to right,#eff6ff,#bfdbfe,#60a5fa,#3b82f6,#1d4ed8,#1e3a8a)" },
  idp_k:          { label:"D\u00e9plac\u00e9s internes (PDI)",    unit:"k pers.", max:8000, key:"idp_k",          baseColor:'#f97316', colors:['#fff7ed','#fed7aa','#fb923c','#f97316','#c2410c','#431407'], grad:"linear-gradient(to right,#fff7ed,#fed7aa,#fb923c,#f97316,#c2410c,#431407)" },
  // \u2500\u2500 CO2 & PRIX \u2500\u2500'''

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK: METRIC_CONFIG migrations added")
else:
    print("ERROR: CO2 anchor not found")

# 2. Sidebar group after Metaux group
OLD2 = '      </div>\n    </div>\n\n    <div id="legend">'
NEW2 = '''      <div class="layer-group">
        <div class="layer-group-header" onclick="toggleGroup('grp-migration')">
          <span class="layer-group-title">&#128694; Migrations</span>
          <span class="layer-group-arrow" id="arr-grp-migration">&#9658;</span>
        </div>
        <div class="layer-group-body collapsed" id="grp-migration">
          <div style="font-size:10px;color:#8b949e;margin-bottom:6px">Source : UNHCR — donn&eacute;es annuelles</div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#ef4444"></span>R&eacute;fugi&eacute;s quittant (k)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-ref-out" value="refugees_out_k" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#3b82f6"></span>R&eacute;fugi&eacute;s accueillis (k)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-ref-in" value="refugees_in_k" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#f97316"></span>D&eacute;plac&eacute;s internes (k)</span>
            <label class="toggle-switch"><input type="checkbox" id="mc-idp" value="idp_k" onchange="onMetricChange()"><span class="toggle-slider"></span></label>
          </div>
          <div class="toggle-row">
            <span class="toggle-label"><span class="toggle-dot" style="background:#f97316"></span>Flux migratoires</span>
            <label class="toggle-switch"><input type="checkbox" id="tog-migration-flows" onchange="toggleMigrationFlowsLayer()"><span class="toggle-slider"></span></label>
          </div>
        </div>
      </div>
      </div>

    <div id="legend">'''

if OLD2 in content:
    content = content.replace(OLD2, NEW2)
    print("OK: migration sidebar group added")
else:
    print("ERROR: sidebar anchor not found")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done step 1")
