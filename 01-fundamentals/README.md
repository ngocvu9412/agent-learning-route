# Week 1: Fundamentals & Environment

## Learning Goals
- Set up development environment for agent building
- Understand LLM APIs and how to call them
- Learn the structure of tool/function calling schemas
- Build a basic agent that responds to questions

## Concepts

### 1. LLM API Integration
LLM providers (Google Gemini, OpenAI, Anthropic) expose HTTP APIs for chat completions. The key components:

- **Base URL**: The API endpoint (e.g., `https://generativelanguage.googleapis.com/v1beta/openai`)
- **API Key**: Authentication credential
- **Model**: Which model to use (e.g., `gemini-flash-latest`)
- **Messages**: Array of conversation messages with roles (system, user, assistant)
- **Tools**: Optional array of function schemas the model can call

### 2. Tool/Function Calling Schemas
Tool calling allows the LLM to request your code to execute specific functions. The schema format:

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

## Libraries You'll Need
- `openai`: Universal SDK compatible with Google Gemini
- `python-dotenv`: Load API keys from .env files
- `nbformat`: Work with Jupyter notebooks (already installed)

## Key Files in Hermes
- `agent/providers/gemini_adapter.py`: How Hermes calls Google Gemini
- `agent/agent_init.py`: Setting up the agent environment
- `tools/__init__.py`: How tools are registered

## This Week's Exercises
1. **exercise_1_hello_agent.ipynb**: Build simplest agent - just call LLM and return response
2. **exercise_2_tool_schema.ipynb**: Define tool schemas and implement the function handler
3. **exercise_3_basic_loop.ipynb**: Implement the basic agent loop with tool calling

## Before Starting
1. Set your Google Gemini API key as environment variable:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```
2. Or create `.env` file in this folder:
   ```
   GEMINI_API_KEY=your-key-here
   ```

## Success Criteria
- You can call Google Gemini API and get responses
- You understand how to define tool schemas
- You can build a loop that executes tools when the LLM requests them

## Next Week
We'll add error handling and make the loop more robust!