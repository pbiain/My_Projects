from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool

_tavily = TavilySearchResults(max_results=5)


@tool
def prospect_search(query: str) -> str:
    """Search the web for real estate agencies, private investors, or potential buyers
    in Argentina. Use when asked to find leads, agencies, investors, or contacts
    in the Buenos Aires / San Pedro area.
    Input should be a descriptive search query in Spanish or English.
    Examples: 'inmobiliarias san pedro buenos aires contacto',
              'inversores inmuebles san pedro argentina',
              'real estate agencies san pedro buenos aires email'.
    Returns names, websites, and contact details found on the web."""

    results = _tavily.invoke({"query": query})
    if not results:
        return "No results found."
    lines = []
    for r in results:
        title = r.get("title", "")
        url = r.get("url", "")
        snippet = r.get("content", "")[:200]
        lines.append(f"- {title}\n  {url}\n  {snippet}")
    return "\n\n".join(lines)
