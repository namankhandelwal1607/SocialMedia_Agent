from pydantic import BaseModel
from config import groq_llm


class ContentStrategy(BaseModel):
    target_audience: str
    platform: str
    content_type: str
    trend_focus: str
    key_insight: str
    enterprise_challenge: str
    future_prediction: str
    angle: str
    call_to_action: str

strategy_llm = groq_llm.with_structured_output(
    ContentStrategy
)