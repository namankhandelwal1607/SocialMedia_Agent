from typing import TypedDict


class SocialMediaState(TypedDict):
    user_request: str

    trend_analysis: dict

    company_context: str

    strategy: dict

    generated_content: dict

    compliance_review: dict

    human_approval: bool

    published: bool

    campaign_history: list