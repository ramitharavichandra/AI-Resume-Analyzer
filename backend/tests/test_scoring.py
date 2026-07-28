from fastapi.testclient import TestClient
from app.main import app
from app.services.vector_similarity import VectorSimilarityService
from app.services.tfidf_service import TFIDFService
from app.services.ats_scorer import ATSScorerService

client = TestClient(app)


def test_vector_similarity_service():
    text1 = "Python FastAPI Docker PostgreSQL React"
    text2 = "Looking for engineer with Python FastAPI and Docker experience"

    score = VectorSimilarityService.calculate_cosine_similarity(text1, text2)
    assert 0.0 <= score <= 1.0
    assert score > 0.2  # Should have positive similarity due to overlapping tokens


def test_tfidf_service():
    resume = "Developed microservices in Python using FastAPI, Docker, and PostgreSQL."
    jd = "Requirements: Python backend developer with FastAPI, Docker, Kubernetes, and AWS."

    features = TFIDFService.compute_tfidf_features(resume, jd)
    assert "fastapi" in features["shared_keywords"] or "python" in features["shared_keywords"]
    assert len(features["top_jd_keywords"]) > 0


def test_ats_scorer_service():
    resume = """
Summary
Experienced SDE with expertise in Python, FastAPI, Docker, and PostgreSQL.

Technical Skills
Python, FastAPI, Docker, PostgreSQL, React, Git.

Work Experience
Software Engineer Intern at Tech Corp. Built microservices.

Projects
AI Resume Analyzer: Built with FastAPI and React.

Education
B.E. Information Science Engineering.
"""

    jd = """
Looking for a Full Stack / AI Engineer proficient in Python, FastAPI, Docker, PostgreSQL, React, AWS, and Kubernetes.
Responsibilities include building scalable REST APIs and containerized microservices.
"""

    result = ATSScorerService.calculate_ats_score(resume, jd)

    assert result["ats_score"] >= 50.0
    assert result["rating"] in ["Needs Improvement", "Strong Match", "Excellent"]
    assert "python" in result["matched_skills"]
    assert "kubernetes" in result["missing_skills"]
    assert len(result["present_sections"]) == 5
    assert len(result["improvement_suggestions"]) > 0


def test_match_resume_api():
    payload = {
        "resume_text": "Skills: Java, Spring Boot, MySQL, Git, Docker. Experience: Developed REST APIs.",
        "job_description_text": "Requirements: Java, Spring Boot, MySQL, Docker, Kubernetes, Microservices."
    }

    response = client.post("/api/v1/match-resume", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "ats_score" in data
    assert data["ats_score"] > 0.0
    assert "java" in data["matched_skills"]
    assert "kubernetes" in data["missing_skills"]
