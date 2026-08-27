"""StudyTracker memory — SQLite: conversation history + user facts.

Two tables (ex-8 shapes, ex-11 lessons):

    conversations(id INTEGER PK AUTOINCREMENT,
                  session_id TEXT NOT NULL,
                  role       TEXT NOT NULL,
                  content    TEXT NOT NULL)   <- json.dumps(WHOLE message dict)

    user_facts(key TEXT PRIMARY KEY,          <- natural key, upsert pattern
               value TEXT NOT NULL)

The 400 lesson lives here: store the FULL message dict as JSON and restore
with json.loads — never (role, content) pairs, or tool messages lose
tool_call_id and every later chat() 400s with "invalid argument".

study_sessions stay in study_log.json (tools.py) — one dataset, one home.
"""
import json
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "studytracker.db"


class MemoryStore:
    """TODO: connection + tables + the methods below (your ex-8 MemoryStore,
    slimmer)."""

    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        """TODO: CREATE TABLE IF NOT EXISTS x2 (conversations, user_facts),
        then commit."""
        # Hint: executescript; conversations gets AUTOINCREMENT id (surrogate
        #       key — ORDER BY id = conversation order), user_facts gets
        #       key as PRIMARY KEY (natural key)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message TEXT NOT NULL
                );
        """)
        self.conn.commit()

    # ── conversations ──
    def save_message(self, session_id, msg: dict):
        """TODO: INSERT INTO conversations (session_id, role, content)
        VALUES (?, ?, ?) with content=json.dumps(msg) — the WHOLE dict.
        Then commit."""
        self.conn.execute("INSERT INTO conversations (session_id, message) VALUES (?, ?)", (session_id, json.dumps(msg)))
        self.conn.commit()

    def get_conversation(self, session_id, limit=100) -> list:
        """TODO: SELECT content ... WHERE session_id=? ORDER BY id LIMIT ?,
        return [json.loads(row["content"]) for row in ...] — lossless restore."""
        # Hint: rows keep insertion order via ORDER BY id (your ex-8 lesson)
        rows = self.conn.execute("SELECT message FROM conversations WHERE session_id = ? ORDER BY id LIMIT ?", (session_id, limit)).fetchall()
        return [json.loads(r["message"]) for r in rows]
    
    def get_conversation_all_session_id(self):
        rows = self.conn.execute("SELECT DISTINCT session_id FROM conversations").fetchall()
        return [row["session_id"] for row in rows]
    
MS = MemoryStore()