# Week 5: Multi-Provider Support & MCP/ACP

## Learning Goals
- Build abstraction layer for multiple LLM providers
- Implement automatic fallback when providers fail
- Understand MCP (Model Context Protocol) in depth
- Learn ACP (Agent Communication Protocol) for agent-to-agent communication

## Concepts

### 1. Multi-Provider Architecture
Different providers have different strengths:
- **Google Gemini**: Access to many models (Gemini, Claude, GPT, etc.)
- **OpenAI**: Best GPT-4 models
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

### 2. Provider Factory
```python
class ProviderFactory:
    _providers = {}

    @classmethod
    def register(cls, name, provider_class):
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, name, **kwargs):
        return cls._providers[name](**kwargs)

# Register
ProviderFactory.register("gemini", GeminiProvider)
ProviderFactory.register("openai", OpenAIProvider)

# Use
provider = ProviderFactory.create("gemini", api_key="...")
response = provider.chat(messages, "gemini-flash-latest")
```

### 3. Fallback Chain
Try providers in priority order until one succeeds:

```python
class FallbackChain:
    def __init__(self):
        self.providers = []  # (provider, model, priority)

    def add_provider(self, provider, model, priority=0):
        self.providers.append((provider, model, priority))
        self.providers.sort(key=lambda x: x[2])  # Sort by priority

    def chat(self, messages):
        for provider, model, _ in self.providers:
            try:
                return provider.chat(messages, model)
            except RetryableError:
                continue  # Try next provider
        raise AllProvidersFailedError()
```

**Retryable vs Non-retryable Errors**:
- **Retryable**: Rate limits (429), timeouts, 502/503/504
- **Non-retryable**: 400 bad request, 401 unauthorized, 404 not found

### 4. MCP (Model Context Protocol) Deep Dive
MCP is the standard for connecting LLMs to tools and data:

**MCP Server**:
```python
# A server exposes tools via JSON-RPC
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}

# Response
{
  "jsonrpc": "2.0",
  "result": [
    {"name": "get_weather", "description": "...", "inputSchema": {...}}
  ],
  "id": 1
}
```

**MCP Client** (in your agent):
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

**Hermes ACP Server**:
```python
# Exposes agent as ACP endpoint
# acp_adapter/server.py
class ACPServer:
    def handle_message(self, message):
        # Route to agent
        response = agent.chat(message.content)
        # Send back to requester
        return ACPMessage(from=self.id, to=message.from, ...)
```

## Libraries You'll Need
- `httpx` or `aiohttp`: HTTP client for MCP/ACP
- `pydantic`: Validate message schemas

## Key Files in Hermes
- `agent/providers/gemini_adapter.py`: Google Gemini provider
- `agent/providers/openai_adapter.py`: OpenAI provider
- `agent/providers/llama_adapter.py`: Local provider
- `hermes_cli/fallback.py`: Fallback chain
- `hermes_cli/mcp_client.py`: MCP client
- `hermes_cli/mcp_server.py`: MCP server
- `acp_adapter/server.py`: ACP server

## This Week's Exercises
1. **exercise_9_provider_factory.ipynb**: Build provider factory with multiple providers
2. **exercise_10_fallback_chain.ipynb**: Implement fallback chain with error classification

## Common Pitfalls
- **Not validating models**: Check if provider supports requested model
- **Infinite fallback loops**: Track failed providers, don't retry immediately
- **Different response formats**: Each provider returns slightly different JSON
- **MCP connection timeouts**: Servers can be slow or offline

## Success Criteria
- Your agent can switch between providers seamlessly
- It falls back automatically when primary provider fails
- You can connect to MCP servers and use their tools
- You understand how agents communicate via ACP

## Next Week
We'll build an ACP server to expose your agent to other agents!