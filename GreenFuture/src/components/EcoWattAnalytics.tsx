import { BarChart3, Award, CheckCircle2 } from 'lucide-react';

export const EcoWattAnalytics: React.FC = () => {
  // Appliance distribution data from EcoWatt specification
  const appliances = [
    { name: "Air Conditioner", percent: 40, color: "bg-blue-500" },
    { name: "Refrigerator", percent: 20, color: "bg-emerald-500" },
    { name: "Ceiling Fans", percent: 15, color: "bg-teal-500" },
    { name: "Lighting", percent: 15, color: "bg-amber-500" },
    { name: "Television", percent: 10, color: "bg-purple-500" },
  ];

  // Model benchmarking metrics from EcoWatt specification
  const modelMetrics = [
    { model: "Logarithmic Regression (SGD Pipeline)", mae: 1.38, mse: 3.12, rmse: 1.76, r2: 0.951, mape: 3.98, best: false },
    { model: "Random Forest Regressor (Lagged)", mae: 1.12, mse: 2.10, rmse: 1.45, r2: 0.968, mape: 3.45, best: true },
  ];

  // Sample consumption trend line (first 20 sample points from EcoWatt_6000.csv)
  const sampleTrend = [
    4.39, 4.06, 1.25, 28.92, 17.69, 20.59, 1.49, 3.08, 4.34, 9.18,
    4.79, 7.29, 7.77, 7.39, 4.10, 6.96, 2.87, 2.16, 31.72, 12.45
  ];
  const maxVal = Math.max(...sampleTrend);

  return (
    <section id="analytics" className="py-12 border-t border-slate-100 dark:border-slate-800">
      <div className="mb-10">
        <span className="font-['Space_Grotesk'] text-[11px] font-bold uppercase tracking-wider text-[#009e52] dark:text-emerald-400">
          Analytics & Benchmarks
        </span>
        <h2 className="font-['Space_Grotesk'] text-[28px] sm:text-[36px] font-bold text-slate-900 dark:text-white tracking-tight mt-1">
          Model Evaluation &amp; Appliance Profiles
        </h2>
        <p className="text-slate-600 dark:text-slate-400 text-[15px] mt-1 max-w-xl">
          Historical dataset analysis from EcoWatt_6000.csv and comparative machine learning accuracy.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Energy Trend Chart & Appliance Shares */}
        <div className="lg:col-span-6 flex flex-col gap-6">
          {/* Energy Consumption Trend Bar representation */}
          <div className="bg-white dark:bg-[#0d1410] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs">
            <h3 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white mb-4 flex items-center justify-between">
              <span>Energy Consumption Trend (EcoWatt_6000.csv)</span>
              <span className="text-[12px] text-[#009e52] dark:text-emerald-400 font-semibold">kWh</span>
            </h3>
            <div className="h-40 flex items-end gap-1.5 sm:gap-2 pt-4 px-2 bg-slate-50/50 dark:bg-[#080d0a] rounded-2xl border border-slate-100/60 dark:border-slate-800">
              {sampleTrend.map((val, idx) => (
                <div key={idx} className="flex-1 flex flex-col items-center gap-1 group relative">
                  <div 
                    className="w-full bg-[#1d6b38] hover:bg-[#009e52] dark:bg-emerald-600 dark:hover:bg-emerald-400 rounded-t-sm transition-all duration-200"
                    style={{ height: `${(val / maxVal) * 100}%` }}
                  />
                  <div className="opacity-0 group-hover:opacity-100 absolute -top-7 bg-slate-900 dark:bg-slate-800 text-white text-[10px] px-1.5 py-0.5 rounded pointer-events-none transition-opacity z-20 whitespace-nowrap border border-slate-700">
                    {val} kWh
                  </div>
                </div>
              ))}
            </div>
            <div className="flex justify-between text-[11px] text-slate-400 dark:text-slate-500 mt-2 px-1">
              <span>Record #1</span>
              <span>Daily Sequence Trend</span>
              <span>Record #20</span>
            </div>
          </div>

          {/* Typical Appliance Distribution */}
          <div className="bg-white dark:bg-[#0d1410] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs">
            <h3 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-[#009e52] dark:text-emerald-400" />
              <span>Typical Appliance Load Distribution (%)</span>
            </h3>
            <div className="flex flex-col gap-3">
              {appliances.map((app, idx) => (
                <div key={idx} className="flex flex-col gap-1">
                  <div className="flex justify-between text-[13px] text-slate-700 dark:text-slate-300">
                    <span className="font-medium">{app.name}</span>
                    <span className="font-semibold text-slate-900 dark:text-white">{app.percent}%</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                    <div 
                      className={`h-full ${app.color} rounded-full transition-all duration-500`}
                      style={{ width: `${app.percent}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Model Benchmarking Table */}
        <div className="lg:col-span-6 flex flex-col gap-6">
          <div className="bg-white dark:bg-[#0d1410] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs h-full flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Award className="w-4 h-4 text-amber-500" />
                <span>Machine Learning Model Comparison</span>
              </h3>
              <span className="text-[11px] font-semibold text-[#009e52] dark:text-emerald-400 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-100 dark:border-emerald-800/60">
                Eco Score Validated
              </span>
            </div>

            <div className="overflow-x-auto flex-1">
              <table className="w-full text-left text-[12px]">
                <thead className="bg-slate-50 dark:bg-slate-900 text-slate-700 dark:text-slate-300">
                  <tr>
                    <th className="py-2.5 px-3 rounded-l-xl">Model</th>
                    <th className="py-2.5 px-2">MAE</th>
                    <th className="py-2.5 px-2">RMSE</th>
                    <th className="py-2.5 px-2">R² Score</th>
                    <th className="py-2.5 px-3 rounded-r-xl">Rank</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-300">
                  {modelMetrics.map((m, idx) => (
                    <tr key={idx} className={m.best ? "bg-emerald-50/40 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-300 font-medium" : "hover:bg-slate-50/40 dark:hover:bg-slate-800/40"}>
                      <td className="py-3 px-3">
                        <div className="flex items-center gap-1.5">
                          {m.best && <CheckCircle2 className="w-4 h-4 text-[#009e52] dark:text-emerald-400 shrink-0" />}
                          <span className={m.best ? "text-[#009e52] dark:text-emerald-400 font-semibold" : ""}>{m.model}</span>
                        </div>
                      </td>
                      <td className="py-3 px-2">{m.mae.toFixed(2)}</td>
                      <td className="py-3 px-2">{m.rmse.toFixed(2)}</td>
                      <td className="py-3 px-2 font-bold text-slate-900 dark:text-white">{m.r2.toFixed(3)}</td>
                      <td className="py-3 px-3">
                        {m.best ? (
                          <span className="px-2 py-0.5 rounded-full bg-[#009e52] text-white text-[10px] font-bold">
                            Top Model
                          </span>
                        ) : (
                          <span className="text-slate-400 dark:text-slate-500 text-[11px]">Benchmark</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-5 p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800 text-[12px] text-slate-600 dark:text-slate-400 leading-relaxed">
              <p>
                <strong>Evaluation Insight:</strong> The Random Forest regressor achieves the lowest root mean squared error (RMSE: 1.45) across multi-step sequences, while the Physics-Informed SGD Logarithmic model provides optimal transparency by isolating the core mechanical load <em>E<sub>load</sub></em>.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
