from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.pdf_parser import PDFParserService
from app.services.text_cleaner import TextCleanerService
from app.services.section_extractor import SectionExtractorService
from app.models.parser import ParseResumeResponse, ParsedSections, TextStatistics

router = APIRouter()


@router.post(
    "/parse-resume",
    response_model=ParseResumeResponse,
    summary="Upload & Parse PDF Resume",
    status_code=status.HTTP_200_OK,
)
async def parse_resume(file: UploadFile = File(...)):
    """
    Upload a PDF resume file to extract, clean, and segment its content into structured sections.

    - **file**: PDF file binary stream (must end with .pdf and be application/pdf).
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF documents (.pdf) are supported.",
        )

    # Read binary bytes
    file_bytes = await file.read()

    # Step 1: Extract text and page count from PDF stream
    raw_text, page_count = PDFParserService.extract_text_from_pdf(file_bytes)

    # Step 2: Clean and normalize text
    cleaned_text = TextCleanerService.clean_text(raw_text)

    # Step 3: Segment text into resume sections
    segmented_dict = SectionExtractorService.segment_sections(cleaned_text)

    # Step 4: Calculate text statistics
    stats = TextCleanerService.get_text_statistics(cleaned_text)

    return ParseResumeResponse(
        filename=file.filename,
        page_count=page_count,
        raw_text=cleaned_text,
        sections=ParsedSections(**segmented_dict),
        statistics=TextStatistics(**stats),
    )
