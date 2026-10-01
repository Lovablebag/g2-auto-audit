export const config = { matcher: ['/((?!login|api/login|favicon.ico).*)'] };

export default async function middleware(request) {
  const password = process.env.APP_PASSWORD || '';
  const url = new URL(request.url);
  if (!password) return new Response('Login is not configured.', { status: 503 });
  const expected = await sign(password);
  const got = readCookie(request.headers.get('cookie') || '', 'g2auth');
  if (got && got === expected) return;
  if (url.pathname.startsWith('/api/')) {
    return new Response(JSON.stringify({ error: 'Sign in required' }), {
      status: 401,
      headers: { 'content-type': 'application/json' }
    });
  }
  const next = url.pathname + url.search;
  return Response.redirect(new URL('/login?next=' + encodeURIComponent(next), request.url), 302);
}

function readCookie(header, name) {
  const part = header.split(';').map(s => s.trim()).find(s => s.startsWith(name + '='));
  return part ? decodeURIComponent(part.slice(name.length + 1)) : '';
}

async function sign(password) {
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(password),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode('g2-auto-audit'));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}
