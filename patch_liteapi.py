from pathlib import Path
p = Path('index.html')
t = p.read_text(encoding='utf-8', errors='replace')
old = 'const HS_API_KEY = "sand_c0155ab8-c683-4f26-8f94-b5e92c5797b9";'
new = '''const HS_API_KEY_DEFAULT = "sand_c0155ab8-c683-4f26-8f94-b5e92c5797b9";
function hsApiKey(){
  const el = document.getElementById('hs-apikey');
  const typed = el && el.value.trim();
  if (typed) {
    try { localStorage.setItem('g2.liteapi.key', typed); } catch (e) {}
    return typed;
  }
  try {
    const s = localStorage.getItem('g2.liteapi.key');
    if (s && s.trim()) return s.trim();
  } catch (e) {}
  return HS_API_KEY_DEFAULT;
}'''
if old not in t:
    raise SystemExit('key const missing')
t = t.replace(old, new, 1)
old_h = '''        <div class="hs-field">
          <label for="hs-limit">Max results</label>
          <input id="hs-limit" type="number" value="50" min="1" max="200" style="width:100px">
        </div>
        <button class="btn-gen" id="hs-search-btn">Search hotels</button>'''
new_h = '''        <div class="hs-field">
          <label for="hs-limit">Max results</label>
          <input id="hs-limit" type="number" value="50" min="1" max="200" style="width:100px">
        </div>
        <div class="hs-field">
          <label for="hs-apikey">LiteAPI key</label>
          <input id="hs-apikey" type="password" placeholder="sand_ or live_ key" style="min-width:260px" autocomplete="off">
        </div>
        <button class="btn-gen" id="hs-search-btn">Search hotels</button>'''
if old_h not in t:
    raise SystemExit('toolbar missing')
t = t.replace(old_h, new_h, 1)
t = t.replace('headers: { "X-API-Key": HS_API_KEY, "Accept": "application/json" }',
              'headers: { "X-API-Key": hsApiKey(), "Accept": "application/json" }', 1)
old_err = 'if (!res.ok) throw new Error(`API error ${res.status}: ${res.statusText}`);'
new_err = '''if (!res.ok) {
      if (res.status === 401) throw new Error('LiteAPI rejected the key (401). Paste a current sandbox or live key from dash.liteapi.travel');
      throw new Error(`API error ${res.status}: ${res.statusText}`);
    }'''
if old_err not in t:
    raise SystemExit('error line missing')
t = t.replace(old_err, new_err, 1)
hook = "document.getElementById('hs-search-btn').addEventListener('click', function() { hsSearchHotels(); });"
extra = '''(function(){try{const k=localStorage.getItem('g2.liteapi.key'); const el=document.getElementById('hs-apikey'); if(el&&k) el.value=k;}catch(e){}})();
  document.getElementById('hs-search-btn').addEventListener('click', function() { hsSearchHotels(); });'''
if hook not in t:
    raise SystemExit('listener missing')
t = t.replace(hook, extra, 1)
p.write_text(t, encoding='utf-8')
print('patched', p.stat().st_size)
