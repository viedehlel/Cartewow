import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add logScale support to getMetricColor
OLD_COLOR = """function getMetricColor(value, metric) {
  const cfg = METRIC_CONFIG[metric];
  if (value == null) return null;
  if (value === 0) return cfg.colors[0];
  const displayVal = value * (cfg.displayFactor || 1);
  const t = Math.min(displayVal / cfg.max, 1);"""

NEW_COLOR = """function getMetricColor(value, metric) {
  const cfg = METRIC_CONFIG[metric];
  if (!cfg) return null;
  if (value == null) return null;
  if (value === 0) return cfg.colors[0];
  const displayVal = value * (cfg.displayFactor || 1);
  let t;
  if (cfg.logScale) {
    t = Math.min(Math.log(displayVal + 1) / Math.log(cfg.max + 1), 1);
  } else {
    t = Math.min(displayVal / cfg.max, 1);
  }"""

if OLD_COLOR in content:
    content = content.replace(OLD_COLOR, NEW_COLOR)
    print('OK: logScale ajoute a getMetricColor')
else:
    print('ERROR: getMetricColor anchor not found')

# 2. Patch skewed metrics: add logScale + fix max
def patch_metric(content, metric, new_max=None, add_log=False):
    pattern = r'(' + re.escape(metric) + r'\s*:\s*\{[^}]+)\}'
    m = re.search(pattern, content)
    if not m:
        print(f'  NOT FOUND: {metric}')
        return content
    old_block = m.group(0)
    new_block = old_block
    if new_max:
        new_block = re.sub(r'max\s*:\s*[\d.]+', f'max: {new_max}', new_block)
    if add_log and 'logScale' not in new_block:
        new_block = new_block.rstrip('}') + ', logScale: true}'
    if new_block != old_block:
        content = content.replace(old_block, new_block, 1)
        print(f'  OK: {metric} -> max={new_max}, logScale={add_log}')
    return content

content = patch_metric(content, 'oil_prod_mbd', new_max=12,   add_log=True)
content = patch_metric(content, 'gas_prod_bcm',  new_max=500,  add_log=True)
content = patch_metric(content, 'coal_mt',        new_max=2000, add_log=True)
content = patch_metric(content, 'nuclear_twh',    new_max=400,  add_log=True)
content = patch_metric(content, 'renewables_gw',  new_max=1000, add_log=True)
content = patch_metric(content, 'co2_mt',         new_max=5000, add_log=True)

with open(r'c:\Users\vkadd\Desktop\Projet carte\carte_energie.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
