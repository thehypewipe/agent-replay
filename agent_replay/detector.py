"""Hallucination detection (basic implementation)"""

import sqlite3
from typing import Optional


def detect_hallucinations(db_path: str, run_id: str, threshold: float = 0.7) -> list[dict]:
    """
    Detect potential hallucinations by comparing with similar runs

    This is a basic implementation that compares responses for similar inputs.
    A production version would use semantic similarity (embeddings).

    Args:
        db_path: Path to database
        run_id: Run ID to check
        threshold: Similarity threshold (0-1)

    Returns:
        List of detected issues
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Get target run's messages
    cursor = conn.execute("""
        SELECT role, content
        FROM messages
        WHERE run_id = ?
        ORDER BY id ASC
    """, (run_id,))

    messages = [dict(row) for row in cursor.fetchall()]

    if not messages:
        return []

    # Get feature for this run
    cursor = conn.execute("""
        SELECT feature FROM runs WHERE run_id = ?
    """, (run_id,))

    feature_row = cursor.fetchone()
    if not feature_row:
        return []

    feature = feature_row["feature"]

    # Find similar runs (same feature, similar first message)
    # This is a simplified check - production would use embeddings
    first_user_msg = next((m for m in messages if m["role"] == "user"), None)

    if not first_user_msg:
        return []

    # For now, just check if response dramatically differs from recent runs
    # A real implementation would use semantic similarity

    issues = []

    # Placeholder: flag if this is the only run for this feature
    cursor = conn.execute("""
        SELECT COUNT(*) as count
        FROM runs
        WHERE feature = ? AND run_id != ?
    """, (feature, run_id))

    count_row = cursor.fetchone()
    if count_row["count"] == 0:
        issues.append({
            "flag_type": "first_run",
            "description": "This is the first run for this feature - no baseline for comparison",
            "severity": "info"
        })

    conn.close()
    return issues


def add_flag(db_path: str, run_id: str, flag_type: str, description: str, severity: str = "warning"):
    """Add a flag to a run"""
    conn = sqlite3.connect(db_path)

    from datetime import datetime
    created_at = datetime.utcnow().isoformat()

    conn.execute("""
        INSERT INTO flags (run_id, flag_type, description, severity, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (run_id, flag_type, description, severity, created_at))

    conn.commit()
    conn.close()
