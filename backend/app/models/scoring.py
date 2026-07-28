from pydantic import BaseModel, Field
from typing import List


class ResumeMatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=1, description="Raw or parsed resume text")
    job_description_text: str = Field(..., min_length=1, description="Target job description text")


class ResumeMatchResponse(BaseModel):
    ats_score: float = Field(..., description="Overall ATS Compatibility Score (0-100)")
    rating: str = Field(..., description="Rating classification (Excellent, Strong Match, Needs Improvement)")
    skill_match_score: float = Field(..., description="Skill match component score (0-100)")
    vector_similarity_score: float = Field(..., description="Cosine similarity component score (0-100)")
    section_completeness_score: float = Field(..., description="Section completeness component score (0-100)")
    matched_skills: List[str] = Field(..., description="List of matching skills")
    missing_skills: List[str] = Field(..., description="List of missing skills")
    shared_keywords: List[str] = Field(..., description="Top TF-IDF shared keywords")
    top_jd_keywords: List[str] = Field(..., description="Top keywords in job description")
    present_sections: List[str] = Field(..., description="Detected structural sections")
    missing_sections: List[str] = Field(..., description="Missing structural sections")
    improvement_suggestions: List[str] = Field(..., description="Actionable improvement recommendations")
