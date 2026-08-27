# Week 4: Memory Systems

## Learning Goals
- Understand why agents need memory
- Build persistent storage for conversations and facts
- Learn conversation compression for context management
- Implement user preference storage

## Concepts

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
# Hermes approach
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    messages TEXT  # JSON array
);
CREATE TABLE user_facts (
    key TEXT PRIMARY KEY,
    value TEXT,
    category TEXT  # identity, preference, etc.
);
```

**Vector DB (semantic search)**:
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

### 4. Memory Store Design (Hermes)
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

    def search_facts(self, query):
        # Vector search for relevant facts
```

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

## Libraries You'll Need
- `sqlite3`: Built-in Python database
- `sentence-transformers`: For embeddings (advanced)
- `chromadb` or `faiss`: Vector database (advanced)

## Key Files in Hermes
- `agent/memory_store.py`: SQLite memory implementation
- `agent/context_engine.py`: Conversation management
- `agent/conversation_compression.py`: Compression strategies

## This Week's Exercises
1. **exercise_8_sqlite_memory.ipynb**: Build a complete SQLite memory store

## Common Pitfalls
- **SQL injection**: Always use parameterized queries
- **Race conditions**: Use transactions for writes
- **Not pruning old data**: Database grows indefinitely
- **Wrong JSON format**: Messages must be valid JSON arrays

## Success Criteria
- Your agent remembers conversations across restarts
- It can retrieve user preferences
- Database handles concurrent access safely
- You understand when to compress context

## Next Week
We'll add support for multiple LLM providers and automatic fallbacks!