from pydantic import BaseModel, Field
from typing import Dict, Any


class TextStatistics(BaseModel):
    character_count: int = Field(..., description="Total characters extracted")
    word_count: int = Field(..., description="Total words counted")
    line_count: int = Field(..., description="Total lines extracted")


class ParsedSections(BaseModel):
    summary: str = Field("", description="Summary or objective section")
    skills: str = Field("", description="Technical skills section")
    experience: str = Field("", description="Work experience section")
    projects: str = Field("", description="Projects section")
    education: str = Field("", description="Education section")
    certifications: str = Field("", description="Certifications section")
    other: str = Field("", description="Uncategorized or miscellaneous sections")


class ParseResumeResponse(BaseModel):
    filename: str = Field(..., description="Uploaded PDF file name")
    page_count: int = Field(..., description="Total pages in PDF")
    raw_text: str = Field(..., description="Cleaned raw text extracted from PDF")
    sections: ParsedSections = Field(..., description="Segmented resume sections")
    statistics: TextStatistics = Field(..., description="Text length and metric counts")
    engine: str = Field("Local Heuristics Fallback", description="The parser engine used")
