from pydantic import BaseModel
from config import groq_llm


class SocialPost(BaseModel):
    platform: str
    title: str
    content: str
    hashtags: list[str]

content_llm = groq_llm.with_structured_output(
    SocialPost
)