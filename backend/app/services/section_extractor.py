import re
from typing import Dict, List


class SectionExtractorService:
    """
    Segmentation engine that partitions resume text into key resume sections:
    - Summary / Objective
    - Technical Skills
    - Work Experience
    - Projects
    - Education
    - Certifications / Achievements
    """

    # Section Header Mapping Patterns
    SECTION_HEADERS = {
        "summary": re.compile(
            r"^(summary|professional summary|about me|objective|career objective|profile)\b",
            re.IGNORECASE,
        ),
        "skills": re.compile(
            r"^(skills|technical skills|core competencies|technologies|tools|languages|skills & expertise)\b",
            re.IGNORECASE,
        ),
        "experience": re.compile(
            r"^(experience|work experience|employment|employment history|professional experience|internships)\b",
            re.IGNORECASE,
        ),
        "projects": re.compile(
            r"^(projects|key projects|personal projects|academic projects)\b",
            re.IGNORECASE,
        ),
        "education": re.compile(
            r"^(education|academic background|qualifications|academic history)\b",
            re.IGNORECASE,
        ),
        "certifications": re.compile(
            r"^(certifications|licenses|courses|awards|achievements|certifications & awards)\b",
            re.IGNORECASE,
        ),
    }

    @classmethod
    def segment_sections(cls, cleaned_text: str) -> Dict[str, str]:
        """
        Segments cleaned text into dictionary map of identified resume sections.
        """
        lines = cleaned_text.split("\n")
        sections: Dict[str, List[str]] = {
            "summary": [],
            "skills": [],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "other": [],
        }

        current_section = "summary"

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check if line matches a known section header
            matched_section = cls._detect_header(line_str)
            if matched_section:
                current_section = matched_section
            else:
                sections[current_section].append(line_str)

        # Convert line lists to consolidated text blocks
        return {
            section_name: "\n".join(content_lines).strip()
            for section_name, content_lines in sections.items()
        }

    @classmethod
    def _detect_header(cls, line: str) -> str | None:
        """
        Heuristic header detection: Checks if line matches pattern and looks like a section heading.
        Section headings are typically short (< 40 chars) and standalone.
        """
        if len(line) > 40:
            return None

        # Clean punctuation from potential header
        clean_header = re.sub(r"[:\-_#=]", "", line).strip()

        for section_name, pattern in cls.SECTION_HEADERS.items():
            if pattern.match(clean_header):
                return section_name

        return None
