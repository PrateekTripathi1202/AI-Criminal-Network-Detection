import React, { useEffect, useState } from 'react';
import { 
  X, Shield, User, Phone, Car, CreditCard, Building2, MapPin, Video, FileText, Printer, Download, CheckCircle2, AlertTriangle, ExternalLink
} from 'lucide-react';
import { api } from '../services/api';

export default function CaseDossierModal({ nodeId, onClose, onSelectConnectedNode }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!nodeId) return;
    loadDetails();
  }, [nodeId]);

  const loadDetails = async () => {
    setLoading(true);
    try {
      const res = await api.getNodeDetails(nodeId);
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!nodeId) return null;

  const node = data?.node;
  const connections = data?.connections || [];
  const meta = node?.metadata || {};

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="glass-panel w-full max-w-3xl max-h-[90vh] overflow-y-auto border border-cyan-500/40 p-6 space-y-6 animate-fadeIn">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-700/60 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-950/80 border border-cyan-500/40 flex items-center justify-center text-cyan-400">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <div className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">
                GOVERNMENT OF INDIA // MINISTRY OF HOME AFFAIRS // NCRB
              </div>
              <h2 className="font-display font-bold text-lg text-slate-100 flex items-center gap-2">
                {node?.label || 'Loading...'}
                <span className="badge badge-critical text-[10px] font-mono">NON-BAILABLE WARRANT</span>
              </h2>
              <div className="text-[10px] text-slate-400 font-mono">
                CCTNS CASE DOSSIER // REF: CCTNS-MHA-2026-DL-88192
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="btn-secondary text-xs"
              title="Print Judicial Report"
            >
              <Printer className="w-3.5 h-3.5" /> Print Dossier
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center text-xs text-cyan-400">Retrieving intelligence dossier...</div>
        ) : node ? (
          <div className="space-y-5 text-xs">
            {/* Suspect / Entity Banner */}
            <div className="grid grid-cols-1 md:grid-cols-12 gap-4 bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              {meta.avatar && (
                <div className="md:col-span-3 flex flex-col items-center">
                  <img
                    src={meta.avatar}
                    alt={node.label}
                    className="w-24 h-24 rounded-lg object-cover border-2 border-rose-500 shadow-md"
                  />
                  <span className="badge badge-critical mt-2 text-[10px]">WANTED TARGET</span>
                </div>
              )}

              <div className={`${meta.avatar ? 'md:col-span-9' : 'md:col-span-12'} space-y-2`}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="badge badge-cyber text-[10px] font-mono">{node.id}</span>
                  <span className={`badge ${node.risk_score > 80 ? 'badge-critical' : 'badge-high'}`}>
                    THREAT RISK: {node.risk_score}%
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-slate-300">
                  {meta.alias && (
                    <div><span className="text-slate-500">Alias:</span> <span className="text-amber-300 font-semibold">{meta.alias}</span></div>
                  )}
                  {meta.role && (
                    <div><span className="text-slate-500">Role:</span> <span className="text-slate-200">{meta.role}</span></div>
                  )}
                  {meta.cctns_id && (
                    <div><span className="text-slate-500">CCTNS ID:</span> <span className="font-mono text-cyan-300">{meta.cctns_id}</span></div>
                  )}
                  {node.syndicate && (
                    <div><span className="text-slate-500">Syndicate:</span> <span className="text-slate-200">{node.syndicate}</span></div>
                  )}
                  {meta.bns_sections && (
                    <div className="col-span-2 text-rose-300"><span className="text-slate-500">Charged Under:</span> {meta.bns_sections}</div>
                  )}
                  {meta.plate_number && (
                    <div><span className="text-slate-500">Plate:</span> <span className="font-mono font-bold text-amber-300">{meta.plate_number}</span></div>
                  )}
                  {meta.bank && (
                    <div className="col-span-2"><span className="text-slate-500">Bank:</span> {meta.bank} (Balance: {meta.balance_inr})</div>
                  )}
                </div>
              </div>
            </div>

            {/* Centrality Metrics (if present) */}
            {node.centrality && (
              <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-2">
                <span className="text-[11px] font-semibold text-cyan-400 uppercase tracking-wider block">
                  Network Intelligence Metrics:
                </span>
                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="bg-slate-950 p-2 rounded border border-slate-800">
                    <div className="text-slate-400 text-[10px]">Kingpin Index</div>
                    <div className="text-sm font-bold text-rose-400 font-mono">{node.centrality.kingpin_index}</div>
                  </div>
                  <div className="bg-slate-950 p-2 rounded border border-slate-800">
                    <div className="text-slate-400 text-[10px]">Betweenness Centrality</div>
                    <div className="text-sm font-bold text-cyan-400 font-mono">{node.centrality.betweenness}</div>
                  </div>
                  <div className="bg-slate-950 p-2 rounded border border-slate-800">
                    <div className="text-slate-400 text-[10px]">PageRank Authority</div>
                    <div className="text-sm font-bold text-amber-400 font-mono">{node.centrality.pagerank}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Connected Graph Neighbors */}
            <div className="space-y-2.5">
              <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider block">
                Direct Criminal Connections ({connections.length}):
              </span>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {connections.map((c, i) => (
                  <div
                    key={i}
                    onClick={() => {
                      if (onSelectConnectedNode) onSelectConnectedNode(c.entity.id);
                    }}
                    className="p-2.5 rounded-lg bg-slate-900/70 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500/40 cursor-pointer flex items-center justify-between transition-all"
                  >
                    <div>
                      <div className="font-bold text-slate-200">{c.entity.label}</div>
                      <div className="text-[11px] text-cyan-400">{c.label || c.relation}</div>
                    </div>
                    <span className="badge badge-cyber text-[10px] capitalize">
                      {c.entity.type}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Judicial Admissibility Certificate */}
            <div className="p-3 rounded-lg bg-emerald-950/20 border border-emerald-500/30 text-[11px] text-emerald-300 space-y-1">
              <div className="font-semibold flex items-center gap-1.5 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" /> Section 65B Indian Evidence Act / BSA Digital Forensics Compliance
              </div>
              <p className="text-slate-400 leading-snug">
                Hash certificate generated. Telemetry corroborated across CDR, CCTNS, and ICJS databases under cryptographic audit trail.
              </p>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
