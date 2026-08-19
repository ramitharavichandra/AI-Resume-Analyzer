import logging
from fastapi import APIRouter, status, HTTPException
from app.config import settings
from app.services.ats_scorer import ATSScorerService
from app.services.gemini_service import GeminiService
from app.services.section_extractor import SectionExtractorService
from app.models.scoring import ResumeMatchRequest, ResumeMatchResponse

logger = logging.getLogger(__name__)

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

    score_details = None
    if settings.GEMINI_API_KEY:
        try:
            logger.info("Attempting semantic scoring using Gemini API.")
            gemini_results = GeminiService.match_resume_semantically(
                resume_text=request.resume_text,
                jd_text=request.job_description_text,
                api_key=settings.GEMINI_API_KEY
            )
            
            # Evaluate sections locally to keep consistency with the hybrid ATS formula
            sections = SectionExtractorService.segment_sections(request.resume_text)
            section_score, present_sections, missing_sections = ATSScorerService._evaluate_sections(sections)
            
            # Calculate overall score based on the weights:
            # 45% Skill match, 35% Vector similarity, 20% Section completeness
            skill_score = gemini_results["skill_match_score"]
            vector_score = gemini_results["vector_similarity_score"]
            
            overall_ats_score = round(
                (0.45 * skill_score) + (0.35 * vector_score) + (0.20 * section_score),
                2,
            )
            
            rating = "Needs Improvement"
            if overall_ats_score >= 80.0:
                rating = "Excellent"
            elif overall_ats_score >= 65.0:
                rating = "Strong Match"
                
            score_details = {
                "ats_score": overall_ats_score,
                "rating": rating,
                "skill_match_score": skill_score,
                "vector_similarity_score": vector_score,
                "section_completeness_score": section_score,
                "matched_skills": gemini_results["matched_skills"],
                "missing_skills": gemini_results["missing_skills"],
                "shared_keywords": gemini_results["shared_keywords"],
                "top_jd_keywords": gemini_results["top_jd_keywords"],
                "present_sections": present_sections,
                "missing_sections": missing_sections,
                "improvement_suggestions": gemini_results["improvement_suggestions"],
                "engine": "Gemini AI Engine"
            }
        except Exception as e:
            logger.warning(
                f"Gemini semantic scoring failed, falling back to local scorer. Error: {str(e)}"
            )

    if not score_details:
        score_details = ATSScorerService.calculate_ats_score(
            resume_text=request.resume_text,
            jd_text=request.job_description_text,
        )
        score_details["engine"] = "Local Heuristics Fallback"

    return ResumeMatchResponse(**score_details)
