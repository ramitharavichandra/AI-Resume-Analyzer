import json
import logging
import httpx
from typing import Dict, Any

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service to interact with Google's Gemini API for semantic resume analysis.
    Uses Direct HTTP calls to avoid extra sdk dependencies and ensure high performance.
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    @classmethod
    def _call_gemini(cls, prompt: str, api_key: str) -> str:
        """
        Sends content generation request to Gemini model and extracts text response.
        """
        url = f"{cls.BASE_URL}?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.1,
            }
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                # Extract text content
                candidates = result.get("candidates", [])
                if not candidates:
                    raise Exception("No candidates returned from Gemini API.")
                
                content_parts = candidates[0].get("content", {}).get("parts", [])
                if not content_parts:
                    raise Exception("Empty content parts in Gemini API response.")
                
                return content_parts[0].get("text", "")
        except httpx.HTTPStatusError as e:
            logger.error(f"Gemini API returned status code {e.response.status_code}: {e.response.text}")
            raise Exception(f"Gemini API HTTP Error: {e.response.text}")
        except Exception as e:
            logger.error(f"Failed to communicate with Gemini API: {str(e)}")
            raise

    @classmethod
    def parse_resume_semantically(cls, resume_text: str, api_key: str) -> Dict[str, str]:
        """
        Segment resume text into structured sections using Gemini.
        """
        prompt = f"""
You are an expert ATS (Applicant Tracking System) parser. Your task is to segment the given resume text into a structured JSON object.
Analyze the resume content and group it into the following sections:
- `summary`: Professional summary, objective, or profile.
- `skills`: Technical skills, languages, tools, frameworks.
- `experience`: Work experience, internships, professional history.
- `projects`: Personal projects, academic projects, open source.
- `education`: Degrees, universities, courses, academic history.
- `certifications`: Certifications, licenses, awards, achievements.
- `other`: Anything else that does not fit into the categories above.

Format your output as a single JSON object with these exact keys: 'summary', 'skills', 'experience', 'projects', 'education', 'certifications', 'other'.
If a section is not present in the resume, set the value to an empty string. Do not include markdown code block syntax (like ```json) in the JSON payload, return the raw JSON string directly.

Resume Text:
{resume_text}
"""
        response_text = cls._call_gemini(prompt, api_key)
        try:
            parsed = json.loads(response_text)
            # Ensure all keys exist
            for key in ["summary", "skills", "experience", "projects", "education", "certifications", "other"]:
                if key not in parsed:
                    parsed[key] = ""
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from Gemini parse: {response_text}. Error: {str(e)}")
            # Raise exception so the fallback handler catches it
            raise Exception("Gemini returned invalid JSON structure.")

    @classmethod
    def match_resume_semantically(
        cls, resume_text: str, jd_text: str, api_key: str
    ) -> Dict[str, Any]:
        """
        Perform deep semantic gap analysis and calculate ATS compatibility scores.
        """
        prompt = f"""
You are an expert HR Specialist and ATS Optimizer. Your task is to evaluate the candidate's Resume against the Job Description (JD).
Perform a deep semantic analysis to match skills and experience:
1. Identify skills listed in the JD that are present in the resume (resolve synonyms semantically: e.g. "ReactJS" / "React" match, "PostgreSQL" / "Postgres" match).
2. Identify missing skills that are required or highly recommended in the JD but not found in the resume.
3. Extract top keywords/technologies from the Job Description.
4. Calculate a semantic 'skill_match_score' (0-100) reflecting how well the candidate's skills cover the requirements.
5. Calculate a semantic 'vector_similarity_score' (0-100) representing how well the candidate's background/experience fits the role responsibilities.
6. Provide specific, highly actionable improvement suggestions for the resume (e.g., "Add experience in AWS", "Incorporate Python metrics").

Format your output as a single JSON object with these exact keys:
- `skill_match_score`: float (0.0 to 100.0)
- `vector_similarity_score`: float (0.0 to 100.0)
- `matched_skills`: list of strings (matched skills from the JD)
- `missing_skills`: list of strings (lacking skills from the JD)
- `top_jd_keywords`: list of strings (main keywords extracted from JD)
- `shared_keywords`: list of strings (matching/shared keywords)
- `improvement_suggestions`: list of strings (actionable feedback)

Do not include markdown code block syntax (like ```json), return raw JSON directly.

Resume Text:
{resume_text}

Job Description:
{jd_text}
"""
        response_text = cls._call_gemini(prompt, api_key)
        try:
            parsed = json.loads(response_text)
            
            # Clean and validate types
            parsed["skill_match_score"] = float(parsed.get("skill_match_score", 0))
            parsed["vector_similarity_score"] = float(parsed.get("vector_similarity_score", 0))
            parsed["matched_skills"] = [str(x) for x in parsed.get("matched_skills", [])]
            parsed["missing_skills"] = [str(x) for x in parsed.get("missing_skills", [])]
            parsed["top_jd_keywords"] = [str(x) for x in parsed.get("top_jd_keywords", [])]
            parsed["shared_keywords"] = [str(x) for x in parsed.get("shared_keywords", [])]
            parsed["improvement_suggestions"] = [str(x) for x in parsed.get("improvement_suggestions", [])]
            
            return parsed
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to decode/validate JSON from Gemini match: {response_text}. Error: {str(e)}")
            raise Exception("Gemini returned invalid JSON structure or types for match.")
