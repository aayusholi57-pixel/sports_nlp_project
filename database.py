"""SQLite persistence layer for analysis history."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DB_NAME = os.getenv("SPORTS_INTEL_DB", "sports_intel.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment_label TEXT NOT NULL,
                sentiment_score REAL NOT NULL,
                entities TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_articles_created_at ON articles(created_at)"
        )


def save_analysis(text: str, sentiment: dict[str, Any], entities: list[dict[str, str]]) -> int:
    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO articles (text, sentiment_label, sentiment_score, entities)
            VALUES (?, ?, ?, ?)
            """,
            (text, sentiment["label"], sentiment["confidence"], json.dumps(entities)),
        )
        return int(cursor.lastrowid)


def fetch_all_analyses(limit: int = 100) -> list[dict[str, Any]]:
    limit = max(1, min(limit, 500))
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT id, text, sentiment_label, sentiment_score, entities, created_at
            FROM articles
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "id": row["id"],
            "text": row["text"],
            "sentiment": {"label": row["sentiment_label"], "confidence": row["sentiment_score"]},
            "entities": json.loads(row["entities"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


if __name__ == "__main__":
    Path(DB_NAME).parent.mkdir(parents=True, exist_ok=True) if Path(DB_NAME).parent != Path(".") else None
    init_db()
    print(f"Database ready: {DB_NAME}")
