# Week 4 — Function Syntax Reference (Explained)

## sqlite3 basics
```python
import sqlite3
conn = sqlite3.connect("file.db")    # open (or create) the database file; returns a Connection object
conn.row_factory = sqlite3.Row       # makes query results accessible by column NAME instead of index
conn.commit()                        # save all changes since last commit — without this, writes are lost
conn.close()                         # close the connection when done using the database
```

## Execute queries
```python
conn.execute("SQL here")                            # run one SQL command, returns a cursor
conn.execute("INSERT ... VALUES (?, ?)", (a, b))    # ? placeholders are filled safely by (a, b) in order
conn.executescript("""SQL1; SQL2; SQL3;""")         # run MULTIPLE commands at once (used for creating tables)
```

## Reading results
```python
rows = conn.execute("SELECT ...").fetchall()   # get ALL matching rows as a list
row = conn.execute("SELECT ...").fetchone()    # get just the FIRST row (or None if no match)
count = conn.execute("SELECT COUNT(*) FROM t").fetchone()[0]   # COUNT returns one row; [0] grabs the number
```

## Row access (with row_factory)
```python
row["column_name"]        # get value by column name — works because we set row_factory earlier
row[0]                    # get value by position (first column selected)
dict(row)                 # convert the row object into a normal Python dict
[dict(r) for r in rows]   # convert EVERY row in the list into a dict
```

## SQL statements
```sql
-- Create table (only creates if it doesn't already exist — safe to run every startup)
CREATE TABLE IF NOT EXISTS name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-numbered unique ID, SQLite fills it in
    col TEXT NOT NULL,                     -- text column, required (can't be empty/NULL)
    created TEXT DEFAULT (datetime('now')) -- if not provided, SQLite uses current time
);

-- Insert (add a new row)
INSERT INTO table (col1, col2) VALUES (?, ?);

-- Upsert: try to insert, but if the key already exists, update instead
INSERT INTO table (key, value) VALUES (?, ?)
ON CONFLICT(key) DO UPDATE SET value = excluded.value;  -- excluded.value = the new value we tried to insert

-- Select (read rows)
SELECT col1, col2 FROM table WHERE x = ? ORDER BY id LIMIT ?;  -- filter, sort oldest-first, cap the count

-- Count
SELECT COUNT(*) FROM table;   -- returns one number: how many rows exist
```

## Why parameterized queries (?)
```python
# SAFE — the ? placeholder treats input as pure DATA, never as SQL code
conn.execute("SELECT * FROM users WHERE name = ?", (user_input,))

# UNSAFE — f-string puts input INTO the SQL itself; a malicious input like
# "x'; DROP TABLE users; --" would delete your table. Never do this.
conn.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
```

## pathlib for db files
```python
Path("file.db").exists()     # True if the file exists on disk
Path("file.db").unlink()     # delete the file
```

## os
```python
import os
os.remove("file.db")         # delete file (older style, same as unlink)
os.path.exists("file.db")    # check exists (older style)
```

## Common patterns
```python
# Always check fetchone() for None before reading columns —
# querying a key that doesn't exist returns None, and None["col"] would crash
row = conn.execute("SELECT ...").fetchone()
if row:
    value = row["column"]
else:
    value = None

# Stats pattern: count rows in each table, collect into one dict
stats = {}
for name, table in [("conversations", "conversations"), ("facts", "user_facts")]:
    stats[name] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
```
