# Week 5 — Function Syntax Reference (Explained)

## ABC (Abstract Base Class)
```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):              # inherit from ABC to make it "abstract"
    @abstractmethod                 # marks this method as REQUIRED in subclasses
    def chat(self, messages):
        pass                        # no body here — subclasses must write their own

class GeminiProvider(LLMProvider):  # subclass promises to implement chat()
    def chat(self, messages):       # now implement it — forget this and Python errors on creation
        ...
```

## @classmethod / @staticmethod
```python
class Factory:
    _providers = {}    # class variable — ONE copy shared by everything, not per-instance

    @classmethod
    def create(cls, name):        # cls = the class itself (Factory), lets you touch _providers
        return cls._providers[name]

    @staticmethod
    def helper(x):                # no self, no cls — just a plain function stored in the class
        return x * 2
```

## Factory pattern (registry + create)
```python
class ProviderFactory:
    _providers = {}                                    # name → provider class

    @classmethod
    def register(cls, name, provider_class):           # save a class under a name for later
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, name, **kwargs):                   # build an instance of a registered class
        provider_class = cls._providers.get(name)      # .get() returns None instead of crashing
        if not provider_class:                         # unknown name → fail loudly
            raise ValueError(f"Unknown provider: {name}")
        return provider_class(**kwargs)                # call the class = make an instance

    @classmethod
    def list_providers(cls):
        return list(cls._providers.keys())             # all registered names
```

## dataclass
```python
from dataclasses import dataclass

@dataclass                              # auto-generates __init__, __repr__, __eq__
class ProviderEntry:
    provider: object          # required — no default means you MUST pass it
    model: str                # required
    priority: int = 0         # optional — defaults to 0 if not passed
    error_count: int = 0      # optional
```

## getattr (safe attribute access)
```python
getattr(obj, "attr")              # same as obj.attr — errors if missing
getattr(obj, "attr", default)     # same, but returns default instead of erroring
getattr(response.usage, "prompt_tokens", 0)   # usage info may be absent → fall back to 0
```

## Sort list of objects
```python
entries.sort(key=lambda e: e.priority)          # key= picks WHAT to compare: each entry's priority
entries.sort(key=lambda e: e.priority, reverse=True)   # highest priority first
```

## time
```python
import time
time.time()      # seconds since 1970 (a big float) — useful for timestamps & measuring gaps
time.sleep(2)    # pause the program for 2 seconds (used between retries)
```

## **kwargs (pass-through arguments)
```python
def chat(self, messages, model=None, tools=None, **kwargs):
    # **kwargs collects any EXTRA keyword arguments into a dict
    # so chat(msgs, temperature=0.7) works without declaring temperature
    return self.client.chat.completions.create(
        model=model or self.model,    # use the argument if given, otherwise the stored one
        messages=messages,
        tools=tools,
        **kwargs                      # unpack the extras and hand them to the API too
    )
```

## "or" fallback pattern
```python
model = model or self.model           # if model is None/empty → use self.model instead
api_key = api_key or os.environ.get("GEMINI_API_KEY")   # caller's key, else the .env key
```

## Parse response pattern (normalizing)
```python
msg = response.choices[0].message     # dig out the message object from the API response
return {
    "content": msg.content,           # plain dict with fixed keys —
    "tool_calls": msg.tool_calls,     # the agent loop only ever sees THIS shape,
    "usage": {...}                    # no matter which provider produced it
}
```

## Health tracking pattern (fallback chain)
```python
now = time.time()
healthy = [e for e in self._providers           # keep an entry if:
           if e.error_count < 3                 # it hasn't failed 3 times, OR
           or (now - e.last_error_time) > 60]   # its last failure was over a minute ago (give it another chance)
```
