# mcp-demo

A simple FastMCP server that exposes an `add` tool for adding two numbers.

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

The server exposes `add(a, b)`, which returns the sum of its two numeric
arguments.
