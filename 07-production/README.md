# Week 7: Integration & Production Readiness

## Learning Goals
- Integrate all components into a complete agent
- Make the agent production-ready (logging, config, CLI)
- Add comprehensive documentation
- Prepare for deployment

## Concepts

### 1. Full Agent Architecture
```
MiniHermesAgent
├── Provider Layer
│   ├── ProviderFactory
│   ├── FallbackChain
│   └── Multiple providers (Google Gemini, OpenAI, local)
├── Tool Layer
│   ├── ToolRegistry
│   ├── Builtin tools (filesystem, web, code)
│   └── MCP client for external tools
├── Memory Layer
│   ├── SQLite store
│   ├── Conversation history
│   └── User preferences
├── Agent Core
│   ├── Conversation loop
│   ├── Error handling
│   └── Context management
└── Interfaces
    ├── CLI interface
    ├── ACP server
    └── HTTP API
```

### 2. Configuration Management
Use `config.yaml` for all settings:

```yaml
model:
  default: gemini-flash-latest
  provider: gemini
  base_url: https://generativelanguage.googleapis.com/v1beta/openai

providers:
  gemini:
    api_key: ${GEMINI_API_KEY}  # From environment
  openai:
    api_key: ${GEMINI_API_KEY}

database:
  path: agent_memory.db

tools:
  filesystem:
    allowed_paths: ["/safe/dir"]
    max_file_size: 10MB

logging:
  level: INFO
  file: agent.log
```

**Load with Pydantic**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    default_model: str = "gemini-flash-latest"
    db_path: str = "agent_memory.db"

    class Config:
        env_file = ".env"
```

### 3. CLI Interface
Make agent usable from terminal:

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="MiniHermes Agent")
    parser.add_argument("query", nargs="*", help="Query to process")
    parser.add_argument("--model", help="Model to use")
    parser.add_argument("--server", action="store_true", help="Start ACP server")
    parser.add_argument("--port", type=int, default=8080, help="ACP server port")

    args = parser.parse_args()

    agent = MiniHermesAgent(model=args.model)

    if args.server:
        # Start ACP server
        start_acp_server(agent, port=args.port)
    elif args.query:
        # Single query
        response = agent.chat(" ".join(args.query))
        print(response)
    else:
        # Interactive mode
        agent.interactive_chat()

if __name__ == "__main__":
    main()
```

### 4. Logging & Observability
Track what your agent does:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("MiniHermes")

# Log important events
logger.info(f"Starting agent with model {model}")
logger.debug(f"Tool calls: {tool_calls}")
logger.warning(f"Retry {attempt} for {provider}")
logger.error(f"All providers failed")
```

### 5. Error Handling Best Practices

**Graceful Degradation**:
```python
def handle_tool_call(tool_name, args):
    try:
        return tool_registry.call(tool_name, args)
    except TimeoutError:
        logger.warning(f"Tool {tool_name} timed out")
        return "Tool timeout - try again"
    except PermissionError:
        logger.error(f"Tool {tool_name} permission denied")
        return "You don't have permission to run this"
    except Exception as e:
        logger.exception(f"Tool {tool_name} failed")
        return f"Tool error: {str(e)}"
```

**Circuit Breaker**:
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None

    def call(self, func):
        if self._is_open():
            raise CircuitBreakerOpenError()

        try:
            return func()
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            raise

    def _is_open(self):
        if self.failures >= self.failure_threshold:
            if time.time() - self.last_failure_time < self.timeout:
                return True
            else:
                self.failures = 0  # Reset after timeout
        return False
```

### 6. Documentation Structure

**Essential Files**:
```
my-agent/
├── README.md           # What it does, how to install, quick start
├── DESIGN.md           # Architecture, design decisions
├── CONFIGURATION.md    # All config options explained
├── API.md             # ACP API reference
├── CONTRIBUTING.md    # How to contribute
└── CHANGELOG.md       # Version history
```

**README.md** should include:
```markdown
# MiniHermes Agent

A lightweight AI agent with tool calling, memory, and multi-provider support.

## Features
- Multi-provider LLM support (Google Gemini, OpenAI, local)
- Persistent memory with SQLite
- Built-in tools (filesystem, web, code execution)
- MCP protocol support
- ACP server for agent-to-agent communication

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Interactive mode
python my_agent.py

# Single query
python my_agent.py "What files are in /home/user?"

# Start ACP server
python my_agent.py --server --port 8080
```

## Configuration

Create `.env` file:
```
GEMINI_API_KEY=your-key-here
```

Or use `config.yaml` for advanced settings.

## License

MIT
```

### 7. Production Checklist

**Before deploying**:
- [ ] All secrets in environment variables (never in code)
- [ ] Input validation on all user inputs
- [ ] Rate limiting on API endpoints
- [ ] Authentication enabled
- [ ] Logging configured (not DEBUG in production)
- [ ] Error tracking (Sentry, etc.)
- [ ] Database backups scheduled
- [ ] Health check endpoint (`/health`)
- [ ] Graceful shutdown handling
- [ ] Monitoring dashboards set up

**Testing**:
- [ ] Unit tests for core logic
- [ ] Integration tests for providers
- [ ] Load testing for performance
- [ ] Security audit for vulnerabilities

## Libraries You'll Need
- `pydantic-settings`: Configuration management
- `loguru`: Better logging
- `click` or `argparse`: CLI interface
- `uvicorn`: Production server

## Key Files in Hermes
- `hermes_cli/cli.py`: Main CLI interface
- `config.yaml`: Global configuration
- `agent/agent_init.py`: Agent initialization
- `gateway/`: Multi-platform deployment

## This Week's Exercises
1. **exercise_12_full_agent.ipynb**: Integrate all components into complete agent

## Common Pitfalls
- **Hardcoded paths**: Use config files and environment variables
- **Not cleaning up resources**: Close database connections, file handles
- **Silent failures**: Log all errors, even if handled
- **Missing graceful shutdown**: Handle SIGTERM/SIGINT

## Success Criteria
- Your agent runs from CLI with multiple modes
- It has configuration file support
- Logging captures important events
- README explains how to use it
- All components integrate seamlessly

## Next Week
Final project: Benchmark, stress test, and document your agent!