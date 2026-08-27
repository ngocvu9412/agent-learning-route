# Week 3: Tool System & MCP

## Learning Goals
- Build a flexible tool registry system
- Implement essential tools (filesystem, web search, code execution)
- Understand MCP (Model Context Protocol) for external tools
- Learn async vs sync tool execution

## Concepts

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

**Why this matters:**
- Easy to add new tools without changing agent code
- Tools can be loaded from plugins (Week 5)
- Support for categories (filesystem, web, code)

### 2. Essential Tool Categories

**Filesystem Tools**:
- `read_file(path)`: Read file contents
- `write_file(path, content)`: Write to file
- `list_files(path)`: List directory contents
- `search_in_files(query, path)`: Search for text in files
- `delete_file(path)`: Delete a file

**Web Tools**:
- `web_search(query)`: Search the web
- `fetch_url(url)`: Get webpage content
- `browse_web(query)`: AI-assisted web browsing

**Code Tools**:
- `execute_code(code)`: Run Python code
- `analyze_code(path)`: Get code structure
- `run_tests()`: Execute test suite

### 3. MCP (Model Context Protocol)
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

### 4. Sync vs Async Execution
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

## Libraries You'll Need
- `aiohttp`: Async HTTP requests (for MCP)
- `asyncio`: Async/await support
- `pathlib`: Modern file path handling

## Key Files in Hermes
- `tools/registry.py`: Tool registry implementation
- `tools/__init__.py`: Tool registration and discovery
- `hermes_cli/mcp_client.py`: MCP client code
- `tools/filesystem/*.py`: Filesystem tool implementations

## This Week's Exercises
1. **exercise_6_filesystem_tools.ipynb**: Implement 5 essential filesystem tools
2. **exercise_7_tool_registry.ipynb**: Build a tool registry that manages tools

## Common Pitfalls
- **Not validating paths**: Prevent `../../../etc/passwd` attacks
- **Timeout issues**: Code execution and web requests can hang
- **Memory leaks**: Keep file handles and connections closed
- **Race conditions**: Multiple tools writing same file

## Success Criteria
- Your registry can dynamically add/remove tools
- Filesystem tools are safe (no directory traversal)
- Tool schemas are valid JSON Schema
- You understand how MCP connects external tools

## Next Week
We'll add persistent memory to remember conversations across sessions!