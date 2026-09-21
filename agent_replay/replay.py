"""Run replay functionality"""

import json
import sqlite3
from typing import Optional


def replay_run(db_path: str, run_id: str) -> dict:
    """
    Replay a specific run

    Args:
        db_path: Path to database
        run_id: Run ID to replay

    Returns:
        Dict with run details and messages
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Get run metadata
    cursor = conn.execute("""
        SELECT * FROM runs WHERE run_id = ?
    """, (run_id,))

    run = cursor.fetchone()
    if not run:
        raise ValueError(f"Run not found: {run_id}")

    # Get messages
    cursor = conn.execute("""
        SELECT role, content, created_at
        FROM messages
        WHERE run_id = ?
        ORDER BY id ASC
    """, (run_id,))

    messages = [dict(row) for row in cursor.fetchall()]

    # Get flags
    cursor = conn.execute("""
        SELECT flag_type, description, severity
        FROM flags
        WHERE run_id = ?
    """, (run_id,))

    flags = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "run_id": run["run_id"],
        "feature": run["feature"],
        "provider": run["provider"],
        "model": run["model"],
        "tokens_in": run["tokens_in"],
        "tokens_out": run["tokens_out"],
        "cost": run["cost"],
        "created_at": run["created_at"],
        "metadata": json.loads(run["metadata"]) if run["metadata"] else None,
        "messages": messages,
        "flags": flags
    }


def list_runs(db_path: str, feature: Optional[str] = None, limit: int = 20) -> list[dict]:
    """
    List recent runs

    Args:
        db_path: Path to database
        feature: Optional feature filter
        limit: Max runs to return

    Returns:
        List of run dicts
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    if feature:
        cursor = conn.execute("""
            SELECT run_id, feature, provider, model, cost, created_at
            FROM runs
            WHERE feature = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (feature, limit))
    else:
        cursor = conn.execute("""
            SELECT run_id, feature, provider, model, cost, created_at
            FROM runs
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

    runs = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return runs
