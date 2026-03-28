import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Dans loadEnergyData(), apres avoir injecte dans COUNTRY_HISTORY,
#    construire aussi window._OWID_BY_M49 = {m49: {metric_app: value}} pour l'annee courante
#    et pour tous les pays OWID (y compris ceux absents de ENERGY_DATA)

OLD_INJECT = """      var enriched = 0;
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
      updateCountriesStyle();"""

NEW_INJECT = """      // Index ISO3->M49 etendu : depuis ENERGY_DATA + M49_TO_ISO3 global
      if (typeof M49_TO_ISO3 !== 'undefined') {
        Object.entries(M49_TO_ISO3).forEach(function(e){ iso3ToM49[e[1]] = e[0]; });
      }

      // Stocker l'historique complet dans COUNTRY_HISTORY (pays ENERGY_DATA)
      // ET construire _OWID_HIST_M49 pour tous les pays OWID
      window._OWID_HIST_M49 = {};  // {m49: {metric_app: {year: val}}}
      var enriched = 0;
      Object.entries(owid).forEach(function(e){
        var iso3 = e[0]; var metrics = e[1];
        var m49 = iso3ToM49[iso3];
        if (!m49) return;
        if (!window._OWID_HIST_M49[m49]) window._OWID_HIST_M49[m49] = {};
        // Injecter dans COUNTRY_HISTORY pour les pays existants
        if (ENERGY_DATA[m49]) {
          if (!COUNTRY_HISTORY[m49]) COUNTRY_HISTORY[m49] = {};
        }
        Object.entries(metrics).forEach(function(me){
          var owid_metric = me[0]; var byYear = me[1];
          var c = conv[owid_metric];
          if (!c) return;
          Object.entries(byYear).forEach(function(ye){
            var r = c(parseFloat(ye[1]));
            // COUNTRY_HISTORY pour pays existants
            if (ENERGY_DATA[m49]) {
              if (!COUNTRY_HISTORY[m49][r.key]) COUNTRY_HISTORY[m49][r.key] = {};
              COUNTRY_HISTORY[m49][r.key][ye[0]] = r.val;
            }
            // _OWID_HIST_M49 pour tous les pays
            if (!window._OWID_HIST_M49[m49][r.key]) window._OWID_HIST_M49[m49][r.key] = {};
            window._OWID_HIST_M49[m49][r.key][ye[0]] = r.val;
          });
        });
        enriched++;
      });
      console.log('OWID energy: ' + enriched + ' pays charges (' + json.updated + ')');
      updateCountriesStyle();"""

if OLD_INJECT in content:
    content = content.replace(OLD_INJECT, NEW_INJECT)
    print("OK: loadEnergyData etendu a tous les pays OWID via _OWID_HIST_M49")
else:
    print("ERROR: bloc injection non trouve")

# 2. Etendre updateCountriesStyle pour colorer les pays non-ENERGY_DATA avec les metriques energie
ENERGY_METRICS = ['oil_prod_mbd','gas_prod_bcm','coal_mt','nuclear_twh','renewables_gw',
                  'co2_mt','solar_twh','wind_twh','primary_twh','energy_per_capita_kwh']

OLD_CEREAL_BLOCK = """      if (cerealOnly && CEREAL_PROD_BY_M49[key] !== undefined) {
        var fakeD = { cereal_prod_mt: CEREAL_PROD_BY_M49[key] };
        var col = getMetricColor(fakeD.cereal_prod_mt, 'cereal_prod_mt');
        layer.setStyle({ fillColor: col || '#1a2e05', fillOpacity: 0.82, weight: 0.5, opacity: 0.7, color:"""

# Find the full cereal block to append after
idx = content.find(OLD_CEREAL_BLOCK)
if idx == -1:
    print("ERROR: cereal block not found")
else:
    # Find the end of the cereal if block (closing brace)
    block_end = content.find('\n      }', idx)
    after_cereal = content.find('\n      return;', block_end)
    if after_cereal == -1:
        after_cereal = content.find('\n      layer.setStyle({', block_end + 10)

    # Find end of the if(!d) block
    not_d_end = content.find('\n      return;\n', idx)
    if not_d_end == -1:
        not_d_end = content.find('\n    }\n', idx)

    # Simpler: just replace the pattern "if (!d) {" block
    OLD_NOT_D = """    if (!d) {
      // For countries not in ENERGY_DATA, check cereal supplemental data
      if (cerealOnly && CEREAL_PROD_BY_M49[key] !== undefined) {
        var fakeD = { cereal_prod_mt: CEREAL_PROD_BY_M49[key] };
        var col = getMetricColor(fakeD.cereal_prod_mt, 'cereal_prod_mt');
        layer.setStyle({ fillColor: col || '#1a2e05', fillOpacity: 0.82, weight: 0.5, opacity: 0.7, color:"""

    full_not_d_idx = content.find(OLD_NOT_D)
    if full_not_d_idx == -1:
        print("ERROR: if(!d) block not found")
    else:
        # Find end of this if(!d) block
        end_not_d = content.find('\n      return;\n', full_not_d_idx)
        if end_not_d == -1:
            end_not_d = content.find('      return;\n', full_not_d_idx)
        end_not_d_block = content.find('\n    }', full_not_d_idx) + 7
        print(f"if(!d) block found at {full_not_d_idx}, ends around {end_not_d_block}")
        print("Context after block:", repr(content[end_not_d_block:end_not_d_block+80]))

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
