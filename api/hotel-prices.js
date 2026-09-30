module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') { res.status(204).end(); return; }
  try {
    const u = new URL(req.url, 'http://localhost');
    const dest = 'https://prebuy-deal-builder.vercel.app/api/hotel-prices?' + u.searchParams.toString();
    const r = await fetch(dest);
    const text = await r.text();
    res.status(r.status).setHeader('Content-Type', 'application/json; charset=utf-8').send(text);
  } catch (e) {
    res.status(502).json({ error: 'Price service unavailable' });
  }
};
