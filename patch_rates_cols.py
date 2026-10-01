from pathlib import Path
p = Path('rates.html')
t = p.read_text(encoding='utf-8')
if '<th class="num">Per night</th>' not in t:
    raise SystemExit('per night header missing')
t = t.replace('<th class="num">Per night</th>', '')
t = t.replace('<td class="num">${money(r.perNight, r.currency)}</td>\n        ', '')
t = t.replace('<th>Board</th><th>Cancellation</th>', '<th>Board</th><th>Rate type</th><th>Supplier</th><th>Cancellation</th>', 1)
marker = '<td>${r.refundable?'
insert = '<td>${esc(r.rateType||\'\u2014\')}</td>\n        <td>${esc(r.supplier||\'\u2014\')}</td>\n        ' + marker
if marker not in t:
    raise SystemExit('refundable marker missing')
t = t.replace(marker, insert, 1)
t = t.replace('colspan="6"', 'colspan="7"')
if 'Per night' in t or 'Rate type' not in t:
    raise SystemExit('table patch failed')
p.write_text(t, encoding='utf-8')
api = Path('api/liteapi-rates.js')
a = api.read_text(encoding='utf-8')
needle = "refundableTag: tag || '',"
insert_api = needle + "\n      rateType: room.rateType || '',\n      supplier: room.supplier || '',"
if 'rateType: room.rateType' not in a:
    if needle not in a:
        raise SystemExit('api needle missing')
    a = a.replace(needle, insert_api, 1)
    api.write_text(a, encoding='utf-8')
print('patched')
