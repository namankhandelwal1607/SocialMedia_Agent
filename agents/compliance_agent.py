from pydantic import BaseModel
from config import groq_llm

class ComplianceReview(BaseModel):

    approved: bool

    feedback: str

    risk_level: str

from langchain.agents import create_agent
compliance_agent = create_agent(
    model=groq_llm,
    response_format=ComplianceReview,
    system_prompt="""
You are Auriga's Brand Compliance Agent.

Review content for:

1. Professional tone
2. Misleading claims
3. Exaggeration
4. Technical accuracy
5. Brand consistency

If content is acceptable:
approved = true

Otherwise:
approved = false

Provide feedback.
"""
)