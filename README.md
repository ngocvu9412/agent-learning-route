# Agent Learning Route

My journey from "I've studied ML theory" to "I've built a working AI agent with my own hands."

I came into this knowing ML theory — Andrew Ng's course, Yaser Abu-Mostafa's *Learning from Data* — but I had never built an agent. Agent frameworks felt like black boxes I was renting. So I set out to build every piece myself, one exercise at a time, until the pieces added up to a real agent.

**How I worked:** I planned and walked this route together with an AI mentor (the Hermes Agent CLI). It broke the goal into exercises, wrote the specs, reviewed my code, and pointed out my bugs — but every line of implementation code in this repo is mine. That division of labor — I type, it reviews — was the whole point of the project.

The reference architecture throughout was the [Hermes Agent](https://github.com/NousResearch/hermes-agent) source: each week's notes point at the exact Hermes files that solve the problem I was working on at the time.

## The route

| Folder | What I built there | Exercises |
|---|---|---|
| `01-fundamentals` | First LLM calls, tool schemas, the simplest agent loop | ex 1–3 |
| `02-agent-core` | Error handling, retries with backoff, the full loop | ex 4–5 |
| `03-tools` | Filesystem tools and a generic tool registry | ex 6–7 |
| `04-memory` | SQLite memory: conversations plus user facts | ex 8 |
| `05-mcp-acp` | Multi-provider factory + fallback chain | ex 9 |
| `06-advanced` | An ACP HTTP server exposing the agent as a service | ex 10 |
| `07-production` | **StudyTracker** — the capstone, everything integrated | 5 modules |

Each folder holds the notebooks where I did the work (TODO stubs, filled in by me) and a README of the theory notes I kept while learning that piece.

## StudyTracker — the capstone

An agent that tracks what I study and reports on it. I tell it "log 45 minutes of langgraph"; later I ask "what did I study this week?" and it answers from its own log, not from the model's recollection. Built with zero frameworks: just the OpenAI SDK, plain functions, dispatch dicts, a JSON file, and SQLite.

- `providers.py` — ZaiProvider and GeminiProvider behind a ProviderFactory and a FallbackChain with per-provider health tracking and retries. If GLM is down, Gemini answers; if everything is dead, the agent says so instead of crashing.
- `tools.py` — `log_session` / `weekly_report` tools with JSON schemas, backed by a JSON log file
- `memory.py` — SQLite store: full conversation round-trips (whole message dicts as JSON), surviving restarts
- `agent.py` — the loop: model → tool calls → tool results → model
- `run.py` — interactive REPL

Acceptance-tested end to end: tool round-trips, lossless persistence across restarts, no duplicate rows, graceful behavior when every provider is dead. More detail in [`07-production/README.md`](07-production/README.md).

## Stack

- Python 3.14, Jupyter
- OpenAI SDK pointed at Google Gemini (`gemini-flash-latest`) and z.ai GLM (`glm-4.5-flash`) — one client, two providers
- SQLite + JSON for persistence; no LangChain, no agent framework anywhere
- Keys live in `.env` (gitignored); `07-production/.env.example` shows what's needed

## Lessons that stuck

- Gemini's 400 "INVALID ARGUMENT" means `model_dump(exclude_none=True)` — it rejects None values in tool schemas
- Tool errors should travel back to the model as messages, not crash the loop
- `WinError 32` on Windows: close the SQLite connection before touching the file — always
- A fallback chain is just priority order + health counting + a retry budget; nothing magical
- python-dotenv tolerates spaces around `=` (verified the hard way)

## What's next

A vision agent: a local LLM brain (ollama) driving an in-process CNN classifier through three tools — same loop pattern, new capabilities.
