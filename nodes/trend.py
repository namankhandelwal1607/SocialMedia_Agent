
from pydantic import BaseModel
from langchain_tavily import TavilySearch
from langchain_core.tools import tool


class TrendAnalysis(BaseModel):
    trending_topics: list[str]
    reasoning: str
    relevance_to_auriga: str


from config import TAVILY_API_KEY

print("TAVILY KEY FOUND:", bool(TAVILY_API_KEY))

tavily = TavilySearch(
    max_results=10,
    # tavily_api_key=TAVILY_API_KEY
)

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