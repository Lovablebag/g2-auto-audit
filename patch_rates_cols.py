from pathlib import Path
import re
p = Path('rates.html')
t = p.read_text(encoding='utf-8')
if '<th>Supplier</th>' not in t:
    raise SystemExit('supplier header missing')
t = t.replace('<th>Supplier</th>', '<th>Perks and promotions</th>', 1)
t2, n = re.subn(r'<td>\$\{esc\(r\.supplier\|\|.[^<]*\)\}</td>', '<td class="hint">${esc(r.extras||\'\u2014\')}</td>', t, count=1)
if n != 1:
    raise SystemExit('supplier cell missing')
p.write_text(t2, encoding='utf-8')
api = Path('api/liteapi-rates.js')
a = api.read_text(encoding='utf-8')
a = a.replace("supplier: room.supplier || '',", "extras: extras(rate.perks, rate.promotions),")
if 'function extras' not in a:
    a = a.replace('function num(v)', "function extras(perks, promotions) {\n  const parts = [].concat(perks || [], promotions || []).map(x => {\n    if (x == null || x === '') return '';\n    if (typeof x === 'string') return x;\n    return x.name || x.description || x.title || x.text || x.code || '';\n  }).filter(Boolean);\n  return parts.join(' \u00b7 ');\n}\n\nfunction num(v)")
if "extras: extras" not in a:
    raise SystemExit('api patch failed')
api.write_text(a, encoding='utf-8')
print('patched')
