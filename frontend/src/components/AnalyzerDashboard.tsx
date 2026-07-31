import React from 'react';
import ScoreGauge from './ScoreGauge';
import ScoreBreakdown from './ScoreBreakdown';
import SkillChips from './SkillChips';
import SuggestionsList from './SuggestionsList';
import AnalysisReportPrint from './AnalysisReportPrint';
import type { ResumeMatchResponse, ParseResumeResponse } from '../services/api';

interface Props {
  matchData: ResumeMatchResponse;
  parseData: ParseResumeResponse;
  onReset: () => void;
}

const AnalyzerDashboard: React.FC<Props> = ({ matchData, parseData, onReset }) => {
  const handlePrint = () => {
    window.print();
  };

  return (
    <>
      <section className="py-12 px-6 max-w-6xl mx-auto space-y-8 animate-fade-in print:hidden">
        {/* Header bar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6">
          <div>
            <span className="text-xs text-brand-300 font-semibold uppercase tracking-wider">Analysis Complete</span>
            <h2 className="text-2xl font-bold text-white mt-1">
              {parseData.filename}
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
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

        {/* Top Grid: Score Gauge & Breakdown */}
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

        {/* Middle Grid: Skill Chips */}
        <SkillChips
          matchedSkills={matchData.matched_skills}
          missingSkills={matchData.missing_skills}
        />

        {/* Bottom Grid: Actionable Suggestions */}
        <SuggestionsList suggestions={matchData.improvement_suggestions} />

        {/* Parsed Sections Accordion/Preview */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Parsed Resume Sections</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(parseData.sections).map(([secName, secText]) => (
              <div key={secName} className="p-4 rounded-xl bg-slate-900/40 border border-slate-800">
                <span className="text-xs font-semibold uppercase text-brand-300 tracking-wider">
                  {secName}
                </span>
                <p className="text-xs text-slate-300 mt-2 whitespace-pre-line line-clamp-4">
                  {secText || <span className="text-slate-500 italic">No content detected</span>}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Hidden Report element visible only during window.print() */}
      <AnalysisReportPrint matchData={matchData} parseData={parseData} />
    </>
  );
};

export default AnalyzerDashboard;
