import React from 'react';
import { motion } from 'motion/react';
import { Zap, Sparkles } from 'lucide-react';

export const HeroRight: React.FC = () => {
  const videoUrl = "https://strvid.nyc3.cdn.digitaloceanspaces.com/motionsite/hero_green_energy.mp4";

  return (
    <div className="relative w-full flex items-center justify-center py-4 lg:py-6">
      {/* Ambient Pulsing Background Glows */}
      {/* Primary Emerald Glow: -z-10 */}
      <div 
        className="absolute -top-6 -right-6 w-80 sm:w-96 md:w-[460px] h-80 sm:h-96 md:h-[460px] rounded-full bg-emerald-400/20 blur-3xl pointer-events-none -z-10 animate-pulse"
        style={{ animationDuration: '6s' }}
      />
      
      {/* Secondary Cyan/Blue Spherical Accent: -z-20 */}
      <div 
        className="absolute -bottom-8 -left-8 w-72 sm:w-88 md:w-[420px] h-72 sm:h-88 md:h-[420px] rounded-full bg-blue-300/20 blur-3xl pointer-events-none -z-20"
      />

      {/* Main Video Wrapper with Framer Motion Entrance */}
      <motion.div
        initial={{ opacity: 0, scale: 0.96 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.25, ease: "easeOut" }}
        className="relative w-full h-[380px] sm:h-[480px] md:h-[540px] lg:h-[600px] rounded-3xl overflow-hidden shadow-2xl shadow-emerald-950/10 ring-1 ring-slate-900/5 dark:ring-slate-800/80 bg-slate-50/50 dark:bg-slate-900/80 group transition-colors"
      >
        {/* Blended High-Impact Background Video */}
        <video
          autoPlay
          loop
          muted
          playsInline
          className="w-full h-full object-cover mix-blend-multiply dark:mix-blend-normal dark:opacity-90 contrast-[1.06] brightness-[1.03] transition-transform duration-700 ease-out group-hover:scale-105"
        >
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support HTML5 video streaming.
        </video>

        {/* Ambient Gradient Overlay for seamless edge integration */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/20 dark:from-[#080d0a]/80 via-transparent to-transparent pointer-events-none" />

        {/* Floating Live Metric Pill (Micro-Interaction) strictly for EcoWatt */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="absolute bottom-6 left-6 right-6 sm:right-auto sm:max-w-xs bg-white/90 dark:bg-[#0f1713]/90 backdrop-blur-md rounded-2xl p-4 border border-white/60 dark:border-slate-800/80 shadow-lg shadow-emerald-950/10 flex items-center gap-3.5 transition-colors"
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-500/15 dark:bg-emerald-500/20 flex items-center justify-center text-[#009e52] dark:text-[#00e575] shrink-0">
            <Zap className="w-5 h-5 fill-current" />
          </div>
          <div className="flex flex-col">
            <span className="font-['Space_Grotesk'] text-[13px] font-bold text-slate-900 dark:text-white leading-tight flex items-center gap-1">
              EcoWatt Intelligence Core <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            </span>
            <span className="text-[11px] text-emerald-700 dark:text-emerald-400 font-medium mt-0.5">
              Physics Load + Ambient Residuals
            </span>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};
