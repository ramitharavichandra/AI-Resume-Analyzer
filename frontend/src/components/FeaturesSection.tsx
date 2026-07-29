import React from 'react';

const features = [
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
    title: 'ATS Compatibility Score',
    description: 'Hybrid AI scoring using TF-IDF vectors, Cosine Similarity, and skill taxonomy matching.',
    color: 'from-brand-500 to-brand-700',
    glow: 'rgba(99,102,241,0.25)',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
      </svg>
    ),
    title: 'Skill Gap Analysis',
    description: 'Identifies missing technologies, frameworks, and domain skills from the job description.',
    color: 'from-emerald-500 to-teal-600',
    glow: 'rgba(52,211,153,0.2)',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
    title: 'Smart Suggestions',
    description: 'Receives tailored, actionable resume improvement suggestions powered by AI analysis.',
    color: 'from-violet-500 to-purple-700',
    glow: 'rgba(167,139,250,0.2)',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
      </svg>
    ),
    title: 'PDF Parsing Engine',
    description: 'Extracts and segments resume sections automatically: Skills, Experience, Education, Projects.',
    color: 'from-orange-500 to-amber-600',
    glow: 'rgba(251,146,60,0.2)',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    title: 'Instant Analysis',
    description: 'Results returned in under 3 seconds via FastAPI async microservices backend.',
    color: 'from-cyan-500 to-blue-600',
    glow: 'rgba(34,211,238,0.2)',
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
    title: 'Download Report',
    description: 'Export a complete PDF analysis report to share with mentors or track your improvement.',
    color: 'from-rose-500 to-pink-600',
    glow: 'rgba(244,63,94,0.2)',
  },
];

const FeaturesSection: React.FC = () => {
  return (
    <section id="features" className="py-24 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full glass border border-brand-500/30 text-brand-300 text-sm font-medium mb-5">
            Everything You Need
          </span>
          <h2 className="text-white font-bold mb-4" style={{ fontSize: 'clamp(1.8rem, 3vw, 2.8rem)' }}>
            AI-Powered Resume Intelligence
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Six powerful features designed to transform your resume from filtered-out to shortlisted.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map(({ icon, title, description, color, glow }) => (
            <div key={title} className="glass-card p-7 group" style={{ '--glow': glow } as React.CSSProperties}>
              {/* Icon */}
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center text-white mb-5 shadow-lg transition-transform duration-300 group-hover:scale-110`}
                   style={{ boxShadow: `0 8px 24px ${glow}` }}>
                {icon}
              </div>
              <h3 className="text-white font-semibold text-lg mb-2">{title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
