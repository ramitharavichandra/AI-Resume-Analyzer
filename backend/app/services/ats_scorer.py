from typing import Dict, Any, List
from app.services.skill_gap_analyzer import SkillGapAnalyzerService
from app.services.vector_similarity import VectorSimilarityService
from app.services.tfidf_service import TFIDFService
from app.services.section_extractor import SectionExtractorService


class ATSScorerService:
    """
    Production Hybrid ATS Scoring Engine.
    Combines Skill Gap Match % (45%), Vector Cosine Similarity (35%),
    and Structural Section Completeness (20%).
    """

    @classmethod
    def calculate_ats_score(
        cls, resume_text: str, jd_text: str
    ) -> Dict[str, Any]:
        """
        Calculates comprehensive ATS Score (0-100) with detailed metric breakdowns
        and improvement suggestions.
        """
        # 1. Skill Gap Analysis (45% Weight)
        gap_analysis = SkillGapAnalyzerService.analyze_gap(resume_text, jd_text)
        skill_score = gap_analysis["match_percentage"]  # 0 to 100

        # 2. Vector Cosine Similarity (35% Weight)
        cosine_sim = VectorSimilarityService.calculate_cosine_similarity(
            resume_text, jd_text
        )
        vector_score = round(cosine_sim * 100, 2)  # 0 to 100

        # 3. Structural Section Completeness Score (20% Weight)
        sections = SectionExtractorService.segment_sections(resume_text)
        section_score, present_sections, missing_sections = cls._evaluate_sections(sections)

        # Weighted Final ATS Score
        overall_ats_score = round(
            (0.45 * skill_score) + (0.35 * vector_score) + (0.20 * section_score),
            2,
        )

        # 4. TF-IDF Keyword Extraction
        tfidf_data = TFIDFService.compute_tfidf_features(resume_text, jd_text)

        # 5. Generate Actionable Feedback Suggestions
        suggestions = cls._generate_suggestions(
            overall_score=overall_ats_score,
            missing_skills=gap_analysis["missing_skills"],
            missing_sections=missing_sections,
            vector_score=vector_score,
        )

        # Rate Profile Level
        rating = "Needs Improvement"
        if overall_ats_score >= 80.0:
            rating = "Excellent"
        elif overall_ats_score >= 65.0:
            rating = "Strong Match"

        return {
            "ats_score": overall_ats_score,
            "rating": rating,
            "skill_match_score": skill_score,
            "vector_similarity_score": vector_score,
            "section_completeness_score": section_score,
            "matched_skills": gap_analysis["matched_skills"],
            "missing_skills": gap_analysis["missing_skills"],
            "shared_keywords": tfidf_data["shared_keywords"],
            "top_jd_keywords": tfidf_data["top_jd_keywords"],
            "present_sections": present_sections,
            "missing_sections": missing_sections,
            "improvement_suggestions": suggestions,
        }

    @staticmethod
    def _evaluate_sections(sections: Dict[str, str]) -> tuple[float, List[str], List[str]]:
        """
        Evaluates presence of critical sections: Skills, Experience, Education, Projects, Summary.
        """
        critical_sections = ["skills", "experience", "education", "projects", "summary"]
        present = []
        missing = []

        for sec in critical_sections:
            if sections.get(sec, "").strip():
                present.append(sec)
            else:
                missing.append(sec)

        score = (len(present) / len(critical_sections)) * 100.0
        return score, present, missing

    @staticmethod
    def _generate_suggestions(
        overall_score: float,
        missing_skills: List[str],
        missing_sections: List[str],
        vector_score: float,
    ) -> List[str]:
        suggestions = []

        if missing_sections:
            sec_list = ", ".join([s.title() for s in missing_sections])
            suggestions.append(f"Add missing structural sections to your resume: {sec_list}.")

        if missing_skills:
            top_missing = ", ".join(missing_skills[:5])
            suggestions.append(f"Incorporate key missing skills from the job description: {top_missing}.")

        if vector_score < 40.0:
            suggestions.append(
                "Align your project descriptions and work experience bullet points closer to the terminology used in the job description."
            )

        if overall_score >= 80.0 and not suggestions:
            suggestions.append("Great job! Your resume is strongly optimized for this job description.")

        return suggestions
