
import sys
import os
import mcp.types as types
from mcp.server import Server, NotificationOptions, InitializationOptions
from mcp.server.stdio import stdio_server

# Ensure we can import rag_core from the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from rag_core import RAGSystem

# Initialize RAG System
# We initialize it globally to keep the persistent client ready
rag_system = RAGSystem()

server = Server("rag-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="rag_search",
            description="Search the agent knowledge base using Retrieval Augmented Generation (RAG). Use this tool to look up information from the codebase, documentation, or other agents' definitions. Efficient for finding context about existing systems.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information."
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return. Default is 5.",
                        "default": 5
                    }
                },
                "required": ["query"]
            },
        ),
        types.Tool(
            name="rag_ingest",
            description="Ingest specific files into the RAG memory. Call this tool immediately after creating or modifying any documentation or significant code file to keep the agentic memory up to date.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of absolute file paths to ingest."
                    }
                },
                "required": ["files"]
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "rag_search":
        query = arguments.get("query")
        n_results = arguments.get("n_results", 5)

        if not query:
            raise ValueError("Missing 'query' argument")

        # Perform the search
        results = rag_system.query(query, n_results=n_results)

        # Format the output
        formatted_text = []
        
        if not results['documents'] or not results['documents'][0]:
            return [types.TextContent(type="text", text="No results found.")]

        formatted_text.append(f"Found {len(results['documents'][0])} results for query: '{query}'\n")

        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            source = meta.get('source', 'unknown')
            
            formatted_text.append(f"--- Result {i+1} (Source: {source}) ---")
            formatted_text.append(doc.strip())
            formatted_text.append("-" * 40 + "\n")

        final_output = "\n".join(formatted_text)

        return [types.TextContent(type="text", text=final_output)]

    elif name == "rag_ingest":
        files = arguments.get("files")
        if not files or not isinstance(files, list):
             raise ValueError("Missing or invalid 'files' argument. Must be a list of strings.")
        
        # Import run_ingest dynamically to avoid circular issues or early loading
        from ingest import run_ingest
        
        count = run_ingest(files=files)
        
        return [types.TextContent(type="text", text=f"Successfully ingested {count} files.")]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="rag-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
