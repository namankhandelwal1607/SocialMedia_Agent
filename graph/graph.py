from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langgraph.checkpoint.memory import InMemorySaver
from graph.state import SocialMediaState

from graph.nodes import (
    trend_node,
    knowledge_node,
    strategy_node,
    content_node,
    compliance_node,
    approval_node,
    publish_node
)

def compliance_router(state):

    print("\n" + "="*50)
    print("COMPLIANCE ROUTER")
    print("="*50)

    review = state.get("compliance_review")

    if not review:
        print("No compliance review found.")
        return "revise"

    print("Approved:", review.get("approved"))
    print("Risk Level:", review.get("risk_level"))

    if review.get("approved", False):
        print("Routing -> approval")
        return "approval"

    print("Routing -> revise")
    return "revise"


def approval_router(state):

    if state["human_approval"]:
        return "publish"

    return "content"
builder = StateGraph(SocialMediaState)

# Nodes
builder.add_node("trend", trend_node)

builder.add_node("knowledge", knowledge_node)

builder.add_node("strategy", strategy_node)

builder.add_node("content", content_node)

builder.add_node("compliance", compliance_node)

builder.add_node("approval", approval_node)

builder.add_node("publish", publish_node)

# Main Flow
builder.add_edge(START, "trend")

builder.add_edge("trend", "knowledge")

builder.add_edge("knowledge", "strategy")

builder.add_edge("strategy", "content")

builder.add_edge("content", "compliance")

# Conditional Routing
builder.add_conditional_edges(
    "compliance",
    compliance_router,
    {
        "approval": "approval",
        "revise": "content"
    }
)

builder.add_conditional_edges(
    "approval",
    approval_router,
    {
        "publish": "publish",
        "content": "content"
    }
)
# Approval Flow
builder.add_edge(
    "approval",
    "publish"
)

builder.add_edge(
    "publish",
    END
)

# memory = InMemorySaver()

graph = builder.compile(
    # checkpointer=memory
)