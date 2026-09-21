# Contributing to Agent Replay

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

1. Clone the repo:
```bash
git clone https://github.com/thehypewipe/agent-replay.git
cd agent-replay
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run tests:
```bash
python -m tests.test_logger
python -m tests.test_replay
python -m tests.test_detector
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to public functions
- Keep functions focused and testable

## Adding a New Provider

To add pricing for a new LLM provider:

1. Edit `agent_replay/pricing.py`
2. Add pricing per 1M tokens (input/output)
3. Update `README.md` with supported models
4. Add a test case

Example:
```python
PRICING = {
    # ... existing providers
    "new-model": {"input": 1.0, "output": 2.0},
}
```

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Update README.md if needed
5. Submit a PR with a clear description

## Testing

All new features should include tests. Run the full test suite before submitting:

```bash
python -m tests.test_logger
python -m tests.test_replay
python -m tests.test_detector
```

## Reporting Issues

Please include:
- Python version
- Agent Replay version
- Steps to reproduce
- Expected vs actual behavior

## Questions?

Open an issue or start a discussion on GitHub!
