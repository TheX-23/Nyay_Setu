import os
import json
import sqlite3
from typing import Any, Dict, List, Optional


# Resolve database path. Defaults to a file next to the backend folder.
_DEFAULT_DB_PATH = os.environ.get(
    "NYAYSETU_DB_PATH",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "nyaysetu.db"),
)


def get_db_connection(db_path: str = _DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection with Row factory for dict-like access."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = _DEFAULT_DB_PATH) -> None:
    """Initialize database with required tables if they don't exist."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        # Chats table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                language TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        # Forms table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS forms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                form_type TEXT NOT NULL,
                form_text TEXT NOT NULL,
                responses_json TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        # Users table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                is_verified INTEGER NOT NULL DEFAULT 0,
                verification_token TEXT,
                created_at TEXT NOT NULL,
                verified_at TEXT
            )
            """
        )
        # Indexes for users
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
            """
        )
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_users_verified ON users(is_verified)
            """
        )
        conn.commit()
    finally:
        conn.close()


def insert_chat(
    question: str,
    answer: str,
    language: str,
    timestamp: str,
    db_path: str = _DEFAULT_DB_PATH,
) -> int:
    """Insert a chat record and return its new id."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chats (question, answer, language, timestamp) VALUES (?, ?, ?, ?)",
            (question, answer, language, timestamp),
        )
        conn.commit()
        return int(cur.lastrowid) # pyright: ignore[reportArgumentType]
    finally:
        conn.close()


def insert_form(
    form_type: str,
    form_text: str,
    responses: Dict[str, Any],
    timestamp: str,
    db_path: str = _DEFAULT_DB_PATH,
) -> int:
    """Insert a form record and return its new id."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO forms (form_type, form_text, responses_json, timestamp) VALUES (?, ?, ?, ?)",
            (form_type, form_text, json.dumps(responses, ensure_ascii=False), timestamp),
        )
        conn.commit()
        return int(cur.lastrowid) # pyright: ignore[reportArgumentType]
    finally:
        conn.close()


def fetch_all_chats(db_path: str = _DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """Fetch all chat records, newest first."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, question, answer, language, timestamp FROM chats ORDER BY timestamp DESC, id DESC")
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def fetch_all_forms(db_path: str = _DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """Fetch all form records, newest first."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, form_type, form_text, responses_json, timestamp FROM forms ORDER BY timestamp DESC, id DESC")
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def fetch_chats_filtered(
    start: Optional[str] = None,
    end: Optional[str] = None,
    language: Optional[str] = None,
    q: Optional[str] = None,
    db_path: str = _DEFAULT_DB_PATH,
) -> List[Dict[str, Any]]:
    """Fetch chats with optional filters: start/end ISO timestamp, language, text query."""
    conn = get_db_connection(db_path)
    try:
        conditions = []
        params: List[Any] = []
        if start:
            conditions.append("timestamp >= ?") # pyright: ignore[reportUnknownMemberType]
            params.append(start)
        if end:
            conditions.append("timestamp <= ?") # pyright: ignore[reportUnknownMemberType]
            params.append(end)
        if language:
            conditions.append("language = ?") # pyright: ignore[reportUnknownMemberType]
            params.append(language)
        if q:
            conditions.append("(question LIKE ? OR answer LIKE ?)") # pyright: ignore[reportUnknownMemberType]
            like = f"%{q}%"
            params.extend([like, like])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else "" # pyright: ignore[reportUnknownArgumentType]
        sql = (
            "SELECT id, question, answer, language, timestamp FROM chats "
            + where_clause
            + " ORDER BY timestamp DESC, id DESC"
        )
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def fetch_forms_filtered(
    start: Optional[str] = None,
    end: Optional[str] = None,
    form_type: Optional[str] = None,
    q: Optional[str] = None,
    db_path: str = _DEFAULT_DB_PATH,
) -> List[Dict[str, Any]]:
    """Fetch forms with optional filters: start/end ISO timestamp, form_type, text query."""
    conn = get_db_connection(db_path)
    try:
        conditions = []
        params: List[Any] = []
        if start:
            conditions.append("timestamp >= ?") # pyright: ignore[reportUnknownMemberType]
            params.append(start)
        if end:
            conditions.append("timestamp <= ?") # pyright: ignore[reportUnknownMemberType]
            params.append(end)
        if form_type:
            conditions.append("form_type = ?") # pyright: ignore[reportUnknownMemberType]
            params.append(form_type)
        if q:
            conditions.append("(form_text LIKE ? OR responses_json LIKE ?)") # pyright: ignore[reportUnknownMemberType]
            like = f"%{q}%"
            params.extend([like, like])

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else "" # pyright: ignore[reportUnknownArgumentType]
        sql = (
            "SELECT id, form_type, form_text, responses_json, timestamp FROM forms "
            + where_clause
            + " ORDER BY timestamp DESC, id DESC"
        )
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# Users helpers
def create_user(
    email: str,
    password_hash: str,
    verification_token: Optional[str],
    created_at: str,
    db_path: str = _DEFAULT_DB_PATH,
) -> int:
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password_hash, is_verified, verification_token, created_at) VALUES (?, ?, 0, ?, ?)",
            (email, password_hash, verification_token, created_at),
        )
        conn.commit()
        return int(cur.lastrowid) # pyright: ignore[reportArgumentType]
    finally:
        conn.close()


def get_user_by_email(email: str, db_path: str = _DEFAULT_DB_PATH) -> Optional[Dict[str, Any]]:
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, password_hash, is_verified, verification_token, created_at, verified_at FROM users WHERE email = ?",
            (email,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_verification_token(token: str, db_path: str = _DEFAULT_DB_PATH) -> Optional[Dict[str, Any]]:
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, password_hash, is_verified, verification_token, created_at, verified_at FROM users WHERE verification_token = ?",
            (token,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def set_user_verified(user_id: int, verified_at: str, db_path: str = _DEFAULT_DB_PATH) -> None:
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET is_verified = 1, verification_token = NULL, verified_at = ? WHERE id = ?",
            (verified_at, user_id),
        )
        conn.commit()
    finally:
        conn.close()


