#!/usr/bin/env python3
from pathlib import Path

NAV_CSS = """
.app-nav{display:flex;align-items:center;gap:4px;margin-left:14px;flex-wrap:wrap;flex:1}
.app-nav-link{color:rgba(255,255,255,.75);text-decoration:none;font-size:12px;font-weight:600;padding:6px 11px;border-radius:20px;border:1px solid transparent;white-space:nowrap;background:none;cursor:pointer;font-family:inherit}
.app-nav-link:hover{background:rgba(255,255,255,.12);color:#fff}
.app-nav-link.is-active{background:rgba(255,255,255,.18);color:#fff;border-color:rgba(255,255,255,.2)}
#phase-entry .entry-grid{display:none}
@media(max-width:1100px){.app-nav-link{font-size:11px;padding:5px 9px}}
"""

NAV_AUDIT = """<nav class="app-nav" aria-label="Tools">
    <a class="app-nav-link" href="#files" data-nav="files">Auto Audit (Files)</a>
    <a class="app-nav-link" href="#excel" data-nav="excel">Auto Audit (Excel)</a>
    <a class="app-nav-link" href="#price" data-nav="price">Price Check</a>
    <a class="app-nav-link" href="#search" data-nav="search">Hotel Search</a>
    <a class="app-nav-link" href="./topup.html" data-nav="topup">Top-up Desk</a>
  </nav>"""

NAV_TOPUP = """<nav class="app-nav" aria-label="Tools">
    <a class="app-nav-link" href="./#files" data-nav="files">Auto Audit (Files)</a>
    <a class="app-nav-link" href="./#excel" data-nav="excel">Auto Audit (Excel)</a>
    <a class="app-nav-link" href="./#price" data-nav="price">Price Check</a>
    <a class="app-nav-link" href="./#search" data-nav="search">Hotel Search</a>
    <a class="app-nav-link is-active" href="./topup.html" data-nav="topup">Top-up Desk</a>
  </nav>"""

NAV_JS = r"""
function setAppNav(active) {
  document.querySelectorAll('.app-nav-link').forEach(function(a) {
    a.classList.toggle('is-active', a.getAttribute('data-nav') === active);
  });
}
function navKeyFromPhase(id) {
  if (id === 'phase-excel') return 'excel';
  if (id === 'phase-pricecheck') return 'price';
  if (id === 'phase-entry') return 'search';
  if (id === 'phase-build1' || id === 'phase-build2' || id === 'phase-dashboard') return 'files';
  return 'search';
}
function goAppNav(key) {
  if (key === 'topup') { window.location.href = './topup.html'; return; }
  if (key === 'files') showPhase('phase-build1');
  else if (key === 'excel') showPhase('phase-excel');
  else if (key === 'price') { showPhase('phase-pricecheck'); if (typeof renderPCTablePC2 === 'function') renderPCTablePC2(); }
  else showPhase('phase-entry');
  if (history.replaceState) history.replaceState(null, '', '#' + (key || 'search'));
}
"""

def patch_index(path: Path):
    t = path.read_text(encoding="utf-8", errors="replace")

    # CSS: replace previous nav css if present, else insert before </style>
    old_css_start = ".app-nav{display:flex;"
    if old_css_start in t:
        # replace from .app-nav through the last .app-nav-link rule we added
        i = t.find(old_css_start)
        j = t.find("</style>", i)
        # cut previous injected nav css only — it sits just before last </style> of first block
        # safer: insert our css before first </style> if marker missing
        t = t[:i] + NAV_CSS + t[j:]
    elif ".app-nav-link" not in t.split("</style>", 1)[0]:
        t = t.replace("</style>", NAV_CSS + "</style>", 1)
    else:
        t = t.replace("</style>", NAV_CSS + "</style>", 1)

    # Header nav
    if 'data-nav="files"' not in t:
        if '<nav class="app-nav"' in t:
            i = t.find('<nav class="app-nav"')
            j = t.find("</nav>", i) + len("</nav>")
            t = t[:i] + NAV_AUDIT + t[j:]
        else:
            raise SystemExit("nav not found in index.html")

    # Entry page becomes Hotel Search
    t = t.replace(
        '<div class="page-title">Hotel Contract Audit</div>\n  <div class="page-sub">Choose how you want to start your audit</div>',
        '<div class="page-title">Hotel Search</div>\n  <div class="page-sub">Search by city or whole country — hotels, hostels, motels, resorts, residences, B&amp;Bs, aparthotels, lodges — and export to Excel</div>',
        1,
    )

    # Enhance showPhase
    old_sp = """function showPhase(id) {
  document.querySelectorAll('.phase').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo(0, 0);
}"""
    new_sp = """function showPhase(id) {
  document.querySelectorAll('.phase').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo(0, 0);
  if (typeof setAppNav === 'function') setAppNav(navKeyFromPhase(id));
}"""
    if old_sp not in t:
        raise SystemExit("showPhase not found")
    if "navKeyFromPhase" not in t:
        t = t.replace(old_sp, NAV_JS + "\n" + new_sp, 1)

    hook = """window.addEventListener('DOMContentLoaded', function() {
  // Entry cards"""
    extra = """window.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.app-nav-link[data-nav]').forEach(function(a) {
    a.addEventListener('click', function(ev) {
      if (a.getAttribute('data-nav') === 'topup') return;
      ev.preventDefault();
      goAppNav(a.getAttribute('data-nav'));
    });
  });
  var hash = (location.hash || '').replace('#', '');
  if (hash === 'files' || hash === 'excel' || hash === 'price' || hash === 'search') goAppNav(hash);
  else setAppNav('search');
  // Entry cards"""
    if extra not in t:
        if hook not in t:
            raise SystemExit("DOMContentLoaded hook not found")
        t = t.replace(hook, extra, 1)

    path.write_text(t, encoding="utf-8")
    print("patched", path, "bytes", path.stat().st_size)


def patch_topup(path: Path):
    t = path.read_text(encoding="utf-8", errors="replace")
    if '<nav class="app-nav"' in t:
        i = t.find('<nav class="app-nav"')
        j = t.find("</nav>", i) + len("</nav>")
        t = t[:i] + NAV_TOPUP + t[j:]
    else:
        raise SystemExit("nav not found in topup.html")
    # refresh css
    if ".app-nav{display:flex;" in t:
        i = t.find(".app-nav{display:flex;")
        k = t.find("</style>", i)
        t = t[:i] + NAV_CSS + t[k:]
    path.write_text(t, encoding="utf-8")
    print("patched", path, "bytes", path.stat().st_size)


if __name__ == "__main__":
    patch_index(Path("index.html"))
    patch_topup(Path("topup.html"))
