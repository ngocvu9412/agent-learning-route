# Week 6: ACP Server & Advanced Patterns

## Learning Goals
- Build an ACP server to expose your agent as a service
- Learn HTTP server patterns for agent APIs
- Understand advanced agent patterns (delegation, collaboration)
- Implement authentication and security

## Concepts

### 1. ACP Server Architecture
An ACP server makes your agent accessible to other agents:

```
Agent A           Agent B (Your Agent with ACP Server)
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
Use Python's built-in `http.server` or frameworks like FastAPI:

**Simple HTTP Server**:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class ACPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            message = json.loads(post_data.decode())

            # Process with agent
            response = agent.chat(message["content"])

            # Send ACP response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "from": agent.id,
                "to": message["from"],
                "type": "response",
                "content": response,
                "timestamp": datetime.now().isoformat()
            }).encode())

def run_server(port=8080):
    httpd = HTTPServer(('localhost', port), ACPRequestHandler)
    httpd.serve_forever()
```

**FastAPI (more production-ready)**:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ACPMessage(BaseModel):
    from: str
    to: str
    type: str
    content: str
    timestamp: str

@app.post("/message")
async def handle_message(message: ACPMessage):
    response = agent.chat(message.content)
    return ACPMessage(
        from=agent.id,
        to=message.from,
        type="response",
        content=response,
        timestamp=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8080)
```

### 3. ACP Endpoints

**Standard ACP Endpoints**:
- `POST /message`: Send message to agent
- `GET /agents`: List available agents
- `GET /runs/{id}`: Get status of async run
- `POST /runs`: Start async task

**Authentication**:
```python
# Simple API key check
API_KEYS = ["secret-key-1", "secret-key-2"]

def check_auth(request):
    api_key = request.headers.get('X-API-Key')
    return api_key in API_KEYS

# Or OAuth 2.0 for production
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

## Libraries You'll Need
- `fastapi`: Modern web framework
- `uvicorn`: ASGI server for FastAPI
- `asyncio`: Async/await support
- `httpx`: Async HTTP client

## Key Files in Hermes
- `acp_adapter/server.py`: ACP server implementation
- `agent/async_utils.py`: Parallel execution utilities
- `agent/conversation_compression.py`: Compression strategies

## This Week's Exercises
1. **exercise_11_acp_server.ipynb**: Build a complete ACP server with endpoints

## Common Pitfalls
- **Blocking I/O**: Use async/await for HTTP calls
- **Memory leaks**: Clean up old conversations
- **Race conditions**: Handle concurrent requests properly
- **Not validating input**: Sanitize all incoming messages

## Success Criteria
- Your ACP server handles POST /message requests
- It returns valid ACP responses
- Multiple agents can communicate with your server
- You understand delegation patterns

## Next Week
We'll integrate everything into a complete production-ready agent!