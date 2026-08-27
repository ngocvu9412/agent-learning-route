# Week 4: Memory Systems

What I was after: an agent that remembers yesterday's conversation without me re-explaining everything.

## Concepts I worked through

### 1. Why Agents Need Memory
LLMs are stateless - they forget everything between requests. Memory provides:

**Conversation History**:
- Remember what user asked 10 turns ago
- Maintain context for follow-up questions
- Enable multi-turn problem solving

**User Knowledge**:
- Remember user preferences ("I prefer Python over JavaScript")
- Store user facts ("User's name is Alex")
- Learn from corrections ("Don't use that API, use this one")

**Skills & Procedures**:
- Save useful workflows for reuse
- Store solutions to common problems
- Share knowledge between sessions

### 2. Memory Storage Options

**In-Memory (volatile)**:
```python
memory = {"messages": [], "user_facts": {}}
# Lost when agent restarts
```

**SQLite (persistent)**:
```python
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    messages TEXT  # JSON array
);
CREATE TABLE user_facts (
    key TEXT PRIMARY KEY,
    value TEXT,
    category TEXT
);
```

**Vector DB (semantic search)** — future territory for me:
- Store embeddings of conversations
- Find relevant past discussions
- Retrieve by similarity, not exact match

### 3. Conversation Compression
Context windows are limited (4k-128k tokens). Strategies:

**Summarization**:
```python
if len(messages) > 85% of max:
    # Summarize middle messages
    summary = llm.summarize(messages[10:-10])
    messages = [first_10, summary, last_10]
```

**Sliding Window**:
```python
# Keep only recent N messages
messages = messages[-100:]  # Last 100 messages
```

**Selective Retention**:
```python
# Keep important messages, drop filler
messages = [m for m in messages if m.is_important()]
```

### 4. Memory Store Design (what exercise 8 actually built)
```python
class MemoryStore:
    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)

    def save_message(self, session_id, role, content):
        # Store with timestamp

    def get_conversation(self, session_id, limit=100):
        # Retrieve conversation history

    def save_user_fact(self, key, value, category):
        # Store user preference/fact

    def get_user_fact(self, key):
        # Retrieve by key

    def save_skill(self, name, content, description):
        # Store reusable procedure

    def get_skill(self, name):
        # Retrieve by name

    def get_stats(self):
        # Row counts per table
```

Three tables: `conversations`, `user_facts`, `skills` — all created with `CREATE TABLE IF NOT EXISTS` and natural/surrogate keys explained in the notebook.

### 5. When to Save to Memory
**Save automatically**:
- Every user message
- Every assistant response
- Every tool call result

**Save on explicit request**:
- "Remember that I prefer..."
- "Save this as a skill: ..."
- User corrections

**Never save**:
- API keys and secrets
- Passwords
- PII without consent

## What I used
- `sqlite3`: built-in — no server, no drivers, perfect at this scale
- everything else was built-in Python

## Key Files in Hermes
- `agent/memory_store.py`: SQLite memory implementation
- `agent/context_engine.py`: Conversation management
- `agent/conversation_compression.py`: Compression strategies

## The exercise
1. **exercise_8_sqlite_memory.ipynb**: a complete `MemoryStore` — three tables (conversations, user_facts, skills), save/get for each, plus `get_stats()`

## Pitfalls I watched for
- **SQL injection**: Always use parameterized queries (`?` placeholders)
- **Race conditions**: Use transactions for writes
- **Not pruning old data**: Database grows indefinitely
- **Wrong JSON format**: Messages must be valid JSON

## Where I got to
- Conversations survive restarts — restart Python, same db, chat continues
- User facts and skills store and retrieve by key
- Parameterized queries everywhere

## What came next
One provider was a single point of failure — fallbacks.
