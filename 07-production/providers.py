"""StudyTracker providers — exercise-9 structure, two providers.

ZaiProvider    priority 1  glm-4.5-flash       (free, unlimited)
GeminiProvider priority 2  gemini-flash-latest (20/day — the safety net)

Then: ProviderFactory (name -> instance) and FallbackChain (priority order,
retries, circuit-breaker health). Same shapes you built in exercise 9.
"""
import os
import time
from dataclasses import dataclass
from typing import List
from openai import OpenAI
from abc import ABC, abstractmethod
from dotenv import load_dotenv

from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")   # route root, any machine
load_dotenv()                                                    # + cwd/.env if present

# Both providers use the SAME OpenAI SDK client — only base_url/key/model
# change. That's the whole reason the factory/chain pattern works here.

class LLMProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    def chat(self, messages, **kwargs):
        """Make a chat request, return raw response."""
        pass

    @abstractmethod
    def parse_response(self, response):
        """Parse response into {content, tool_calls, usage}."""
        pass

class ZaiProvider(LLMProvider):
    """TODO: z.ai GLM provider — priority 1.
    """
    # TODO: __init__ / chat
    def __init__(self, api_key=None, model=None):
        self.client = OpenAI(
            base_url = "https://api.z.ai/api/paas/v4/",
            api_key= api_key or os.environ.get("ZAI_API_KEY")
            )
        self.model = model or os.environ.get("ZAI_MODEL")

    def chat(self, messages, tools=None):
        response = self.client.chat.completions.create(
            model= self.model,
            messages= messages,
            tools=tools,         # Pass function tools
            tool_choice="auto"   # Automatically choose whether to call functions
        )
        return response

    def parse_response(self, response):
        msg = response.choice[0].message
        return {
            "content": msg.content,
            "tool_calls": msg.tool_calls,
            "usage": {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                "completion_tokens": getattr(response.usage, "completion_tokens", 0)
            } 
        }
        

class GeminiProvider(LLMProvider):
    """TODO: Gemini provider — priority 2 (LAST: 20 requests/day quota).

    Hint: base_url="https://generativelanguage.googleapis.com/v1beta/openai"
          api_key from GEMINI_API_KEY, model from GEMINI_MODEL env
          (both already in ../.env — your ex-1 setup)
    """
    # TODO: __init__ / chat
    def __init__(self, api_key=None, model=None):
        self.client = OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
            api_key= api_key if api_key != None else os.environ.get("GEMINI_API_KEY"))
        self.model = model if model != None else os.environ.get("GEMINI_3.0_MODEL")

    def chat(self, messages, tools=None):
        response = self.client.chat.completions.create(
                model= self.model,
                messages= messages,
                tools=tools,         # Pass function tools
            )
        return response

    def parse_response(self, response):
            msg = response.choice[0].message
            return {
                "content": msg.content,
                "tool_calls": msg.tool_calls,
                "usage": {
                    "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                    "completion_tokens": getattr(response.usage, "completion_tokens", 0)
                } 
            }

class ProviderFactory:
    """TODO: name-string -> provider instance (ex-9).

    Hint:

    Difference from a chain: the factory only BUILDS. It knows nothing
    about priorities, retries, or health — that's FallbackChain's job.
    """
    # TODO: register / create / list_providers
    _providers = {}                       # class-level registry

    @classmethod
    def register(cls, name, provider_class):
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, name, **kwargs):
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}")
        return cls._providers[name](**kwargs)

    @classmethod
    def list_providers(cls):
        return list(cls._providers.keys())

@dataclass
class ProviderEntry:
    """One provider inside the chain, plus its health record (ex-9)."""
    provider: object
    model: str
    priority: int = 0
    error_count: int = 0
    last_error_time: float = 0.0


class FallbackChain:
    """TODO: try providers in priority order until one succeeds (ex-9).
    """
    # TODO: all five methods
    def __init__(self):
        self._providers: List[ProviderEntry] = []

    def add_provider(self, provider, model, priority=0):
        """TODO: Add with priority ordering."""
        # Hint: create a ProviderEntry, append, sort by priority
        provider_entry = ProviderEntry(provider, model, priority)
        self._providers.append(provider_entry)
        self._providers.sort(key = lambda e: e.priority)

    def get_healthy_providers(self):
        """TODO: Return providers with fewer than 3 recent errors."""
        # Hint: keep entries where error_count < 3,
        #       OR last error was more than 60 seconds ago
        return [provider_entry for provider_entry in self._providers
                if provider_entry.error_count < 3 or (time.time()-provider_entry.last_error_time > 60)]

    def chat(self, messages, tools= None, max_retries=2):
        """TODO: Try each provider until one succeeds."""
        # Hint: loop over healthy providers, retry each up to max_retries,
        #       on success return parse_response, on failure record the error
        #       (error_count += 1, last_error_time = time.time())
        #       after ALL loops: return {"error": "All providers failed"}
        healthy_providers = self.get_healthy_providers()
        for provider_entry in healthy_providers:
            for attempt in range(max_retries + 1):
                try:
                    response = provider_entry.provider.chat(messages, tools)

                    # return provider_entry.provider.parse_response(response)
                    return response
                
                except Exception as E:
                    
                    provider_entry.error_count += 1
                    provider_entry.last_error_time = time.time()
                    retryable = self._is_retryable_error(str(E)) 

                    if not retryable or attempt == max_retries:
                        print(f"Giving up on error {E}")
                        break
                    
                    time.sleep(2 ** attempt)               
                    
        return {"error": "All providers failed"}

    def _is_retryable_error(self, error_str):
        retryable = ["rate limit", "timeout", "502", "503", "504"]
        return any(p in error_str.lower() for p in retryable)



def build_chain() -> FallbackChain:
    """Convenience: register classes in the factory, build the priority chain.
    """
    ProviderFactory.register("zai", ZaiProvider)
    ProviderFactory.register("gemini", GeminiProvider)

    chain = FallbackChain()
    if os.environ.get("ZAI_API_KEY"):
        chain.add_provider(ProviderFactory.create("zai"), "zai-model", priority=1)
    if os.environ.get("GEMINI_API_KEY"):
        chain.add_provider(ProviderFactory.create("gemini"), "...", priority=2)
    return chain
