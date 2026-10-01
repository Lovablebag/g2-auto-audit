from pathlib import Path
p = Path('rates.html')
t = p.read_text(encoding='utf-8')
t = t.replace('hotel:null, hits:[], rates:[]', 'hotel:null, hits:[], more:false, rates:[]')
t = t.replace('placeholder="optional filter"', 'placeholder="part of the name"')
old = """async function findHotels(){
  read();
  if(S.country.length!==2){ S.msg='Enter a 2-letter country code.'; S.msgk='err'; return render(); }
  S.busy=true; S.msg='Searching hotels\u2026'; S.msgk=''; render();
  try{
    const j = await api({mode:'hotels', countryCode:S.country, cityName:S.city, hotelName:S.q});
    S.hits = j.hotels||[];
    S.msg = S.hits.length ? S.hits.length+' hotels. Pick one, then load rates.' : 'No hotels found. Try a city name.';
    S.msgk = S.hits.length ? 'ok' : 'warn';
  }catch(e){ S.msg=e.message; S.msgk='err'; }
  S.busy=false; render();
}"""
new = """async function findHotels(more){
  read();
  if(S.country.length!==2){ S.msg='Enter a 2-letter country code.'; S.msgk='err'; return render(); }
  if(!S.city && !S.q){ S.msg='Enter a city or part of a hotel name.'; S.msgk='err'; return render(); }
  const offset = more ? S.hits.length : 0;
  S.busy=true; S.msg = more ? 'Loading more hotels\u2026' : 'Searching hotels\u2026'; S.msgk=''; render();
  try{
    const j = await api({mode:'hotels', countryCode:S.country, cityName:S.city, hotelName:S.q, offset});
    const rows = j.hotels||[];
    S.hits = more ? S.hits.concat(rows) : rows;
    S.more = !!j.more;
    const where = j.widened ? ' in the country, not only that city' : '';
    S.msg = S.hits.length ? (S.hits.length+' hotels'+where+'. Pick one.'+(S.more?' More are available.':'')) : 'No hotels found. Try a shorter name, or clear the city.';
    S.msgk = S.hits.length ? 'ok' : 'warn';
  }catch(e){ S.msg=e.message; S.msgk='err'; }
  S.busy=false; render();
}"""
if old not in t:
    raise SystemExit('findHotels block missing')
t = t.replace(old, new, 1)
old_btn = """${S.hits.length?`<div class="hits">${S.hits.map((h,i)=>`<div class="hit"><div><b>${esc(h.name)}</b><div class="hint">${esc([h.address,h.city,h.country].filter(Boolean).join(', '))}</div></div><button class="btn sm" data-use="${i}">Use</button></div>`).join('')}</div>`:''}"""
new_btn = old_btn + """
      ${S.more?`<div class="row" style="margin-top:10px"><button class="btn sm" id="more">Load more hotels</button></div>`:''}"""
if old_btn not in t:
    raise SystemExit('hits block missing')
t = t.replace(old_btn, new_btn, 1)
t = t.replace("$('#find').onclick=findHotels;", "$('#find').onclick=()=>findHotels(false);\n  const moreBtn=document.getElementById('more'); if(moreBtn) moreBtn.onclick=()=>findHotels(true);")
p.write_text(t, encoding='utf-8')
print('patched', len(t))
