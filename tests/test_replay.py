"""Tests for replay module"""

import os
import tempfile

from agent_replay import AgentLogger
from agent_replay.replay import replay_run, list_runs


def test_replay_run():
    """Test replaying a single run"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test")

        messages = [
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "4"}
        ]

        result = logger.log_call(
            provider="openai",
            model="gpt-4",
            messages=[messages[0]],
            response=messages[1]["content"],
            tokens_in=10,
            tokens_out=5,
            metadata={"test": True}
        )

        run_id = result["run_id"]

        # Replay the run
        replayed = replay_run(db_path, run_id)

        assert replayed["run_id"] == run_id
        assert replayed["feature"] == "test"
        assert replayed["model"] == "gpt-4"
        assert replayed["tokens_in"] == 10
        assert replayed["tokens_out"] == 5
        assert replayed["metadata"]["test"] is True
        assert len(replayed["messages"]) == 2
        assert replayed["messages"][0]["role"] == "user"
        assert replayed["messages"][1]["role"] == "assistant"

        logger.close()


def test_list_runs():
    """Test listing runs"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")

        # Create multiple runs
        logger1 = AgentLogger(db_path=db_path, feature="feature1")
        logger1.log_call(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "test1"}],
            response="response1",
            tokens_in=10,
            tokens_out=5
        )

        logger2 = AgentLogger(db_path=db_path, feature="feature2")
        logger2.log_call(
            provider="anthropic",
            model="claude-sonnet-4",
            messages=[{"role": "user", "content": "test2"}],
            response="response2",
            tokens_in=20,
            tokens_out=10
        )

        # List all runs
        all_runs = list_runs(db_path)
        assert len(all_runs) == 2

        # List filtered by feature
        feature1_runs = list_runs(db_path, feature="feature1")
        assert len(feature1_runs) == 1
        assert feature1_runs[0]["feature"] == "feature1"

        logger1.close()
        logger2.close()


def test_replay_nonexistent():
    """Test replaying non-existent run raises error"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        logger = AgentLogger(db_path=db_path, feature="test")
        logger.close()

        try:
            replay_run(db_path, "nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not found" in str(e)


if __name__ == "__main__":
    test_replay_run()
    test_list_runs()
    test_replay_nonexistent()
    print("✅ All replay tests passed!")
