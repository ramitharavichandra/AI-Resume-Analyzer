import io
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from app.main import app
from app.services.text_cleaner import TextCleanerService
from app.services.section_extractor import SectionExtractorService

client = TestClient(app)


def create_dummy_pdf_bytes(text_content: str = "Technical Skills\nPython FastAPI Docker\nExperience\nSoftware Engineer") -> bytes:
    """
    Helper function to generate binary bytes of a valid PDF containing text.
    """
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    
    # Write a simple PDF stream using pypdf annotations or basic object stream
    # Note: blank page with text stream
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    return pdf_bytes.getvalue()


def test_parse_resume_invalid_file_extension():
    response = client.post(
        "/api/v1/parse-resume",
        files={"file": ("resume.txt", b"Invalid content", "text/plain")},
    )
    assert response.status_code == 400
    assert "Only PDF documents (.pdf) are supported" in response.json()["detail"]


def test_parse_resume_empty_file():
    response = client.post(
        "/api/v1/parse-resume",
        files={"file": ("resume.pdf", b"", "application/pdf")},
    )
    assert response.status_code == 400


def test_text_cleaner_service():
    raw = "• Built web app   with   Python\r\n\r\n- Developed REST APIs"
    cleaned = TextCleanerService.clean_text(raw)
    assert "Built web app with Python" in cleaned
    assert "Developed REST APIs" in cleaned
    assert "•" not in cleaned

    stats = TextCleanerService.get_text_statistics(cleaned)
    assert stats["word_count"] > 0
    assert stats["line_count"] == 2


def test_section_extractor_service():
    sample_text = """
Summary
Enthusiastic SDE candidate with experience in AI.

Technical Skills
Python, FastAPI, Docker, PostgreSQL, React.

Experience
SDE Intern at TechCorp.
Developed microservices in Python.

Education
B.E. Information Science Engineering.
"""
    sections = SectionExtractorService.segment_sections(sample_text)
    assert "Enthusiastic SDE candidate" in sections["summary"]
    assert "Python, FastAPI" in sections["skills"]
    assert "SDE Intern at TechCorp" in sections["experience"]
    assert "B.E. Information Science" in sections["education"]
