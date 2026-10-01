const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  const password = process.env.APP_PASSWORD || '';
  if (!password) return res.status(503).json({ error: 'Login is not configured.' });
  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body || '{}'); } catch (e) { body = {}; }
  }
  const given = String((body && body.password) || '');
  const a = Buffer.from(given);
  const b = Buffer.from(password);
  const same = a.length === b.length && crypto.timingSafeEqual(a, b);
  if (!same) return res.status(401).json({ error: 'Wrong password.' });
  const token = crypto.createHmac('sha256', password).update('g2-auto-audit').digest('hex');
  res.setHeader('Set-Cookie', 'g2auth=' + token + '; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=2592000');
  return res.status(200).json({ ok: true });
};
