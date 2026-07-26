from pydantic import BaseModel, Field
from typing import Dict, List


class SkillExtractionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw text from resume or job description")


class SkillExtractionResponse(BaseModel):
    total_skills_found: int = Field(..., description="Total unique skills extracted")
    categorized_skills: Dict[str, List[str]] = Field(..., description="Skills grouped by taxonomy category")
    flat_skills: List[str] = Field(..., description="Flat list of extracted skills")


class SkillGapAnalysisRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, description="Extracted resume text")
    job_description_text: str = Field(..., min_length=1, description="Target job description text")


class SkillGapAnalysisResponse(BaseModel):
    match_percentage: float = Field(..., description="Skill match ratio percentage (0-100%)")
    total_jd_skills_count: int = Field(..., description="Total skills detected in JD")
    total_resume_skills_count: int = Field(..., description="Total skills detected in Resume")
    matched_skills_count: int = Field(..., description="Number of overlapping skills")
    missing_skills_count: int = Field(..., description="Number of missing skills required in JD")
    matched_skills: List[str] = Field(..., description="List of skills present in both Resume & JD")
    missing_skills: List[str] = Field(..., description="List of skills required in JD but missing in Resume")
    additional_skills: List[str] = Field(..., description="Bonus skills present in Resume but absent in JD")
    resume_skills_by_category: Dict[str, List[str]] = Field(..., description="Resume skills by category")
    jd_skills_by_category: Dict[str, List[str]] = Field(..., description="JD skills by category")
