# Week 2: Agent Core Architecture

## Learning Goals
- Understand the complete agent loop with error handling
- Learn retry logic for API failures
- Build robust conversation management
- Master the ReAct pattern (Reasoning + Acting)

## Concepts

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
API calls fail. Common issues:
- **Rate limits**: Too many requests → wait and retry
- **Timeouts**: Network issues → retry with exponential backoff
- **Invalid requests**: Bad parameters → don't retry (user error)
- **Server errors**: 500/502/503 → retry

**Exponential Backoff**:
- Wait 1s, then 2s, then 4s, then 8s
- `delay = base_delay * (2 ^ attempt)`

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
- Manage context window: summarize when too long (Week 4)

## Libraries You'll Need
- `tenacity`: Retry logic with exponential backoff
- `time`: For delays between retries

## Key Files in Hermes
- `agent/conversation_loop.py`: The core loop implementation
- `agent/fallback.py`: Error handling and retry logic
- `agent/context_engine.py`: Conversation history management

## This Week's Exercises
1. **exercise_4_error_handling.ipynb**: Classify errors and implement retry with exponential backoff
2. **exercise_5_complete_loop.ipynb**: Full agent with error handling, tools, and message management

## Common Pitfalls
- **Infinite loops**: Always set `max_iterations` (default 10-20)
- **Missing tool_call_id**: Each tool result must reference which call it answers
- **Wrong role values**: Only use "system", "user", "assistant", "tool"
- **Not validating tool results**: Check function returned successfully before appending

## Success Criteria
- Your agent recovers from rate limit errors automatically
- It stops after giving a final answer (not infinite loops)
- It handles multiple tool calls in a single turn
- Error messages are clear, not cryptic

## Next Week
We'll build a sophisticated tool system with registry and discovery!