# Week 1: Fundamentals & Environment

What I was after: make my first LLM calls, learn the tool-schema format, and get one real agent loop running.

## Concepts I worked through

### 1. LLM API Integration
LLM providers (Google Gemini, OpenAI, Anthropic) expose HTTP APIs for chat completions. The key components:

- **Base URL**: The API endpoint (e.g., `https://generativelanguage.googleapis.com/v1beta/openai`)
- **API Key**: Authentication credential
- **Model**: Which model to use (e.g., `gemini-flash-latest`)
- **Messages**: Array of conversation messages with roles (system, user, assistant)
- **Tools**: Optional array of function schemas the model can call

### 2. Tool/Function Calling Schemas
Tool calling lets the LLM request that my code execute a function. The schema format:

```json
{
  "type": "function",
  "function": {
    "name": "get_current_weather",
    "description": "Get current weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City name"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
}
```

### 3. The Agent Loop (Preview)
An agent is a loop:
1. **Observe**: Read user input and conversation history
2. **Think**: Ask LLM what to do (may request tool calls)
3. **Act**: Execute tools, get results
4. **Learn**: Add tool results back to conversation
5. **Repeat** until LLM gives final answer

## What I used
- `openai`: universal SDK, pointed at Google Gemini
- `python-dotenv`: load the API key from `.env` at the route root (`load_dotenv("../.env")`)

## Key Files in Hermes
- `agent/providers/gemini_adapter.py`: How Hermes calls Google Gemini
- `agent/agent_init.py`: Setting up the agent environment
- `tools/__init__.py`: How tools are registered

## The exercises
1. **exercise_1_hello_agent.ipynb**: simplest agent — one call to the LLM, no tools
2. **exercise_2_tool_schema.ipynb**: a weather tool schema + handler, plus error handling for unknown functions and wrong arguments
3. **exercise_3_basic_loop.ipynb**: the basic agent loop — `get_time` / `add_numbers` tools, a dispatcher, model requests → code executes → result goes back

## Setup I used
The `.env` file lives at the route root (the parent of this folder) — every notebook loads it with `load_dotenv("../.env")`:
```
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-flash-latest
```

## Where I got to
- Calling the Gemini API and getting real responses back
- Defining tool schemas the model actually calls
- A loop that executes tools when the LLM requests them

## What came next
Error handling and retries — the loop worked, but any API hiccup killed it.
