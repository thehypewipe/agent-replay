"""Example usage of Agent Replay"""

from agent_replay import AgentLogger

# Initialize logger with budget limit
logger = AgentLogger(
    db_path="./agent_runs.db",
    feature="email-classifier",
    budget_limit=5.0  # Alert if feature exceeds $5
)

# Example 1: Log an OpenAI call
print("Example 1: Logging OpenAI call...")
result1 = logger.log_call(
    provider="openai",
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an email classifier."},
        {"role": "user", "content": "Classify this email: 'Your invoice is ready'"}
    ],
    response="Category: Billing",
    tokens_in=150,
    tokens_out=10,
    metadata={"user_id": "user123", "email_id": "email456"}
)

print(f"[OK] Logged run {result1['run_id']}")
print(f"  Cost: ${result1['cost']:.4f}")
print(f"  Feature total: ${result1['feature_total']:.4f}")
print()

# Example 2: Log an Anthropic call
print("Example 2: Logging Anthropic call...")
result2 = logger.log_call(
    provider="anthropic",
    model="claude-sonnet-5",
    messages=[
        {"role": "user", "content": "Classify this email: 'Meeting tomorrow at 3pm'"}
    ],
    response="Category: Calendar",
    tokens_in=100,
    tokens_out=8,
    metadata={"user_id": "user123", "email_id": "email789"}
)

print(f"[OK] Logged run {result2['run_id']}")
print(f"  Cost: ${result2['cost']:.4f}")
print(f"  Feature total: ${result2['feature_total']:.4f}")
print()

# Example 3: Automatic token estimation
print("Example 3: Automatic token estimation...")
result3 = logger.log_call(
    provider="openai",
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Quick test message"}
    ],
    response="Quick response",
    # tokens_in and tokens_out omitted - will be estimated
)

print(f"[OK] Logged run {result3['run_id']}")
print(f"  Estimated tokens: {result3['tokens_in']} in, {result3['tokens_out']} out")
print(f"  Cost: ${result3['cost']:.4f}")
print()

# Get total cost for this feature
total_cost = logger.get_feature_cost()
print(f"Total cost for 'email-classifier': ${total_cost:.4f}")

# Close the logger
logger.close()

print("\n" + "="*60)
print("Now try the CLI commands:")
print("="*60)
print("  agent-replay list")
print("  agent-replay report")
print(f"  agent-replay replay --run-id {result1['run_id']}")
print(f"  agent-replay diff --run1 {result1['run_id']} --run2 {result2['run_id']}")
print("  agent-replay export --output runs.csv")
