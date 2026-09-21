"""Model pricing data (per 1M tokens)"""

PRICING = {
    # OpenAI
    "gpt-4": {"input": 30.0, "output": 60.0},
    "gpt-4-turbo": {"input": 10.0, "output": 30.0},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},

    # Anthropic (September 2026 pricing)
    "claude-opus-5": {"input": 15.0, "output": 75.0},
    "claude-sonnet-5": {"input": 3.0, "output": 15.0},
    "claude-fable-5-1": {"input": 1.5, "output": 7.5},
    "claude-haiku-4-5": {"input": 0.25, "output": 1.25},
    "claude-opus-4": {"input": 15.0, "output": 75.0},
    "claude-sonnet-4": {"input": 3.0, "output": 15.0},

    # Older Claude models
    "claude-3-opus": {"input": 15.0, "output": 75.0},
    "claude-3-sonnet": {"input": 3.0, "output": 15.0},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},

    # Cohere
    "command": {"input": 1.0, "output": 2.0},
    "command-light": {"input": 0.3, "output": 0.6},

    # Ollama (local, free)
    "ollama": {"input": 0.0, "output": 0.0},
}


def calculate_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    """Calculate cost for a model call"""
    # Normalize model name
    model_key = model.lower().strip()

    # Try exact match first
    if model_key in PRICING:
        pricing = PRICING[model_key]
        cost = (tokens_in / 1_000_000 * pricing["input"]) + \
               (tokens_out / 1_000_000 * pricing["output"])
        return round(cost, 6)

    # Try partial match (e.g., "gpt-4-0125" matches "gpt-4")
    for key, pricing in PRICING.items():
        if key in model_key or model_key.startswith(key):
            cost = (tokens_in / 1_000_000 * pricing["input"]) + \
                   (tokens_out / 1_000_000 * pricing["output"])
            return round(cost, 6)

    # Unknown model - return 0 and warn
    return 0.0


def get_supported_models() -> list[str]:
    """Return list of supported models"""
    return sorted(PRICING.keys())
