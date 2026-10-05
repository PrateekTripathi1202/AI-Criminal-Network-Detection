import React, { useState, useEffect } from 'react';
import { 
  Sparkles, Network, ArrowRight, ShieldCheck, CheckCircle2, XCircle, Brain, Layers, GitMerge, AlertCircle, FileCheck
} from 'lucide-react';
import { api } from '../services/api';
import confetti from 'canvas-confetti';

export default function IntelligenceHub({ onGraphUpdate }) {
  const [activeTab, setActiveTab] = useState('xai'); // 'xai' | 'cross_case' | 'memory'
  const [predictions, setPredictions] = useState([]);
  const [crossCases, setCrossCases] = useState([]);
  const [memoryItems, setMemoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [validationStatuses, setValidationStatuses] = useState({});

  useEffect(() => {
    loadIntelligenceData();
  }, []);

  const loadIntelligenceData = async () => {
    setLoading(true);
    try {
      const [preds, cross, mem] = await Promise.all([
        api.getPredictedLinks(),
        api.getCrossCase(),
        api.getMemory()
      ]);
      setPredictions(preds);
      setCrossCases(cross);
      setMemoryItems(mem);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleValidate = async (pred, approved) => {
    try {
      const key = `${pred.source}-${pred.target}`;
      setValidationStatuses(prev => ({ ...prev, [key]: approved ? 'APPROVED' : 'REJECTED' }));
      await api.validateLink({
        source: pred.source,
        target: pred.target,
        approved,
        officer_badge: 'INSP-DL-4902',
        notes: `Validated by Investigator based on XAI confidence ${pred.confidence}%`
      });
      if (approved) {
        confetti({ particleCount: 40, spread: 50, origin: { y: 0.6 } });
        if (onGraphUpdate) onGraphUpdate();
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-5">
      {/* Header Banner */}
      <div className="glass-panel p-4 flex flex-wrap items-center justify-between gap-3 border-l-4 border-cyan-400">
        <div>
          <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">
            AI INTELLIGENCE & FORENSIC REASONING // CCTNS 4.0
          </span>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Brain className="w-4 h-4 text-cyan-400" />
            Explainable AI (XAI), Cross-Case Discovery & Investigation Memory
          </h2>
        </div>
        <div className="flex items-center gap-1.5 text-xs">
          <button
            onClick={() => setActiveTab('xai')}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              activeTab === 'xai'
                ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                : 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60'
            }`}
          >
            Explainable AI (XAI) Link Prediction
          </button>
          <button
            onClick={() => setActiveTab('cross_case')}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              activeTab === 'cross_case'
                ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                : 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60'
            }`}
          >
            Cross-Case Discovery (FIRs)
          </button>
          <button
            onClick={() => setActiveTab('memory')}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              activeTab === 'memory'
                ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                : 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60'
            }`}
          >
            Investigation Memory
          </button>
        </div>
      </div>

      {/* Tab 1: Explainable AI Link Prediction */}
      {activeTab === 'xai' && (
        <div className="space-y-4">
          <div className="text-xs text-slate-400">
            Explainable AI calculates hidden links between entities with transparent feature weights and evidentiary reasoning:
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {predictions.map((pred, idx) => {
              const statusKey = `${pred.source}-${pred.target}`;
              const currentStatus = validationStatuses[statusKey];

              return (
                <div key={idx} className="glass-panel p-5 flex flex-col justify-between space-y-4 border border-slate-700/60 hover:border-cyan-500/50">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className={`badge ${pred.risk_elevation === 'EXTREME' ? 'badge-critical' : 'badge-high'}`}>
                        {pred.risk_elevation} THREAT
                      </span>
                      <span className="font-mono text-xs font-bold text-cyan-400">
                        {pred.confidence}% CONFIDENCE
                      </span>
                    </div>

                    <div>
                      <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Predicted Covert Linkage:</div>
                      <div className="text-sm font-bold text-slate-100 mt-0.5">{pred.predicted_relation}</div>
                      <div className="text-xs text-cyan-300 mt-1 flex items-center gap-1 font-mono">
                        <span>{pred.source_name}</span>
                        <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
                        <span>{pred.target_name}</span>
                      </div>
                    </div>

                    {/* Evidentiary reasons */}
                    <div className="space-y-1.5 pt-1">
                      <span className="text-[11px] font-semibold text-slate-300">Evidentiary Grounds:</span>
                      {pred.reasons.map((r, rIdx) => (
                        <div key={rIdx} className="text-[11px] text-slate-400 flex items-start gap-1.5 leading-snug">
                          <span className="text-cyan-400 font-bold">•</span>
                          <span>{r}</span>
                        </div>
                      ))}
                    </div>

                    {/* XAI Feature Importance Bar */}
                    {pred.xai_feature_weights && (
                      <div className="pt-2 border-t border-slate-800">
                        <span className="text-[10px] text-slate-400 font-semibold block mb-1.5">
                          XAI Feature Attribution Breakdown:
                        </span>
                        <div className="space-y-1 text-[11px]">
                          {Object.entries(pred.xai_feature_weights).map(([feature, weight]) => (
                            <div key={feature} className="flex items-center justify-between">
                              <span className="text-slate-400 text-[10px] truncate max-w-[170px]">{feature}</span>
                              <div className="flex items-center gap-1.5">
                                <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                  <div className="h-full bg-cyan-400" style={{ width: `${weight}%` }} />
                                </div>
                                <span className="font-mono text-[10px] text-slate-300">{weight}%</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Human-in-the-Loop Validation Action */}
                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
                    {currentStatus ? (
                      <div className={`text-xs font-semibold flex items-center gap-1.5 ${
                        currentStatus === 'APPROVED' ? 'text-emerald-400' : 'text-rose-400'
                      }`}>
                        {currentStatus === 'APPROVED' ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
                        Investigator {currentStatus} (Badge INSP-DL-4902)
                      </div>
                    ) : (
                      <>
                        <button
                          onClick={() => handleValidate(pred, false)}
                          className="px-3 py-1.5 rounded bg-slate-800/80 hover:bg-slate-700 text-xs text-slate-400 hover:text-slate-200 transition-all"
                        >
                          Dismiss
                        </button>
                        <button
                          onClick={() => handleValidate(pred, true)}
                          className="btn-primary text-xs"
                        >
                          <ShieldCheck className="w-3.5 h-3.5" /> Confirm & Link in Graph
                        </button>
                      </>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Tab 2: Cross-Case Discovery */}
      {activeTab === 'cross_case' && (
        <div className="space-y-4">
          <div className="text-xs text-slate-400">
            Cross-Case Discovery correlates disparate police FIRs across states (Delhi, Mumbai, Bengaluru) by finding shared getaway vehicles, shell entities, and burner phone IMEI clusters:
          </div>

          <div className="space-y-4">
            {crossCases.map((cc, idx) => (
              <div key={idx} className="glass-panel p-5 space-y-4 border-l-4 border-rose-500">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-700/60 pb-3">
                  <div className="flex items-center gap-2">
                    <GitMerge className="w-5 h-5 text-rose-400" />
                    <div>
                      <h3 className="font-display font-bold text-sm text-slate-100">
                        {cc.primary_fir} ⟷ {cc.secondary_fir}
                      </h3>
                      <p className="text-xs text-slate-400">Syndicate Nexus: <span className="text-cyan-300">{cc.syndicate}</span></p>
                    </div>
                  </div>
                  <span className="badge badge-critical text-xs">
                    {cc.correlation_score}% CROSS-CASE OVERLAP
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block">
                      Discovered Shared Threads:
                    </span>
                    {cc.shared_threads.map((st, sIdx) => (
                      <div key={sIdx} className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs space-y-1">
                        <div className="font-semibold text-cyan-400">{st.type}</div>
                        <p className="text-slate-300 leading-relaxed">{st.detail}</p>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-3 bg-slate-900/50 p-4 rounded-lg border border-slate-800/80 flex flex-col justify-between">
                    <div>
                      <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider block mb-1">
                        Correlated Modus Operandi:
                      </span>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {cc.modus_operandi_match}
                      </p>
                    </div>

                    <div className="pt-2 border-t border-slate-800">
                      <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider block mb-1">
                        ICJS Inter-Department Recommendation:
                      </span>
                      <p className="text-xs text-slate-200">
                        {cc.icjs_recommendation}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Investigation Memory */}
      {activeTab === 'memory' && (
        <div className="space-y-4">
          <div className="text-xs text-slate-400">
            Investigation Memory preserves operational context, lessons, and syndicate tradecraft from solved and cold cases:
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {memoryItems.map((mem) => (
              <div key={mem.id} className="glass-panel p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="badge badge-cyber text-[10px]">{mem.tag}</span>
                  <span className="text-xs text-slate-400 font-mono">{mem.recorded_date}</span>
                </div>

                <div>
                  <h4 className="font-bold text-sm text-slate-100">{mem.title}</h4>
                  <p className="text-xs text-cyan-400 mt-0.5">{mem.syndicate}</p>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  {mem.insight}
                </p>

                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>Confidence: {(mem.confidence * 100).toFixed(0)}%</span>
                  <span className="text-emerald-400 font-medium">Verified MO</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
