# Week 7 — Function Syntax Reference (Explained)

The syntax StudyTracker actually uses, with notes on where each piece earns its keep.

## JSON round-trip storage (the 400 lesson)
```python
# Save — store the WHOLE message dict, not (role, content) pairs.
# Gemini 400s ("invalid argument") if a tool message loses tool_call_id.
self.conn.execute(
    "INSERT INTO conversations (session_id, message) VALUES (?, ?)",
    (session_id, json.dumps(msg))    # dict → JSON string, nothing dropped
)
conn.commit()

# Restore — lossless: json.loads brings the exact dict back
rows = conn.execute(
    "SELECT message FROM conversations WHERE session_id = ? ORDER BY id LIMIT ?",
    (session_id, limit)
).fetchall()
history = [json.loads(r["message"]) for r in rows]
```

## Env loading that works from any cwd
```python
from pathlib import Path
load_dotenv(Path(__file__).resolve().parent.parent / ".env")   # route root — machine-independent
load_dotenv()                                                    # plus cwd/.env if present
```

## Session handling
```python
# All distinct sessions (for the picker at startup)
rows = conn.execute("SELECT DISTINCT session_id FROM conversations").fetchall()
sessions = [row["session_id"] for row in rows]
```

## The dispatch dict (tools without classes)
```python
TOOL_FUNCTIONS = {
    "log_session": log_session,     # name → plain function
    "weekly_report": weekly_report,
}

# The model asks; the dict answers:
result = TOOL_FUNCTIONS[tc.function.name](**args)   # **args unpacks the JSON dict
```

## The tool result message
```python
messages.append({
    "role": "tool",                     # marks this as a tool result
    "tool_call_id": tc.id,              # links result to the exact call
    "name": tc.function.name,
    "content": json.dumps(result),      # must be a string for the API
})
```

## Chain errors as values, not exceptions
```python
response = self.chain.chat(messages=..., tools=...)
if isinstance(response, dict) and "error" in response:
    return "Sorry — all providers are down right now."   # graceful, no crash
```

## Health tracking (circuit-breaker shape)
```python
provider_entry.error_count += 1
provider_entry.last_error_time = time.time()

# Healthy = fewer than 3 errors, OR the last error was >60s ago
healthy = [e for e in self._providers
           if e.error_count < 3 or (time.time() - e.last_error_time > 60)]
```

## Retry with backoff, classify first
```python
retryable = ["rate limit", "timeout", "502", "503", "504"]
if not any(p in error_str.lower() for p in retryable):
    break            # permanent error (e.g. 404 bad model) — stop wasting calls
time.sleep(2 ** attempt)   # 1s, 2s, 4s
```

## Date math for weekly_report
```python
from datetime import date, timedelta
cutoff = date.today() - timedelta(days=7)
if date.fromisoformat(session["date"]) >= cutoff:   # ISO strings compare as dates
    ...
```

## input() REPL essentials
```python
user_input = input("You: ")
if user_input == "quit":
    break
print(f"Agent: {agent.chat(user_input)}")
```
