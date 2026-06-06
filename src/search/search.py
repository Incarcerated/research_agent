import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

load_dotenv()
# Initialize Tavily (if API key exists)
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) if TavilyClient else None


def search_tavily(query: str, max_results: int = 5):
    """
    Primary search using Tavily
    """
    if not tavily_client:
        raise Exception("Tavily client not available")

    response = tavily_client.search(
        query=query,
        max_results=max_results,
        search_depth="advanced"
    )

    # Normalize Tavily results into same format as DDG
    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title"),
            "href": item.get("url"),
            "body": item.get("content")
        })

    return results


def search_duckduckgo(query: str, max_results: int = 5):
    """
    Fallback search using DuckDuckGo
    """
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))


def search_web(query: str, max_results: int = 5):
    """
    Hybrid search:
    Tavily first → fallback to DuckDuckGo on failure
    """

    # Try Tavily first
    try:
        if tavily_client:
            results = search_tavily(query, max_results)
            if results:  # valid response
                return {
                    "source": "tavily",
                    "results": results
                }

    except Exception as e:
        print(f"[Tavily failed → fallback]: {e}")

    # Fallback to DuckDuckGo
    try:
        results = search_duckduckgo(query, max_results)
        return {
            "source": "duckduckgo",
            "results": results
        }

    except Exception as e:
        return {
            "source": "none",
            "error": str(e),
            "results": []
        }