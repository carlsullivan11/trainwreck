from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class SQLiteMemoryStore:
    """SQLite-backed memory store for conversation and step history."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                iteration INTEGER,
                plan TEXT,
                result TEXT,
                reflection TEXT,
                score REAL,
                description TEXT,
                outcome TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        self.conn.commit()

    def add_step(self, step: dict[str, Any]) -> None:
        """Add a step to the memory store."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO steps (iteration, plan, result, reflection, score, description, outcome)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                step["iteration"],
                json.dumps(step["plan"]),
                json.dumps(step["result"]),
                json.dumps(step["reflection"]),
                step["score"],
                step["description"],
                step["outcome"],
            ),
        )
        self.conn.commit()

    def get_history(self, limit: int = 100) -> list[dict[str, Any]]:
        """Retrieve step history."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT iteration, plan, result, reflection, score, description, outcome, timestamp
            FROM steps
            ORDER BY id DESC
            LIMIT ?
        """,
            (limit,),
        )
        rows = cursor.fetchall()
        history = []
        for row in rows:
            history.append(
                {
                    "iteration": row[0],
                    "plan": json.loads(row[1]),
                    "result": json.loads(row[2]),
                    "reflection": json.loads(row[3]),
                    "score": row[4],
                    "description": row[5],
                    "outcome": row[6],
                    "timestamp": row[7],
                }
            )
        return history

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
