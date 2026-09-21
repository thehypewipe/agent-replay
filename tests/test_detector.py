"""Tests for detector module"""

import os
import tempfile

from agent_replay import AgentLogger
from agent_replay.detector import detect_hallucinations, add_flag


def test_detect_first_run():
    """Test detection flags first run"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test")

        result = logger.log_call(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            response="Hi!",
            tokens_in=10,
            tokens_out=5
        )

        issues = detect_hallucinations(db_path, result["run_id"])

        # Should flag as first run
        assert len(issues) == 1
        assert issues[0]["flag_type"] == "first_run"
        assert issues[0]["severity"] == "info"

        logger.close()


def test_add_flag():
    """Test adding custom flags"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test")

        result = logger.log_call(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            response="Hi!",
            tokens_in=10,
            tokens_out=5
        )

        run_id = result["run_id"]

        # Add a custom flag
        add_flag(db_path, run_id, "custom_check", "Something suspicious", "warning")

        # Verify flag was added
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM flags WHERE run_id = ?", (run_id,))
        flags = [dict(row) for row in cursor.fetchall()]
        conn.close()

        assert len(flags) == 1
        assert flags[0]["flag_type"] == "custom_check"
        assert flags[0]["severity"] == "warning"

        logger.close()


if __name__ == "__main__":
    test_detect_first_run()
    test_add_flag()
    print("✅ All detector tests passed!")
