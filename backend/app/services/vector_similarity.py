from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class VectorSimilarityService:
    """
    Vector Space & Cosine Similarity Service.
    Calculates the mathematical angle (cosine of similarity) between
    high-dimensional document vector representations.
    """

    @classmethod
    def calculate_cosine_similarity(cls, text1: str, text2: str) -> float:
        """
        Calculates Cosine Similarity score (0.0 to 1.0) between two text blocks
        using TF-IDF vector representations.

        Formula: Cosine Similarity = (A · B) / (||A|| * ||B||)
        """
        if not text1.strip() or not text2.strip():
            return 0.0

        try:
            vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([text1, text2])

            # Calculate cosine similarity matrix (2x2)
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = float(similarity_matrix[0][0])

            # Clamp between 0.0 and 1.0 and round to 4 decimals
            return round(max(0.0, min(1.0, similarity_score)), 4)
        except Exception:
            return 0.0
