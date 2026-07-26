import re
from typing import Dict, List, Set
from app.services.skill_taxonomy import SkillTaxonomy


class SkillExtractorService:
    """
    NLP & Keyword Matching service to extract technical skills from raw text.
    Uses regex word boundary matching to ensure precise extraction without false positives.
    """

    @classmethod
    def extract_skills(cls, text: str) -> Dict[str, List[str]]:
        """
        Extracts skills from text and groups them by taxonomy category.
        """
        if not text:
            return {category: [] for category in SkillTaxonomy.SKILL_DATABASE.keys()}

        lower_text = text.lower()
        extracted_categorized: Dict[str, List[str]] = {}

        for category, skill_list in SkillTaxonomy.SKILL_DATABASE.items():
            matched_in_category = []
            for skill in skill_list:
                if cls._match_skill(skill, lower_text):
                    # Standardize skill representation
                    matched_in_category.append(skill)
            extracted_categorized[category] = sorted(list(set(matched_in_category)))

        return extracted_categorized

    @classmethod
    def extract_flat_skills(cls, text: str) -> Set[str]:
        """
        Extracts a flat set of all matched skills in lower case.
        """
        categorized = cls.extract_skills(text)
        flat_skills = set()
        for skill_list in categorized.values():
            flat_skills.update(skill_list)
        return flat_skills

    @staticmethod
    def _match_skill(skill: str, text: str) -> bool:
        """
        Regex matcher handling special character skills like C++, C#, .NET, Node.js safely.
        """
        # Escape special regex characters in skill name
        escaped_skill = re.escape(skill)

        # Handle C++, C#, .NET, etc. where standard \b word boundaries don't work natively
        if skill in ["c++", "c#", ".net", "asp.net", "dot net", "react.js", "vue.js", "node.js", "next.js"]:
            pattern = rf"(?:^|\s|\,|/){escaped_skill}(?:$|\s|\,|/|\.|\))"
        else:
            pattern = rf"\b{escaped_skill}\b"

        return bool(re.search(pattern, text, re.IGNORECASE))
