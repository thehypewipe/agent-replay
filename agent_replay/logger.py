"""Core logging functionality"""

import json
import sqlite3
import uuid
from datetime import datetime
from typing import Any, Optional

from .models import init_db
from .pricing import calculate_cost


class AgentLogger:
    """Main logger for agent calls"""

    def __init__(
        self,
        db_path: str = "./agent_runs.db",
        feature: str = "default",
        budget_limit: Optional[float] = None
    ):
        """
        Initialize logger

        Args:
            db_path: Path to SQLite database
            feature: Feature name for grouping runs
            budget_limit: Optional budget limit in USD (raises warning if exceeded)
        """
        self.db_path = db_path
        self.feature = feature
        self.budget_limit = budget_limit
        self.conn = init_db(db_path)

    def log_call(
        self,
        provider: str,
        model: str,
        messages: list[dict[str, str]],
        response: str,
        tokens_in: Optional[int] = None,
        tokens_out: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Log an agent call

        Args:
            provider: Provider name (openai, anthropic, etc.)
            model: Model name
            messages: List of message dicts with role/content
            response: Response text
            tokens_in: Input tokens (estimated if not provided)
            tokens_out: Output tokens (estimated if not provided)
            metadata: Optional metadata dict

        Returns:
            Dict with run_id, cost, and budget status
        """
        run_id = str(uuid.uuid4())[:8]
        created_at = datetime.utcnow().isoformat()

        # Estimate tokens if not provided (rough: 4 chars = 1 token)
        if tokens_in is None:
            total_input = sum(len(m.get("content", "")) for m in messages)
            tokens_in = max(1, total_input // 4)

        if tokens_out is None:
            tokens_out = max(1, len(response) // 4)

        # Calculate cost
        cost = calculate_cost(model, tokens_in, tokens_out)

        # Insert run record
        self.conn.execute("""
            INSERT INTO runs (run_id, feature, provider, model, tokens_in, tokens_out, cost, created_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            self.feature,
            provider,
            model,
            tokens_in,
            tokens_out,
            cost,
            created_at,
            json.dumps(metadata) if metadata else None
        ))

        # Insert messages
        for msg in messages:
            self.conn.execute("""
                INSERT INTO messages (run_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
            """, (run_id, msg["role"], msg["content"], created_at))

        # Insert response message
        self.conn.execute("""
            INSERT INTO messages (run_id, role, content, created_at)
            VALUES (?, ?, ?, ?)
        """, (run_id, "assistant", response, created_at))

        self.conn.commit()

        # Check budget
        budget_status = self._check_budget()

        return {
            "run_id": run_id,
            "cost": cost,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "budget_exceeded": budget_status["exceeded"],
            "feature_total": budget_status["total"]
        }

    def _check_budget(self) -> dict[str, Any]:
        """Check if feature budget is exceeded"""
        cursor = self.conn.execute("""
            SELECT SUM(cost) as total
            FROM runs
            WHERE feature = ?
        """, (self.feature,))

        row = cursor.fetchone()
        total = row["total"] or 0.0

        exceeded = False
        if self.budget_limit and total > self.budget_limit:
            exceeded = True
            print(f"⚠️  Budget exceeded for feature '{self.feature}': ${total:.2f} / ${self.budget_limit:.2f}")

        return {"total": total, "exceeded": exceeded}

    def get_feature_cost(self, feature: Optional[str] = None) -> float:
        """Get total cost for a feature"""
        feature = feature or self.feature

        cursor = self.conn.execute("""
            SELECT SUM(cost) as total
            FROM runs
            WHERE feature = ?
        """, (feature,))

        row = cursor.fetchone()
        return row["total"] or 0.0

    def close(self):
        """Close database connection"""
        self.conn.close()
