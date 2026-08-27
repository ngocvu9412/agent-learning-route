# Agentic Engineer Learning Route: Building Your Own AI Agent

> A hands-on curriculum derived from analyzing the Hermes Agent repository to teach you how to build, understand, and extend AI agents with tool calling, memory, and multi-platform integration.

## You Are
Someone with basic ML knowledge (Andrew Ng / Yaser Abu-Mostafa background) who wants to **build** an agentic engineer from scratch.

## API Setup

This course uses **Google Gemini** (free tier, 1500 requests/day).

**Setup steps:**
1. Get a free API key at https://aistudio.google.com/apikey
2. Put it in the `.env` file at the project root:

```
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-flash-latest
```

3. Install dependencies:

```bash
pip install openai python-dotenv jupyter
```

**Current configuration:**
- Provider: Google Gemini
- Base URL: `https://generativelanguage.googleapis.com/v1beta/openai`
- Model: `gemini-flash-latest` (from GEMINI_MODEL env var)
- API key: `GEMINI_API_KEY` (from .env)

## Repository Map (Hermes Structure We'll Learn From)

| Concept | Key Files in Hermes | What You'll Build |
|---|---|---|
| Agent Loop | `agent/conversation_loop.py`, `agent/agent_init.py` | Minimal agent with tool-calling loop |
| Tool System | `tools/` directory (186+ tools) | Generic tool registry + executor |
| MCP Client | `hermes_cli/mcp_*.py` | Connect to external tools via MCP |
| Memory | `agent/memory_store.py`, `agent/context_engine.py` | Persistent memory layer |
| Providers | `agent/providers/llama_adapter.py` etc | Multi-provider LLM abstraction |
| ACP | `acp_adapter/server.py` | Agent Communication Protocol server |
| Gateway | `gateway/` | Multi-platform messaging bridge |

## Learning Path (7 Weeks)

```
Week 1: Foundations & Environment    -> 01-fundamentals/  (Exercises 1-3)
Week 2: Agent Core Architecture      -> 02-agent-core/    (Exercises 4-5)
Week 3: Tool System                  -> 03-tools/         (Exercises 6-7)
Week 4: Memory Systems               -> 04-memory/        (Exercise 8)
Week 5: Multi-Provider & Fallback    -> 05-mcp-acp/       (Exercises 9-10)
Week 6: ACP Server & Advanced        -> 06-advanced/      (Exercise 11)
Week 7: Integration & Production     -> 07-production/    (Exercise 12)
```

## How to Use This Guide

1. **Read the theory** in each week's README.md
2. **Do the exercises** in Jupyter notebooks (TODO stubs — you implement!)
3. **Compare with Hermes** — each file references exact Hermes source for comparison
4. **Run everything** — you need Python 3.11+

## Quick Start

```bash
cd agent-learning-route   # (or whatever you named the cloned folder)

# Install dependencies
pip install openai python-dotenv jupyter

# Set up your .env file (see API Setup above)

# Week 1: Start here
cd 01-fundamentals
jupyter notebook exercise_1_hello_agent.ipynb
```

## Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.11+ installed
- [ ] Google Gemini API key (free): https://aistudio.google.com/apikey
- [ ] `.env` file set up with `GEMINI_API_KEY` and `GEMINI_MODEL`
- [ ] Git (to explore Hermes source code)

**Set up your environment**:
```bash
# Install core dependencies
pip install openai python-dotenv jupyter

# Create .env file at project root:
echo "GEMINI_API_KEY=your-key-here" > .env
echo "GEMINI_MODEL=gemini-flash-latest" >> .env
```

## Week-by-Week Overview

### Week 1: Fundamentals & Environment
**Goal**: Build a basic agent that calls LLM APIs

Exercises:
- `exercise_1_hello_agent.ipynb`: Simplest agent - just call LLM
- `exercise_2_tool_schema.ipynb`: Define tool schemas + error handling
- `exercise_3_basic_loop.ipynb`: Implement agent loop

**You'll learn**:
- How LLM APIs work (Google Gemini via OpenAI SDK)
- Tool/function calling schemas
- Basic agent loop pattern
- Error handling (ValueError, TypeError)

**Libraries**: `openai`, `python-dotenv`

### Week 2: Agent Core Architecture
**Goal**: Robust agent with error handling

Exercises:
- `exercise_4_error_handling.ipynb`: Retry logic with exponential backoff
- `exercise_5_complete_loop.ipynb`: Full agent with error handling

**You'll learn**:
- Error classification (retryable vs permanent)
- Exponential backoff strategy
- ReAct pattern (Reasoning + Acting)
- Conversation history management

**Libraries**: `openai`, `time`

### Week 3: Tool System
**Goal**: Sophisticated tool registry with essential tools

Exercises:
- `exercise_6_filesystem_tools.ipynb`: 5 filesystem tools
- `exercise_7_tool_registry.ipynb`: Tool registry system

**You'll learn**:
- Tool registry pattern
- Filesystem tools (read, write, list, search, delete)
- MCP (Model Context Protocol) basics

**Libraries**: `pathlib`

### Week 4: Memory Systems
**Goal**: Persistent memory for conversations and preferences

Exercises:
- `exercise_8_sqlite_memory.ipynb`: SQLite memory store

**You'll learn**:
- Why agents need memory
- SQLite for persistent storage
- User preference storage
- Skill/procedure storage

**Libraries**: `sqlite3` (built-in)

### Week 5: Multi-Provider Support & Fallback
**Goal**: Multiple LLM providers with automatic fallback

Exercises:
- `exercise_9_provider_factory.ipynb`: Multi-provider factory
- `exercise_10_fallback_chain.ipynb`: Provider fallback logic

**You'll learn**:
- Provider abstraction layer
- Fallback chain pattern
- Health tracking and error counting

**Libraries**: `openai`, `dataclasses`

### Week 6: ACP Server & Advanced Patterns
**Goal**: Expose agent as service via ACP

Exercises:
- `exercise_11_acp_server.ipynb`: ACP HTTP server

**You'll learn**:
- HTTP server patterns for agents
- ACP message format
- REST API design (GET, POST endpoints)

**Libraries**: `http.server` (built-in)

### Week 7: Integration & Production Readiness
**Goal**: Complete production-ready agent

Exercises:
- `exercise_12_full_agent.ipynb`: Integrate all components

**You'll learn**:
- Full agent architecture
- Configuration management
- Memory persistence
- Interactive REPL

**Libraries**: `openai`, `sqlite3`, `pathlib`

## Success Criteria

By the end of Week 7, you'll have:

- [ ] A working agent that responds to questions
- [ ] Tool calling for filesystem operations
- [ ] Persistent memory across sessions
- [ ] Multi-provider support with fallbacks
- [ ] ACP server for agent-to-agent communication
- [ ] Interactive CLI interface
- [ ] Comprehensive understanding of agent architecture

## Resources

- [Hermes Agent source](https://github.com/NousResearch/hermes-agent)
- [MCP spec](https://spec.modelcontextprotocol.io/)
- [ACP spec](https://agentcommunicationprotocol.com/)
- [Google Gemini API docs](https://ai.google.dev/gemini-api/docs)
- [OpenAI Python SDK docs](https://platform.openai.com/docs)

## Troubleshooting

**Gemini API issues**:
- Get a free key at https://aistudio.google.com/apikey
- Check your API key in `.env` file
- Verify model name: `gemini-flash-latest`
- Check `.env` has NO spaces around `=`: `GEMINI_MODEL=gemini-flash-latest`
- 400 error "INVALID ARGUMENT": use `model_dump(exclude_none=True)` — Gemini rejects None values

**Jupyter not starting**:
- Run: `pip install jupyter`
- Try: `python -m notebook` instead of `jupyter notebook`

**SQLite errors**:
- Delete `agent_memory.db` and restart (safe, it's just test data)
- Check file permissions

**Module not found**:
- Run: `pip install openai python-dotenv`
- Use the correct Python (Python 3.14 at `AppData\Local\Python`)

## Contributing

Found an issue? Have an improvement?
1. Check existing exercises first
2. Add your exercise to the appropriate week
3. Update this README with your contribution

## License

This learning route is MIT licensed - use it, learn from it, build amazing things!

---

**Happy coding!** Remember: agents are loops, tools are capabilities, memory is persistence. Build it step by step, test each component, and integrate thoughtfully.
