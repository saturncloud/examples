import asyncio
import os
import aiosqlite
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP Server
mcp = FastMCP("SQLite-Local-Server")
DB_PATH = os.getenv("SQLITE_DB_PATH", "local_data.db")

@mcp.tool()
async def query_db(sql: str):
    """Execute a read-only SQL query on the local SQLite database."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(sql) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

@mcp.tool()
async def list_tables():
    """List all tables available in the local database."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table';") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

@mcp.tool()
async def describe_table(table_name: str):
    """Get the schema/columns for a specific table."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(f"PRAGMA table_info({table_name});") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

if __name__ == "__main__":
    # Run the server using the MCP stdio transport
    mcp.run()
