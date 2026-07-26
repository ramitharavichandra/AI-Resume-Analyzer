from typing import Dict, List, Any
from app.services.skill_extractor import SkillExtractorService


class SkillGapAnalyzerService:
    """
    Skill Gap Analysis Engine: Performs comparative set matching between
    Resume skills and Job Description skills.
    """

    @classmethod
    def analyze_gap(cls, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Calculates skill match breakdown between Resume and JD.
        """
        resume_skills_by_cat = SkillExtractorService.extract_skills(resume_text)
        jd_skills_by_cat = SkillExtractorService.extract_skills(jd_text)

        resume_skills_flat = SkillExtractorService.extract_flat_skills(resume_text)
        jd_skills_flat = SkillExtractorService.extract_flat_skills(jd_text)

        matched_skills = sorted(list(resume_skills_flat.intersection(jd_skills_flat)))
        missing_skills = sorted(list(jd_skills_flat.difference(resume_skills_flat)))
        additional_skills = sorted(list(resume_skills_flat.difference(jd_skills_flat)))

        total_jd_skills = len(jd_skills_flat)
        total_matched = len(matched_skills)

        match_percentage = (
            round((total_matched / total_jd_skills) * 100, 2)
            if total_jd_skills > 0
            else 0.0
        )

        return {
            "match_percentage": match_percentage,
            "total_jd_skills_count": total_jd_skills,
            "total_resume_skills_count": len(resume_skills_flat),
            "matched_skills_count": total_matched,
            "missing_skills_count": len(missing_skills),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "resume_skills_by_category": resume_skills_by_cat,
            "jd_skills_by_category": jd_skills_by_cat,
        }
