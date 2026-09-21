"""SQLite database models and schema"""

import sqlite3
from pathlib import Path
from typing import Optional


def init_db(db_path: str) -> sqlite3.Connection:
    """Initialize database with schema"""
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Create runs table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            feature TEXT NOT NULL,
            provider TEXT NOT NULL,
            model TEXT NOT NULL,
            tokens_in INTEGER NOT NULL,
            tokens_out INTEGER NOT NULL,
            cost REAL NOT NULL,
            created_at TEXT NOT NULL,
            metadata TEXT
        )
    """)

    # Create messages table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
    """)

    # Create flags table for hallucination detection
    conn.execute("""
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            flag_type TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
    """)

    # Create indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_feature ON runs(feature)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_run_id ON messages(run_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_flags_run_id ON flags(run_id)")

    conn.commit()
    return conn
