import React from 'react';
import { 
  ShieldAlert, Users, PhoneCall, Car, Landmark, Video, Activity, Zap, TrendingUp, AlertOctagon, CheckCircle2, ChevronRight, Lock
} from 'lucide-react';

export default function DashboardOverview({ graphData, onNavigate, onSelectSuspect }) {
  const summary = graphData?.summary || {};
  const topKingpins = summary.top_kingpins || [];

  return (
    <div className="space-y-5">
      {/* Official National Security Directive Banner */}
      <div className="glass-panel p-3 px-4 flex flex-wrap items-center justify-between gap-3 bg-gradient-to-r from-red-950/40 via-slate-900/60 to-cyan-950/40 border-l-4 border-rose-500">
        <div className="flex items-center gap-2.5">
          <ShieldAlert className="w-5 h-5 text-rose-500 animate-pulse" />
          <div>
            <div className="flex items-center gap-2">
              <span className="font-display font-bold text-xs text-rose-400 tracking-wider">
                MHA NATIONAL THREAT LEVEL: DEFCON-2 (INTER-STATE SYNDICATE ELEVATION)
              </span>
              <span className="badge badge-critical text-[10px]">RESTRICTED ACCESS</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Active Warrants: 4 High-Value Targets • Central CCTNS & ICJS Inter-Agency Grid Synchronization Live
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <div className="bg-slate-950 px-2.5 py-1 rounded border border-slate-800 text-[11px] font-mono text-cyan-300">
            ENCRYPTION: AES-256 GCM
          </div>
          <div className="bg-slate-950 px-2.5 py-1 rounded border border-slate-800 text-[11px] font-mono text-emerald-400">
            SEC. 65B FORENSICS CERTIFIED
          </div>
        </div>
      </div>

      {/* Top Telemetry Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="glass-panel p-3.5 border-l-4 border-rose-500">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>Suspects Tracked</span>
            <Users className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold font-display text-slate-100">{summary.suspects_count || 6}</div>
          <span className="badge badge-critical text-[10px] mt-1">2 Red Notice</span>
        </div>

        <div className="glass-panel p-3.5 border-l-4 border-cyan-400">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>Burner Phones / CDR</span>
            <PhoneCall className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold font-display text-slate-100">{summary.phones_tracked || 3}</div>
          <span className="badge badge-cyber text-[10px] mt-1">820 Calls Analyzed</span>
        </div>

        <div className="glass-panel p-3.5 border-l-4 border-amber-400">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>Vehicles / ANPR</span>
            <Car className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-display text-slate-100">{summary.vehicles_monitored || 3}</div>
          <span className="badge badge-high text-[10px] mt-1">41 Toll Passes</span>
        </div>

        <div className="glass-panel p-3.5 border-l-4 border-emerald-400">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>Flagged Accounts</span>
            <Landmark className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-display text-slate-100">{summary.bank_accounts_flagged || 3}</div>
          <span className="badge badge-verified text-[10px] mt-1">₹ 6.7 Cr Frozen</span>
        </div>

        <div className="glass-panel p-3.5 border-l-4 border-violet-400">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>CCTV AI Nodes</span>
            <Video className="w-4 h-4 text-violet-400" />
          </div>
          <div className="text-2xl font-bold font-display text-slate-100">{summary.cctv_nodes || 3}</div>
          <span className="badge badge-cyber text-[10px] mt-1">4K Facial Live</span>
        </div>

        <div className="glass-panel p-3.5 border-l-4 border-blue-400">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-1">
            <span>CCTNS Status</span>
            <ShieldAlert className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-xl font-bold font-display text-emerald-400">SYNCED</div>
          <span className="text-[10px] text-slate-400 mt-1 block">ICJS Central API</span>
        </div>
      </div>

      {/* Main Grid: Kingpin Centrality + Live Threat Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Kingpin & Syndicate Centrality Leaderboard */}
        <div className="lg:col-span-7 glass-panel p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
            <div>
              <h3 className="font-display font-bold text-base text-slate-100 flex items-center gap-2">
                <Zap className="w-4 h-4 text-cyan-400" />
                Network Centrality & Kingpin Detection
              </h3>
              <p className="text-xs text-slate-400">
                Calculated via PageRank, Betweenness Centrality, and Risk Scores
              </p>
            </div>
            <button 
              onClick={() => onNavigate('graph')}
              className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-semibold"
            >
              View Full 3D Graph <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div className="space-y-2.5">
            {topKingpins.map((k, idx) => (
              <div 
                key={k.id}
                onClick={() => onSelectSuspect && onSelectSuspect(k.id)}
                className="flex items-center justify-between p-3 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 border border-slate-800 hover:border-cyan-500/40 cursor-pointer transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs ${
                    idx === 0 ? 'bg-rose-500 text-white shadow-lg shadow-rose-500/30' : 'bg-slate-800 text-slate-300'
                  }`}>
                    #{idx + 1}
                  </div>
                  <div>
                    <div className="font-bold text-sm text-slate-100 flex items-center gap-2">
                      {k.name}
                      {k.alias && <span className="text-xs text-amber-400 font-normal">({k.alias})</span>}
                    </div>
                    <div className="text-xs text-slate-400">{k.role} • <span className="text-slate-300">{k.syndicate}</span></div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-xs text-cyan-400 font-mono font-bold">Kingpin Index: {k.kingpin_index}</div>
                  <span className={`badge ${k.risk_score > 85 ? 'badge-critical' : 'badge-high'} text-[10px] mt-0.5`}>
                    Risk: {k.risk_score}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Real-time Threat Ticker & Cross-Case Alerts */}
        <div className="lg:col-span-5 glass-panel p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
            <h3 className="font-display font-bold text-base text-slate-100 flex items-center gap-2">
              <AlertOctagon className="w-4 h-4 text-rose-500 animate-pulse" />
              Real-Time Intelligence Alerts
            </h3>
            <span className="badge badge-critical text-[10px]">LIVE FEED</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-lg bg-rose-950/20 border border-rose-500/30 space-y-1">
              <div className="flex items-center justify-between text-rose-400 font-bold">
                <span>CRITICAL: Cross-Case Link Discovered</span>
                <span className="font-mono text-[10px]">21:42 PM</span>
              </div>
              <p className="text-slate-300">
                Getaway Fortuner <strong>DL-01-AB-9821</strong> (Delhi Extortion) confirmed registered to shell entity in <strong>FIR-2025-MUM-844</strong> (Mumbai Hawala).
              </p>
              <button 
                onClick={() => onNavigate('intelligence')}
                className="text-cyan-400 hover:underline text-[11px] font-semibold pt-1 block"
              >
                Inspect XAI Link Prediction ➔
              </button>
            </div>

            <div className="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 space-y-1">
              <div className="flex items-center justify-between text-amber-400 font-bold">
                <span>WARNING: Hawala Smurfing Pattern</span>
                <span className="font-mono text-[10px]">21:18 PM</span>
              </div>
              <p className="text-slate-300">
                48 transactions of ₹ 9,80,000 detected from ICICI #1102 to HDFC #8819 just below PMLA reporting threshold.
              </p>
            </div>

            <div className="p-3 rounded-lg bg-cyan-950/20 border border-cyan-500/30 space-y-1">
              <div className="flex items-center justify-between text-cyan-400 font-bold">
                <span>CCTV ANPR MATCH: Connaught Place</span>
                <span className="font-mono text-[10px]">20:55 PM</span>
              </div>
              <p className="text-slate-300">
                Camera #DEL-CP-041 logged 94.8% facial biometric match for enforcer Amit 'Rana' Tyagi.
              </p>
              <button 
                onClick={() => onNavigate('cctv')}
                className="text-cyan-400 hover:underline text-[11px] font-semibold pt-1 block"
              >
                Open Live CCTV View ➔
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
