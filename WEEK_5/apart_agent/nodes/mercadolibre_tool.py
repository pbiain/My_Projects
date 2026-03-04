from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

_ddg = DuckDuckGoSearchRun()


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

    return _ddg.run(query)
