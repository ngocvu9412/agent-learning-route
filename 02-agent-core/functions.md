# Week 2 — Function Syntax Reference

## Error handling
```python
str(error)                      # error → string
str(error).lower()              # lowercase for keyword matching
"keyword" in some_string        # check if substring exists
```

## try/except
```python
try:
    ...
except TypeError as e:
    ...
except Exception as e:
    ...
```

## time
```python
time.sleep(1)                   # pause 1 second
time.time()                     # current timestamp (float)
```

## Exponential backoff formula
```python
delay = base_delay * (2 ** attempt)    # 1, 2, 4, 8, ...
```

## Conditionals
```python
if not retryable or attempt == max_retries:
    return None
```

## Tuple unpacking
```python
error_type, is_retryable = classify(error)
```

## Check if empty
```python
if not response_message.tool_calls:    # None or [] → True
    return answer
```
