import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  Zap, ArrowRight, ChevronDown, Menu, X, Cpu, 
  LineChart, Database, CloudSun, History, Sun, Moon 
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

interface HeaderProps {
  onScrollToPredictor?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onScrollToPredictor }) => {
  const { theme, toggleTheme } = useTheme();
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const modelItems = [
    { title: 'Physics-Informed SGD Logarithmic Model', desc: 'Separates equipment load (E_load) and models ambient residuals with SGDRegressor.', icon: Zap },
    { title: 'Random Forest Forecaster', desc: 'Lagged multi-step time-series regression for future horizons.', icon: Cpu },
    { title: 'Logarithmic Regression Pipeline', desc: 'Log-transformed residual estimation for power spikes.', icon: LineChart }
  ];

  return (
    <header className="w-full bg-white/90 dark:bg-[#0a0f0d]/90 backdrop-blur-md sticky top-0 z-50 border-b border-slate-100 dark:border-slate-800/80 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-6 md:px-12 h-20 flex items-center justify-between">
        {/* Left: Brand */}
        <a href="#" className="flex items-center gap-3 group focus:outline-none focus:ring-2 focus:ring-[#009e52] rounded-lg">
          <motion.div 
            whileHover={{ scale: 1.1, rotate: 6 }}
            transition={{ type: "spring", stiffness: 350, damping: 15 }}
            className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-100 dark:border-emerald-800/60 flex items-center justify-center text-[#009e52] dark:text-[#00e575] shadow-xs"
          >
            <Zap className="w-5 h-5 fill-current" />
          </motion.div>
          <div className="flex flex-col">
            <span className="font-['Space_Grotesk'] text-[21px] font-bold tracking-tight text-slate-900 dark:text-white group-hover:text-[#009e52] dark:group-hover:text-[#00e575] transition-colors flex items-center gap-1.5">
              EcoWatt
            </span>
            <span className="font-['Space_Grotesk'] text-[10px] font-bold tracking-wider uppercase text-[#009e52] dark:text-[#00e575]">
              Predict • Save • Sustain
            </span>
          </div>
        </a>

        {/* Center: Desktop Navigation */}
        <nav className="hidden lg:flex items-center gap-8" aria-label="Main Navigation">
          <button 
            onClick={onScrollToPredictor}
            className="text-[15px] font-medium text-slate-600 dark:text-slate-300 hover:text-[#009e52] dark:hover:text-[#00e575] transition-colors cursor-pointer"
          >
            Energy Predictor
          </button>

          {/* ML Models Dropdown */}
          <div 
            className="relative"
            onMouseEnter={() => setActiveDropdown('models')}
            onMouseLeave={() => setActiveDropdown(null)}
          >
            <button 
              className="flex items-center gap-1.5 text-[15px] font-medium text-slate-600 dark:text-slate-300 hover:text-[#009e52] dark:hover:text-[#00e575] transition-colors py-2 focus:outline-none cursor-pointer"
              aria-expanded={activeDropdown === 'models'}
            >
              ML Models
              <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${activeDropdown === 'models' ? 'rotate-180 text-[#009e52] dark:text-[#00e575]' : ''}`} />
            </button>
            <AnimatePresence>
              {activeDropdown === 'models' && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  transition={{ duration: 0.18, ease: "easeOut" }}
                  className="absolute top-full left-0 w-88 bg-white dark:bg-[#0f1713] rounded-2xl shadow-xl shadow-slate-200/50 dark:shadow-black/60 border border-slate-100 dark:border-slate-800 p-3 z-50"
                >
                  {modelItems.map((item, idx) => (
                    <div 
                      key={idx} 
                      className="flex items-start gap-3.5 p-3 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800/60 transition-colors group cursor-pointer"
                      onClick={onScrollToPredictor}
                    >
                      <div className="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/60 text-[#009e52] dark:text-[#00e575] group-hover:bg-[#009e52] group-hover:text-white transition-colors">
                        <item.icon className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="font-['Space_Grotesk'] text-[14px] font-bold text-slate-900 dark:text-white group-hover:text-[#009e52] dark:group-hover:text-[#00e575] transition-colors">{item.title}</p>
                        <p className="text-[12px] text-slate-500 dark:text-slate-400 leading-snug">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <a 
            href="#weather" 
            className="flex items-center gap-1.5 text-[15px] font-medium text-slate-600 dark:text-slate-300 hover:text-[#009e52] dark:hover:text-[#00e575] transition-colors"
          >
            <CloudSun className="w-4 h-4" />
            Live Weather
          </a>

          <a 
            href="#analytics" 
            className="flex items-center gap-1.5 text-[15px] font-medium text-slate-600 dark:text-slate-300 hover:text-[#009e52] dark:hover:text-[#00e575] transition-colors"
          >
            <Database className="w-4 h-4" />
            Analytics
          </a>

          <a 
            href="#history" 
            className="flex items-center gap-1.5 text-[15px] font-medium text-slate-600 dark:text-slate-300 hover:text-[#009e52] dark:hover:text-[#00e575] transition-colors"
          >
            <History className="w-4 h-4" />
            History
          </a>
        </nav>

        {/* Right: Theme Toggle, CTA Button & Mobile Toggle */}
        <div className="flex items-center gap-3">
          {/* Dark / Light Theme Toggle Button */}
          <button
            onClick={toggleTheme}
            className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-colors cursor-pointer flex items-center justify-center"
            aria-label={theme === 'dark' ? "Switch to light mode" : "Switch to dark mode"}
            title={theme === 'dark' ? "Switch to light mode" : "Switch to dark mode"}
          >
            {theme === 'dark' ? (
              <Sun className="w-4 h-4 text-amber-400 fill-amber-400/20" />
            ) : (
              <Moon className="w-4 h-4 text-slate-700" />
            )}
          </button>

          <motion.button 
            onClick={onScrollToPredictor}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="group hidden sm:inline-flex items-center gap-2.5 px-5 py-2.5 rounded-full bg-[#1d6b38] hover:bg-[#144b27] dark:bg-[#009e52] dark:hover:bg-[#008947] text-white text-[14px] font-semibold tracking-wide transition-all shadow-sm hover:shadow-emerald-900/20 cursor-pointer"
          >
            <span>Simulate Now</span>
            <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
          </motion.button>

          {/* Mobile hamburger button */}
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none"
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden bg-white dark:bg-[#0a0f0d] border-b border-slate-200 dark:border-slate-800 px-6 py-4 flex flex-col gap-3 transition-colors"
          >
            <div className="flex items-center justify-between py-2 border-b border-slate-100 dark:border-slate-800">
              <span className="text-[14px] font-medium text-slate-700 dark:text-slate-300">Theme Mode</span>
              <button
                onClick={toggleTheme}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-[13px] font-semibold text-slate-800 dark:text-slate-200 cursor-pointer"
              >
                {theme === 'dark' ? (
                  <>
                    <Sun className="w-4 h-4 text-amber-400" />
                    <span>Light Mode</span>
                  </>
                ) : (
                  <>
                    <Moon className="w-4 h-4 text-slate-700" />
                    <span>Dark Mode</span>
                  </>
                )}
              </button>
            </div>

            <button onClick={() => { setMobileMenuOpen(false); onScrollToPredictor?.(); }} className="text-left text-[16px] font-semibold text-slate-800 dark:text-slate-200 py-2 border-b border-slate-100 dark:border-slate-800">Energy Predictor</button>
            <a href="#weather" onClick={() => setMobileMenuOpen(false)} className="text-[16px] font-semibold text-slate-800 dark:text-slate-200 py-2 border-b border-slate-100 dark:border-slate-800">Live Weather</a>
            <a href="#analytics" onClick={() => setMobileMenuOpen(false)} className="text-[16px] font-semibold text-slate-800 dark:text-slate-200 py-2 border-b border-slate-100 dark:border-slate-800">Analytics</a>
            <a href="#history" onClick={() => setMobileMenuOpen(false)} className="text-[16px] font-semibold text-slate-800 dark:text-slate-200 py-2 border-b border-slate-100 dark:border-slate-800">History</a>
            <button 
              onClick={() => { setMobileMenuOpen(false); onScrollToPredictor?.(); }}
              className="inline-flex items-center justify-center gap-2 mt-2 px-5 py-3 rounded-xl bg-[#1d6b38] dark:bg-[#009e52] text-white text-[15px] font-semibold cursor-pointer"
            >
              <span>Simulate Now</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};

