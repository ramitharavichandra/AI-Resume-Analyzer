import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.config import settings
from app.services.pdf_parser import PDFParserService
from app.services.docx_parser import DocxParserService
from app.services.text_cleaner import TextCleanerService
from app.services.section_extractor import SectionExtractorService
from app.services.gemini_service import GeminiService
from app.models.parser import ParseResumeResponse, ParsedSections, TextStatistics

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/parse-resume",
    response_model=ParseResumeResponse,
    summary="Upload & Parse Resume",
    status_code=status.HTTP_200_OK,
)
async def parse_resume(file: UploadFile = File(...)):
    """
    Upload a PDF or Word resume file to extract, clean, and segment its content into structured sections.

    - **file**: PDF (.pdf) or Word (.docx) file binary stream.
    """
    filename_lower = file.filename.lower() if file.filename else ""
    if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF (.pdf) and Word (.docx) documents are supported.",
        )

    # Read binary bytes
    file_bytes = await file.read()

    # Step 1: Extract text and page count from the document stream
    if filename_lower.endswith(".pdf"):
        raw_text, page_count = PDFParserService.extract_text_from_pdf(file_bytes)
    else:
        raw_text, page_count = DocxParserService.extract_text_from_docx(file_bytes)

    # Step 2: Clean and normalize text
    cleaned_text = TextCleanerService.clean_text(raw_text)

    # Step 3: Segment text into resume sections
    engine_used = "Local Heuristics Fallback"
    segmented_dict = None

    if settings.GEMINI_API_KEY:
        try:
            logger.info("Attempting semantic parsing using Gemini API.")
            segmented_dict = GeminiService.parse_resume_semantically(
                cleaned_text, settings.GEMINI_API_KEY
            )
            engine_used = "Gemini AI Engine"
        except Exception as e:
            logger.warning(
                f"Gemini parsing failed, falling back to local extractor. Error: {str(e)}"
            )

    if not segmented_dict:
        segmented_dict = SectionExtractorService.segment_sections(cleaned_text)

    # Step 4: Calculate text statistics
    stats = TextCleanerService.get_text_statistics(cleaned_text)

    return ParseResumeResponse(
        filename=file.filename or "resume",
        page_count=page_count,
        raw_text=cleaned_text,
        sections=ParsedSections(**segmented_dict),
        statistics=TextStatistics(**stats),
        engine=engine_used,
    )

