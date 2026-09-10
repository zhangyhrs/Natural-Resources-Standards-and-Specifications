CREATE TABLE IF NOT EXISTS download_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  visitor_hash TEXT NOT NULL,
  downloaded_at INTEGER NOT NULL,
  category TEXT NOT NULL CHECK(category IN ('standard','law')),
  item_name TEXT NOT NULL,
  file_hash TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_download_logs_visitor_time
  ON download_logs(visitor_hash, downloaded_at);

CREATE INDEX IF NOT EXISTS idx_download_logs_time
  ON download_logs(downloaded_at);
