from pathlib import Path
import re
p = Path('rates.html')
t = p.read_text(encoding='utf-8')
if 'Perks and promotions' not in t:
    raise SystemExit('column missing')
t = t.replace('<th>Perks and promotions</th>', '')
t2, n = re.subn(r'<td class="hint">\$\{esc\(r\.extras\|\|.[^<]*\)\}</td>\n        ', '', t, count=1)
if n != 1:
    raise SystemExit('cell missing')
t2 = t2.replace('colspan="7"', 'colspan="6"')
if 'Perks and promotions' in t2 or 'r.extras' in t2:
    raise SystemExit('still present')
p.write_text(t2, encoding='utf-8')
print('patched')
