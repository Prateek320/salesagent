"""
tools/search.py — Web Search Tool
──────────────────────────────────
This is a "tool" — a function that agents can call to interact
with the outside world. Think of it as giving the agent a browser.

We use Tavily, which is purpose-built for AI agents (unlike Google,
it returns clean text summaries instead of raw HTML junk).
"""

import os
from tavily import TavilyClient
from dotenv import load_dotenv

# load_dotenv() reads your .env file and makes the keys available
# as environment variables. os.getenv() then fetches them safely.
load_dotenv()


def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web and return a clean text summary of results.

    Args:
        query      : What to search for  e.g. "Notion company overview 2024"
        max_results: How many sources to pull from (default 5)

    Returns:
        A single string containing the combined search results.
        We join them so agents receive plain text, not a complex object.
    """

    # Grab the API key from environment variables
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found. Did you create your .env file?")

    # Create the Tavily client (this is what makes the actual API call)
    client = TavilyClient(api_key=api_key)

    # .search() hits the Tavily API and returns results
    # search_depth="advanced" gets richer content (vs "basic" which is faster)
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results
    )

    # response["results"] is a list of dicts, each with "content" and "url"
    # We pull out the content from each result and join them into one text block
    results_text = "\n\n".join(
        f"Source: {r['url']}\n{r['content']}"
        for r in response["results"]
        if r.get("content")  # skip any result with no content
    )

    return results_text if results_text else "No results found."
