# Week 2: Agent Core Architecture

What I was after: a loop that survives API failures instead of crashing on the first rate limit.

## Concepts I worked through

### 1. The Complete Agent Loop
```
Initialize conversation history with system prompt
Loop until done:
  1. Call LLM with messages + tools
  2. Parse response:
     - If has tool_calls:
       * For each tool call:
         - Extract name and arguments
         - Execute the function
         - Append tool result to messages
     - If no tool_calls:
       * Return assistant message (done!)
  3. Handle errors with retry logic
```

### 2. Error Handling & Retry Logic
API calls fail. What I ran into:
- **Rate limits**: Too many requests → wait and retry
- **Timeouts**: Network issues → retry with exponential backoff
- **Invalid requests**: Bad parameters → don't retry (user error)
- **Server errors**: 500/502/503 → retry

**Exponential Backoff**:
- Wait 1s, then 2s, then 4s, then 8s
- `delay = base_delay * (2 ^ attempt)`

I wrote the retry loop by hand with `time.sleep` — no retry library needed, and I understood every line.

### 3. ReAct Pattern (Reasoning + Acting)
The LLM should:
1. **Reason**: "I need to check the weather to answer this question"
2. **Act**: Call `get_current_weather(location="New York")`
3. **Observe**: "Weather in New York is 72°F"
4. **Reason again**: "Now I can answer: It's 72°F in New York"
5. **Answer**: "The weather in New York is 72°F and sunny."

This requires good system prompting:
```
You are a helpful assistant with access to tools.
When you need information, call the appropriate tool.
Think step by step about what you need.
```

### 4. Conversation History Management
- Keep all messages in an array
- Each message has: `role` (system/user/assistant/tool), `content`
- Tool results have: `role="tool"`, `tool_call_id`, `content`

## What I used
- `openai` + `python-dotenv` (same setup as week 1)
- `time` (built-in) for delays between retries

## Key Files in Hermes
- `agent/conversation_loop.py`: The core loop implementation
- `agent/fallback.py`: Error handling and retry logic
- `agent/context_engine.py`: Conversation history management

## The exercises
1. **exercise_4_error_handling.ipynb**: `ErrorClassifier` (retryable vs permanent), then `safe_api_call` with exponential backoff — plus a deliberately broken model to prove the permanent-error path
2. **exercise_5_complete_loop.ipynb**: the full loop — tools, error classification, message management in one `run_conversation`

## Pitfalls I watched for
- **Infinite loops**: always set `max_iterations` (mine default to 10)
- **Missing tool_call_id**: each tool result must reference which call it answers
- **Wrong role values**: only "system", "user", "assistant", "tool"
- **Not validating tool results**: check the function returned successfully before appending

## Where I got to
- The agent recovers from rate-limit errors automatically
- It stops after a final answer instead of looping forever
- Multiple tool calls in a single turn work
- Errors come back as readable messages, not tracebacks

## What came next
Hardcoding tool names was getting old — a real tool registry.
