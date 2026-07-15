from pydantic import BaseModel
from typing import List, Optional

class AnalysisRequest(BaseModel):
    job_description: str

class SkillCategory(BaseModel):
    category: str
    weight: int
    matched_skills: List[str]
    missing_skills: List[str]
    points_earned: float = 0.0
    points_possible: float = 0.0

class Statistics(BaseModel):
    total_required_skills: int
    total_matched_skills: int
    total_missing_skills: int
    coverage_percentage: float
    total_points_earned: float = 0.0
    total_points_possible: float = 0.0

class SectionMatch(BaseModel):
    section_name: str
    matched_skills: List[str]

class AnalysisResponse(BaseModel):
    filename: str
    match_score: float
    
    # Backwards compatibility
    matching_keywords: List[str]
    missing_keywords: List[str]
    
    # New structured fields
    matched_skills: List[SkillCategory]
    missing_skills: List[SkillCategory]
    statistics: Statistics
    sections: List[SectionMatch] = []
