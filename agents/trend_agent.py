from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from config import gemini_llm
from langchain.agents import create_agent
from pydantic import BaseModel


class TrendAnalysis(BaseModel):
    trending_topics: list[str]
    reasoning: str
    relevance_to_auriga: str

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

trend_agent = create_agent(
    model=gemini_llm,
    tools=[
        search_reddit,
        search_news,
        search_tech_blogs
    ],
    response_format=TrendAnalysis,

    system_prompt="""
You are a Trend Discovery Agent.

Your responsibility is to discover
emerging AI and technology trends from:

- Reddit discussions
- AI news
- Technical blogs

Return:

1. Trending Topics
2. Why They Are Trending
3. Source Category
4. Relevance to Auriga IT
5. Confidence Score
"""
)