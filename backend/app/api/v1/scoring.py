from fastapi import APIRouter, status, HTTPException
from app.services.ats_scorer import ATSScorerService
from app.models.scoring import ResumeMatchRequest, ResumeMatchResponse

router = APIRouter()


@router.post(
    "/match-resume",
    response_model=ResumeMatchResponse,
    summary="Compute Comprehensive ATS Score & Match Metrics",
    status_code=status.HTTP_200_OK,
)
async def match_resume(request: ResumeMatchRequest):
    """
    Evaluates Candidate Resume against Job Description using Hybrid ATS Analysis:
    - **Skill Gap Ratio** (45%)
    - **Vector Cosine Similarity** (35%)
    - **Section Completeness** (20%)
    """
    if not request.resume_text.strip() or not request.job_description_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both resume_text and job_description_text are required.",
        )

    score_details = ATSScorerService.calculate_ats_score(
        resume_text=request.resume_text,
        jd_text=request.job_description_text,
    )

    return ResumeMatchResponse(**score_details)
