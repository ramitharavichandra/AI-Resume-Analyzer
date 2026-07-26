from typing import Dict, List, Set


class SkillTaxonomy:
    """
    Master Skill Taxonomy & Categorized Tech Stack Dictionary.
    Organized into domain categories for targeted skill extraction.
    """

    SKILL_DATABASE: Dict[str, List[str]] = {
        "programming_languages": [
            "python", "javascript", "typescript", "java", "c++", "c#", "go",
            "golang", "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
            "sql", "html", "css", "bash", "shell"
        ],
        "frameworks_and_libraries": [
            "react", "react.js", "next.js", "vue", "vue.js", "angular", "node.js",
            "express", "fastapi", "flask", "django", "spring boot", "dot net",
            "asp.net", "tailwind css", "bootstrap", "shadcn", "material ui",
            "redux", "zustand", "graphql", "rest api", "pandas", "numpy",
            "scikit-learn", "sklearn", "pytorch", "tensorflow", "keras",
            "sentence-transformers", "transformers", "langchain", "llama-index",
            "spacy", "nltk", "opencv"
        ],
        "databases_and_storage": [
            "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis",
            "firebase", "firestore", "supabase", "dynamodb", "cassandra",
            "elasticsearch", "chromadb", "faiss", "pinecone", "qdrant", "weaviate"
        ],
        "cloud_and_devops": [
            "docker", "kubernetes", "k8s", "aws", "amazon web services", "gcp",
            "google cloud", "azure", "terraform", "ci/cd", "github actions",
            "gitlab ci", "jenkins", "nginx", "linux", "ubuntu", "helm"
        ],
        "tools_and_platforms": [
            "git", "github", "gitlab", "bitbucket", "jira", "confluence",
            "postman", "figma", "vs code", "docker desktop", "celery", "rabbitmq",
            "kafka", "spark", "hadoop", "airflow"
        ],
        "ai_ml_concepts": [
            "natural language processing", "nlp", "machine learning",
            "deep learning", "computer vision", "llm", "large language models",
            "rag", "retrieval-augmented generation", "embeddings", "vector search",
            "tf-idf", "cosine similarity", "prompt engineering", "supervised learning",
            "unsupervised learning", "reinforcement learning", "fine-tuning", "bert"
        ],
    }

    @classmethod
    def get_all_skills_set(cls) -> Set[str]:
        """Returns flat set of all unique skills in lower case."""
        all_skills = set()
        for category_skills in cls.SKILL_DATABASE.values():
            all_skills.update(category_skills)
        return all_skills
