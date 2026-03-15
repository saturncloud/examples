from mcp.server.fastmcp import FastMCP

# Initialize the MCP tool server
mcp = FastMCP("DataAnalyzer")

@mcp.tool()
def analyze_text_metrics(text_input: str) -> str:
    """A custom Python tool that analyzes string length and word count."""
    words = len(text_input.split())
    chars = len(text_input)
    return f"Analysis complete: {words} words, {chars} characters."

if __name__ == "__main__":
    # Runs the server over standard I/O so cagent can communicate with it
    mcp.run()