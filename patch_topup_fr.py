from pathlib import Path
p = Path('topup.html')
t = p.read_text(encoding='utf-8')

def need(old, label):
    if old not in t:
        raise SystemExit(label)

fr = (
"const FR_TPL={topupOne:'Pourriez-vous nous accorder un **top-up** pour **{property}** pour les dates ci-dessous ?',"
"topupMany:'Pourriez-vous nous accorder de la **disponibilite supplementaire** pour vos etablissements a {city} pour les dates ci-dessous ?',"
"releaseOne:'Pourriez-vous **ramener le release a 0 jour** pour **{property}** pour les dates ci-dessous, afin que le restant de disponibilite soit remis en vente ?',"
"releaseMany:'Pourriez-vous **ramener le release a 0 jour** pour vos etablissements a {city} pour les dates ci-dessous, afin que le restant de disponibilite soit remis en vente ?',"
"releaseAlsoOne:'Pourriez-vous egalement **ramener le release a 0 jour** pour les dates ci-dessous, afin que le restant de disponibilite soit remis en vente ?',"
"releaseAlsoMany:'Pourriez-vous egalement **ramener le release a 0 jour** pour vos etablissements a {city} pour les dates ci-dessous, afin que le restant de disponibilite soit remis en vente ?',"
"opening:\"J'espere que vous allez bien.\",closing:\"Merci beaucoup d'avance pour votre verification et votre aide !\",regards:'Cordialement,',signature:''};\n"
"const activeTpl=()=>S.lang==='fr'?FR_TPL:P.tpl;\n"
)
# Use real French accents via unicode escapes in the JS source, not in this file.
fr = fr.replace('disponibilite', 'disponibilit\u00e9').replace('supplementaire', 'suppl\u00e9mentaire').replace('etablissements', '\u00e9tablissements').replace(' a {city}', ' \u00e0 {city}').replace('egalement', '\u00e9galement').replace('J\'espere', 'J\'esp\u00e8re').replace('verification', 'v\u00e9rification')
if 'const FR_TPL' not in t:
    need('const TPL_LABELS=', 'labels')
    t = t.replace('const TPL_LABELS=', fr + 'const TPL_LABELS=', 1)
if 'P.lang=' not in t:
    need('P.threshold=s.threshold==null?1:s.threshold', 'load')
    t = t.replace('P.threshold=s.threshold==null?1:s.threshold', "P.threshold=s.threshold==null?1:s.threshold;P.lang=s.lang==='fr'?'fr':'en'", 1)
if 'lang:P.lang' not in t:
    need("grouping:'each',combine:true,active:0", 'state')
    t = t.replace("grouping:'each',combine:true,active:0", "grouping:'each',combine:true,lang:P.lang||'en',active:0", 1)
need("if(e.type==='topup')return one?'Top-up for '+p:'Availability Request - '", 'subject')
t = t.replace(
"function defSubject(e){\n  const one=e.items.length===1,c=cityOf(e),p=one?e.items[0].prop:'';\n  if(e.type==='combined')return one?'Availability & Release Request for '+p:'Availability & Release Request - '+(c?c+' ':'')+'Properties';\n  if(e.type==='topup')return one?'Top-up for '+p:'Availability Request - '+(c?c+' ':'')+'Properties';\n  return one?'Release reduction for '+p:'Release Request - '+(c?c+' ':'')+'Properties';\n}",
"function defSubject(e){\n  const one=e.items.length===1,c=cityOf(e),p=one?e.items[0].prop:'',fr=S.lang==='fr';\n  if(e.type==='combined')return one?(fr?'Disponibilites et release pour ':'Availability & Release Request for ')+p:(fr?'Demande de disponibilites et de release - ':'Availability & Release Request - ')+(c?c+' ':'')+(fr?'etablissements':'Properties');\n  if(e.type==='topup')return one?(fr?'Top-up pour ':'Top-up for ')+p:(fr?'Demande de disponibilites - ':'Availability Request - ')+(c?c+' ':'')+(fr?'etablissements':'Properties');\n  return one?(fr?'Reduction du release pour ':'Release reduction for ')+p:(fr?'Demande de release - ':'Release Request - ')+(c?c+' ':'')+(fr?'etablissements':'Properties');\n}")
t = t.replace('Disponibilites', 'Disponibilit\u00e9s').replace('etablissements', '\u00e9tablissements').replace('Reduction du release', 'R\u00e9duction du release')
t = t.replace("const greetOf=e=>P.greet[e.key]!=null?P.greet[e.key]:'Team';", "const greetOf=e=>P.greet[e.key]!=null?P.greet[e.key]:(S.lang==='fr'?'\u00e0 tous':'Team');")
t = t.replace('<span>Hi</span><input id="greet"', '<span>\'+(S.lang===\'fr\'?\'Bonjour\':\'Hi\')+\'</span><input id="greet"')
# The previous line is too quoted. Do a simpler marker replace.
t = t.replace('<span>Hi</span>', "<span>'+(S.lang==='fr'?'Bonjour':'Hi')+'</span>")
t = t.replace('const one=e.items.length===1,T=P.tpl,ps=', 'const one=e.items.length===1,T=activeTpl(),ps=')
t = t.replace("'Hi '+esc(greetOf(e))+','", "(S.lang==='fr'?'Bonjour ':'Hi ')+esc(greetOf(e))+','")
t = t.replace("'Hi '+greetOf(e)+',\\n\\n'", "(S.lang==='fr'?'Bonjour ':'Hi ')+greetOf(e)+',\\n\\n'")
old = "['Room/Category','Date','Allotment','Freesale','Total','Sold','Available'].concat(top?['Top-Up']:[],['Yes/No'])"
new = "(S.lang==='fr'?['Chambre','Date','Allotement','Freesale','Total','Vendu','Disponible']:['Room/Category','Date','Allotment','Freesale','Total','Sold','Available']).concat(top?[S.lang==='fr'?'Top-up':'Top-Up']:[],[S.lang==='fr'?'Oui/Non':'Yes/No'])"
need(old, 'text headers')
t = t.replace(old, new, 1)
old = "th('Room/Category')+th('Date')+th('Allotment',1)+th('Freesale',1)+th('Total',1)+th('Sold',1)+th('Available',1)+(top?th('Top-Up'):'')+th('Yes/No')"
new = "th(S.lang==='fr'?'Chambre':'Room/Category')+th('Date')+th(S.lang==='fr'?'Allotement':'Allotment',1)+th('Freesale',1)+th('Total',1)+th(S.lang==='fr'?'Vendu':'Sold',1)+th(S.lang==='fr'?'Disponible':'Available',1)+(top?th(S.lang==='fr'?'Top-up':'Top-Up'):'')+th(S.lang==='fr'?'Oui/Non':'Yes/No')"
need(old, 'html headers')
t = t.replace(old, new, 1)
old = '<label class="chk"><input type="checkbox" data-action="combine"'
new = '<div class="seg" role="group" aria-label="Language"><button data-action="lang" data-l="en" aria-pressed="\'+(S.lang!==\'fr\')+\'">English</button><button data-action="lang" data-l="fr" aria-pressed="\'+(S.lang===\'fr\')+\'">Francais</button></div>' + old
need(old, 'filters')
t = t.replace(old, new, 1)
old = "else if(a==='combine'){S.combine=b.checked;S.active=0;render()}"
new = old + "\n  else if(a==='lang'){S.lang=b.dataset.l;S.subj={};P.lang=S.lang;save();render()}"
need(old, 'click')
t = t.replace(old, new, 1)
if 'const FR_TPL' not in t or "a==='lang'" not in t or 'Bonjour' not in t:
    raise SystemExit('incomplete')
p.write_text(t, encoding='utf-8')
print('ok')
