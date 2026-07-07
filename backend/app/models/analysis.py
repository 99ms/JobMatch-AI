from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    resume_text: str
    job_description: str