import io
import zipfile
import xml.etree.ElementTree as ET
from fastapi import HTTPException, status
from typing import Tuple


class DocxParserService:
    """
    Production-grade DOCX parsing service using standard python libraries.
    Handles file stream extraction, XML parsing, and metadata-based page count retrieval.
    """

    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> Tuple[str, int]:
        """
        Extracts raw text content and estimates/reads total page count from raw DOCX bytes.

        :param file_bytes: Raw binary bytes of uploaded DOCX file.
        :return: Tuple containing (extracted_text, page_count)
        :raises HTTPException: 400 Bad Request if DOCX is invalid, empty, or corrupt.
        """
        if not file_bytes or len(file_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        # Check magic bytes for OLE compound files (encrypted DOCX or older .doc files)
        if file_bytes.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported document format. The file is either password-protected, encrypted, or in an older Word 97-2003 (.doc) format.",
            )


        try:
            docx_file_stream = io.BytesIO(file_bytes)
            with zipfile.ZipFile(docx_file_stream) as docx:
                # Step 1: Read main document XML
                try:
                    xml_content = docx.read("word/document.xml")
                except KeyError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid DOCX file: missing word/document.xml",
                    )

                root = ET.fromstring(xml_content)
                ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

                paragraphs = []
                # Retrieve all paragraphs (which includes text inside table cells, lists, and headers)
                for p in root.findall(".//w:p", ns):
                    texts = [t.text for t in p.findall(".//w:t", ns) if t.text]
                    if texts:
                        paragraphs.append("".join(texts))

                extracted_text = "\n".join(paragraphs)

                if not extracted_text.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Could not extract text from DOCX file. The document might be empty.",
                    )

                # Step 2: Try to read page count from docProps/app.xml
                page_count = 1
                try:
                    app_xml = docx.read("docProps/app.xml")
                    app_root = ET.fromstring(app_xml)
                    ns_app = {
                        "ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
                    }
                    pages_el = app_root.find(".//ep:Pages", ns_app)
                    if pages_el is not None and pages_el.text:
                        page_count = max(1, int(pages_el.text))
                except Exception:
                    # Fallback page calculation: approx 400 words per page
                    words = len(extracted_text.split())
                    page_count = max(1, (words + 399) // 400)

                return extracted_text, page_count

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Corrupt or invalid DOCX file stream: {str(e)}",
            )
