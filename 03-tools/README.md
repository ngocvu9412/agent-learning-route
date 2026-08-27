# Week 3: Tool System & MCP

What I was after: stop hardcoding tools — build a registry, and understand what MCP adds on top.

## Concepts I worked through

### 1. Tool Registry Pattern
Instead of hardcoding tool names, use a registry:

```python
class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, description, parameters, handler, category="general"):
        self._tools[name] = Tool(name, description, parameters, handler, category)

    def get_schema(self, name):
        return self._tools[name].to_schema()

    def call(self, name, args):
        return self._tools[name].handler(**args)
```

**Why this matters**:
- Easy to add new tools without changing agent code
- Tools can be loaded from plugins (Week 5)
- Support for categories (filesystem, web, code)

**Essential tool categories** (what Hermes ships):
- **Filesystem**: `read_file`, `write_file`, `list_files`, `search_in_files`, `delete_file`
- **Web**: `web_search`, `fetch_url`, `browse_web`
- **Code**: `execute_code`, `analyze_code`, `run_tests`

I implemented the filesystem set myself (exercise 6); the web/code categories stayed conceptual for me at this stage — good to know Hermes's 186+ tools organize along these lines.

### 2. MCP (Model Context Protocol)
MCP is a standard for connecting LLMs to external tools and data:

**Architecture**:
```
Agent → MCP Client → MCP Server → External System
                      (e.g., GitHub, DB, API)
```

**Key Benefits**:
- **Standardized**: All tools use same protocol
- **Pluggable**: Add new tools by connecting MCP servers
- **Language-agnostic**: Server can be any language
- **Secure**: Controlled tool access and permissions

**Hermes Implementation**:
- `hermes_cli/mcp_client.py`: Connects to MCP servers
- `hermes_cli/mcp_server.py`: Runs tool servers
- `tools/mcp_*.py`: Tools exposed via MCP

**Exercise 7 simulated this**: a fake `MCPServer` class (name, command, connect/disconnect) — enough to feel the shape of the protocol without running a real server.

### 3. Sync vs Async Execution
**Sync (blocking)**:
```python
def call_tool_sync(name, args):
    result = tool_registry.call(name, args)
    return result  # Agent waits
```

**Async (non-blocking)**:
```python
async def call_tool_async(name, args):
    result = await tool_registry.call_async(name, args)
    return result  # Agent continues
```

**When to use which**:
- **Sync**: Simple tools (read_file, get_time)
- **Async**: I/O heavy (web_search, execute_code with timeout)
- **Parallel**: Run multiple independent tools together

My tools stayed sync (simple functions — the right complexity level for me); async stayed a theory note.

## What I used
- `pathlib`: file path handling, `read_text` / `glob` / `unlink`
- `dataclasses`: the `Tool` dataclass in exercise 7

## Key Files in Hermes
- `tools/registry.py`: Tool registry implementation
- `tools/__init__.py`: Tool registration and discovery
- `hermes_cli/mcp_client.py`: MCP client code
- `tools/filesystem/*.py`: Filesystem tool implementations

## The exercises
1. **exercise_6_filesystem_tools.ipynb**: `FileSystemTools` class — write/read/list/search/delete + `get_tool_schemas()` for all five
2. **exercise_7_tool_registry.ipynb**: `Tool` dataclass → `ToolRegistry` (register/get_schema/call/list) → a simulated `MCPServer` class

## Pitfalls I watched for
- **Not validating paths**: Prevent `../../../etc/passwd` attacks
- **Timeout issues**: Code execution and web requests can hang
- **Memory leaks**: Keep file handles and connections closed
- **Race conditions**: Multiple tools writing same file

## Where I got to
- The registry adds/removes tools dynamically at runtime
- Filesystem tools are safe (no directory traversal)
- Tool schemas are valid JSON Schema

## What came next
The agent worked but forgot everything on restart — memory.
