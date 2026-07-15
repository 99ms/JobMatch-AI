from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

# --- Provider Independent Models ---

class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class ProviderResponse(BaseModel):
    content: str
    token_usage: TokenUsage
    provider: str
    model: str
    duration_ms: int

# --- Future Operation Requests ---
# These are placeholders for Milestone 3, representing structured JSON the AI will consume.

class BaseAIRequest(BaseModel):
    job_description: str
    resume_stats: Dict[str, Any]  # Parsed ATS structured stats

class ResumeFeedbackRequest(BaseAIRequest):
    pass

class ResumeTailorRequest(BaseAIRequest):
    pass

class CoverLetterRequest(BaseAIRequest):
    pass

class InterviewQuestionsRequest(BaseAIRequest):
    pass

# --- Future Operation Responses ---

class ResumeFeedbackResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    overall_assessment: str
    strengths: List[str]
    weaknesses: List[str]
    missing_skills_explanation: List[str]
    ats_optimization: List[str]
    action_plan: List[str]

class ResumeTailorResponse(BaseModel):
    tailored_summary: str
    tailored_bullet_points: List[str]

class CoverLetterResponse(BaseModel):
    cover_letter: str

class InterviewQuestionsResponse(BaseModel):
    questions: List[str]
