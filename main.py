import random

from fastmcp import FastMCP


mcp = FastMCP("number-tools")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return their sum."""
    return a + b


@mcp.tool()
def generate_random_number(lower: int, upper: int) -> int:
    """Generate a random integer between lower and upper, inclusive."""
    return random.randint(lower, upper)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
