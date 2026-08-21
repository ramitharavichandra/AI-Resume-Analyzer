import io
from pypdf import PdfReader
from fastapi import HTTPException, status
from typing import Tuple


class PDFParserService:
    """
    Production-grade PDF parsing service using PyPDF.
    Handles file stream extraction, password checks, and corruption handling.
    This service is integrated with the main resume segmentation pipeline.
    """

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, int]:
        """
        Extracts raw text content and total page count from raw PDF bytes.

        :param file_bytes: Raw binary bytes of uploaded PDF file.
        :return: Tuple containing (extracted_text, page_count)
        :raises HTTPException: 400 Bad Request with details if:
            - The uploaded file is empty.
            - The PDF file is password-protected or encrypted.
            - The PDF file contains 0 pages.
            - The PDF contains only scanned images (no selectable text).
            - The file stream is corrupt or invalid.
        """
        if not file_bytes or len(file_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        try:
            pdf_file_stream = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file_stream)

            if reader.is_encrypted:
                try:
                    # Attempt decrypt with empty password for standard encrypted PDFs
                    reader.decrypt("")
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="PDF file is password-protected or encrypted.",
                    )

            page_count = len(reader.pages)
            if page_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="PDF file contains 0 pages.",
                )

            extracted_text = ""
            for page_idx, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"

            if not extracted_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not extract text from PDF. File might contain only scanned images/OCR.",
                )

            return extracted_text, page_count

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Corrupt or invalid PDF file stream: {str(e)}",
            )
