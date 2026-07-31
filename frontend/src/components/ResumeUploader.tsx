import React, { useState, useRef } from 'react';

interface Props {
  onAnalyze: (file: File, jobDescription: string) => void;
  isLoading: boolean;
  error?: string | null;
}

const ResumeUploader: React.FC<Props> = ({ onAnalyze, isLoading, error }) => {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isDragOver, setIsDragOver] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (selected.type === 'application/pdf' || selected.name.endsWith('.pdf')) {
        setFile(selected);
      } else {
        alert('Please upload a valid PDF document (.pdf).');
      }
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const dropped = e.dataTransfer.files[0];
      if (dropped.type === 'application/pdf' || dropped.name.endsWith('.pdf')) {
        setFile(dropped);
      } else {
        alert('Please upload a valid PDF document (.pdf).');
      }
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      alert('Please select or drop a PDF resume file.');
      return;
    }
    if (!jobDescription.trim()) {
      alert('Please enter or paste the target Job Description.');
      return;
    }
    onAnalyze(file, jobDescription);
  };

  return (
    <section id="analyze" className="py-16 px-6 max-w-5xl mx-auto">
      <div className="glass-card p-8 md:p-12 relative overflow-hidden">
        {/* Glow effect */}
        <div className="absolute -top-24 -right-24 w-72 h-72 bg-brand-500/20 rounded-full blur-3xl pointer-events-none" />

        <div className="mb-8 text-center md:text-left">
          <span className="inline-block px-4 py-1.5 rounded-full glass border border-brand-500/30 text-brand-300 text-sm font-medium mb-3">
            Interactive Analyzer
          </span>
          <h2 className="text-3xl font-bold text-white mb-2">Analyze Your Resume</h2>
          <p className="text-slate-400 text-base">
            Upload your resume PDF and paste the target Job Description to get instant ATS scoring and feedback.
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm flex items-center gap-3">
            <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Drag & Drop File Upload */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-3 flex items-center justify-between">
                <span>1. Upload Resume (PDF)</span>
                {file && <span className="text-xs text-brand-300 font-normal">{(file.size / 1024).toFixed(1)} KB</span>}
              </label>

              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center min-h-[220px] ${
                  isDragOver
                    ? 'border-brand-400 bg-brand-500/10'
                    : file
                    ? 'border-emerald-500/50 bg-emerald-500/5'
                    : 'border-slate-700 hover:border-brand-500/50 bg-slate-900/40'
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                  className="hidden"
                />

                {file ? (
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center mb-3">
                      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <p className="text-white font-medium text-sm max-w-[200px] truncate mb-1">{file.name}</p>
                    <p className="text-xs text-emerald-400">PDF Loaded • Click to change</p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-12 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center mb-3">
                      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 0115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    <p className="text-slate-200 font-medium text-sm mb-1">
                      Drag & Drop your resume PDF here
                    </p>
                    <p className="text-slate-500 text-xs">or click to browse from device</p>
                  </div>
                )}
              </div>
            </div>

            {/* Job Description Input */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-3">
                2. Target Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the target job description here (e.g. requirements, responsibilities, tech stack)..."
                rows={8}
                className="w-full rounded-2xl bg-slate-900/60 border border-slate-700/80 p-4 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all resize-none font-sans"
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={isLoading || !file || !jobDescription.trim()}
              className="btn-brand px-10 py-4 text-base font-semibold w-full md:w-auto disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none"
            >
              {isLoading ? (
                <span className="flex items-center gap-3">
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing Vectors & Skills...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Calculate ATS Score
                </span>
              )}
            </button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default ResumeUploader;
