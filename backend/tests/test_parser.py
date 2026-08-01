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
    assert "Only PDF (.pdf) and Word (.docx) documents are supported" in response.json()["detail"]


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


def create_dummy_docx_bytes(text_content: str) -> bytes:
    import zipfile
    import xml.etree.ElementTree as ET

    # Create word/document.xml content
    root = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}document')
    body = ET.SubElement(root, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body')
    
    for line in text_content.split('\n'):
        p = ET.SubElement(body, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
        r = ET.SubElement(p, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
        t = ET.SubElement(r, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
        t.text = line

    ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    xml_str = ET.tostring(root, encoding='utf-8')

    # Create dummy app.xml for page count
    app_root = ET.Element('{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Properties')
    pages = ET.SubElement(app_root, '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Pages')
    pages.text = "2"
    ET.register_namespace('ep', 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties')
    app_xml_str = ET.tostring(app_root, encoding='utf-8')

    docx_bytes = io.BytesIO()
    with zipfile.ZipFile(docx_bytes, 'w') as docx:
        docx.writestr('word/document.xml', xml_str)
        docx.writestr('docProps/app.xml', app_xml_str)
        
    return docx_bytes.getvalue()


def test_parse_resume_docx():
    sample_resume = """
Summary
Senior Software Engineer with Docker experience.

Skills
Python, PyTest, FastAPI, Kubernetes

Experience
Senior Dev at CloudCorp.
Built platforms.
"""
    docx_data = create_dummy_docx_bytes(sample_resume)
    response = client.post(
        "/api/v1/parse-resume",
        files={"file": ("my_resume.docx", docx_data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "my_resume.docx"
    assert data["page_count"] == 2
    assert "Senior Software Engineer" in data["raw_text"]
    assert "Python, PyTest" in data["sections"]["skills"]

