from langchain_tavily import TavilySearch
from langchain_core.tools import tool

tavily = TavilySearch(max_results=10)

@tool
def search_reddit(query: str):
    """
    Search Reddit discussions for AI trends.
    """

    return tavily.invoke(
        {
            "query": f"site:reddit.com {query}"
        }
    )


@tool
def search_news(query: str):
    """
    Search latest AI and technology news.
    """

    return tavily.invoke(
        {
            "query": f"latest AI news {query}"
        }
    )


@tool
def search_tech_blogs(query: str):
    """
    Search technical blogs and engineering articles.
    """

    return tavily.invoke(
        {
            "query": f"AI engineering blogs {query}"
        }
    )