const LIMIT = 5;
const WINDOW_MS = 24 * 60 * 60 * 1000;
const LOG_RETENTION_MS = 30 * 24 * 60 * 60 * 1000;

const ALLOWED_ORIGINS = [
  'https://zhangyhrs.github.io'
];

function corsHeaders(request) {
  const origin = request.headers.get('Origin') || '';
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowed,
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
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      ...corsHeaders(request)
    }
  });
}

async function sha256Hex(text) {
  const data = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return [...new Uint8Array(digest)]
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

async function visitorHash(request, env) {
  const ip =
    request.headers.get('CF-Connecting-IP') ||
    request.headers.get('X-Forwarded-For') ||
    'unknown';
  return sha256Hex(`${ip}|${env.VISITOR_SALT}`);
}

function validDownloadUrl(raw) {
  try {
    const u = new URL(raw);
    if (u.protocol !== 'https:') return false;
    if (!['raw.githubusercontent.com', 'github.com'].includes(u.hostname)) return false;
    const path = decodeURIComponent(u.pathname).toLowerCase();
    return path.includes('zhangyhrs') && path.includes('natural-resources-standards-and-specifications');
  } catch {
    return false;
  }
}

async function quota(env, hash, now) {
  const since = now - WINDOW_MS;
  const result = await env.DB.prepare(`
    SELECT COUNT(*) AS used, MIN(created_at) AS earliest
    FROM download_logs
    WHERE visitor_hash = ?1 AND created_at >= ?2
  `).bind(hash, since).first();

  const used = Number(result?.used || 0);
  const earliest = result?.earliest == null ? null : Number(result.earliest);
  return {
    ok: true,
    limit: LIMIT,
    used,
    remaining: Math.max(0, LIMIT - used),
    reset_at: earliest == null ? null : earliest + WINDOW_MS
  };
}

async function handleStatus(request, env) {
  const hash = await visitorHash(request, env);
  return json(request, await quota(env, hash, Date.now()));
}

async function handleStats(request, env) {
  const url = new URL(request.url);
  const fileType = (url.searchParams.get('file_type') || '').trim();
  const allowedTypes = ['技术标准', '法律法规'];
  if (fileType && !allowedTypes.includes(fileType)) {
    return json(request, { ok: false, message: '资料类型无效' }, 400);
  }

  let result;
  if (fileType) {
    result = await env.DB.prepare(`
      SELECT file_type, file_name, COUNT(*) AS downloads
      FROM download_logs
      WHERE file_type = ?1
      GROUP BY file_type, file_name
      ORDER BY downloads DESC, file_name ASC
    `).bind(fileType).all();
  } else {
    result = await env.DB.prepare(`
      SELECT file_type, file_name, COUNT(*) AS downloads
      FROM download_logs
      GROUP BY file_type, file_name
      ORDER BY downloads DESC, file_type ASC, file_name ASC
    `).all();
  }

  return json(request, {
    ok: true,
    source: 'D1',
    items: (result.results || []).map(r => ({
      file_type: r.file_type,
      file_name: r.file_name,
      downloads: Number(r.downloads || 0)
    }))
  });
}

async function handleDownload(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json(request, { ok: false, message: '请求参数错误' }, 400);
  }

  const fileUrl = String(body?.url || '').trim();
  const fileName = String(body?.file_name || '').trim().slice(0, 300);
  const fileType = String(body?.file_type || '').trim();

  if (!fileUrl || !fileName || !['技术标准', '法律法规'].includes(fileType)) {
    return json(request, { ok: false, message: '缺少或存在无效下载参数' }, 400);
  }
  if (!validDownloadUrl(fileUrl)) {
    return json(request, { ok: false, message: '下载地址不在允许范围内' }, 403);
  }

  const now = Date.now();
  const since = now - WINDOW_MS;
  const hash = await visitorHash(request, env);
  const fileUrlHash = await sha256Hex(fileUrl);

  try {
    await env.DB.prepare('DELETE FROM download_logs WHERE created_at < ?1')
      .bind(now - LOG_RETENTION_MS)
      .run();
  } catch {}

  const inserted = await env.DB.prepare(`
    INSERT INTO download_logs
      (visitor_hash, file_type, file_name, file_url_hash, created_at)
    SELECT ?1, ?2, ?3, ?4, ?5
    WHERE (
      SELECT COUNT(*)
      FROM download_logs
      WHERE visitor_hash = ?6 AND created_at >= ?7
    ) < ?8
  `).bind(
    hash,
    fileType,
    fileName,
    fileUrlHash,
    now,
    hash,
    since,
    LIMIT
  ).run();

  const changes = Number(inserted?.meta?.changes || 0);
  if (changes < 1) {
    const q = await quota(env, hash, now);
    return json(request, {
      ...q,
      ok: false,
      allowed: false,
      limited: true,
      message: '今天下载次数已达上限，请稍后再试。'
    }, 429);
  }

  const q = await quota(env, hash, now);
  return json(request, {
    ...q,
    ok: true,
    allowed: true,
    download_url: fileUrl,
    message: '允许下载'
  });
}

async function handleAdminLogs(request, env) {
  const auth = request.headers.get('Authorization') || '';
  if (!env.ADMIN_TOKEN || auth !== `Bearer ${env.ADMIN_TOKEN}`) {
    return json(request, { ok: false, message: 'Unauthorized' }, 401);
  }

  const url = new URL(request.url);
  let limit = Number(url.searchParams.get('limit') || 100);
  if (!Number.isFinite(limit)) limit = 100;
  limit = Math.min(500, Math.max(1, limit));

  const rows = await env.DB.prepare(`
    SELECT id, visitor_hash, file_type, file_name, file_url_hash, created_at
    FROM download_logs
    ORDER BY created_at DESC
    LIMIT ?1
  `).bind(limit).all();

  return json(request, {
    ok: true,
    count: rows.results?.length || 0,
    logs: rows.results || []
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(request) });
    }

    try {
      if (!env.DB) return json(request, { ok: false, message: 'D1 数据库未绑定' }, 500);
      if (!env.VISITOR_SALT) return json(request, { ok: false, message: 'VISITOR_SALT 未配置' }, 500);

      const url = new URL(request.url);

      if (request.method === 'GET' && url.pathname === '/') {
        return json(request, {
          ok: true,
          service: '自然资源标准规范与法律法规库下载网关',
          version: '1.1',
          limit: LIMIT,
          window_hours: 24,
          stats_source: 'D1'
        });
      }
      if (request.method === 'GET' && url.pathname === '/status') return handleStatus(request, env);
      if (request.method === 'GET' && url.pathname === '/stats') return handleStats(request, env);
      if (request.method === 'POST' && url.pathname === '/download') return handleDownload(request, env);
      if (request.method === 'GET' && url.pathname === '/admin/logs') return handleAdminLogs(request, env);

      return json(request, { ok: false, message: 'Not Found' }, 404);
    } catch (err) {
      console.error(err);
      return json(request, { ok: false, message: '服务器处理失败' }, 500);
    }
  }
};
