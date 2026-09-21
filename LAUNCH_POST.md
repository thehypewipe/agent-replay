# Launch Post Templates

## Reddit - r/MachineLearning

**Title:** [P] Agent Replay – Local-first debugging for the "it worked yesterday" moments

**Body:**
```markdown
Hi r/MachineLearning,

I built **Agent Replay** to solve a problem I kept hitting: my AI agents would work perfectly, then mysteriously fail on the same input the next day.

**The Problem:**
- Agents fail non-deterministically
- Zero cost visibility per feature
- No way to replay and debug what changed
- LangSmith is cloud-locked and expensive

**Agent Replay** is 100% local, stores everything in SQLite, and lets you:
- 📊 Track costs per feature with budget alerts
- 🔄 Replay any past run to catch regressions
- 🔍 Diff two runs side-by-side
- 💾 Fully offline, no cloud dependencies
- 🛠️ Rich CLI (list, report, replay, diff, export)

**Quick Example:**
```python
from agent_replay import AgentLogger

logger = AgentLogger(db_path="./runs.db", feature="email-classifier")

result = logger.log_call(
    provider="openai",
    model="gpt-4",
    messages=[{"role": "user", "content": "Classify this email..."}],
    response="Category: Billing",
    tokens_in=150,
    tokens_out=10
)

print(f"Cost: ${result['cost']:.4f}")
```

**Supports:**
- OpenAI, Anthropic, Cohere, Ollama
- Multi-feature cost tracking
- Budget alerts
- Run replay and comparison
- CSV export for analysis

**GitHub:** https://github.com/YOUR_USERNAME/agent-replay

**Install:**
```bash
pip install agent-replay
```

Feedback welcome! Let me know what features you'd want to see.
```

---

## Hacker News - Show HN

**Title:** Show HN: Agent Replay – Local-first debugging for AI agents

**Body:**
```
Hi HN,

I built Agent Replay to debug non-deterministic AI agent failures - the "it worked yesterday" moments that waste hours.

The problem: You ship an agent, it works, next day same input fails. Was it a prompt change? Model update? Temperature randomness? No way to know.

Agent Replay records everything locally (SQLite), lets you replay runs, compare what changed, and track costs per feature. Zero cloud dependencies.

Features:
- Replay any past run with full conversation history
- Diff two runs side-by-side to see what changed
- Per-feature cost tracking with budget alerts
- Multi-provider (OpenAI, Anthropic, Cohere, Ollama)
- Rich CLI for analysis
- Hallucination detection (basic, improving)

Example:
    from agent_replay import AgentLogger
    
    logger = AgentLogger(db_path="./runs.db", feature="support-bot")
    
    result = logger.log_call(
        provider="anthropic",
        model="claude-sonnet-4",
        messages=[{"role": "user", "content": "..."}],
        response="...",
        tokens_in=100,
        tokens_out=50
    )

Then:
    agent-replay list
    agent-replay replay --run-id abc123
    agent-replay diff --run1 abc123 --run2 def456

GitHub: https://github.com/YOUR_USERNAME/agent-replay
Install: pip install agent-replay

Built this because LangSmith is cloud-locked and I wanted something local-first. Feedback appreciated!
```

---

## Twitter/X Post

**Thread:**

Tweet 1:
```
🚀 Just shipped Agent Replay – local-first debugging for AI agents

Ever had an agent work perfectly, then mysteriously fail the next day on the same input?

Agent Replay solves this. 🧵
```

Tweet 2:
```
The problem: 
• Agents fail non-deterministically
• Zero cost visibility per feature
• Can't replay to debug what changed
• Existing tools (LangSmith) are cloud-locked

I needed something 100% local.
```

Tweet 3:
```
Agent Replay features:

🔄 Replay any past run
🔍 Diff runs side-by-side
💰 Track costs per feature
⚠️ Budget alerts
📊 Rich CLI reports
💾 SQLite storage (offline)
```

Tweet 4:
```
Quick example:

from agent_replay import AgentLogger

logger = AgentLogger(
    db_path="./runs.db",
    feature="my-agent",
    budget_limit=10.0
)

result = logger.log_call(...)
print(f"Cost: ${result['cost']}")
```

Tweet 5:
```
Supports:
• OpenAI (GPT-4, GPT-3.5, etc.)
• Anthropic (Claude Opus, Sonnet, Haiku)
• Cohere
• Ollama (local)

Install: pip install agent-replay

GitHub ⭐: https://github.com/YOUR_USERNAME/agent-replay
```

---

## Dev.to Article

**Title:** How I Built Agent Replay: Debugging Non-Deterministic AI Agents

**Tags:** #ai #python #debugging #opensource

**Body:** (Write a longer article covering)
1. The problem you faced
2. Why existing solutions didn't work
3. How Agent Replay works
4. Technical architecture (SQLite, pricing data, CLI)
5. Code examples
6. Future roadmap
7. Call to action (star on GitHub, contribute)

---

## LinkedIn Post

```
🚀 Just open-sourced Agent Replay – a local-first debugging tool for AI agents.

The problem: AI agents fail non-deterministically. Same input, different output. "It worked yesterday" becomes a daily debugging nightmare.

Agent Replay solves this by:
✅ Recording every agent run locally (SQLite)
✅ Letting you replay and compare runs
✅ Tracking costs per feature with budget alerts
✅ Working 100% offline (no cloud dependencies)

Built for developers working with:
• OpenAI (GPT-4, etc.)
• Anthropic (Claude)
• Cohere
• Ollama

Open source, MIT licensed, ready to use:
pip install agent-replay

GitHub: https://github.com/YOUR_USERNAME/agent-replay

#AI #MachineLearning #OpenSource #Python #LLM #AgentDebugging
```

---

## Awesome Lists to Submit To

1. **awesome-langchain**
   - https://github.com/kyrolabs/awesome-langchain
   - Submit PR adding Agent Replay under "Tools > Debugging"

2. **awesome-ai-tools**
   - https://github.com/mahseema/awesome-ai-tools
   - Submit PR under "Developer Tools"

3. **awesome-llm**
   - https://github.com/Hannibal046/Awesome-LLM
   - Submit PR under "Tools"

4. **awesome-chatgpt**
   - https://github.com/humanloop/awesome-chatgpt
   - Submit PR under "Development Tools"

---

## Launch Timeline (Suggested)

**Day 1 (Launch Day):**
- 9am: Post on Reddit r/MachineLearning
- 10am: Submit to Hacker News
- 11am: Tweet thread
- 2pm: Post on LinkedIn
- Evening: Monitor comments, respond quickly

**Day 2-3:**
- Submit to awesome lists
- Post on Dev.to
- Cross-post to r/LangChain, r/LocalLLaMA
- Respond to all comments and issues

**Week 1:**
- Write detailed documentation
- Add more examples
- Create demo video
- Monitor GitHub stars/issues

**Week 2+:**
- Ship first feature requests
- Write technical blog post
- Consider Product Hunt launch

---

Remember to:
✅ Respond to ALL comments within 24 hours
✅ Be helpful and humble
✅ Thank people for feedback
✅ Fix bugs quickly
✅ Add requested features when they make sense
