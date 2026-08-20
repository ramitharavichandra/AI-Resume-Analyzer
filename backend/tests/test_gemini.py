from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import pytest
import httpx
from app.main import app
from app.services.gemini_service import GeminiService

client = TestClient(app)

def test_gemini_parse_resume_semantically_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": '{"summary": "Experienced dev", "skills": "Python, Go", "experience": "Worked at Google", "projects": "", "education": "", "certifications": "", "other": ""}'
                        }
                    ]
                }
            }
        ]
    }
    
    with patch("httpx.Client.post", return_value=mock_response) as mock_post:
        result = GeminiService.parse_resume_semantically("Resume text", "fake_api_key")
        assert result["summary"] == "Experienced dev"
        assert result["skills"] == "Python, Go"
        assert result["experience"] == "Worked at Google"
        mock_post.assert_called_once()


def test_gemini_parse_resume_semantically_invalid_json():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "invalid json content"
                        }
                    ]
                }
            }
        ]
    }
    
    with patch("httpx.Client.post", return_value=mock_response):
        with pytest.raises(Exception) as exc_info:
            GeminiService.parse_resume_semantically("Resume text", "fake_api_key")
        assert "Gemini returned invalid JSON structure" in str(exc_info.value)


def test_gemini_match_resume_semantically_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": '{"skill_match_score": 85.0, "vector_similarity_score": 90.0, "matched_skills": ["python", "fastapi"], "missing_skills": ["aws"], "top_jd_keywords": ["python", "aws"], "shared_keywords": ["python"], "improvement_suggestions": ["Add AWS project"]}'
                        }
                    ]
                }
            }
        ]
    }
    
    with patch("httpx.Client.post", return_value=mock_response):
        result = GeminiService.match_resume_semantically("Resume text", "JD text", "fake_api_key")
        assert result["skill_match_score"] == 85.0
        assert result["vector_similarity_score"] == 90.0
        assert "python" in result["matched_skills"]
        assert "aws" in result["missing_skills"]


def test_gemini_match_resume_semantically_api_error():
    with patch("httpx.Client.post", side_effect=httpx.HTTPError("Network issue")):
        with pytest.raises(httpx.HTTPError) as exc_info:
            GeminiService.match_resume_semantically("Resume text", "JD text", "fake_api_key")
        assert "Network issue" in str(exc_info.value)


def test_parse_resume_endpoint_gemini_success():
    mock_parse_result = {
        "summary": "Experienced engineer",
        "skills": "Python, FastAPI",
        "experience": "Dev at Startup",
        "projects": "",
        "education": "",
        "certifications": "",
        "other": ""
    }
    
    with patch("app.config.settings.GEMINI_API_KEY", "fake_key"), \
         patch("app.services.gemini_service.GeminiService.parse_resume_semantically", return_value=mock_parse_result):
        
        mock_docx_bytes = b"dummy docx bytes"
        with patch("app.services.docx_parser.DocxParserService.extract_text_from_docx", return_value=("Resume Text", 1)):
            response = client.post(
                "/api/v1/parse-resume",
                files={"file": ("resume.docx", mock_docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["engine"] == "Gemini AI Engine"
            assert data["sections"]["summary"] == "Experienced engineer"


def test_parse_resume_endpoint_gemini_fallback():
    with patch("app.config.settings.GEMINI_API_KEY", "fake_key"), \
         patch("app.services.gemini_service.GeminiService.parse_resume_semantically", side_effect=Exception("Gemini error")):
        
        mock_docx_bytes = b"dummy docx bytes"
        with patch("app.services.docx_parser.DocxParserService.extract_text_from_docx", return_value=("Summary\nSelf motivated\nSkills\nPython, FastAPI", 1)):
            response = client.post(
                "/api/v1/parse-resume",
                files={"file": ("resume.docx", mock_docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["engine"] == "Local Heuristics Fallback"
            assert "Self motivated" in data["sections"]["summary"]


def test_match_resume_endpoint_gemini_success():
    mock_match_result = {
        "skill_match_score": 80.0,
        "vector_similarity_score": 75.0,
        "matched_skills": ["python"],
        "missing_skills": ["kubernetes"],
        "top_jd_keywords": ["python", "kubernetes"],
        "shared_keywords": ["python"],
        "improvement_suggestions": ["Add Kubernetes"]
    }
    
    payload = {
        "resume_text": "Skills: python",
        "job_description_text": "Requirements: python, kubernetes"
    }
    
    with patch("app.config.settings.GEMINI_API_KEY", "fake_key"), \
         patch("app.services.gemini_service.GeminiService.match_resume_semantically", return_value=mock_match_result):
        
        response = client.post("/api/v1/match-resume", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["engine"] == "Gemini AI Engine"
        assert data["skill_match_score"] == 80.0
        assert data["vector_similarity_score"] == 75.0
        assert "python" in data["matched_skills"]


def test_match_resume_endpoint_gemini_fallback():
    payload = {
        "resume_text": "Skills: Python, FastAPI. Experience: Developed REST APIs.",
        "job_description_text": "Requirements: Python, FastAPI, Docker, Kubernetes."
    }
    
    with patch("app.config.settings.GEMINI_API_KEY", "fake_key"), \
         patch("app.services.gemini_service.GeminiService.match_resume_semantically", side_effect=Exception("Gemini error")):
        
        response = client.post("/api/v1/match-resume", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["engine"] == "Local Heuristics Fallback"
        assert data["ats_score"] > 0.0
