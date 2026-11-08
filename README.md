# Auto Audit - G2 Travel

Hotel contract audit app for G2 Travel.

Upload Excel source files, review the dashboard, and generate a PowerPoint audit.

## Header / navigation
The top bar is defined once in `nav.js` (the list of tools) and `nav.css` (the look). Every page just contains
`<header class="header" id="g2-header" data-page="KEY"></header>` and loads `nav.js`. To add, rename or reorder a tool, edit `TOOLS` in `nav.js`.
