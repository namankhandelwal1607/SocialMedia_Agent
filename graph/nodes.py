from graph.state import SocialMediaState
from langgraph.types import interrupt

from agents.trend_agent import trend_agent
from agents.knowledge_agent import knowledge_agent
from agents.strategy_agent import strategy_agent
from agents.content_agent import content_agent
from agents.compliance_agent import compliance_agent


def trend_node(state: SocialMediaState):

    print("\n" + "="*50)
    print("TREND NODE START")
    print("="*50)

    result = trend_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state["user_request"]
                }
            ]
        }
    )

    trend_data = result["structured_response"].model_dump()

    print("Trend Output:")
    print(trend_data)
    print("Trend Size:", len(str(trend_data)))

    return {
        "trend_analysis": trend_data
    }


def knowledge_node(state: SocialMediaState):

    print("\n" + "="*50)
    print("KNOWLEDGE NODE START")
    print("="*50)

    print("Incoming Trend Size:",
          len(str(state["trend_analysis"])))

    result = knowledge_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": str(state["trend_analysis"])
                }
            ]
        }
    )

    last_message = result["messages"][-1].content

    if isinstance(last_message, list):
        company_context = last_message[0]["text"]
    else:
        company_context = last_message

    print("Knowledge Output Size:",
          len(company_context))

    print("\nKnowledge Preview:")
    print(company_context[:500])

    return {
        "company_context": company_context
    }


def strategy_node(state: SocialMediaState):

    print("\n" + "="*50)
    print("STRATEGY NODE START")
    print("="*50)

    print("Trend Size:",
          len(str(state["trend_analysis"])))

    print("Company Context Size:",
          len(str(state["company_context"])))

    trend = state["trend_analysis"]

    prompt = f"""
    TRENDING TOPICS:
    {trend['trending_topics']}

    WHY TRENDING:
    {trend['reasoning']}

    RELEVANCE TO AURIGA:
    {trend['relevance_to_auriga']}

    AURIGA KNOWLEDGE:
    {state['company_context']}

    Create a content strategy that connects one
    high-value trend with Auriga's expertise.

    Avoid generic AI marketing.
    """
    print("Strategy Prompt Size:",
          len(prompt))

    result = strategy_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    strategy = result["structured_response"].model_dump()

    print("Strategy Output:")
    print(strategy)

    return {
        "strategy": strategy
    }


def content_node(state: SocialMediaState):

    print("\n" + "="*50)
    print("CONTENT NODE START")
    print("="*50)

    prompt = f"""
TREND ANALYSIS:
{state['trend_analysis']}

AURIGA KNOWLEDGE:
{state['company_context']}

CONTENT STRATEGY:
{state['strategy']}
"""

    print("Trend Size:",
          len(str(state["trend_analysis"])))

    print("Knowledge Size:",
          len(str(state["company_context"])))

    print("Strategy Size:",
          len(str(state["strategy"])))

    print("Content Prompt Size:",
          len(prompt))

    result = content_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    content = result["structured_response"].model_dump()

    print("Generated Content Size:",
          len(str(content)))

    print("Generated Content:")
    print(content)

    return {
        "generated_content": content
    }

def compliance_node(state: SocialMediaState):

    print("\n" + "="*50)
    print("COMPLIANCE NODE START")
    print("="*50)

    print("Content Size:",
          len(str(state["generated_content"])))

    content_to_review = f"""
Title:
{state['generated_content']['title']}

Content:
{state['generated_content']['content']}
"""

    print("Compliance Input Size:",
          len(content_to_review))

    result = compliance_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": content_to_review
                }
            ]
        }
    )

    review = result["structured_response"].model_dump()

    print("\nCOMPLIANCE OUTPUT")
    print(review)

    print("\nRETURNING COMPLIANCE REVIEW")
    print({
        "compliance_review": review
    })

    return {
        "compliance_review": review
    }

# def approval_node(state):

#     print("\nGenerated Post:\n")

#     print(state["generated_content"]["title"])
#     print()
#     print(state["generated_content"]["content"])

#     approval = input(
#         "\nApprove post? (yes/no): "
#     )

#     return {
#         "human_approval":
#         approval.lower() == "yes"
#     }


def approval_node(state):

    approval = interrupt(
        {
            "title": state["generated_content"]["title"],
            "content": state["generated_content"]["content"],
            "hashtags": state["generated_content"]["hashtags"]
        }
    )

    return {
        "human_approval": approval
    }


def publish_node(state):

    print("\n" + "="*50)
    print("PUBLISH NODE")
    print("="*50)

    print("Publishing Content...")

    print(state["generated_content"]["title"])

    return {
        "published": True
    }