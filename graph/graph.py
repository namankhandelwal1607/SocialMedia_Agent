from langgraph.graph import StateGraph
from langgraph.graph import START, END

from graph.state import SocialMediaState

from graph.nodes import (
    trend_node,
    knowledge_node,
    strategy_node,
    content_node,
    compliance_node
)

def compliance_router(state):

    print("\n" + "="*50)
    print("ROUTER CALLED")
    print("="*50)

    print("State Keys:")
    print(state.keys())

    print("\nCompliance Review:")
    print(state.get("compliance_review"))

    if state["compliance_review"]["approved"]:
        return "approved"

    return "retry"

builder = StateGraph(SocialMediaState)

builder.add_node("trend", trend_node)

builder.add_node("knowledge", knowledge_node)

builder.add_node("strategy", strategy_node)

builder.add_node("content", content_node)

builder.add_node("compliance", compliance_node)

builder.add_edge(START, "trend")

builder.add_edge("trend", "knowledge")

builder.add_edge("knowledge", "strategy")

builder.add_edge("strategy", "content")

builder.add_edge("content", "compliance")

builder.add_conditional_edges(
    "compliance",
    compliance_router,
    {
        "approved": END,
        "retry": "content"
    }
)

graph = builder.compile()

