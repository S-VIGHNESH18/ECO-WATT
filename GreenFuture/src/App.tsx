import React, { useRef } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { Header } from './components/Header';
import { HeroLeft } from './components/HeroLeft';
import { HeroRight } from './components/HeroRight';
import { EcoWattSimulator } from './components/EcoWattSimulator';
import { Zap } from 'lucide-react';

const AppContent: React.FC = () => {
  const simulatorRef = useRef<HTMLDivElement>(null);

  const scrollToPredictor = () => {
    simulatorRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-white dark:bg-[#080d0a] text-slate-900 dark:text-slate-100 selection:bg-emerald-100 dark:selection:bg-emerald-950 selection:text-emerald-900 dark:selection:text-emerald-300 relative overflow-x-hidden transition-colors duration-200">
      {/* Top Navigation Header strictly for EcoWatt with Dark Theme Toggle */}
      <Header onScrollToPredictor={scrollToPredictor} />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-6 md:px-12 pt-6 pb-16 lg:py-16">
        {/* Hero Section: Retains the exact video background theme & ambient glows */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          {/* Left Column: EcoWatt's Real Content & Features */}
          <div className="lg:col-span-6 xl:col-span-6 order-2 lg:order-1">
            <HeroLeft onScrollToPredictor={scrollToPredictor} />
          </div>

          {/* Right Column: High-Definition Blended Video & Ambient Glowing Theme */}
          <div className="lg:col-span-6 xl:col-span-6 order-1 lg:order-2">
            <HeroRight />
          </div>
        </section>

        {/* EcoWatt Interactive Energy Simulator (Complete Streamlit features same-to-same) */}
        <div ref={simulatorRef}>
          <EcoWattSimulator />
        </div>
      </main>

      {/* Clean EcoWatt Footer */}
      <footer className="border-t border-slate-100 dark:border-slate-800/80 py-8 bg-slate-50/50 dark:bg-slate-950/60 transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-6 md:px-12 flex flex-col sm:flex-row items-center justify-between gap-4 text-[13px] text-slate-500 dark:text-slate-400">
          <div className="flex items-center gap-2 font-['Space_Grotesk'] font-bold text-slate-800 dark:text-slate-200">
            <div className="w-6 h-6 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800/60 flex items-center justify-center text-[#009e52] dark:text-[#00e575]">
              <Zap className="w-3.5 h-3.5 fill-current" />
            </div>
            <span>EcoWatt Energy Intelligence</span>
            <span className="font-normal text-slate-400 dark:text-slate-500">| Predict • Save • Sustain</span>
          </div>

          <div className="flex items-center gap-1">
            <span>Powered by Physics-Informed ML</span>
            <span>•</span>
            <span>EcoWatt_6000 Benchmark</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
};

export default App;

