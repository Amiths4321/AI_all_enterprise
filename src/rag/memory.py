import sqlite3
from datetime import datetime


class ChatMemory:

    def __init__(
        self,
        db_path="chat_history.db",
    ):

        self.db_path = db_path

        self._initialize()

    def _initialize(self):

        with sqlite3.connect(
            self.db_path
        ) as conn:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            conn.commit()

    def add_message(
        self,
        session_id,
        role,
        content,
    ):

        with sqlite3.connect(
            self.db_path
        ) as conn:

            conn.execute(
                """
                INSERT INTO messages
                (session_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    session_id,
                    role,
                    content,
                    datetime.utcnow().isoformat(),
                ),
            )

            conn.commit()

    def get_history(
        self,
        session_id,
        limit=10,
    ):

        with sqlite3.connect(
            self.db_path
        ) as conn:

            rows = conn.execute(
                """
                SELECT role, content
                FROM messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    session_id,
                    limit,
                ),
            ).fetchall()

        rows.reverse()

        return rows