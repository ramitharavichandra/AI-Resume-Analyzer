// API Service Layer — All backend endpoint calls centralized here
// Base URL auto-detects dev vs production environment

const BASE_URL = import.meta.env.VITE_API_URL ?? '';

// ── Types ────────────────────────────────────────────────────────────────────

export interface ParsedSections {
  summary: string;
  skills: string;
  experience: string;
  projects: string;
  education: string;
  certifications: string;
  other: string;
}

export interface TextStatistics {
  character_count: number;
  word_count: number;
  line_count: number;
}

export interface ParseResumeResponse {
  filename: string;
  page_count: number;
  raw_text: string;
  sections: ParsedSections;
  statistics: TextStatistics;
  engine: string;
}

export interface ResumeMatchResponse {
  ats_score: number;
  rating: string;
  skill_match_score: number;
  vector_similarity_score: number;
  section_completeness_score: number;
  matched_skills: string[];
  missing_skills: string[];
  shared_keywords: string[];
  top_jd_keywords: string[];
  present_sections: string[];
  missing_sections: string[];
  improvement_suggestions: string[];
  engine: string;
}

// ── API Client ───────────────────────────────────────────────────────────────

/**
 * Helper to process backend fetch responses.
 * Parses JSON success payloads or extracts error details (defaulting to a generic HTTP message).
 * 
 * @param res Fetch Response object
 * @returns Parsed JSON body cast to type T
 * @throws Error containing backend detail message or default HTTP status message
 */
async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

/**
 * Uploads a PDF resume file to the backend parser endpoint.
 */
export async function parsePdfResume(file: File): Promise<ParseResumeResponse> {
  const form = new FormData();
  form.append('file', file);

  const res = await fetch(`${BASE_URL}/api/v1/parse-resume`, {
    method: 'POST',
    body: form,
  });

  return handleResponse<ParseResumeResponse>(res);
}

/**
 * Sends extracted resume text + JD text to the ATS scoring engine.
 */
export async function matchResume(
  resumeText: string,
  jobDescriptionText: string,
): Promise<ResumeMatchResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/match-resume`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description_text: jobDescriptionText,
    }),
  });

  return handleResponse<ResumeMatchResponse>(res);
}
