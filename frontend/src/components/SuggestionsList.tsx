import React from 'react';

interface Props {
  suggestions: string[];
}

const SuggestionsList: React.FC<Props> = ({ suggestions }) => {
  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-8 h-8 rounded-lg bg-brand-500/20 text-brand-400 flex items-center justify-center">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 01-2 2h-4a2 2 0 01-2-2v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
            />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-white">Actionable Resume Improvements</h3>
          <p className="text-xs text-slate-400">AI-generated recommendations to boost your ATS ranking</p>
        </div>
      </div>

      {suggestions.length > 0 ? (
        <ul className="space-y-4">
          {suggestions.map((suggestion, index) => (
            <li key={index} className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-900/40 border border-slate-800">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-500/20 text-brand-300 text-xs font-bold flex items-center justify-center mt-0.5">
                {index + 1}
              </span>
              <p className="text-sm text-slate-200 leading-relaxed">{suggestion}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-slate-400">Your resume is well-optimized for this position!</p>
      )}
    </div>
  );
};

export default SuggestionsList;
