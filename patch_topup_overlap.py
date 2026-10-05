from pathlib import Path
p = Path('topup.html')
t = p.read_text(encoding='utf-8')
old = '.cols{display:flex;align-items:flex-start;gap:28px}\n.ed{flex:0 1 420px;width:420px;max-width:42%;min-width:0}\n.pv{flex:1 1 0;min-width:0;position:static;z-index:auto}\n@media(max-width:1100px){.cols{flex-direction:column}.ed{flex:1 1 auto;width:100%;max-width:none}.pv{width:100%}.top{gap:12px}}'
new = '.cols{display:grid;grid-template-columns:minmax(340px,440px) minmax(0,1fr);gap:28px;align-items:start;width:100%}\n.ed{min-width:0;width:auto;max-width:none;overflow:hidden}\n.pv{min-width:0;position:static;z-index:1;overflow:hidden}\n@media(max-width:1100px){.cols{grid-template-columns:minmax(0,1fr)}.ed,.pv{width:100%;max-width:none}.top{gap:12px}}'
if old not in t:
    raise SystemExit('cols block missing')
t = t.replace(old, new, 1)
t = t.replace('.pv{position:static}', '.pv{position:static;overflow:hidden;min-width:0}')
t = t.replace('.paper{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px 18px;overflow:auto;max-width:100%;max-height:calc(100vh - 240px)}',
              '.paper{background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px 18px;overflow:auto;max-width:100%;min-width:0;max-height:calc(100vh - 240px)}')
t = t.replace('.paper table{width:100%;display:block;overflow-x:auto}',
              '.paper table{width:max-content;min-width:100%;display:table;border-collapse:collapse}')
if 'grid-template-columns:minmax(340px,440px)' not in t:
    raise SystemExit('patch failed')
p.write_text(t, encoding='utf-8')
print('patched')
