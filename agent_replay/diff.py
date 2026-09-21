"""Run comparison functionality"""

import difflib
from typing import Optional

from .replay import replay_run


def diff_runs(db_path: str, run_id1: str, run_id2: str) -> dict:
    """
    Compare two runs

    Args:
        db_path: Path to database
        run_id1: First run ID
        run_id2: Second run ID

    Returns:
        Dict with comparison results
    """
    run1 = replay_run(db_path, run_id1)
    run2 = replay_run(db_path, run_id2)

    # Compare metadata
    metadata_diff = {
        "model": {
            "run1": run1["model"],
            "run2": run2["model"],
            "changed": run1["model"] != run2["model"]
        },
        "cost": {
            "run1": run1["cost"],
            "run2": run2["cost"],
            "delta": run2["cost"] - run1["cost"]
        },
        "tokens": {
            "run1": {"in": run1["tokens_in"], "out": run1["tokens_out"]},
            "run2": {"in": run2["tokens_in"], "out": run2["tokens_out"]},
            "delta_in": run2["tokens_in"] - run1["tokens_in"],
            "delta_out": run2["tokens_out"] - run1["tokens_out"]
        }
    }

    # Compare messages
    messages1 = run1["messages"]
    messages2 = run2["messages"]

    message_diffs = []
    max_len = max(len(messages1), len(messages2))

    for i in range(max_len):
        if i >= len(messages1):
            message_diffs.append({
                "index": i,
                "status": "added_in_run2",
                "content": messages2[i]["content"]
            })
        elif i >= len(messages2):
            message_diffs.append({
                "index": i,
                "status": "removed_in_run2",
                "content": messages1[i]["content"]
            })
        elif messages1[i]["content"] != messages2[i]["content"]:
            # Generate unified diff
            diff = list(difflib.unified_diff(
                messages1[i]["content"].splitlines(keepends=True),
                messages2[i]["content"].splitlines(keepends=True),
                lineterm=""
            ))

            message_diffs.append({
                "index": i,
                "role": messages1[i]["role"],
                "status": "changed",
                "diff": "".join(diff)
            })

    return {
        "run1": {"run_id": run_id1, "feature": run1["feature"], "created_at": run1["created_at"]},
        "run2": {"run_id": run_id2, "feature": run2["feature"], "created_at": run2["created_at"]},
        "metadata_diff": metadata_diff,
        "message_diffs": message_diffs,
        "flags": {
            "run1": run1["flags"],
            "run2": run2["flags"]
        }
    }
