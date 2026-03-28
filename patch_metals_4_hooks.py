import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add layerVis.metal_flows init
OLD1 = "layerVis.arms_flows = false;"
if OLD1 in content:
    content = content.replace(OLD1, OLD1 + "\n  layerVis.metal_flows = false;")
    print("OK: layerVis.metal_flows init")
else:
    print("ERROR: layerVis.arms_flows not found — trying alternative")
    # find layerVis declaration
    idx = content.find('var layerVis =')
    if idx == -1:
        idx = content.find('layerVis = {')
    print(f"layerVis found at: {idx}")

# 2. Add updateMetalProdForYear call in updateFlowsForYear
OLD2 = "  if (typeof updateCerealProdForYear === 'function') updateCerealProdForYear(year);"
NEW2 = """  if (typeof updateMetalProdForYear === 'function') updateMetalProdForYear(year);
  if (typeof updateCerealProdForYear === 'function') updateCerealProdForYear(year);"""
if OLD2 in content:
    content = content.replace(OLD2, NEW2)
    print("OK: updateMetalProdForYear hooked into updateFlowsForYear")
else:
    print("ERROR: updateCerealProdForYear hook not found")

# 3. Add rebuildMetalFlowsLayer call in updateFlowsForYear
OLD3 = "  if (typeof rebuildCerealFlowsLayer === 'function') rebuildCerealFlowsLayer();"
NEW3 = """  if (typeof rebuildCerealFlowsLayer === 'function') rebuildCerealFlowsLayer();
  if (typeof rebuildMetalFlowsLayer === 'function') rebuildMetalFlowsLayer();"""
if OLD3 in content:
    content = content.replace(OLD3, NEW3)
    print("OK: rebuildMetalFlowsLayer hooked")
else:
    print("ERROR: rebuildCerealFlowsLayer hook not found")

# 4. Add metal metrics to onMetricChange selector
OLD4 = "#mc-cereal-prod')"
NEW4 = "#mc-cereal-prod, #mc-copper, #mc-lithium, #mc-cobalt, #mc-nickel, #mc-iron, #mc-gold')"
if OLD4 in content:
    content = content.replace(OLD4, NEW4)
    print("OK: onMetricChange selector updated")
else:
    print("ERROR: onMetricChange selector not found")

# 5. Init metal prod on page load (in initTimeline, after cereal prod load)
OLD5 = "  if (typeof loadCerealProductionData === 'function') setTimeout(loadCerealProductionData, 700);"
NEW5 = """  if (typeof loadCerealProductionData === 'function') setTimeout(loadCerealProductionData, 700);
  if (typeof updateMetalProdForYear === 'function') setTimeout(function(){ updateMetalProdForYear(currentYear || 2022); }, 800);"""
if OLD5 in content:
    content = content.replace(OLD5, NEW5)
    print("OK: metal prod init on load")
else:
    print("ERROR: cereal prod load anchor not found")

# 6. Add filterFlowsByCountry support for metalFlowsLayerItems
OLD6 = "  cerealFlowsLayerItems.forEach(function(item) {"
if OLD6 in content:
    # Find the cereal filter block and add metals after it
    cereal_block = """  cerealFlowsLayerItems.forEach(function(item) {
    if (!item._flowFrom) return;
    var visible = !name || item._flowFrom === name || item._flowTo === name;
    if (visible) { try { item.addTo(map); } catch(e){} }
    else { try { map.removeLayer(item); } catch(e){} }
  });"""
    if cereal_block in content:
        content = content.replace(cereal_block, cereal_block + """
  metalFlowsLayerItems.forEach(function(item) {
    if (!item._flowFrom) return;
    var visible = !name || item._flowFrom === name || item._flowTo === name;
    if (visible) { try { item.addTo(map); } catch(e){} }
    else { try { map.removeLayer(item); } catch(e){} }
  });""")
        print("OK: filterFlowsByCountry metal support added")
    else:
        print("WARNING: cereal filter block not found exactly, skipping")
else:
    print("WARNING: cerealFlowsLayerItems not found in filter, skipping")

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done step 4")
