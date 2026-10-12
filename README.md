# mcp-demo

A FastMCP server with expense-tracking and number utility tools.

## Run

Install FastMCP:

```bash
python -m pip install fastmcp
```

Start the server over HTTP:

```bash
python main.py
```

The server listens on `0.0.0.0:8000` and serves the MCP endpoint at
`http://localhost:8000/mcp`.

The server exposes:

- `add(a, b)`: returns the sum of its two numeric arguments.
- `generate_random_number(lower, upper)`: returns a random integer in the
  inclusive range from `lower` to `upper`.
- `add_expense(date, amount, category, note="")`: records an expense using an
  ISO 8601 date (`YYYY-MM-DD`) and one of the categories in `categories.json`.
  The note defaults to an empty string.
- `list_expenses()`: returns all recorded expenses ordered by date, then ID.

The expense tools create and use `expense.db` next to `main.py`. Its `expenses`
table has an auto-incrementing integer primary key, required date, amount, and
category columns, and a required note column that defaults to an empty string.
If the server's project directory is read-only, set `EXPENSE_DB_PATH` to a
writable database file path before starting the server, for example:

```bash
EXPENSE_DB_PATH="$HOME/.local/share/mcp-demo/expense.db" uv run fastmcp dev inspector main.py
```

The server creates the parent directory when needed.
