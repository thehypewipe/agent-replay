"""Generate realistic demo data for Agent Replay dashboard"""

from agent_replay import AgentLogger
from datetime import datetime, timedelta
import random

# Create demo runs across multiple features
features = [
    ("email-classifier", "openai", "gpt-4"),
    ("customer-support", "anthropic", "claude-sonnet-5"),
    ("content-moderation", "openai", "gpt-4o"),
    ("data-extraction", "anthropic", "claude-opus-5"),
    ("code-review", "openai", "gpt-4-turbo"),
]

conversations = [
    ("Classify this email: 'Your invoice is ready'", "Category: Billing", 150, 10),
    ("Is this comment spam? 'Click here for free prizes!'", "Yes, likely spam", 120, 8),
    ("Extract customer info from: 'John Doe, john@example.com, +1234567890'", "Name: John Doe\nEmail: john@example.com\nPhone: +1234567890", 180, 45),
    ("Review this Python function for bugs", "Found 2 potential issues: 1) Missing null check 2) Off-by-one error", 400, 120),
    ("Summarize customer complaint about late delivery", "Customer ordered on Jan 5, expected Jan 10, arrived Jan 15. Requesting refund.", 250, 60),
]

print("Generating realistic demo data...")
print("=" * 60)

for feature, provider, model in features:
    logger = AgentLogger(
        db_path="./demo_runs.db",
        feature=feature,
        budget_limit=10.0
    )

    # Generate 3-5 runs per feature
    num_runs = random.randint(3, 5)

    for i in range(num_runs):
        conv = random.choice(conversations)
        user_msg, response, base_tokens_in, base_tokens_out = conv

        # Add some variance to token counts
        tokens_in = base_tokens_in + random.randint(-20, 20)
        tokens_out = base_tokens_out + random.randint(-5, 15)

        result = logger.log_call(
            provider=provider,
            model=model,
            messages=[{"role": "user", "content": user_msg}],
            response=response,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            metadata={
                "user_id": f"user{random.randint(100, 999)}",
                "session": f"sess_{random.randint(1000, 9999)}",
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat()
            }
        )

        print(f"[OK] {feature}: run {result['run_id']} (${result['cost']:.4f})")

    feature_cost = logger.get_feature_cost()
    print(f"     Feature total: ${feature_cost:.4f}")
    print()

    logger.close()

print("=" * 60)
print(f"Generated demo data in demo_runs.db")
print()
print("Try these commands:")
print("  agent-replay list --db demo_runs.db")
print("  agent-replay report --db demo_runs.db")
print("  agent-replay report --db demo_runs.db --feature email-classifier")
