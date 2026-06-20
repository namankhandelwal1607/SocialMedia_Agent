from graph.graph import graph

initial_state = {
    "user_request":
    """
    Find trending developments around AI Agents and autonomous workflows.

Create a LinkedIn thought-leadership post for Auriga explaining why governance, auditability, and human oversight may become bigger challenges than building the agents themselves.

Target audience: CIOs, CTOs, and enterprise technology leaders.
    """
}

config = {
    "configurable": {
        "thread_id": "auriga-campaign"
    }
}

result = graph.invoke(
    initial_state,
    config=config
)
print("\nCONTENT\n")

print(result["generated_content"])

print("\nCOMPLIANCE\n")

print(result["compliance_review"])