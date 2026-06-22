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

Your responsibility is to identify emerging AI and technology trends by analyzing information from:

- Reddit discussions
- AI and technology news
- Technical blogs and engineering articles

Use the available tools to gather information and identify the most relevant trends.

Return:

1. trending_topics
   - A list of the most important AI and technology trends currently gaining attention.

2. reasoning
   - Explain why these trends are important and what evidence from the gathered sources supports them.

3. relevance_to_auriga
   - Explain how these trends relate to Auriga IT's expertise in AI Consulting, Data Analytics, and Digital Transformation.
"""
)