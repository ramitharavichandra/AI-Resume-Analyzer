from fastapi import APIRouter, status, HTTPException
from app.services.skill_extractor import SkillExtractorService
from app.services.skill_gap_analyzer import SkillGapAnalyzerService
from app.models.skills import (
    SkillExtractionRequest,
    SkillExtractionResponse,
    SkillGapAnalysisRequest,
    SkillGapAnalysisResponse,
)

router = APIRouter()


@router.post(
    "/extract-skills",
    response_model=SkillExtractionResponse,
    summary="Extract & Categorize Technical Skills",
    status_code=status.HTTP_200_OK,
)
async def extract_skills(request: SkillExtractionRequest):
    """
    Extracts tech stack skills from raw input text (resume or job description)
    and categorizes them according to the master skill taxonomy.
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input text cannot be empty.",
        )

    categorized = SkillExtractorService.extract_skills(request.text)
    flat_skills = sorted(list(SkillExtractorService.extract_flat_skills(request.text)))

    return SkillExtractionResponse(
        total_skills_found=len(flat_skills),
        categorized_skills=categorized,
        flat_skills=flat_skills,
    )


@router.post(
    "/analyze-skill-gap",
    response_model=SkillGapAnalysisResponse,
    summary="Analyze Resume vs Job Description Skill Gap",
    status_code=status.HTTP_200_OK,
)
async def analyze_skill_gap(request: SkillGapAnalysisRequest):
    """
    Compares Resume text against Job Description text to calculate match percentage,
    matched skills, missing skills, and additional skills.
    """
    if not request.resume_text.strip() or not request.job_description_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both resume_text and job_description_text are required.",
        )

    gap_data = SkillGapAnalyzerService.analyze_gap(
        resume_text=request.resume_text,
        jd_text=request.job_description_text,
    )

    return SkillGapAnalysisResponse(**gap_data)
