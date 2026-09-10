from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

from app.config.settings import settings
from app.utils.logger import logger


search = TavilySearchResults(
    tavily_api_key=settings.TAVILY_API_KEY,
    max_results=3,
)


@tool
def MedicalWebSearchTool(query: str) -> str:
    """
    Use this tool ONLY for general medical knowledge, definitions,
    symptoms, cures, causes, disease overviews, and clinical guidelines.

    Do NOT use this tool for database-specific record lookups
    or numbers from datasets.
    """
    try:
        results = search.invoke({"query": query})

        if not results:
            return "No medical web results found."

        formatted = []

        for r in results:
            formatted.append(
                f"Content: {r.get('content', '')}\n"
                f"Source: {r.get('url', '')}"
            )

        return "\n\n".join(formatted)

    except Exception as e:
        logger.error(
            f"MedicalWebSearchTool execution failed: {e}",
            exc_info=True,
        )
        return f"Error executing web search: {str(e)}"