from pydantic import BaseModel
from config import groq_llm


class ComplianceReview(BaseModel):

    approved: bool

    feedback: str

    risk_level: str

compliance_llm = groq_llm.with_structured_output(
    ComplianceReview
)