"""Tests for logger module"""

import os
import sqlite3
import tempfile
from pathlib import Path

from agent_replay import AgentLogger


def test_basic_logging():
    """Test basic logging functionality"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test-feature")

        result = logger.log_call(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            response="Hi there!",
            tokens_in=10,
            tokens_out=5
        )

        assert "run_id" in result
        assert result["cost"] > 0
        assert result["tokens_in"] == 10
        assert result["tokens_out"] == 5
        assert not result["budget_exceeded"]

        logger.close()


def test_budget_tracking():
    """Test budget limit enforcement"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test", budget_limit=0.001)

        # First call should be fine
        result1 = logger.log_call(
            provider="openai",
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            response="response",
            tokens_in=10,
            tokens_out=5
        )

        # Large second call should trigger budget warning
        result2 = logger.log_call(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test" * 1000}],
            response="response" * 1000,
            tokens_in=10000,
            tokens_out=5000
        )

        assert result2["budget_exceeded"]

        logger.close()


def test_feature_cost_tracking():
    """Test per-feature cost tracking"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")

        # Log to feature 1
        logger1 = AgentLogger(db_path=db_path, feature="feature1")
        logger1.log_call(
            provider="openai",
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            response="response",
            tokens_in=100,
            tokens_out=50
        )

        # Log to feature 2
        logger2 = AgentLogger(db_path=db_path, feature="feature2")
        logger2.log_call(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            response="response",
            tokens_in=100,
            tokens_out=50
        )

        cost1 = logger1.get_feature_cost()
        cost2 = logger2.get_feature_cost()

        # GPT-4 should be more expensive than GPT-3.5
        assert cost2 > cost1
        assert cost1 > 0

        logger1.close()
        logger2.close()


def test_metadata_storage():
    """Test metadata storage and retrieval"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test")

        metadata = {"user_id": "123", "session": "abc"}

        result = logger.log_call(
            provider="anthropic",
            model="claude-sonnet-4",
            messages=[{"role": "user", "content": "Hello"}],
            response="Hi!",
            tokens_in=10,
            tokens_out=5,
            metadata=metadata
        )

        # Verify metadata was stored
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT metadata FROM runs WHERE run_id = ?", (result["run_id"],))
        row = cursor.fetchone()
        conn.close()

        import json
        stored_metadata = json.loads(row["metadata"])
        assert stored_metadata == metadata

        logger.close()


def test_token_estimation():
    """Test automatic token estimation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test")

        # Log without explicit token counts
        result = logger.log_call(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "A" * 400}],  # ~100 tokens
            response="B" * 40  # ~10 tokens
        )

        # Should estimate tokens (4 chars = 1 token)
        assert result["tokens_in"] == 100
        assert result["tokens_out"] == 10
        assert result["cost"] > 0

        logger.close()


if __name__ == "__main__":
    test_basic_logging()
    test_budget_tracking()
    test_feature_cost_tracking()
    test_metadata_storage()
    test_token_estimation()
    print("✅ All tests passed!")
