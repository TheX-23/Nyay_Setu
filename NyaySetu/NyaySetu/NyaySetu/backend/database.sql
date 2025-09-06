-- NyaySetu SQLite schema and helpful data collection queries

PRAGMA foreign_keys = ON;

-- Tables
CREATE TABLE IF NOT EXISTS chats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  language TEXT NOT NULL,
  timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS forms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  form_type TEXT NOT NULL,
  form_text TEXT NOT NULL,
  responses_json TEXT NOT NULL,
  timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  is_verified INTEGER NOT NULL DEFAULT 0,
  verification_token TEXT,
  created_at TEXT NOT NULL,
  verified_at TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_chats_timestamp ON chats (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_forms_timestamp ON forms (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_chats_language ON chats (language);
CREATE INDEX IF NOT EXISTS idx_forms_form_type ON forms (form_type);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_verified ON users (is_verified);

-- Sample data collection queries

-- Get all chats (newest first)
SELECT id, question, answer, language, timestamp
FROM chats
ORDER BY timestamp DESC, id DESC;

-- Get all forms (newest first)
SELECT id, form_type, form_text, responses_json, timestamp
FROM forms
ORDER BY timestamp DESC, id DESC;

-- Count by language
SELECT language, COUNT(*) AS total
FROM chats
GROUP BY language
ORDER BY total DESC;

-- Count by form type
SELECT form_type, COUNT(*) AS total
FROM forms
GROUP BY form_type
ORDER BY total DESC;

-- Users statistics (examples)
SELECT COUNT(*) AS total_users FROM users;
SELECT COUNT(*) AS verified_users FROM users WHERE is_verified = 1;

-- Filtered chat queries (examples)
-- By date range
-- SELECT id, question, answer, language, timestamp FROM chats
-- WHERE timestamp >= '2025-01-01T00:00:00' AND timestamp <= '2025-12-31T23:59:59'
-- ORDER BY timestamp DESC, id DESC;

-- By text search
-- SELECT id, question, answer, language, timestamp FROM chats
-- WHERE question LIKE '%contract%' OR answer LIKE '%contract%'
-- ORDER BY timestamp DESC, id DESC;

-- Filtered form queries (examples)
-- By form type and date range
-- SELECT id, form_type, form_text, responses_json, timestamp FROM forms
-- WHERE form_type = 'FIR' AND timestamp >= '2025-01-01T00:00:00'
-- ORDER BY timestamp DESC, id DESC;

-- By text search
-- SELECT id, form_type, form_text, responses_json, timestamp FROM forms
-- WHERE form_text LIKE '%police%' OR responses_json LIKE '%John%'
-- ORDER BY timestamp DESC, id DESC;


