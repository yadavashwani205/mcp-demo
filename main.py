import json
import os
import random
import sqlite3
from contextlib import closing
from datetime import date as Date
from pathlib import Path

from fastmcp import FastMCP


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(
    os.environ.get("EXPENSE_DB_PATH", "/tmp/mcp-demo/expense.db")
).expanduser()
CATEGORIES_PATH = BASE_DIR / "categories.json"

mcp = FastMCP("expense-and-number-tools")


def load_categories() -> list[str]:
    with CATEGORIES_PATH.open(encoding="utf-8") as categories_file:
        categories = json.load(categories_file)
    if not isinstance(categories, list) or not all(
        isinstance(category, str) for category in categories
    ):
        raise ValueError("categories.json must contain a JSON array of strings.")
    return categories


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT ''
            )
            """
        )
        connection.commit()


initialize_database()
CATEGORIES = load_categories()


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return their sum."""
    return a + b


@mcp.tool()
def generate_random_number(lower: int, upper: int) -> int:
    """Generate a random integer between lower and upper, inclusive."""
    return random.randint(lower, upper)


@mcp.tool()
def add_expense(date: str, amount: float, category: str, note: str = "") -> dict:
    """Add an expense using an ISO 8601 date and a category from categories.json."""
    if Date.fromisoformat(date).isoformat() != date:
        raise ValueError("date must use the YYYY-MM-DD format.")
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category. Choose one of: {', '.join(CATEGORIES)}")

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        with connection:
            cursor = connection.execute(
                """
                INSERT INTO expenses (date, amount, category, note)
                VALUES (?, ?, ?, ?)
                """,
                (date, amount, category, note),
            )
            expense = connection.execute(
                "SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(expense)


@mcp.tool()
def list_expenses() -> list[dict]:
    """List all recorded expenses, ordered by date and then ID."""
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        expenses = connection.execute(
            "SELECT * FROM expenses ORDER BY date, id"
        ).fetchall()
        return [dict(expense) for expense in expenses]


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
