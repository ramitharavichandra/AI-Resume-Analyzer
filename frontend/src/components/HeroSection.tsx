import React from 'react';

const HeroSection: React.FC = () => {
  return (
    <section
      id="hero"
      className="relative min-h-screen flex flex-col items-center justify-center px-6 pt-24 pb-16 overflow-hidden"
    >
      {/* Radial glow background */}
      <div className="hero-glow absolute inset-0 pointer-events-none" />

      {/* Animated background grid */}
      <div
        className="absolute inset-0 pointer-events-none opacity-10"
        style={{
          backgroundImage: `linear-gradient(rgba(99,102,241,0.4) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(99,102,241,0.4) 1px, transparent 1px)`,
          backgroundSize: '60px 60px',
        }}
      />

      {/* Badge */}
      <div className="animate-fade-in mb-6">
        <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass border border-brand-500/30 text-brand-300 text-sm font-medium">
          <span className="w-2 h-2 rounded-full bg-accent-400 animate-pulse-slow" />
          AI-Powered • NLP • Vector Similarity
        </span>
      </div>

      {/* Heading */}
      <h1
        className="animate-slide-up text-center font-bold leading-tight mb-6"
        style={{ fontSize: 'clamp(2.4rem, 5vw, 4rem)', animationDelay: '0.1s' }}
      >
        <span className="text-white">Beat the ATS.</span>
        <br />
        <span
          style={{
            background: 'linear-gradient(135deg, #818cf8, #6366f1, #34d399)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}
        >
          Land Your Dream Job.
        </span>
      </h1>

      {/* Subheading */}
      <p
        className="animate-slide-up text-center text-slate-400 max-w-2xl text-lg leading-relaxed mb-10"
        style={{ animationDelay: '0.2s' }}
      >
        Upload your resume and a job description. Our AI analyzes skill gaps,
        calculates your ATS compatibility score, and gives you{' '}
        <span className="text-brand-300 font-medium">targeted suggestions</span> to get shortlisted.
      </p>

      {/* CTA Buttons */}
      <div
        className="animate-slide-up flex flex-col sm:flex-row gap-4"
        style={{ animationDelay: '0.3s' }}
      >
        <a href="#analyze" className="btn-brand text-base px-8 py-3.5">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Upload Resume
        </a>
        <a
          href="#how-it-works"
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl glass border border-white/10 text-slate-300 font-semibold text-base hover:border-brand-500/40 hover:text-white transition-all duration-200"
        >
          See How It Works
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </a>
      </div>

      {/* Stats Row */}
      <div
        className="animate-slide-up mt-16 grid grid-cols-3 gap-6 w-full max-w-xl"
        style={{ animationDelay: '0.4s' }}
      >
        {[
          { value: '95%', label: 'ATS Accuracy' },
          { value: '50+', label: 'Skill Categories' },
          { value: '3s', label: 'Analysis Speed' },
        ].map(({ value, label }) => (
          <div key={label} className="glass-card p-5 text-center">
            <p className="text-2xl font-bold text-brand-400 mb-1">{value}</p>
            <p className="text-slate-400 text-sm">{label}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default HeroSection;
