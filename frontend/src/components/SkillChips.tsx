import React from 'react';

interface Props {
  matchedSkills: string[];
  missingSkills: string[];
}

const SkillChips: React.FC<Props> = ({ matchedSkills, missingSkills }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Matched Skills */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-3 h-3 rounded-full bg-emerald-400" />
          <h4 className="text-base font-semibold text-white">
            Matched Skills ({matchedSkills.length})
          </h4>
        </div>

        {matchedSkills.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {matchedSkills.map((skill) => (
              <span
                key={skill}
                className="px-3 py-1 rounded-lg text-xs font-medium bg-emerald-500/10 border border-emerald-500/30 text-emerald-300"
              >
                ✓ {skill}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-500 italic">No matching skills found in taxonomy.</p>
        )}
      </div>

      {/* Missing Skills */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-3 h-3 rounded-full bg-red-400" />
          <h4 className="text-base font-semibold text-white">
            Missing Skills ({missingSkills.length})
          </h4>
        </div>

        {missingSkills.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((skill) => (
              <span
                key={skill}
                className="px-3 py-1 rounded-lg text-xs font-medium bg-red-500/10 border border-red-500/30 text-red-300"
              >
                + {skill}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-emerald-400 font-medium">All required skills are present!</p>
        )}
      </div>
    </div>
  );
};

export default SkillChips;
