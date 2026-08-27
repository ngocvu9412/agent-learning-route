# Week 3 — Function Syntax Reference

## pathlib
```python
Path("file.txt")                                    # create Path object
Path(path).read_text(encoding="utf-8")              # read whole file → string
Path(path).read_text().splitlines()                 # string → list of lines
Path(path).parent                                   # get parent folder
Path(path).parent.mkdir(parents=True, exist_ok=True)# create folders
Path(path).unlink()                                 # delete file
Path(path).glob("*.py")                             # find files (one folder)
Path(path).rglob("*.py")                            # find files (all subfolders)
```

## open()
```python
open(path, "w", encoding="utf-8")    # write mode
open(path, "a", encoding="utf-8")    # append mode
```

## with statement (auto-closes file)
```python
with open(p, mode, encoding="utf-8") as f:
    f.write(content)
```

## String methods
```python
"\n".join(list)          # join list into string with newlines
"Text".lower()           # lowercase
" text ".strip()         # remove whitespace
```

## List slicing
```python
list[:limit]             # first N items
list[-1]                 # last item
```

## enumerate
```python
enumerate(list)          # (0, item), (1, item), ...
enumerate(list, 1)       # (1, item), (2, item), ...
```

## Generator expression
```python
str(m) for m in list     # convert each item inline
```

## sorted
```python
sorted(list)                       # alphabetical
sorted(list, reverse=True)         # reverse alphabetical
sorted(list, key=lambda e: e.priority)  # sort by field
```

## dataclass
```python
@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    handler: callable
    source: str = "builtin"
    category: str = "general"
```

## Dict operations
```python
d[key] = value
if key not in d:
    d[key] = []
d[key].append(item)
dict(d)                  # copy a dict
```

## **args (keyword unpacking)
```python
func(**{"a": 5, "b": 3})    # same as func(a=5, b=3)
```
