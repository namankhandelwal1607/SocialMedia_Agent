from graph.state import SocialMediaState
from langgraph.types import interrupt

from nodes.trend import (
    search_reddit,
    search_news,
    search_tech_blogs,
    TrendAnalysis
)
from nodes.knowledge import auriga_search
from nodes.strategy import strategy_llm
from nodes.content import content_llm
from nodes.compliance import compliance_llm
from config import gemini_llm



def trend_node(state: SocialMediaState):

    print("\n" + "=" * 50)
    print("TREND NODE START")
    print("=" * 50)

    query = state["user_request"]

    reddit_results = search_reddit.invoke(query)

    news_results = search_news.invoke(query)

    blog_results = search_tech_blogs.invoke(query)

    prompt = f"""
You are a Trend Discovery Assistant.

Analyze the information collected from Reddit, News, and Technical Blogs.

Identify:

1. trending_topics
2. reasoning
3. relevance_to_auriga

USER REQUEST:
{query}

REDDIT RESULTS:
{reddit_results}

NEWS RESULTS:
{news_results}

BLOG RESULTS:
{blog_results}
"""

    trend_llm = gemini_llm.with_structured_output(
        TrendAnalysis
    )

    result = trend_llm.invoke(prompt)

    trend_data = result.model_dump()

    print("Trend Output:")
    print(trend_data)

    print(
        "Trend Size:",
        len(str(trend_data))
    )

    return {
        "trend_analysis": trend_data
    }

def knowledge_node(state: SocialMediaState):

    print("\n" + "=" * 50)
    print("KNOWLEDGE NODE START")
    print("=" * 50)

    print(
        "Incoming Trend Size:",
        len(str(state["trend_analysis"]))
    )

    context = auriga_search.invoke(
        " ".join(
            state["trend_analysis"]["trending_topics"]
        )
    )

    prompt = f"""
You are Auriga's Knowledge Assistant.

Use the provided knowledge base context and return ONLY:

1. Relevant Auriga services
2. Relevant expertise
3. Relevant case studies
4. Why this trend matches Auriga

Keep response under 300 words.

TREND INFORMATION:
{state["trend_analysis"]}

AURIGA KNOWLEDGE:
{context}
"""

    result = gemini_llm.invoke(prompt)

    company_context = result.content

    print(
        "Knowledge Output Size:",
        len(company_context)
    )

    print("\nKnowledge Preview:")
    print(company_context[:500])

    return {
        "company_context": company_context
    }


def strategy_node(state: SocialMediaState):

    print("\n" + "=" * 50)
    print("STRATEGY NODE START")
    print("=" * 50)

    prompt = f"""
You are Auriga's Content Strategy Assistant.

Your responsibility is to transform trend research and company expertise into a strong thought-leadership content strategy.

PRIMARY OBJECTIVE

Generate industry insights, not marketing campaigns.

The audience should learn something valuable about the future of AI adoption before they learn about Auriga.

RULES

- Select ONE trend only.
- Select ONE Auriga capability most relevant to that trend.
- Focus on enterprise realities.
- Focus on implementation challenges.
- Focus on lessons learned.
- Focus on future implications.
- Think like a senior AI consultant.

DO NOT

- Create advertisements.
- Create product pitches.
- Create sales messaging.
- Use generic business buzzwords.
- Focus on Auriga services.

TREND ANALYSIS:

{state["trend_analysis"]}

COMPANY CONTEXT:

{state["company_context"]}
"""

    result = strategy_llm.invoke(prompt)

    strategy = result.model_dump()

    print("\nStrategy Output:")
    print(strategy)

    return {
        "strategy": strategy
    }


def content_node(state: SocialMediaState):

    print("\n" + "=" * 50)
    print("CONTENT NODE START")
    print("=" * 50)

    prompt = f"""
You are Auriga's Social Media Content Assistant.

Your job is to write executive-level LinkedIn thought leadership content.

INPUTS

TREND ANALYSIS:
{state["trend_analysis"]}

AURIGA CONTEXT:
{state["company_context"]}

CONTENT STRATEGY:
{state["strategy"]}

PRIMARY OBJECTIVE

Educate first.
Market second.

The reader should finish the post having learned something useful.

THINK LIKE

- Senior AI Consultant
- Enterprise Architect
- Technology Advisor
- Industry Analyst

NOT

- Salesperson
- Marketing Manager
- Copywriter

WRITING STYLE

- Analytical
- Insightful
- Practical
- Credible
- Executive-level

DO NOT USE

- Unlock the power of AI
- Transform your business
- Revolutionize your organization
- Game changer
- Cutting-edge
- Next-generation
- Industry-leading
- World-class

Auriga should not appear until at least halfway through the post.

POST STRUCTURE

1. Hook
2. Trend explanation
3. Enterprise challenge
4. Future implication
5. Expert insight
6. Auriga perspective
7. Discussion question

CONTENT LENGTH

220-350 words

OUTPUT

Generate:
- Platform
- Title
- Content
- Hashtags
"""

    result = content_llm.invoke(prompt)

    content_data = result.model_dump()

    print("\nGenerated Content:")
    print(content_data["title"])

    return {
        "generated_content": content_data
    }


def compliance_node(state: SocialMediaState):

    print("\n" + "=" * 50)
    print("COMPLIANCE NODE START")
    print("=" * 50)

    generated_content = state["generated_content"]

    prompt = f"""
You are Auriga's Brand Compliance Assistant.

Review the content for:

1. Professional tone
2. Misleading claims
3. Exaggeration
4. Technical accuracy
5. Brand consistency

If content is acceptable:
approved = true

Otherwise:
approved = false

Provide feedback and risk level.

CONTENT TO REVIEW:

Title:
{generated_content["title"]}

Content:
{generated_content["content"]}

Hashtags:
{generated_content["hashtags"]}
"""

    result = compliance_llm.invoke(prompt)

    review = result.model_dump()

    print("\nCompliance Review:")
    print(review)

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