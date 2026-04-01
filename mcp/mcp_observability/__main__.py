"""Entry point for observability MCP server."""

from mcp_observability import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
