import sqlite3
import argparse
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('sqlite-demo')

def init_db():
    conn = sqlite3.connect('demo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            profession TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor


@mcp.tool()
def add_data(name: str, age: int, profession: str) -> bool:
    """Add a new record to the people table.

    Args:
        name (str): Person's name
        age (int): Person's age
        profession (str): Person's profession

    Returns:
        bool: True if data was added successfully, False otherwise
    """
    conn, cursor = init_db()
    try:
        cursor.execute(
            "INSERT INTO people (name, age, profession) VALUES (?, ?, ?)",
            (name, age, profession)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding data: {e}")
        return False
    finally:
        conn.close()


@mcp.tool()
def read_data(query: str = "SELECT * FROM people") -> list:
    """Read data from the people table.

    Args:
        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM people".

    Returns:
        list: List of tuples with query results.
    """
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error reading data: {e}")
        return []
    finally:
        conn.close()


if __name__ == "__main__":
    print("🚀Starting server... ")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)
