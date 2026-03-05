import os
from tavily import TavilyClient
from langchain.tools import tool


@tool
def property_web_search(query: str) -> str:
    """Search the web for general information about Amarras San Pedro,
    its location, distances from nearby cities or landmarks, local amenities,
    or any question not covered by the property documents.
    Use for questions like 'how far is Amarras San Pedro from Buenos Aires?',
    'what is San Pedro like?', 'how do I get there?', or access/location questions.
    Input should be a descriptive search query in Spanish or English.
    Examples: 'Amarras San Pedro distancia Buenos Aires',
              'San Pedro Buenos Aires como llegar autopista'."""

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    try:
        response = client.search(query, max_results=3)
        results = response.get("results", [])
        if not results:
            return "No results found."
        lines = []
        for r in results:
            title = r.get("title", "")
            snippet = r.get("content", "")[:300]
            lines.append(f"- {title}\n  {snippet}")
        return "\n\n".join(lines)
    except Exception as e:
        return f"Web search unavailable: {str(e)}"
