from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, Any, List


class TFIDFService:
    """
    TF-IDF (Term Frequency - Inverse Document Frequency) Vectorization Service.
    Calculates term weights and lexical feature overlap between Resume and Job Description.
    """

    @classmethod
    def compute_tfidf_features(cls, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """
        Computes TF-IDF vector matrix for Resume and Job Description,
        extracts top weighted keywords, and measures term overlap.
        """
        if not resume_text.strip() or not jd_text.strip():
            return {
                "top_jd_keywords": [],
                "top_resume_keywords": [],
                "shared_keywords": [],
            }

        # Initialize TfidfVectorizer with unigrams and bigrams
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=50,
        )

        try:
            tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
            feature_names = vectorizer.get_feature_names_out()

            # Row 0: JD TF-IDF weights, Row 1: Resume TF-IDF weights
            jd_weights = tfidf_matrix[0].toarray()[0]
            resume_weights = tfidf_matrix[1].toarray()[0]

            # Top keywords in JD by TF-IDF weight
            jd_top_indices = jd_weights.argsort()[::-1][:15]
            top_jd_keywords = [
                feature_names[i] for i in jd_top_indices if jd_weights[i] > 0
            ]

            # Top keywords in Resume by TF-IDF weight
            resume_top_indices = resume_weights.argsort()[::-1][:15]
            top_resume_keywords = [
                feature_names[i] for i in resume_top_indices if resume_weights[i] > 0
            ]

            # Shared top weighted keywords
            shared_keywords = sorted(
                list(set(top_jd_keywords).intersection(set(top_resume_keywords)))
            )

            return {
                "top_jd_keywords": top_jd_keywords,
                "top_resume_keywords": top_resume_keywords,
                "shared_keywords": shared_keywords,
            }
        except Exception:
            return {
                "top_jd_keywords": [],
                "top_resume_keywords": [],
                "shared_keywords": [],
            }
