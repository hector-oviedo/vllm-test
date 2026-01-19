from duckduckgo_search import DDGS
from typing import List, Dict, Any

# Tool Definition (OpenAI Schema)
WEB_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the internet for current information using DuckDuckGo.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default 5).",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}

async def execute_web_search(query: str, max_results: int = 5) -> str:
    """Executes the DuckDuckGo search and returns formatted results."""
    try:
        print(f"🔎 Native Tool: Searching for '{query}'...")
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No results found."
        
        formatted = ""
        for i, r in enumerate(results, 1):
            formatted += f"{i}. {r['title']}\n   {r['href']}\n   {r['body']}\n\n"
        return formatted
    except Exception as e:
        return f"Error performing search: {str(e)}"

# Registry of native tools
NATIVE_TOOLS_REGISTRY = {
    "web_search": execute_web_search
}

