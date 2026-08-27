# Week 7 — Function Syntax Reference (Explained)

## SQLite in the agent loop
```python
# Load history — pull every saved message for this session, oldest first
rows = conn.execute(
    "SELECT role, content FROM messages WHERE session_id=? ORDER BY id",
    (self.session_id,)          # tuple fills the ? — trailing comma makes it a tuple!
).fetchall()

for r in rows:
    messages.append({"role": r[0], "content": r[1]})   # r[0]=role, r[1]=content (SELECT order)

# Save a message
conn.execute(
    "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
    (self.session_id, "user", user_input)
)
conn.commit()    # required after INSERT — without it the row vanishes when program ends
```

## Session IDs
```python
import time
session_id = f"s{int(time.time())}"     # "s1722864000" — unique per second, groups this chat's rows
```

## input() (terminal input)
```python
text = input("You: ")           # print the prompt, WAIT for the user to type + press Enter, return the string
text = input("You: ").strip()   # remove accidental spaces/newlines around the text
text.lower() in ("bye", "exit", "quit")   # check exit commands (lower() so "Quit" also works)
```

## lambda (inline functions)
```python
lambda: datetime.now().strftime("%H:%M:%S")   # zero-arg lambda — call it to get the time string
lambda a, b: a + b                             # two-arg lambda — adds its arguments

# stored in a dict as handlers (functions are values in Python — you can store them):
self._handlers = {
    "get_time": lambda: datetime.now().strftime("%H:%M:%S"),
    "add_numbers": lambda a, b: a + b,
}
```

## Interactive REPL pattern
```python
while True:                              # loop until user quits
    try:
        user_input = input("You: ").strip()
        if user_input.lower() in ("bye", "exit", "quit"):
            break                        # exit the while loop
        elif user_input:                 # skip empty input (just pressed Enter)
            self.chat(user_input)
    except KeyboardInterrupt:            # Ctrl+C pressed — exit gracefully, no traceback
        break
```

## The full agent loop essentials
```python
resp = client.chat.completions.create(model=..., messages=..., tools=...)
msg = resp.choices[0].message

messages.append(msg.model_dump(exclude_none=True))   # save to history; exclude_none stops Gemini 400 errors

if not msg.tool_calls:                               # empty/None = no more tools wanted →
    return msg.content                               # this IS the final answer

for tc in msg.tool_calls:
    fname = tc.function.name                         # which tool the LLM wants
    fargs = json.loads(tc.function.arguments)        # arguments arrive as a JSON string → dict
    result = self._handlers[fname](**fargs)          # dict → keyword args, run the tool
    messages.append({
        "role": "tool",                              # mark this as a tool result message
        "tool_call_id": tc.id,                       # link result to the specific request
        "name": fname,
        "content": str(result)                       # must be a string for the API
    })
```

## Wiring components in __init__
```python
class MiniHermesAgent:
    def __init__(self, db_path="mini_agent.db", model=None):
        self.model = model or os.environ.get("GEMINI_MODEL")   # argument wins; else .env value
        self.session_id = f"s{int(time.time())}"
        self._init_provider()      # creates self.client (OpenAI SDK pointed at Gemini)
        self._init_tools()         # creates self.tools (schemas) + self._handlers (dict)
        self._init_memory(db_path) # creates self.conn (SQLite) + the messages table
```

## try/except around everything
```python
try:
    resp = client.chat.completions.create(...)
except Exception as e:
    print(f"API error: {e}")      # network/key/quota problems — report instead of crashing
    return None
```

## Cleanup
```python
conn.close()               # close db connection — flushes everything safely
os.remove("mini_agent.db") # delete the test database between runs for a fresh start
```
