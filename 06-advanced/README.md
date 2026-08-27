# Week 6: ACP Server & Advanced Patterns

What I was after: expose my agent as a service other agents can call — HTTP endpoints, runs, agent discovery.

## Concepts I worked through

### 1. ACP Server Architecture
An ACP server makes my agent accessible to other agents:

```
Agent A           Agent B (My Agent with ACP Server)
   |                          |
   |--- ACP Request --------->|
   |    "What's the weather?" |
   |                          |
   |   (Agent processes)      |
   |                          |
   |<-- ACP Response ---------|
   |   "72°F in Tokyo"        |
```

### 2. HTTP Server for Agents
Python's built-in `http.server` was enough:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class ACPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/runs":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            message = json.loads(post_data.decode())

            # Process with agent, send JSON response
            self._send_json({"status": "completed", "result": ...}, 201)
```

No FastAPI/uvicorn needed for this scale — one handler class, three routes, done. (FastAPI is the production path; that's a later journey.)

### 3. The Endpoints I Implemented
- `GET /agents` — list registered agents (id, name, description, capabilities)
- `POST /runs` — submit a task: read body, create a run id (`str(uuid.uuid4())[:8]`), store, respond 201
- `GET /runs/{id}` — fetch a run's status/result, 404 when unknown

**Authentication** (theory for now):
```python
# Simple API key check
API_KEYS = ["secret-key-1", "secret-key-2"]

def check_auth(request):
    api_key = request.headers.get('X-API-Key')
    return api_key in API_KEYS
```

### 4. Advanced Agent Patterns

**Delegation**:
Agent A delegates a specialized task to Agent B:
```
User: "Analyze this dataset"
Agent A: [delegates to data-analyst agent]
Agent B: [performs analysis]
Agent B -> Agent A: "Analysis complete: ..."
Agent A -> User: "Here's the analysis: ..."
```

**Collaboration**:
Multiple agents work together:
```
User: "Build a web scraper"
Agents:
  - Planner agent: breaks down task
  - Coder agent: writes scraper code
  - Tester agent: tests scraper
  - Reporter agent: summarizes results
```

**Hierarchical Agents**:
```
Orchestrator Agent
  ├── Web Agent
  ├── File Agent
  ├── Code Agent
  └── Memory Agent
```

### 5. Conversation Compression (Advanced)
When context gets too long, compress intelligently:

```python
def compress_conversation(messages):
    # Keep first 2 (system, initial user)
    # Keep last 5 (recent context)
    # Summarize middle

    if len(messages) <= 50:
        return messages

    first_part = messages[:2]
    last_part = messages[-5:]
    middle_part = messages[2:-5]

    # Summarize middle with LLM
    summary = llm.summarize(middle_part)

    return first_part + [summary] + last_part
```

### 6. Parallel Tool Execution
Run multiple tools at once when independent:

```python
import asyncio

async def execute_parallel_tools(tool_calls):
    """Execute multiple tools concurrently"""
    tasks = [
        tool_registry.call_async(t.name, t.args)
        for t in tool_calls
    ]
    results = await asyncio.gather(*tasks)
    return results

# Example: user asks "Check weather in Tokyo, London, and Paris"
# Agent generates 3 tool calls
# Execute all 3 in parallel instead of sequentially
```

## What I used
- `http.server` (built-in) — HTTPServer, BaseHTTPRequestHandler
- `json`, `uuid` (built-in)

## Key Files in Hermes
- `acp_adapter/server.py`: ACP server implementation
- `agent/async_utils.py`: Parallel execution utilities
- `agent/conversation_compression.py`: Compression strategies

## The exercise
1. **exercise_10_acp_server.ipynb**: the ACP server — `AGENTS`/`RUNS` stores, `ACPRequestHandler` (`_send_json`, `do_GET` for /agents and /runs/{id}, `do_POST` for /runs), `run_server(port=8080)` on localhost

## Pitfalls I watched for
- **Blocking I/O**: Use async/await for HTTP calls (theory note — my server is sync)
- **Memory leaks**: Clean up old conversations/runs
- **Race conditions**: Handle concurrent requests properly
- **Not validating input**: Sanitize all incoming messages

## Where I got to
- GET /agents lists the registry; GET /runs/{id} returns stored runs (404 on unknown)
- POST /runs creates a run and responds 201
- Everything is JSON in, JSON out

## What came next
Putting it all together: the StudyTracker capstone.
