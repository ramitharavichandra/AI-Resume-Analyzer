import { useState } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import FeaturesSection from './components/FeaturesSection';
import ResumeUploader from './components/ResumeUploader';
import AnalyzerDashboard from './components/AnalyzerDashboard';
import Footer from './components/Footer';
import { parsePdfResume, matchResume, type ParseResumeResponse, type ResumeMatchResponse } from './services/api';
import './index.css';

function App() {
  const [isDark, setIsDark] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [parseData, setParseData] = useState<ParseResumeResponse | null>(null);
  const [matchData, setMatchData] = useState<ResumeMatchResponse | null>(null);

  const toggleTheme = () => {
    setIsDark((prev) => !prev);
    document.documentElement.classList.toggle('dark');
  };

  const handleAnalyze = async (file: File, jobDescription: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // Step 1: Parse PDF File
      const parsed = await parsePdfResume(file);
      setParseData(parsed);

      // Step 2: Calculate ATS Match Metrics
      const matched = await matchResume(parsed.raw_text, jobDescription);
      setMatchData(matched);
    } catch (err: any) {
      console.error('Analysis error:', err);
      setError(err.message || 'Failed to analyze resume. Please ensure the backend API is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setParseData(null);
    setMatchData(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-surface-950 text-white font-sans">
      <Navbar isDark={isDark} onToggle={toggleTheme} />
      <main>
        {!parseData || !matchData ? (
          <>
            <HeroSection />
            <ResumeUploader onAnalyze={handleAnalyze} isLoading={isLoading} error={error} />
            <FeaturesSection />
          </>
        ) : (
          <div className="pt-24 pb-16">
            <AnalyzerDashboard matchData={matchData} parseData={parseData} onReset={handleReset} />
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default App;
