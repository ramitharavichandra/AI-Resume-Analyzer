import React from 'react';

interface Props {
  score: number;
  rating: string;
}

const ScoreGauge: React.FC<Props> = ({ score, rating }) => {
  const radius = 68;
  const strokeWidth = 12;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let colorClass = 'stroke-emerald-400 text-emerald-400';
  let bgGlow = 'rgba(52,211,153,0.15)';

  if (score < 65) {
    colorClass = 'stroke-amber-400 text-amber-400';
    bgGlow = 'rgba(251,191,36,0.15)';
  } else if (score < 80) {
    colorClass = 'stroke-brand-400 text-brand-400';
    bgGlow = 'rgba(129,140,248,0.15)';
  }

  return (
    <div className="flex flex-col items-center justify-center p-6 glass-card relative" style={{ background: bgGlow }}>
      <div className="relative w-44 h-44 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90">
          {/* Track */}
          <circle
            cx="88"
            cy="88"
            r={radius}
            strokeWidth={strokeWidth}
            className="stroke-slate-800"
            fill="transparent"
          />
          {/* Progress ring */}
          <circle
            cx="88"
            cy="88"
            r={radius}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className={`score-ring ${colorClass}`}
            fill="transparent"
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold text-white tracking-tight">{Math.round(score)}</span>
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">out of 100</span>
        </div>
      </div>

      <div className="mt-4 text-center">
        <span className="inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-white/10 text-white border border-white/10">
          {rating}
        </span>
      </div>
    </div>
  );
};

export default ScoreGauge;
