# AI Resume Analyzer 🚀

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-green)
![React](https://img.shields.io/badge/React-19-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5%2B-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4-38bdf8)

A production-grade, full-stack AI system that parses candidate resumes (PDF format), extracts skill taxonomies, calculates ATS compatibility scores using **TF-IDF Vectorization** and **Vector Cosine Similarity**, and generates actionable resume improvement recommendations.

---

## 🌟 Key Features

- **📄 PDF Text Extraction & Cleaning Engine**: In-memory binary PDF parsing via `PyPDF` with text normalization, bullet stripping, and metric auditing.
- **🏷️ Section Segmentation Pipeline**: Heuristic regex engine partitioning resumes into `summary`, `skills`, `experience`, `projects`, `education`, and `certifications`.
- **🎯 Skill Taxonomy & Gap Analytics**: 6-domain tech stack taxonomy using set algebra (`intersection`, `difference`) for keyword gap analysis.
- **🧮 Hybrid ATS Scoring Algorithm**: Multi-factor weighted score combining:
  - Skill Match Score (45% weight)
  - Vector Cosine Similarity Score (35% weight)
  - Structural Section Score (20% weight)
- **💡 Actionable Feedback Generator**: Automated recommendations identifying missing skills, structural section gaps, and terminology misalignments.
- **🎨 Glassmorphism React SPA**: Built with Vite, React 19, TypeScript, and Tailwind CSS v4 featuring an animated SVG score ring and downloadable PDF report export.

---

## 🏗️ System Architecture

```
+--------------------------+        HTTP POST /api/v1/match-resume        +-------------------------+
|                          |  ----------------------------------------->  |                         |
|  React 19 + TypeScript   |                                              |  FastAPI Backend        |
|  Tailwind CSS v4 Client  |  <-----------------------------------------  |  (Python 3.10+)         |
+--------------------------+          JSON ATS Analysis Payload           +------------+------------+
                                                                                       |
                                                                                       v
                                                                          +-------------------------+
                                                                          |  NLP Engine Services    |
                                                                          |  - PyPDF Parser         |
                                                                          |  - Section Segmenter    |
                                                                          |  - Skill Taxonomy       |
                                                                          |  - TF-IDF Vectorizer    |
                                                                          |  - Cosine Similarity    |
                                                                          +-------------------------+
```

---

## 🔌 API Documentation

| Method | Endpoint | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/api/v1/health` | Health Check | None | `{"status": "healthy", "version": "1.0.0"}` |
| **POST** | `/api/v1/parse-resume` | Upload & Segment PDF | `file: UploadFile` (.pdf) | Extracted text, section map & page stats |
| **POST** | `/api/v1/extract-skills` | Categorized Skill Extraction | `{"text": "..."}` | Flat & categorized skills dictionary |
| **POST** | `/api/v1/analyze-skill-gap` | Skill Match Gap Analytics | `{"resume_text": "...", "job_description_text": "..."}` | `match_percentage`, `matched_skills`, `missing_skills` |
| **POST** | `/api/v1/match-resume` | Hybrid ATS Score & Recommendations | `{"resume_text": "...", "job_description_text": "..."}` | `ats_score`, `rating`, metric scores, suggestions |

---

## 📂 Project Monorepo Structure

```
AI-Resume-Analyzer/
├── backend/
│   ├── app/
│   │   ├── api/v1/             # FastAPI Endpoint Routers
│   │   ├── models/             # Pydantic Request/Response Schemas
│   │   ├── services/           # PDF Parser, Skill Taxonomy, TF-IDF & ATS Engine
│   │   ├── config.py           # Pydantic v2 Settings Manager
│   │   └── main.py             # FastAPI App Entrypoint
│   ├── tests/                  # Pytest Automated Test Suite (26 passing tests)
│   └── requirements.txt        # Python Dependencies
├── frontend/
│   ├── src/
│   │   ├── components/         # Glassmorphism React UI Components
│   │   ├── services/           # Typed API Service Client
│   │   ├── index.css           # Tailwind v4 Design System & Glass Utility
│   │   └── App.tsx             # Root Application Flow
│   └── package.json            # Node.js Dependencies
├── README.md                   # Project Documentation
└── .gitignore
```

---

## ⚙️ Quick Start & Installation

### 1. Backend Setup (FastAPI)

```bash
cd backend

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run automated tests (specify PYTHONPATH so pytest resolves the 'app' module)
PYTHONPATH=. pytest

# Start development server
uvicorn app.main:app --reload --port 8000
```

Interactive API Swagger documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 📄 License

MIT License. Created for Placement Portfolio Development.
