/* Shared G2 Travel header. To add, rename or reorder a tool, edit TOOLS below: every page picks it up.
   Each page contains <header class="header" id="g2-header" data-page="KEY"></header> followed by this script. */
(function () {
  var TOOLS = [
    { key: 'region', label: 'Overview',            href: './region.html' },
    { key: 'audit',  label: 'Auto Audit',          home: 'files'  },
    { key: 'price',  label: 'Price Check',         home: 'price'  },
    { key: 'search', label: 'Hotel Search',        home: 'search' },
    { key: 'topup',  label: 'Top-up Desk',         href: './topup.html'  },
    { key: 'rates',  label: 'Live Rates',          href: './rates.html'  },
    { key: 'uuid',   label: 'Property UUID',       href: './uuid.html'   },
    { key: 'prebuy', label: 'Pre-buy Price Check', href: './prebuy.html' },
    { key: 'period', label: 'Period Compare',      href: './period.html' }
  ];
  var header = document.getElementById('g2-header');
  if (!header) return;
  var page = header.getAttribute('data-page') || '';
  var onIndex = page === 'index';   // index.html switches its own screens and marks its own active link

  var links = TOOLS.map(function (t) {
    var attrs;
    if (t.home) {
      attrs = onIndex ? 'href="#' + t.home + '" data-nav="' + t.home + '"' : 'href="./index.html#' + t.home + '"';
    } else {
      attrs = 'href="' + t.href + '"';
    }
    var active = !onIndex && t.key === page;
    return '<a class="app-nav-link' + (active ? ' is-active' : '') + '" ' + attrs + (active ? ' aria-current="page"' : '') + '>' + t.label + '</a>';
  }).join('');

  header.innerHTML =
    '<div class="logo-mark">G2</div>' +
    '<div><div class="header-title">G2 Travel</div><div class="header-sub">Contract &amp; Availability Tools</div></div>' +
    '<nav class="app-nav" aria-label="Tools">' + links + '</nav>' +
    '<button class="dark-toggle" id="dark-toggle" type="button" title="Toggle dark mode">🌙 Dark</button>';
})();
