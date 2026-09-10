# 下载限流服务（Cloudflare Worker + D1）

本目录用于给 GitHub Pages 的“技术标准检索”和“法律法规检索”提供统一下载限流与私有日志能力。

## 规则

- 技术标准 + 法律法规共用一个额度。
- 同一访问来源在滚动 24 小时内最多下载 5 个文件。
- 达到上限后返回：`今天下载次数已达上限，请稍后再试。`
- 真实下载地址仅在服务端判断允许后返回。
- 日志保存在 Cloudflare D1 中，不写入公开 GitHub 仓库。

## 日志与隐私设计

服务端不保存原始 IP。Worker 使用 `CF-Connecting-IP` 与私密 `VISITOR_HASH_PEPPER` 生成 SHA-256 访客标识，仅记录：匿名访客标识、下载时间、资料类型、资料名称、文件 URL 哈希。

管理员可通过 `GET /admin/logs` 查看最近日志，必须携带 `Authorization: Bearer <ADMIN_TOKEN>`。`ADMIN_TOKEN` 与 `VISITOR_HASH_PEPPER` 必须使用 Cloudflare Secret 保存，禁止提交到仓库。

匿名访客标识只能用于限流和安全审计，不能识别真实姓名。若未来需要知道具体是谁下载，必须增加登录/账号体系，并重新评估个人信息处理规则。

## 部署步骤

1. 在 Cloudflare 创建 D1 数据库，例如 `natural-resources-downloads`。
2. 用 `schema.sql` 初始化数据库。
3. 复制 `wrangler.toml.example` 为本地 `wrangler.toml`，填写 D1 `database_id`。不要把真实 `wrangler.toml`、密钥或数据库导出提交到公开仓库。
4. 设置两个 Secret：`VISITOR_HASH_PEPPER`、`ADMIN_TOKEN`。
5. 部署 Worker，得到类似 `https://natural-resources-download-gate.<account>.workers.dev` 的地址。
6. 将该地址接入 `docs/index.html` 和 `docs/laws.html` 后，页面即可显示全站共享的“24 小时内剩余下载次数：x / 5”，并由 Worker 强制执行限流。

## API

### GET /status
返回当前访问来源的 `limit`、`used`、`remaining`、`resetAt`。

### POST /download
请求体：

```json
{
  "type": "standard",
  "name": "GB/T 18314-2024 全球定位系统（GPS）测量规范",
  "url": "https://raw.githubusercontent.com/..."
}
```

允许时返回真实下载地址与最新剩余次数；超限时返回 HTTP 429。

### GET /admin/logs?limit=100
仅管理员可访问。日志默认不公开。
