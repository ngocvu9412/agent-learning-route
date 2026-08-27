"""StudyTracker agent — the loop from exercises 3/5, with the chain plugged in.

Where ex 3 called client.chat.completions.create directly, this calls
chat_with_fallback. Everything else you already know:
model_dump, tool_calls, json.loads of the arguments string, the tool message.
"""
import json

from providers import build_chain
from tools import TOOL_FUNCTIONS, get_tool_schemas
from memory import MS

class StudyTrackerAgent:
    """TODO: build chain + tools, then the chat loop."""

    def __init__(self, session_id):
        # Hint:
        #   self.chain = build_chain()
        #   self.schemas = get_tool_schemas()
        #   self.functions = TOOL_FUNCTIONS
        self.chain = build_chain()
        self.schemas = get_tool_schemas()
        self.functions = TOOL_FUNCTIONS
        self.session_id = session_id

    def save_message(self, messages):
        for message in messages:
            MS.save_message(self.session_id, message)

    def chat(self, user_input: str) -> str:
        """TODO: the loop — this is exercise 3's run_agent_loop with two swaps:
        client...create(...) becomes chat_with_fallback(...), and the dispatch
        dict is self.functions.
        """
        old_messages = MS.get_conversation(self.session_id)
        if old_messages == []:
            old_messages = [
                {"role": "system", "content": "You are a study-tracking assistant."},
            ]

        new_messages = []
        new_messages.append({"role": "user", "content": user_input})

        for iteration in range(6):                      # turn cap
            response = self.chain.chat(messages= old_messages + new_messages, tools= self.schemas)

            if isinstance(response, dict) and "error" in response:
                return "Sorry — all providers are down right now."
            
            msg = response.choices[0].message
            new_messages.append(msg.model_dump(exclude_none=True))

            if not msg.tool_calls:
                self.save_message(new_messages)
                return msg.content
            
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments or "{}")   # STRING -> dict

                result = self.functions[tc.function.name](**args)

                new_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.function.name,
                    "content": json.dumps(result),
                })