# mcp-demo

A simple FastMCP server that exposes tools for adding two numbers and
generating a random integer within a range.

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
