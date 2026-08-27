# StudyTracker — the capstone

An agent that tracks what I study and reports back. I tell it *"log 45 minutes of langgraph"*; later I ask *"what did I study this week?"* and it answers from its own log file — not from the model's fuzzy recollection.

This is where everything from the route comes together: the provider chain from ex-9, the loop from ex-3/5, tool schemas from ex-2, SQLite memory from ex-8. No frameworks — just the OpenAI SDK, plain functions, a dispatch dict, a JSON file, and SQLite.

## The pieces

| File | What it does | Grew out of |
|---|---|---|
| `providers.py` | ZaiProvider + GeminiProvider, ProviderFactory, FallbackChain with health tracking | ex-9 |
| `tools.py` | `log_session` / `weekly_report` tools + JSON schemas, JSON log file | ex-2/6 |
| `memory.py` | SQLite: conversations stored as full JSON round-trips, survives restarts | ex-8/11 |
| `agent.py` | the loop: model → tool calls → results → model, turn cap 6 | ex-3/5 |
| `run.py` | REPL: pick or create a session, then chat | ex-11 |
| `ROADMAP.md` | the phase-by-phase plan I built from, kept as a record | — |

## Providers

Priority-ordered fallback, both behind the same OpenAI SDK client — only base URL, key, and model change:

| pri | provider | model | env |
|---|---|---|--- |
| 1 | z.ai | `glm-4.5-flash` | `ZAI_API_KEY` |
| 2 | Google | `gemini-flash-latest` (from `GEMINI_MODEL`) | `GEMINI_API_KEY` |

A provider is marked unhealthy after 3 errors (or skips if its last error was <60s ago); the chain retries twice per provider with exponential backoff. The factory only *builds* providers; the chain *runs* them — that separation was the ex-9 lesson.

## Run it

```bash
# keys go in .env at the route root (see .env.example); .venv has the deps
py run.py
```

The REPL lists saved sessions — pick one by number or start a new one — then chat. Tool calls (`log_session`, `weekly_report`) fire automatically when the model asks for them.

## What "done" meant

The acceptance bar I set before calling it finished:

- tool round-trip: "log 30 min" grows `study_log.json`; "what did I study?" answers from `weekly_report`, not memory
- persistence is lossless across restarts (same session continues where it left off)
- no duplicate rows when the same message is re-saved
- every provider dead → `{"error": "All providers failed"}` message, never a crash
- unknown tool name → error message back to the model, never a crash

## What I'd do next

- `weekly_report` covering a custom date range, not just last 7 days
- a third tool: `strength_report()` (per-topic totals)
- a system prompt with a bit of personality + today's date
