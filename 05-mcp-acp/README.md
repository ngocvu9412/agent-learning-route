# Week 5: Multi-Provider Support & MCP/ACP

What I was after: an abstraction layer so the agent isn't married to one provider — and automatic fallback when that provider dies.

## Concepts I worked through

### 1. Multi-Provider Architecture
Different providers have different strengths:
- **Google Gemini**: Generous free tier
- **z.ai**: GLM models
- **Anthropic**: Claude with long context
- **Local**: llama.cpp, Ollama (no API cost, offline)

**Provider Pattern**:
```python
class LLMProvider(ABC):
    @abstractmethod
    def chat(self, messages, model, **kwargs):
        """Make chat request"""
        pass

    @abstractmethod
    def parse_response(self, response):
        """Convert to standard format"""
        pass
```

**Why abstract**:
- Switch providers without changing agent code
- Compare models easily
- Fallback when one fails

The kicker I discovered: with the OpenAI SDK, both providers use the SAME client — only base_url, key, and model change. The abstraction is thin on purpose.

### 2. Provider Factory
```python
class ProviderFactory:
    _providers = {}

    @classmethod
    def register(cls, name, provider_class):
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, name, **kwargs):
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}")
        return cls._providers[name](**kwargs)

# Register
ProviderFactory.register("gemini", GeminiProvider)

# Use
provider = ProviderFactory.create("gemini", api_key="...")
response = provider.chat(messages, "gemini-flash-latest")
```

The division of labor that stuck with me: **the factory only BUILDS** (name → instance). It knows nothing about priorities, retries, or health.

### 3. Fallback Chain
Try providers in priority order until one succeeds:

```python
@dataclass
class ProviderEntry:
    provider: object
    model: str
    priority: int = 0
    error_count: int = 0
    last_error_time: float = 0.0

class FallbackChain:
    def add_provider(self, provider, model, priority=0):
        # append + sort by priority

    def get_healthy_providers(self):
        # error_count < 3, OR last error > 60s ago

    def chat(self, messages, max_retries=2):
        # per provider: retry with backoff, record errors,
        # return {"error": "All providers failed"} at the end
```

**Retryable vs Non-retryable Errors**:
- **Retryable**: Rate limits (429), timeouts, 502/503/504
- **Non-retryable**: 400 bad request, 401 unauthorized, 404 not found

Retrying a 404 (wrong model name) is pure waste — classify first, then retry.

### 4. MCP (Model Context Protocol)
MCP is the standard for connecting LLMs to tools and data:

**MCP Server**:
```json
// A server exposes tools via JSON-RPC
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": [
    {"name": "get_weather", "description": "...", "inputSchema": {...}}
  ],
  "id": 1
}
```

**MCP Client** (in my agent, conceptually):
```python
class MCPClient:
    def __init__(self, server_url):
        self.server_url = server_url

    async def list_tools(self):
        response = await http.post(f"{self.server_url}/tools/list")
        return response["result"]

    async def call_tool(self, name, args):
        response = await http.post(f"{self.server_url}/tools/call", {
            "name": name,
            "arguments": args
        })
        return response["result"]
```

**Benefits**:
- Language-agnostic: Write tools in Python, Go, Rust, etc.
- Standard protocol: All tools work the same way
- Pluggable: Add tools by connecting new servers
- Secure: Controlled access, permissions

### 5. ACP (Agent Communication Protocol)
ACP enables agent-to-agent communication:

**Use Cases**:
- Delegation: Agent A asks Agent B for help
- Collaboration: Multiple agents work on different aspects
- Distributed systems: Microservices of agents

**ACP Message Format**:
```json
{
  "from": "agent-id-1",
  "to": "agent-id-2",
  "type": "request",
  "content": "What's the weather in Tokyo?",
  "timestamp": "2024-08-04T10:00:00Z",
  "conversation_id": "conv-123"
}
```

The ACP server itself is Week 6's build.

## What I used
- `openai` SDK for both providers (same client, different base_url/key/model)
- `abc` (ABC, abstractmethod), `dataclasses`, `time` — all built-in

## Key Files in Hermes
- `agent/providers/gemini_adapter.py`: Google Gemini provider
- `agent/providers/openai_adapter.py`: OpenAI provider
- `agent/providers/llama_adapter.py`: Local provider
- `hermes_cli/fallback.py`: Fallback chain
- `hermes_cli/mcp_client.py`: MCP client

## The exercise
1. **exercise_9_provider_factory_and_fallback.ipynb** — one notebook, two halves: the factory half (LLMProvider ABC → GeminiProvider → ProviderFactory) and the fallback half (ProviderEntry dataclass → FallbackChain with health tracking and retries). Both halves shipped straight into the capstone's `providers.py`.

## Pitfalls I watched for
- **Not validating models**: Check if provider supports requested model
- **Infinite fallback loops**: Track failed providers, don't retry immediately
- **Different response formats**: Each provider returns slightly different JSON
- **Health state**: without error_count + last_error_time, a dead provider poisons every request

## Where I got to
- The agent switches providers seamlessly — same interface, same parse
- Fallback fires automatically when the primary provider fails
- All providers dead → clean error dict, not a crash

## What came next
Exposing the agent as a service — an ACP HTTP server.
