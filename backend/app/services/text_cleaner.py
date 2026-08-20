import re
from typing import Dict, Any


class TextCleanerService:
    """
    Utility service for cleaning, normalizing, and auditing raw text extracted from resumes.
    Normalizes multi-line spacing, bullet points, and tab characters for downstream text parsing.
    """

    # Common unicode bullet points found in resumes
    BULLET_PATTERN = re.compile(r"[\u2022\u2023\u25b6\u25c0\u25ba\u25c4\u2013\u2014\u2026\u25cf\u25cb\u25a0\u25a1▪■•\*\-]")

    @classmethod
    def clean_text(cls, raw_text: str) -> str:
        """
        Cleans raw extracted text:
        1. Strips non-printable characters.
        2. Normalizes bullet points to standard space separators.
        3. Collapses redundant blank lines while preserving structural spacing.
        """
        if not raw_text:
            return ""

        # Replace unicode bullets with whitespace
        cleaned = cls.BULLET_PATTERN.sub(" ", raw_text)

        # Normalize carriage returns and line feeds
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

        # Replace multiple spaces within a line with a single space
        lines = []
        for line in cleaned.split("\n"):
            normalized_line = re.sub(r"[ \t]+", " ", line).strip()
            if normalized_line:
                lines.append(normalized_line)

        return "\n".join(lines)

    @staticmethod
    def get_text_statistics(text: str) -> Dict[str, Any]:
        """
        Returns metric analysis of the text (word count, line count, character count).
        """
        lines = text.split("\n") if text else []
        words = re.findall(r"\b\w+\b", text) if text else []

        return {
            "character_count": len(text),
            "word_count": len(words),
            "line_count": len(lines),
        }
