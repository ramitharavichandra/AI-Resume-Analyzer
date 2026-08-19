import React, { useState } from 'react';
import ScoreGauge from './ScoreGauge';
import ScoreBreakdown from './ScoreBreakdown';
import SkillChips from './SkillChips';
import SuggestionsList from './SuggestionsList';
import AnalysisReportPrint from './AnalysisReportPrint';
import type { ResumeMatchResponse, ParseResumeResponse } from '../services/api';

interface Props {
  matchData: ResumeMatchResponse;
  parseData: ParseResumeResponse;
  jobDescription: string;
  onReMatch: (newJd: string) => void;
  onReset: () => void;
  isLoading: boolean;
  error?: string | null;
}

const AnalyzerDashboard: React.FC<Props> = ({
  matchData,
  parseData,
  jobDescription,
  onReMatch,
  onReset,
  isLoading,
  error,
}) => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'skills' | 'sections' | 'editor'>('dashboard');
  const [editedJd, setEditedJd] = useState(jobDescription);

  const handlePrint = () => {
    window.print();
  };

  const handleUpdateMatch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!editedJd.trim()) {
      alert('Job Description cannot be empty.');
      return;
    }
    onReMatch(editedJd);
  };

  // Determine engine badge styles
  const isGemini = matchData.engine?.includes('Gemini') || parseData.engine?.includes('Gemini');
  const engineText = isGemini ? 'Gemini AI Semantic Engine' : 'Local Heuristics Fallback';

  return (
    <>
      <section className="py-12 px-6 max-w-6xl mx-auto space-y-8 animate-fade-in print:hidden">
        {/* Header bar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 glass-card p-6">
          <div>
            <div className="flex items-center gap-3">
              <span className="text-xs text-brand-300 font-semibold uppercase tracking-wider">Analysis Complete</span>
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold tracking-wide border uppercase ${
                isGemini 
                  ? 'bg-brand-500/10 text-brand-400 border-brand-500/30' 
                  : 'bg-slate-500/10 text-slate-400 border-slate-700'
              }`}>
                {isGemini ? '⚡' : '⚙️'} {engineText}
              </span>
            </div>
            <h2 className="text-2xl font-bold text-white mt-1.5">
              {parseData.filename}
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              {parseData.page_count} Page(s) • {parseData.statistics.word_count} Words • {parseData.statistics.character_count} Characters
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handlePrint}
              className="btn-brand px-5 py-2.5 text-sm flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Export Report PDF
            </button>

            <button
              onClick={onReset}
              className="px-5 py-2.5 rounded-xl glass border border-white/10 text-sm font-semibold text-slate-200 hover:text-white hover:border-brand-500/50 transition-all flex items-center justify-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Analyze Another
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-6 py-3.5 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'dashboard'
                ? 'border-brand-500 text-brand-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Overview & Breakdown
          </button>
          <button
            onClick={() => setActiveTab('skills')}
            className={`px-6 py-3.5 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'skills'
                ? 'border-brand-500 text-brand-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Skill Gap Matrix
          </button>
          <button
            onClick={() => setActiveTab('sections')}
            className={`px-6 py-3.5 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'sections'
                ? 'border-brand-500 text-brand-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Extracted Resume
          </button>
          <button
            onClick={() => setActiveTab('editor')}
            className={`px-6 py-3.5 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'editor'
                ? 'border-brand-500 text-brand-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Interactive Review (Editor)
          </button>
        </div>

        {/* Tab Contents */}
        <div className="space-y-8">
          {activeTab === 'dashboard' && (
            <>
              {/* Score Gauge & Breakdown */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="md:col-span-1">
                  <ScoreGauge score={matchData.ats_score} rating={matchData.rating} />
                </div>
                <div className="md:col-span-2">
                  <ScoreBreakdown
                    skillMatchScore={matchData.skill_match_score}
                    vectorSimilarityScore={matchData.vector_similarity_score}
                    sectionCompletenessScore={matchData.section_completeness_score}
                  />
                </div>
              </div>

              {/* Actionable Suggestions */}
              <SuggestionsList suggestions={matchData.improvement_suggestions} />
            </>
          )}

          {activeTab === 'skills' && (
            <SkillChips
              matchedSkills={matchData.matched_skills}
              missingSkills={matchData.missing_skills}
            />
          )}

          {activeTab === 'sections' && (
            <div className="glass-card p-6 space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-white">Segmented Resume View</h3>
                <p className="text-xs text-slate-400">Reviewing parsed content across standard resume components</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {Object.entries(parseData.sections).map(([secName, secText]) => (
                  <div key={secName} className="p-5 rounded-xl bg-slate-900/40 border border-slate-800 flex flex-col justify-between">
                    <div>
                      <span className="text-[10px] font-bold uppercase text-brand-300 tracking-wider">
                        {secName}
                      </span>
                      <p className="text-xs text-slate-300 mt-3 whitespace-pre-line leading-relaxed max-h-72 overflow-y-auto custom-scrollbar">
                        {secText || <span className="text-slate-600 italic">No content detected in this section</span>}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'editor' && (
            <div className="glass-card p-8">
              <div>
                <h3 className="text-lg font-semibold text-white">Interactive Job Description Review</h3>
                <p className="text-xs text-slate-400">Update the Job Description and re-evaluate ATS compatibility immediately without re-uploading the resume file.</p>
              </div>

              {error && (
                <div className="my-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm flex items-center gap-3">
                  <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{error}</span>
                </div>
              )}

              <form onSubmit={handleUpdateMatch} className="mt-6 space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-3">
                    Target Job Description Text
                  </label>
                  <textarea
                    value={editedJd}
                    onChange={(e) => setEditedJd(e.target.value)}
                    placeholder="Paste the target job description here..."
                    rows={12}
                    className="w-full rounded-2xl bg-slate-900/60 border border-slate-700/80 p-4 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all resize-none font-sans"
                  />
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    type="submit"
                    disabled={isLoading || !editedJd.trim()}
                    className="btn-brand px-10 py-4 text-base font-semibold w-full md:w-auto disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none"
                  >
                    {isLoading ? (
                      <span className="flex items-center gap-3">
                        <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Recalculating Score...
                      </span>
                    ) : (
                      <span className="flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Update Match Analysis
                      </span>
                    )}
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </section>

      {/* Hidden Report element visible only during window.print() */}
      <AnalysisReportPrint matchData={matchData} parseData={parseData} />
    </>
  );
};

export default AnalyzerDashboard;
