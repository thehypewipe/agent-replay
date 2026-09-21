# Agent Replay 🔄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/thehypewipe/agent-replay?style=social)](https://github.com/thehypewipe/agent-replay/stargazers)

> **Local-first agent debugging for the "it worked yesterday" moments**

Stop debugging non-deterministic AI agent failures in the dark. Agent Replay logs every agent run locally, shows you what changed, and lets you replay the exact same conversation to catch regressions.

## Why?

- **Zero cloud lock-in** — Everything stored in SQLite, runs offline
- **Cost transparency** — See exactly what each feature costs across OpenAI/Anthropic/etc
- **Replay any run** — Re-run the exact same conversation to catch non-deterministic failures  
- **Hallucination flags** — Auto-detect when responses contradict previous runs
- **Compare runs** — Diff two runs side-by-side to see what changed

## Problem

You ship an agent. It works. Next day, same input → different (broken) output. "Nothing changed" but it's failing. Was it:
- A prompt regression?
- Model update from the provider?
- Temperature randomness?
- Context window differences?

**Agent Replay** records everything so you can replay, compare, and debug.

## Quick Start

```bash
pip install agent-replay
```

### 1. Wrap your agent calls

```python
from agent_replay import AgentLogger

logger = AgentLogger(db_path="./runs.db", feature="user-onboarding")

# Wrap any LLM call
response = logger.log_call(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    response="Hi there!",
    metadata={"user_id": "123"}
)
```

### 2. View cost breakdown

```bash
agent-replay report --feature user-onboarding
```

```
Feature: user-onboarding
Total cost: $2.34
Runs: 145

By model:
  gpt-4:      $1.82 (78%)
  claude-3:   $0.52 (22%)
```

### 3. Replay a specific run

```bash
agent-replay replay --run-id abc123
```

Shows the full conversation, cost, and flags any hallucinations detected.

### 4. Compare two runs

```bash
agent-replay diff --run1 abc123 --run2 def456
```

Side-by-side diff of inputs, outputs, costs, and detected issues.

## Features

- ✅ **Multi-provider support** — OpenAI, Anthropic, Cohere, Ollama
- ✅ **Token & cost tracking** — Automatic calculation per model
- ✅ **SQLite storage** — No external services, fully offline
- ✅ **Budget alerts** — Set per-feature cost limits
- ✅ **Run replay** — Re-execute past conversations
- ✅ **Hallucination detection** — Compare responses across runs
- ✅ **Export to CSV** — For external analysis

## Installation

```bash
pip install agent-replay
```

Or install from source:

```bash
git clone https://github.com/thehypewipe/agent-replay.git
cd agent-replay
pip install -e .
```

## Usage

### Basic logging

```python
from agent_replay import AgentLogger

logger = AgentLogger(
    db_path="./agent_runs.db",
    feature="email-classifier"
)

# Log a call
result = logger.log_call(
    provider="anthropic",
    model="claude-sonnet-4",
    messages=[
        {"role": "user", "content": "Classify this email: ..."}
    ],
    response="Category: Support",
    tokens_in=150,
    tokens_out=10
)

print(f"Cost: ${result['cost']:.4f}")
print(f"Run ID: {result['run_id']}")
```

### Budget alerts

```python
logger = AgentLogger(
    db_path="./runs.db",
    feature="chatbot",
    budget_limit=10.0  # Alert if feature exceeds $10
)

# Raises warning if budget exceeded
logger.log_call(...)
```

### CLI Commands

```bash
# View all runs
agent-replay list

# Filter by feature
agent-replay list --feature email-classifier

# Show cost report
agent-replay report

# Replay a specific run
agent-replay replay --run-id abc123

# Compare two runs
agent-replay diff --run1 abc123 --run2 def456

# Export to CSV
agent-replay export --output runs.csv

# Watch for budget violations
agent-replay watch --budget 50
```

## Architecture

```
agent-replay/
├── agent_replay/
│   ├── __init__.py
│   ├── logger.py          # Core logging logic
│   ├── models.py          # SQLite schema
│   ├── pricing.py         # Model pricing data
│   ├── replay.py          # Run replay logic
│   ├── diff.py            # Run comparison
│   ├── detector.py        # Hallucination detection
│   └── cli.py             # CLI commands
├── tests/
│   ├── test_logger.py
│   ├── test_replay.py
│   └── test_detector.py
├── README.md
├── setup.py
└── requirements.txt
```

## Pricing Data

Agent Replay includes up-to-date pricing for:
- OpenAI (GPT-4, GPT-3.5, etc.)
- Anthropic (Claude Opus, Sonnet, Haiku)
- Cohere
- Custom models (configurable)

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Add tests
4. Submit a PR

## License

MIT License - see LICENSE file

## Roadmap

- [ ] Web UI for viewing runs
- [ ] Integration with LangChain/LlamaIndex
- [ ] Automatic regression testing
- [ ] Team collaboration features
- [ ] Slack/Discord notifications for budget alerts

---

**Built for developers who are tired of "it worked yesterday" debugging.**

⭐ Star this repo if Agent Replay saves you debugging time!
