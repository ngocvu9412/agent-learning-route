# StudyTracker — Exercise 11 Project Roadmap

An agent that tracks what you study and reports on it.
Two providers with fallback, two simple tools, a JSON log file.

You write ALL the code. The .py files are stubs with hints.

## Files

```
providers.py   ZaiProvider + GeminiProvider classes, ProviderFactory,
               FallbackChain with health tracking                (ex-9 structure)
tools.py       2 tools (log_session, weekly_report) + schemas     (ex-2/3/6)
memory.py      MemoryStore: SQLite conversations + user_facts      (ex-8/11)
agent.py       the loop                                           (ex-3/5)
run.py         REPL + demo                                        (ex-11)
.env.example   keys to ADD to ../.env at the route root
```

Data stays simple: a JSON file and plain-function tools. The CLASSES live
in providers.py — that's where the ex-9 structure earns its keep
(priority, retries, per-provider health).

## Provider plan (priority = fallback order)

| pri | provider class | base_url | model | env |
|---|---|---|---|---|
| 1 | ZaiProvider | https://api.z.ai/api/paas/v4 | glm-4.5-flash | ZAI_API_KEY |
| 2 | GeminiProvider | ...googleapis.com/v1beta/openai | from GEMINI_MODEL | GEMINI_API_KEY (existing) |

Order = the lesson: free unlimited first, 20/day quota last.
Both use the SAME OpenAI SDK client — only base_url/key/model change.
Division of labor (your ex-9 takeaway): ProviderFactory only BUILDS
(name -> instance); FallbackChain RUNS (priority, retries, health).

---

## Phase 0 — setup                                   [10 min]

- [ ] add ZAI_API_KEY to ../.env (route root; .env.example shows how)
- [ ] `py -3.14 run.py` prints the banner and exits cleanly

## Phase 1 — tools.py                                [~1 hr]

- [ ] _load / _save: JSON file round-trip
- [ ] log_session(topic, minutes): append + save + confirmation string
- [ ] weekly_report(): last 7 days, minutes per topic, one string
- [ ] TOOL_FUNCTIONS dispatch dict + get_tool_schemas() (2 schemas)
- [ ] ACCEPT: in a REPL — log_session("rag", 45); weekly_report() shows it;
      log twice, hours accumulate

## Phase 2 — providers.py                            [~2 hrs]

- [ ] ZaiProvider + GeminiProvider: __init__ (client, model) + chat
      (NO try/except inside — errors must reach the chain)
- [ ] ProviderFactory: register / create (ValueError on unknown name)
- [ ] ProviderEntry dataclass + FallbackChain: add_provider sorts by
      entry.priority; get_healthy_providers (error_count < 3 OR last
      error > 60s ago); chat retries max_retries=2 per provider with
      2**attempt backoff, short-circuit return on success,
      {"error": "All providers failed"} at the end
- [ ] build_chain(): factory-register both, add only providers whose
      key exists in env
- [ ] ACCEPT (~2 API calls): one real chat through priority-1; then
      pass model="bogus" to the ZaiProvider in build_chain -> answer
      still arrives from Gemini; poison both -> {"error": ...}, no crash

## Phase 3 — agent.py                                [~2 hrs]

- [ ] chat loop: copy your ex-3 run_agent_loop shape; swap
      client...create -> self.chain.chat, dispatch dict -> TOOL_FUNCTIONS
- [ ] the tool message: role/tool_call_id/name/content, json.dumps(result)
- [ ] turn cap 6; chain-error -> friendly message, no crash
- [ ] ACCEPT: "Log 30 minutes of rag" -> study_log.json grows;
      "What did I study?" -> answered from weekly_report, not memory

## Phase 4 — run.py + polish                         [~1 hr]

- [ ] repl() + demo()
- [ ] error handling: unknown tool name -> "Error: ..." message back
      to the model (ex-2 pattern), not a crash
- [ ] full flow works twice in a row (restart python, same JSON file)

## Phase 5 — memory + polish

- [ ] memory.py: MemoryStore — conversations table (full-dict JSON round-trip!)
      + user_facts table (upsert pattern). Study sessions STAY in JSON —
      one dataset, one home
- [ ] wire into agent: load history at chat() start, save new messages at
      end (saved_upto pattern from ex-11); session_id = f"s{int(time.time())}"
- [ ] "what's my name?" -> "Alex" from user_facts (save_user_fact first) —
      proves cross-turn + cross-restart memory
- [ ] restart python, same db -> conversation continues where it left off
- [ ] close the connection cleanly (WinError 32 lesson: close before delete)

## Phase 6 — optional extras

- [ ] third tool: strength_report() (per-topic totals, same file)
- [ ] system prompt with a bit of personality + today's date
- [ ] close connection on exit: try/finally in run.py around repl()

---

## Cost control

- Phases 1, 3: 0 API calls (test tools + loop with fake providers —
  a ZaiProvider-shaped stand-in returning/raising on script; the
  smoke-test pattern you used for tools.py)
- Phase 2 ACCEPT: ~2 real calls. Phase 3 ACCEPT: ~3-5.
- Poisoned model = permanent 404 = instant skip, costs nothing.

## Where each piece comes from

| phase | you already built this in |
|---|---|
| 1 | ex-6 (file tools), ex-2 (schemas) |
| 2 | ex-9 (chain), ex-4 (retryable) |
| 3 | ex-3 / ex-5 (the loop) |
| 4 | ex-2 (error-as-message), ex-11 (REPL) |
| 5 | ex-8 (SQLite, upserts) + ex-11 (400 lesson, saved_upto) |
