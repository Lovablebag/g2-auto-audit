from pathlib import Path
p = Path('index.html')
t = p.read_text(encoding='utf-8', errors='replace')

# Remove duplicate page subtitle
old_sub = '<div class="page-title">Hotel Search</div>\n  <div class="page-sub">Search by city or whole country \u2014 hotels, hostels, motels, resorts, residences, B&Bs, aparthotels, lodges \u2014 and export to Excel</div>'
new_sub = '<div class="page-title">Hotel Search</div>'
if old_sub in t:
    t = t.replace(old_sub, new_sub, 1)
    print('removed page-sub')
else:
    # fallback em dash variants
    import re
    t2, n = re.subn(
        r'(<div class="page-title">Hotel Search</div>)\s*<div class="page-sub">[^<]*</div>',
        r'\1',
        t,
        count=1,
    )
    t = t2
    print('page-sub regex', n)

# Remove in-card description
old_desc = '<div class="section-desc">Search by city or whole country - hotels, hostels, motels, resorts, residences, B&Bs, aparthotels, lodges - and export to Excel</div>'
if old_desc in t:
    t = t.replace(old_desc, '', 1)
    print('removed section-desc')
else:
    import re
    t2, n = re.subn(r'<div class="section-desc">Search by city or whole country[^<]*</div>', '', t, count=1)
    t = t2
    print('section-desc regex', n)

# Hide API key field once a key is stored; tiny change-key control
old_field = '''        <div class="hs-field">
          <label for="hs-apikey">LiteAPI key</label>
          <input id="hs-apikey" type="password" placeholder="sand_ or live_ key" style="min-width:260px" autocomplete="off">
        </div>'''
new_field = '''        <div class="hs-field" id="hs-key-wrap">
          <label for="hs-apikey">LiteAPI key</label>
          <input id="hs-apikey" type="password" placeholder="saved after first search" style="min-width:260px" autocomplete="off">
          <button type="button" class="btn-reset" id="hs-key-clear" style="display:none;margin-top:6px">Change key</button>
        </div>'''
if old_field in t:
    t = t.replace(old_field, new_field, 1)
    print('updated key field')
else:
    print('key field already updated or missing')

# Restore key and hide field if stored
old_boot = "(function(){try{const k=localStorage.getItem('g2.liteapi.key'); const el=document.getElementById('hs-apikey'); if(el&&k) el.value=k;}catch(e){}})();"
new_boot = '''(function(){
    function applyHsKey(){
      try{
        const k=localStorage.getItem('g2.liteapi.key');
        const el=document.getElementById('hs-apikey');
        const wrap=document.getElementById('hs-key-wrap');
        const clr=document.getElementById('hs-key-clear');
        if(el&&k){
          el.value=k;
          if(wrap) wrap.style.display='none';
          if(clr){ clr.style.display='inline-block'; clr.onclick=function(){ if(wrap) wrap.style.display=''; el.value=''; el.focus(); }; }
        }
      }catch(e){}
    }
    applyHsKey();
    const keyEl=document.getElementById('hs-apikey');
    if(keyEl) keyEl.addEventListener('change', function(){ const v=keyEl.value.trim(); if(v){ try{localStorage.setItem('g2.liteapi.key', v);}catch(e){} } });
  })();'''
if old_boot in t:
    t = t.replace(old_boot, new_boot, 1)
    print('updated boot')
else:
    print('boot snippet missing', old_boot in t)

p.write_text(t, encoding='utf-8')
print('done', p.stat().st_size)
