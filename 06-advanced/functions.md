# Week 6 — Function Syntax Reference (Explained)

## http.server basics
```python
from http.server import HTTPServer, BaseHTTPRequestHandler

server = HTTPServer(("localhost", 8080), MyHandler)   # listen on port 8080, send requests to MyHandler
server.serve_forever()      # loop forever answering requests — blocks the program here
```

## RequestHandler — GET requests
```python
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):                              # called automatically for every GET request
        # self.path = requested URL, e.g. "/agents" — you route on it
        if self.path == "/agents":
            self._send_json({"agents": []})        # path matches → respond with data
        else:
            self._send_json({"error": "not found"}, 404)   # no match → 404
```

## RequestHandler — POST requests
```python
    def do_POST(self):                             # called for every POST request
        # 1. Read the body — the client sends length first, then the bytes
        length = int(self.headers.get("Content-Length", 0))   # how many bytes to read
        body = self.rfile.read(length)          # raw bytes sent by the client
        data = json.loads(body)                 # bytes → Python dict

        # 2. Process
        ...

        # 3. Respond
        self._send_json({"status": "ok"}, 201)     # 201 = "created"
```

## Sending JSON response
```python
    def _send_json(self, data, status=200):
        body = json.dumps(data).encode()        # dict → JSON string → bytes (network sends bytes)
        self.send_response(status)              # writes the status line ("HTTP/1.0 200 OK")
        self.send_header("Content-Type", "application/json")   # tell client it's JSON
        self.send_header("Content-Length", str(len(body)))      # tell client how big
        self.end_headers()                      # finish the headers section
        self.wfile.write(body)                  # send the actual data
```

## Handler attributes reference
```python
self.path                            # URL path only: "/runs/abc123" (no domain, no query string)
self.headers.get("Content-Length")   # read a request header (case-insensitive)
self.rfile.read(n)                   # read n bytes of the request body
self.send_response(200)              # set the HTTP status code
self.send_header("Key", "Value")     # add one response header
self.end_headers()                   # close the header block — required before writing body
self.wfile.write(data)               # send the response body (must be bytes)
```

## HTTP status codes
```python
200    # OK — success, here's your data
201    # Created — success, and I made a new resource (POST /runs)
400    # Bad Request — client sent invalid data
404    # Not Found — that path/resource doesn't exist
500    # Internal Server Error — my code crashed while handling it
```

## String methods for URL routing
```python
path == "/agents"                 # exact match — for fixed endpoints
path.startswith("/runs/")         # prefix match — catches /runs/ANYTHING
path.split("/")                   # "/runs/abc" → ["", "runs", "abc"] (empty string before first /)
path.split("/")[-1]               # last segment → "abc" — this is the run ID
```

## uuid (unique IDs)
```python
import uuid
str(uuid.uuid4())          # random 36-char ID: "550e8400-e29b-41d4-a716-446655440000"
str(uuid.uuid4())[:8]      # first 8 chars: "550e8400" — shorter, still very unlikely to collide
```

## Dict as in-memory storage
```python
RUNS = {}
RUNS["id123"] = {"id": "id123", "status": "running"}   # create/update by key
run = RUNS.get("id123")                                 # read — None if missing (no crash)
list(RUNS.values())                                     # all stored items as a list
del RUNS["id123"]                                       # remove one entry
```

## json
```python
json.dumps(data).encode()    # dict → JSON string → bytes (for sending over network)
json.loads(body)             # bytes or string → dict (for reading what arrived)
```
