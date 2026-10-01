from pathlib import Path

p = Path('rates.html')
t = p.read_text(encoding='utf-8')
t = t.replace(
    '<th>Room</th><th>Board</th><th>Cancellation</th><th class="num">Per night</th><th class="num">Stay total</th><th>Extra taxes</th>',
    '<th>Room</th><th>Board</th><th>Rate type</th><th>Supplier</th><th>Cancellation</th><th class="num">Stay total</th><th>Extra taxes</th>')
old = """        <td>${esc(r.room)}</td>
        <td>${esc(r.board||'\u2014')} ${r.boardName?`<span class=\"hint\">${esc(r.boardName)}</span>`:''}</td>
        <td>${r.refundable?'<span class=\"tag ok\">Flexible</span>':'<span class=\"tag bad\">Non-refundable</span>'}</td>
        <td class=\"num\">${money(r.perNight, r.currency)}</td>
        <td class=\"num\"><b>${money(r.total, r.currency)}</b></td>"""
# The live file uses an em dash character, not the escape. Match the actual bytes.
old = '''        <td>${esc(r.room)}</td>
        <td>${esc(r.board||'\u2014')} ${r.boardName?`<span class="hint">${esc(r.boardName)}</span>`:''}</td>
        <td>${r.refundable?'<span class="tag ok">Flexible</span>':'<span class="tag bad">Non-refundable</span>'}</td>
        <td class="num">${money(r.perNight, r.currency)}</td>
        <td class="num"><b>${money(r.total, r.currency)}</b></td>'''
new = '''        <td>${esc(r.room)}</td>
        <td>${esc(r.board||'\u2014')} ${r.boardName?`<span class="hint">${esc(r.boardName)}</span>`:''}</td>
        <td>${esc(r.rateType||'\u2014')}</td>
        <td>${esc(r.supplier||'\u2014')}</td>
        <td>${r.refundable?'<span class="tag ok">Flexible</span>':'<span class="tag bad">Non-refundable</span>'}</td>
        <td class="num"><b>${money(r.total, r.currency)}</b></td>'''
old = old.encode().decode('unicode_escape')
new = new.encode().decode('unicode_escape')
if old not in t:
    raise SystemExit('row missing')
t = t.replace(old, new, 1)
t = t.replace('colspan="6"', 'colspan="7"')
if 'Per night' in t or 'Rate type' not in t:
    raise SystemExit('table patch failed')
p.write_text(t, encoding='utf-8')

api = Path('api/liteapi-rates.js')
a = api.read_text(encoding='utf-8')
needle = 'refundableTag: tag || \'\','
insert = needle + '\n      rateType: room.rateType || \'\',\n      supplier: room.supplier || \'\','
if 'rateType: room.rateType' not in a:
    if needle not in a:
        raise SystemExit('api needle missing')
    a = a.replace(needle, insert, 1)
    api.write_text(a, encoding='utf-8')
print('patched')
