import React from 'react';

interface Props {
  skillMatchScore: number;
  vectorSimilarityScore: number;
  sectionCompletenessScore: number;
}

const ScoreBreakdown: React.FC<Props> = ({
  skillMatchScore,
  vectorSimilarityScore,
  sectionCompletenessScore,
}) => {
  const metrics = [
    {
      label: 'Skill Gap Match (45% weight)',
      score: skillMatchScore,
      color: 'bg-emerald-400',
      description: 'Explicit overlap of required tech stack skills',
    },
    {
      label: 'Vector Cosine Similarity (35% weight)',
      score: vectorSimilarityScore,
      color: 'bg-brand-400',
      description: 'Semantic contextual alignment between experience and JD',
    },
    {
      label: 'Section Completeness (20% weight)',
      score: sectionCompletenessScore,
      color: 'bg-purple-400',
      description: 'Presence of critical resume structural sections',
    },
  ];

  return (
    <div className="glass-card p-6 flex flex-col justify-center space-y-6">
      <h3 className="text-lg font-semibold text-white mb-2">Score Components Breakdown</h3>

      {metrics.map(({ label, score, color, description }) => (
        <div key={label} className="space-y-2">
          <div className="flex justify-between items-center text-sm">
            <span className="font-medium text-slate-200">{label}</span>
            <span className="font-bold text-white">{Math.round(score)}%</span>
          </div>

          <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-1000 ${color}`}
              style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
            />
          </div>

          <p className="text-xs text-slate-400">{description}</p>
        </div>
      ))}
    </div>
  );
};

export default ScoreBreakdown;
