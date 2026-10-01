module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  const key = process.env.LITEAPI_KEY;
  if (!key) return res.status(500).json({ error: 'Rates key is not configured on the server.' });

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body || '{}'); } catch (e) { return res.status(400).json({ error: 'Invalid JSON' }); }
  }
  body = body || {};

  try {
    if (body.mode === 'hotels') return await searchHotels(res, key, body);
    if (body.mode === 'rates') return await searchRates(res, key, body);
    return res.status(400).json({ error: 'Unknown mode' });
  } catch (e) {
    return res.status(502).json({ error: e.message || 'LiteAPI request failed' });
  }
};

async function searchHotels(res, key, body) {
  const country = String(body.countryCode || '').trim().toUpperCase();
  const city = String(body.cityName || '').trim();
  const name = String(body.hotelName || '').trim().toLowerCase();
  if (country.length !== 2) return res.status(400).json({ error: 'A 2-letter country code is required.' });
  const url = new URL('https://api.liteapi.travel/v3.0/data/hotels');
  url.searchParams.set('countryCode', country);
  url.searchParams.set('limit', '40');
  if (city) url.searchParams.set('cityName', city);
  const json = await lite(key, url.toString());
  let rows = Array.isArray(json.data) ? json.data : [];
  if (name) rows = rows.filter(h => String(h.name || '').toLowerCase().includes(name));
  return res.status(200).json({
    hotels: rows.slice(0, 20).map(h => ({
      id: h.id,
      name: h.name,
      city: h.city,
      country: h.country,
      address: h.address,
      stars: h.stars || h.starRating || null
    }))
  });
}

async function searchRates(res, key, body) {
  const hotelId = String(body.hotelId || '').trim();
  const checkin = String(body.checkin || '').trim();
  const checkout = String(body.checkout || '').trim();
  if (!hotelId || !checkin || !checkout) return res.status(400).json({ error: 'Hotel, check-in and check-out are required.' });
  const adults = Math.min(Math.max(Number(body.adults) || 2, 1), 6);
  const payload = {
    hotelIds: [hotelId],
    checkin,
    checkout,
    currency: String(body.currency || 'EUR').toUpperCase(),
    guestNationality: String(body.guestNationality || 'IT').toUpperCase(),
    occupancies: [{ adults }],
    timeout: 12
  };
  const json = await lite(key, 'https://api.liteapi.travel/v3.0/hotels/rates', payload);
  const hotel = (json.data || [])[0] || {};
  const nights = Math.max(1, Math.round((Date.parse(checkout) - Date.parse(checkin)) / 86400000));
  const rates = [];
  for (const room of hotel.roomTypes || []) {
    const rate = (room.rates || [])[0] || {};
    const total = num(room.offerRetailRate && room.offerRetailRate.amount) ?? num(rate.retailRate && rate.retailRate.total && rate.retailRate.total[0] && rate.retailRate.total[0].amount);
    const currency = (room.offerRetailRate && room.offerRetailRate.currency) || (rate.retailRate && rate.retailRate.total && rate.retailRate.total[0] && rate.retailRate.total[0].currency) || payload.currency;
    const taxes = ((rate.retailRate && rate.retailRate.taxesAndFees) || []).filter(t => t && t.included === false);
    const tag = rate.cancellationPolicies && rate.cancellationPolicies.refundableTag;
    rates.push({
      room: rate.name || 'Room',
      board: rate.boardType || '',
      boardName: rate.boardName || '',
      refundable: tag === 'RFN',
      refundableTag: tag || '',
      total,
      perNight: total == null ? null : Math.round((total / nights) * 100) / 100,
      currency,
      taxes: taxes.map(t => ({ description: t.description, amount: t.amount, currency: t.currency })),
      adults: rate.adultCount || adults
    });
  }
  rates.sort((a, b) => (a.total == null ? 1 : a.total) - (b.total == null ? 1 : b.total));
  return res.status(200).json({
    hotelId,
    nights,
    currency: payload.currency,
    rates: rates.slice(0, 40)
  });
}

function num(v) { return v == null || v === '' || Number.isNaN(Number(v)) ? null : Number(v); }

async function lite(key, url, payload) {
  const res = await fetch(url, {
    method: payload ? 'POST' : 'GET',
    headers: { 'X-API-Key': key, 'Accept': 'application/json', 'Content-Type': 'application/json' },
    body: payload ? JSON.stringify(payload) : undefined
  });
  const text = await res.text();
  let json = {};
  try { json = text ? JSON.parse(text) : {}; } catch (e) { json = { error: text.slice(0, 180) }; }
  if (!res.ok) {
    const msg = (json.error && (json.error.message || json.error.description)) || json.message || ('LiteAPI ' + res.status);
    throw new Error(msg);
  }
  return json;
}
