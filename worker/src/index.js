const LIMIT = 5;
const WINDOW_MS = 24 * 60 * 60 * 1000;
const ALLOWED_ORIGINS = new Set([
  'https://zhangyhrs.github.io',
  'http://localhost:8000',
  'http://127.0.0.1:8000'
]);

function corsHeaders(request) {
  const origin = request.headers.get('Origin') || '';
  return {
    'Access-Control-Allow-Origin': ALLOWED_ORIGINS.has(origin) ? origin : 'https://zhangyhrs.github.io',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
    'Cache-Control': 'no-store'
  };
}

function json(request, body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', ...corsHeaders(request) }
  });
}

async function sha256Hex(text) {
  const data = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function visitorHash(request, env) {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  return sha256Hex(`${env.VISITOR_HASH_PEPPER}:${ip}`);
}

function validDownloadUrl(raw) {
  try {
    const u = new URL(raw);
    if (u.protocol !== 'https:') return false;
    if (u.hostname !== 'raw.githubusercontent.com') return false;
    return u.pathname.startsWith('/zhangyhrs/Natural-Resources-Standards-and-Specifications/main/');
  } catch {
    return false;
  }
}

async function quota(env, hash, now) {
  const since = now - WINDOW_MS;
  const result = await env.DB.prepare(
    `SELECT COUNT(*) AS used, MIN(downloaded_at) AS earliest
       FROM download_logs
      WHERE visitor_hash = ?1 AND downloaded_at >= ?2`
  ).bind(hash, since).first();
  const used = Number(result?.used || 0);
  const earliest = result?.earliest == null ? null : Number(result.earliest);
  return {
    limit: LIMIT,
    used,
    remaining: Math.max(0, LIMIT - used),
    resetAt: earliest == null ? null : new Date(earliest + WINDOW_MS).toISOString()
  };
}

async function handleStatus(request, env) {
  const hash = await visitorHash(request, env);
  const q = await quota(env, hash, Date.now());
  return json(request, q);
}

async function handleDownload(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json(request, { error: '请求格式错误' }, 400);
  }

  const category = body?.type === 'law' ? 'law' : body?.type === 'standard' ? 'standard' : null;
  const name = String(body?.name || '').trim().slice(0, 300);
  const url = String(body?.url || '').trim();
  if (!category || !name || !validDownloadUrl(url)) {
    return json(request, { error: '下载参数无效' }, 400);
  }

  const now = Date.now();
  const hash = await visitorHash(request, env);
  const q = await quota(env, hash, now);
  if (q.remaining <= 0) {
    return json(request, {
      allowed: false,
      message: '今天下载次数已达上限，请稍后再试。',
      ...q
    }, 429);
  }

  const fileHash = await sha256Hex(url);
  await env.DB.prepare(
    `INSERT INTO download_logs
       (visitor_hash, downloaded_at, category, item_name, file_hash)
     VALUES (?1, ?2, ?3, ?4, ?5)`
  ).bind(hash, now, category, name, fileHash).run();

  const next = await quota(env, hash, now);
  return json(request, {
    allowed: true,
    downloadUrl: url,
    ...next
  });
}

async function handleAdminLogs(request, env) {
  const auth = request.headers.get('Authorization') || '';
  if (!env.ADMIN_TOKEN || auth !== `Bearer ${env.ADMIN_TOKEN}`) {
    return json(request, { error: 'Unauthorized' }, 401);
  }

  const u = new URL(request.url);
  const limit = Math.min(500, Math.max(1, Number(u.searchParams.get('limit') || 100)));
  const rows = await env.DB.prepare(
    `SELECT id, visitor_hash, downloaded_at, category, item_name, file_hash
       FROM download_logs
      ORDER BY downloaded_at DESC
      LIMIT ?1`
  ).bind(limit).all();

  return json(request, {
    items: (rows.results || []).map(r => ({
      id: r.id,
      visitor: String(r.visitor_hash).slice(0, 16),
      downloadedAt: new Date(Number(r.downloaded_at)).toISOString(),
      type: r.category,
      name: r.item_name,
      fileHash: r.file_hash
    }))
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders(request) });
    const u = new URL(request.url);
    try {
      if (request.method === 'GET' && u.pathname === '/status') return handleStatus(request, env);
      if (request.method === 'POST' && u.pathname === '/download') return handleDownload(request, env);
      if (request.method === 'GET' && u.pathname === '/admin/logs') return handleAdminLogs(request, env);
      return json(request, { error: 'Not found' }, 404);
    } catch (err) {
      console.error(err);
      return json(request, { error: '服务暂时不可用，请稍后再试。' }, 500);
    }
  }
};
