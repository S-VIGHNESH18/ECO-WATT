import React from 'react';
import { motion } from 'motion/react';
import { ArrowRight, Leaf, Zap, BarChart3 } from 'lucide-react';

interface HeroLeftProps {
  onScrollToPredictor?: () => void;
}

export const HeroLeft: React.FC<HeroLeftProps> = ({ onScrollToPredictor }) => {
  return (
    <div className="flex flex-col justify-center py-6 lg:py-10">
      {/* Brand Tagline Badge */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.05 }}
        className="mb-4 inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-100 dark:border-emerald-800/60 text-[#009e52] dark:text-[#00e575] text-[12px] font-semibold tracking-wide w-fit transition-colors"
      >
        <span className="w-2 h-2 rounded-full bg-[#009e52] dark:bg-[#00e575] animate-pulse" />
        EcoWatt Energy Intelligence Platform
      </motion.div>

      {/* 1. Main Headline */}
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1, ease: "easeOut" }}
        className="font-['Space_Grotesk'] text-[30px] sm:text-[42px] md:text-[52px] lg:text-[54px] leading-[1.1] font-bold tracking-tight text-slate-900 dark:text-white transition-colors"
      >
        Predict energy today. <br />
        Sustain <span className="text-[#009e52] dark:text-[#00e575]">tomorrow.</span>
      </motion.h1>

      {/* 2. Subtitle / Body text strictly focused on EcoWatt */}
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
        className="mt-6 text-base md:text-[17px] leading-relaxed text-slate-600 dark:text-slate-300 max-w-xl transition-colors"
      >
        Physics-informed machine learning for smart energy prediction, real-time tariff cost calculation, and intelligent carbon footprint reduction.
      </motion.p>

      {/* 3. CTAs Area */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3, ease: "easeOut" }}
        className="mt-8 flex flex-wrap items-center gap-4"
      >
        <motion.button
          onClick={onScrollToPredictor}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="group inline-flex items-center gap-3 px-7 py-3.5 rounded-full bg-[#1d6b38] hover:bg-[#144b27] dark:bg-[#009e52] dark:hover:bg-[#008947] text-white text-[15px] font-semibold tracking-wide shadow-md shadow-emerald-900/15 transition-all duration-200 cursor-pointer"
        >
          <span>Simulate Energy Usage</span>
          <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
        </motion.button>

        <motion.a
          href="#analytics"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full bg-white dark:bg-[#0f1713] border border-[#009e52]/45 dark:border-emerald-500/40 hover:border-[#009e52] hover:bg-emerald-50/40 dark:hover:bg-emerald-950/40 text-slate-800 dark:text-slate-200 text-[15px] font-semibold transition-all duration-200"
        >
          <BarChart3 className="w-4 h-4 text-[#009e52] dark:text-[#00e575] transition-transform duration-200 group-hover:scale-110" />
          <span>View Analytics</span>
        </motion.a>
      </motion.div>

      {/* 4. Bottom Feature Grid: EcoWatt's Real Feature Highlights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
        className="mt-14 pt-8 border-t border-slate-100 dark:border-slate-800/80 transition-colors"
      >
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 lg:gap-8 items-start relative">
          {/* Feature 1: Physics-Informed ML */}
          <div className="flex flex-col gap-3 group relative sm:pr-4">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-100/80 dark:border-emerald-800/60 flex items-center justify-center text-[#009e52] dark:text-[#00e575] transition-all duration-200 group-hover:scale-110 group-hover:bg-[#009e52] group-hover:text-white shadow-xs">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-['Space_Grotesk'] text-[16px] font-bold leading-tight text-slate-900 dark:text-white group-hover:text-[#009e52] dark:group-hover:text-[#00e575] transition-colors">
                Physics-Informed ML
              </h4>
              <p className="mt-1 text-[13px] leading-relaxed text-slate-500 dark:text-slate-400">
                Calculates base load E<sub>load</sub> with ambient residual modeling.
              </p>
            </div>
          </div>

          {/* Feature 2: Tariff & Cost Analytics */}
          <div className="flex flex-col gap-3 group relative sm:px-4 sm:border-l sm:border-slate-100 dark:sm:border-slate-800/80">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-100/80 dark:border-emerald-800/60 flex items-center justify-center text-[#009e52] dark:text-[#00e575] transition-all duration-200 group-hover:scale-110 group-hover:bg-[#009e52] group-hover:text-white shadow-xs">
              <Leaf className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-['Space_Grotesk'] text-[16px] font-bold leading-tight text-slate-900 dark:text-white group-hover:text-[#009e52] dark:group-hover:text-[#00e575] transition-colors">
                Tariff & CO₂ Impact
              </h4>
              <p className="mt-1 text-[13px] leading-relaxed text-slate-500 dark:text-slate-400">
                Instant ₹8.4/kWh billing calculation &amp; carbon footprint audit.
              </p>
            </div>
          </div>

          {/* Feature 3: Eco Score & Peak Optimization */}
          <div className="flex flex-col gap-3 group relative sm:pl-4 sm:border-l sm:border-slate-100 dark:sm:border-slate-800/80">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-100/80 dark:border-emerald-800/60 flex items-center justify-center text-[#009e52] dark:text-[#00e575] transition-all duration-200 group-hover:scale-110 group-hover:bg-[#009e52] group-hover:text-white shadow-xs">
              <BarChart3 className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-['Space_Grotesk'] text-[16px] font-bold leading-tight text-slate-900 dark:text-white group-hover:text-[#009e52] dark:group-hover:text-[#00e575] transition-colors">
                Eco Score &amp; Savings
              </h4>
              <p className="mt-1 text-[13px] leading-relaxed text-slate-500 dark:text-slate-400">
                Automated peak-hour detection and energy efficiency scoring.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
