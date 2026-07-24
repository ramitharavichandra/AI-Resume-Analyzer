# AI Resume Analyzer

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-green)
![React](https://img.shields.io/badge/React-18%2B-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5%2B-blue)

An production-grade AI-powered Resume Analyzer that parses resumes (PDF format), extracts key skills, calculates ATS compatibility scores against Job Descriptions using Natural Language Processing (NLP), Sentence Embeddings, and Cosine Similarity, and provides actionable resume improvement suggestions.

---

## 🎯 Problem Statement
Job applicants often face high rejection rates due to Automated Applicant Tracking Systems (ATS) filtering out resumes before a human recruiter ever sees them. Candidates lack objective, data-driven feedback on how well their resumes match target Job Descriptions (JDs) and what specific skills or key phrases are missing.

## 🚀 Proposed Solution
The **AI Resume Analyzer** provides an instant, privacy-aware breakdown of any uploaded PDF resume:
1. **Automated Document Parsing & Text Extraction**: Robust PDF text parsing preserving context and structural sections.
2. **Skill & Keyword Extraction**: NLP-based named entity and keyword recognition to identify tech stacks, domain skills, and experience keywords.
3. **Vector Similarity & ATS Scoring**: Hybrid scoring combining TF-IDF lexical matching and Sentence Transformer semantic embeddings with Cosine Similarity.
4. **Missing Skill & Gap Analysis**: Comparative set analysis highlighting critical missing skills and keyword deficiencies relative to job descriptions.
5. **Actionable Improvement Recommendations**: Rule-based & LLM-assisted feedback report downloadable as PDF.

---

## 🏗️ Architecture & High-Level System Design

```
+-------------------+        HTTP POST /api/v1/analyze        +--------------------+
|                   |  ------------------------------------->  |                    |
|  React + TS Frontend |                                        |  FastAPI Backend   |
|  (Shadcn UI, UI)  |  <-------------------------------------  |  (Python 3.10+)    |
+-------------------+         JSON Analysis Payload           +---------+----------+
                                                                        |
                                                                        v
                                                              +--------------------+
                                                              |  NLP Engine        |
                                                              |  - PDF Parser      |
                                                              |  - TF-IDF Vectorizer|
                                                              |  - SBERT Embeddings|
                                                              |  - Similarity Calc |
                                                              +--------------------+
```

---

## 📂 Project Structure

```
AI-Resume-Analyzer/
├── backend/
│   ├── app/
│   │   ├── api/             # API routes (v1 endpoints)
│   │   ├── core/            # Core logic, security, & config
│   │   ├── services/        # Business logic & NLP pipeline
│   │   ├── models/          # Pydantic schemas & response models
│   │   └── main.py          # FastAPI application entrypoint
│   ├── tests/               # Unit & integration tests
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/                # React TypeScript Web Application
├── README.md                # Project documentation
└── .gitignore
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2
- **NLP & AI**: PyPDF, Scikit-Learn (TF-IDF, Cosine Similarity), Sentence-Transformers, NLTK/spaCy
- **Frontend**: React 18, TypeScript, Tailwind CSS, Vite
- **Testing**: Pytest, HTTPX

---

## ⚙️ Quick Start & Installation

### Backend Setup
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. Access interactive API documentation at `http://localhost:8000/docs`.

---

## 📄 License
MIT License. Created for Placement Portfolio Development.
