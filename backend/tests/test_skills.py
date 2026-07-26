from fastapi.testclient import TestClient
from app.main import app
from app.services.skill_extractor import SkillExtractorService
from app.services.skill_gap_analyzer import SkillGapAnalyzerService

client = TestClient(app)


def test_skill_extractor_service():
    sample_text = "Proficient in Python, FastAPI, Docker, C++, React, PostgreSQL, and Machine Learning."
    skills_flat = SkillExtractorService.extract_flat_skills(sample_text)

    assert "python" in skills_flat
    assert "fastapi" in skills_flat
    assert "docker" in skills_flat
    assert "c++" in skills_flat
    assert "react" in skills_flat
    assert "postgresql" in skills_flat
    assert "machine learning" in skills_flat


def test_skill_gap_analyzer_service():
    resume_text = "Experienced SDE with Python, FastAPI, Docker, and PostgreSQL."
    jd_text = "Looking for SDE with Python, FastAPI, Docker, Kubernetes, AWS, and React."

    result = SkillGapAnalyzerService.analyze_gap(resume_text, jd_text)

    assert result["matched_skills_count"] == 3  # python, fastapi, docker
    assert "python" in result["matched_skills"]
    assert "kubernetes" in result["missing_skills"]
    assert "aws" in result["missing_skills"]
    assert "react" in result["missing_skills"]
    assert result["match_percentage"] == 50.0  # 3 out of 6 matched


def test_extract_skills_api():
    payload = {"text": "Expert in TypeScript, Node.js, Next.js, and Redis."}
    response = client.post("/api/v1/extract-skills", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["total_skills_found"] == 4
    assert "typescript" in data["flat_skills"]
    assert "next.js" in data["flat_skills"]


def test_analyze_skill_gap_api():
    payload = {
        "resume_text": "Skills: Java, Spring Boot, MySQL, Git.",
        "job_description_text": "Requirements: Java, Spring Boot, Microservices, Kafka, MySQL."
    }
    response = client.post("/api/v1/analyze-skill-gap", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["matched_skills_count"] == 3  # java, spring boot, mysql
    assert "kafka" in data["missing_skills"]
    assert data["match_percentage"] == 75.0  # 3 matched out of 4 (java, spring boot, kafka, mysql)
