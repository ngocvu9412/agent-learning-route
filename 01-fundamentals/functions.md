# Week 1 — Function Syntax Reference

## OpenAI SDK
```python
client = OpenAI(base_url="...", api_key="...")
response = client.chat.completions.create(model="...", messages=[...])
response = client.chat.completions.create(model="...", messages=[...], tools=TOOLS)
response.choices[0].message.content
response.choices[0].message.tool_calls
response.choices[0].message.model_dump(exclude_none=True)
```

## os / dotenv
```python
os.environ.get("KEY_NAME")
load_dotenv("path/to/.env")
```

## json
```python
json.loads(string)      # string → dict
json.dumps(dict)        # dict → string
json.dumps(dict, indent=2)
```

## Dict
```python
d["key"] = value
d.get("key")
d.get("key", default)
if key in d:
```

## f-string
```python
f"Hello {name}"
f"Error: {error}"
```

## Tuple return
```python
return ("retryable", True)
type, retryable = classify(error)
```
