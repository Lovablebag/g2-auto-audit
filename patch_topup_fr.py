from pathlib import Path
p = Path('topup.html')
t = p.read_text(encoding='utf-8')
fr = r'''
const FR_TPL={
  topupOne:'Pourriez-vous nous accorder un **top-up** pour **{property}** pour les dates ci-dessous ?',
  topupMany:'Pourriez-vous nous accorder de la **disponibilit\u00e9 suppl\u00e9mentaire** pour vos \u00e9tablissements \u00e0 {city} pour les dates ci-dessous ?',
  releaseOne:'Pourriez-vous **ramener le release \u00e0 0 jour** pour **{property}** pour les dates ci-dessous, afin que le restant de disponibilit\u00e9 soit remis en vente ?',
  releaseMany:'Pourriez-vous **ramener le release \u00e0 0 jour** pour vos \u00e9tablissements \u00e0 {city} pour les dates ci-dessous, afin que le restant de disponibilit\u00e9 soit remis en vente ?',
  releaseAlsoOne:'Pourriez-vous \u00e9galement **ramener le release \u00e0 0 jour** pour les dates ci-dessous, afin que le restant de disponibilit\u00e9 soit remis en vente ?',
  releaseAlsoMany:'Pourriez-vous \u00e9galement **ramener le release \u00e0 0 jour** pour vos \u00e9tablissements \u00e0 {city} pour les dates ci-dessous, afin que le restant de disponibilit\u00e9 soit remis en vente ?',
  opening:"J'esp\u00e8re que vous allez bien.",
  closing:"Merci beaucoup d'avance pour votre v\u00e9rification et votre aide !",
  regards:'Cordialement,',
  signature:''
};
const activeTpl=()=>S.lang==='fr'?FR_TPL:P.tpl;
'''
if 'const FR_TPL' not in t:
    anchor = 'const TPL_LABELS='
    if anchor not in t:
        raise SystemExit('tpl labels missing')
    t = t.replace(anchor, fr + anchor, 1)
old = 'P.threshold=s.threshold==null?1:s.threshold'
new = old + ";P.lang=s.lang==='fr'?'fr':'en'"
if 'P.lang=' not in t:
    if old not in t:
        raise SystemExit('load missing')
    t = t.replace(old, new, 1)
old = "grouping:'each',combine:true,active:0"
new = "grouping:'each',combine:true,lang:P.lang||'en',active:0"
if "lang:P.lang" not in t:
    if old not in t:
        raise SystemExit('state missing')
    t = t.replace(old, new, 1)
old = '''function defSubject(e){
  const one=e.items.length===1,c=cityOf(e),p=one?e.items[0].prop:'';
  if(e.type==='combined')return one?'Availability & Release Request for '+p:'Availability & Release Request - '+(c?c+' ':'')+'Properties';
  if(e.type==='topup')return one?'Top-up for '+p:'Availability Request - '+(c?c+' ':'')+'Properties';
  return one?'Release reduction for '+p:'Release Request - '+(c?c+' ':'')+'Properties';
}'''
new = '''function defSubject(e){
  const one=e.items.length===1,c=cityOf(e),p=one?e.items[0].prop:'',fr=S.lang==='fr';
  if(e.type==='combined')return one?(fr?'Disponibilit\u00e9s et release pour ':'Availability & Release Request for ')+p:(fr?'Demande de disponibilit\u00e9s et de release - ':'Availability & Release Request - ')+(c?c+' ':'')+(fr?'\u00e9tablissements':'Properties');
  if(e.type==='topup')return one?(fr?'Top-up pour ':'Top-up for ')+p:(fr?'Demande de disponibilit\u00e9s - ':'Availability Request - ')+(c?c+' ':'')+(fr?'\u00e9tablissements':'Properties');
  return one?(fr?'R\u00e9duction du release pour ':'Release reduction for ')+p:(fr?'Demande de release - ':'Release Request - ')+(c?c+' ':'')+(fr?'\u00e9tablissements':'Properties');
}'''
old = old.encode().decode('unicode_escape')
new = new.encode().decode('unicode_escape')
if old not in t:
    raise SystemExit('subject missing')
t = t.replace(old, new, 1)
t = t.replace("const greetOf=e=>P.greet[e.key]!=null?P.greet[e.key]:'Team';", "const greetOf=e=>P.greet[e.key]!=null?P.greet[e.key]:(S.lang==='fr'?'\u00e0 tous':'Team');")
t = t.replace("<span>Hi</span><input id=\"greet\"", "<span>'+(S.lang==='fr'?'Bonjour':'Hi')+'</span><input id=\"greet\"")
t = t.replace('const one=e.items.length===1,T=P.tpl,ps=', 'const one=e.items.length===1,T=activeTpl(),ps=')
t = t.replace("'Hi '+esc(greetOf(e))+','", "(S.lang==='fr'?'Bonjour ':'Hi ')+esc(greetOf(e))+','")
t = t.replace("'Hi '+greetOf(e)+',\\n\\n'", "(S.lang==='fr'?'Bonjour ':'Hi ')+greetOf(e)+',\\n\\n'")
cols = "['Room/Category','Date','Allotment','Freesale','Total','Sold','Available'].concat(top?['Top-Up']:[],['Yes/No'])"
cols_fr = "(S.lang==='fr'?['Chambre / Cat\u00e9gorie','Date','Allotement','Freesale','Total','Vendu','Disponible']:['Room/Category','Date','Allotment','Freesale','Total','Sold','Available']).concat(top?[S.lang==='fr'?'Top-up':'Top-Up']:[],[S.lang==='fr'?'Oui/Non':'Yes/No'])"
if cols not in t:
    raise SystemExit('text headers missing')
t = t.replace(cols, cols_fr.encode().decode('unicode_escape'), 1)
th = "th('Room/Category')+th('Date')+th('Allotment',1)+th('Freesale',1)+th('Total',1)+th('Sold',1)+th('Available',1)+(top?th('Top-Up'):'')+th('Yes/No')"
th_fr = "th(S.lang==='fr'?'Chambre / Cat\u00e9gorie':'Room/Category')+th('Date')+th(S.lang==='fr'?'Allotement':'Allotment',1)+th('Freesale',1)+th('Total',1)+th(S.lang==='fr'?'Vendu':'Sold',1)+th(S.lang==='fr'?'Disponible':'Available',1)+(top?th(S.lang==='fr'?'Top-up':'Top-Up'):'')+th(S.lang==='fr'?'Oui/Non':'Yes/No')"
if th not in t:
    raise SystemExit('html headers missing')
t = t.replace(th, th_fr.encode().decode('unicode_escape'), 1)
ui_old = '<label class="chk"><input type="checkbox" data-action="combine"'
ui_new = '<div class="seg" role="group" aria-label="Language"><button data-action="lang" data-l="en" aria-pressed="'+(S.lang!=='fr')+'">English</button><button data-action="lang" data-l="fr" aria-pressed="'+(S.lang==='fr')+'">Fran\u00e7ais</button></div>' + ui_old
# The UI string is inside a JS single-quoted HTML builder. Insert as source text.
ui_new = '''<div class="seg" role="group" aria-label="Language"><button data-action="lang" data-l="en" aria-pressed="'+(S.lang!==\'fr\')+'">English</button><button data-action="lang" data-l="fr" aria-pressed="'+(S.lang===\'fr\')+'">Fran\u00e7ais</button></div><label class="chk"><input type="checkbox" data-action="combine"'''
if 'data-action="lang"' not in t:
    if ui_old not in t:
        raise SystemExit('filters missing')
    t = t.replace(ui_old, ui_new.encode().decode('unicode_escape'), 1)
hook = "else if(a==='combine'){S.combine=b.checked;S.active=0;render()}"
hook_new = hook + "\n  else if(a==='lang'){S.lang=b.dataset.l;S.subj={};P.lang=S.lang;save();render()}"
if "a==='lang'" not in t:
    if hook not in t:
        raise SystemExit('click missing')
    t = t.replace(hook, hook_new, 1)
if 'const FR_TPL' not in t or "a==='lang'" not in t:
    raise SystemExit('incomplete')
p.write_text(t, encoding='utf-8')
print('patched', t.count('Fran'))
