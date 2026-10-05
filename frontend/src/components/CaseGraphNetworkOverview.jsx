import React, { useState } from 'react';
import { 
  Sparkles, Check, X, ShieldAlert, FileText, Database, ArrowRight, 
  ExternalLink, Info, CheckCircle2, AlertCircle, RefreshCw, Layers, Eye
} from 'lucide-react';
import { soundEffects } from '../services/soundEffects';

export default function CaseGraphNetworkOverview({ 
  onNavigate, 
  onSelectEntity,
  onOpenEvidenceReview 
}) {
  // Case State
  const [caseId, setCaseId] = useState('CN-024');
  const [entitiesCount, setEntitiesCount] = useState(24);
  const [candidateLinksCount, setCandidateLinksCount] = useState(38);
  const [needsReviewCount, setNeedsReviewCount] = useState(7);
  const [sourceRecordsCount, setSourceRecordsCount] = useState(12);

  // Active / Selected Node
  const [selectedNode, setSelectedNode] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);

  // Candidate Link Insight State
  const [insightStatus, setInsightStatus] = useState('PENDING'); // 'PENDING' | 'ACCEPTED' | 'REJECTED'
  const [acceptedLinks, setAcceptedLinks] = useState([]);
  const [graphMode, setGraphMode] = useState('2D_SCHEMATIC'); // '2D_SCHEMATIC' | 'EXPLORER'

  // Current Gemini Insight being evaluated
  const currentInsight = {
    id: 'INS-881',
    source: 'Person A',
    target: 'Vehicle 7',
    intermediary: 'Phone X',
    title: 'Possible relationship detected',
    description: 'between Person A and Vehicle 7 through Phone X in sample records.',
    evidence: 'Records 03, 07',
    confidence: 'Review required',
    explanation: 'Phone X (associated with Person A) had repeated cell-tower pings in synchronized proximity with Vehicle 7 automated toll transponder entries.',
    traceability: [
      { id: 'Record 03', text: 'Phone X contacted Person A', date: '12 Aug 2026', type: 'CDR Telemetry' },
      { id: 'Record 07', text: 'Vehicle 7 observed near Location B', date: '14 Aug 2026', type: 'CCTV ANPR Hit' }
    ]
  };

  // Node coordinate & metadata matching user diagram exactly
  const nodes = [
    { 
      id: 'person-a', 
      label: 'Person A', 
      type: 'PERSON', 
      color: '#2563EB', // Blue
      x: 130, 
      y: 130, 
      r: 22,
      details: "Prime Subject // Identified in 3 CDR transcripts and surveillance sector 2"
    },
    { 
      id: 'location-b', 
      label: 'Location B', 
      type: 'LOCATION', 
      color: '#D97706', // Yellow / Amber
      x: 95, 
      y: 250, 
      r: 22,
      details: "Safehouse / Staging Warehouse // Connaught Place Peripheral Sector"
    },
    { 
      id: 'phone-x', 
      label: 'Phone X', 
      type: 'DEVICE', 
      color: '#7C3AED', // Purple
      x: 270, 
      y: 75, 
      r: 20,
      details: "Burner SIM IMEI 86940201948 // 42 encrypted signal bursts recorded"
    },
    { 
      id: 'account-z', 
      label: 'Account Z', 
      type: 'FINANCE', 
      color: '#059669', // Emerald / Teal
      x: 250, 
      y: 240, 
      r: 20,
      details: "Mule Bank Account // ₹2.4 Crore hawala structuring deposits"
    },
    { 
      id: 'vehicle-7', 
      label: 'Vehicle 7', 
      type: 'VEHICLE', 
      color: '#EA580C', // Orange
      x: 375, 
      y: 140, 
      r: 22,
      details: "Black SUV // ANPR hit on Expressway at 03:14 IST"
    },
    { 
      id: 'record-12', 
      label: 'Record 12', 
      type: 'EVIDENCE', 
      color: '#2563EB', // Blue
      x: 410, 
      y: 260, 
      r: 20,
      details: "CCTNS FIR #2026-DL-881 // Impounded contraband ledger"
    }
  ];

  // Confirmed edges connecting nodes
  const edges = [
    { from: 'person-a', to: 'location-b' },
    { from: 'person-a', to: 'phone-x' },
    { from: 'phone-x', to: 'account-z' },
    { from: 'phone-x', to: 'vehicle-7' },
    { from: 'vehicle-7', to: 'record-12' },
    { from: 'account-z', to: 'record-12' },
  ];

  const handleAcceptLink = () => {
    soundEffects.playTargetLock();
    setInsightStatus('ACCEPTED');
    setCandidateLinksCount(prev => Math.max(0, prev - 1));
    setNeedsReviewCount(prev => Math.max(0, prev - 1));
    setAcceptedLinks(prev => [...prev, 'Person A ↔ Vehicle 7']);
  };

  const handleRejectLink = () => {
    soundEffects.playRadioClick();
    setInsightStatus('REJECTED');
    setNeedsReviewCount(prev => Math.max(0, prev - 1));
  };

  const handleResetReview = () => {
    setInsightStatus('PENDING');
    setNeedsReviewCount(7);
    setCandidateLinksCount(38);
    setAcceptedLinks([]);
  };

  return (
    <div className="w-full space-y-5 animate-fadeIn">
      {/* Top Header info */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-900 font-sans">
            Network overview
          </h1>
          <div className="flex items-center gap-2 mt-1 text-sm text-slate-500 font-medium">
            <span>Sample case: <strong className="text-slate-800">{caseId}</strong></span>
            <span>•</span>
            <span>Last processed: Just now</span>
            <span className="inline-flex items-center gap-1 ml-2 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Live Sync
            </span>
          </div>
        </div>

        {/* Quick controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => onOpenEvidenceReview?.()}
            className="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300 shadow-sm flex items-center gap-1.5 transition-all"
            title="Open Live CCTV & Audio Evidence"
          >
            <Eye className="w-3.5 h-3.5 text-blue-600" />
            <span>Review Live Evidence (CCTV / Audio)</span>
          </button>

          <button
            onClick={() => onNavigate?.('case-explorer')}
            className="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-blue-600 text-white hover:bg-blue-700 shadow-sm flex items-center gap-1.5 transition-all"
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Open 3D Knowledge Web</span>
          </button>
        </div>
      </div>

      {/* 4 KPI Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Entities found */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:shadow-md transition-all">
          <div className="text-sm font-medium text-slate-500">
            Entities found
          </div>
          <div className="text-3xl md:text-4xl font-bold text-blue-600 mt-2 tracking-tight">
            {entitiesCount}
          </div>
        </div>

        {/* Card 2: Candidate links */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:shadow-md transition-all">
          <div className="text-sm font-medium text-slate-500">
            Candidate links
          </div>
          <div className="text-3xl md:text-4xl font-bold text-purple-600 mt-2 tracking-tight">
            {candidateLinksCount}
          </div>
        </div>

        {/* Card 3: Needs review */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:shadow-md transition-all">
          <div className="text-sm font-medium text-slate-500">
            Needs review
          </div>
          <div className="text-3xl md:text-4xl font-bold text-orange-600 mt-2 tracking-tight">
            {needsReviewCount}
          </div>
        </div>

        {/* Card 4: Source records */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:shadow-md transition-all">
          <div className="text-sm font-medium text-slate-500">
            Source records
          </div>
          <div className="text-3xl md:text-4xl font-bold text-emerald-600 mt-2 tracking-tight">
            {sourceRecordsCount}
          </div>
        </div>
      </div>

      {/* Middle Grid: Relationship Graph (Left) & Gemini Insight (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Relationship Graph */}
        <div className="lg:col-span-8 bg-white rounded-2xl p-5 md:p-6 border border-slate-200/90 shadow-[0_2px_12px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-900 tracking-tight">
                  Relationship graph
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Illustrative links from synthetic records
                </p>
              </div>

              {selectedNode && (
                <div className="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 flex items-center gap-1.5 animate-fadeIn">
                  <span>Selected: <strong>{selectedNode.label}</strong></span>
                  <button 
                    onClick={() => setSelectedNode(null)} 
                    className="hover:text-blue-900 ml-1 text-slate-400"
                  >
                    ×
                  </button>
                </div>
              )}
            </div>

            {/* SVG Interactive Graph Canvas */}
            <div className="relative w-full h-[320px] md:h-[360px] mt-4 bg-gradient-to-b from-slate-50/50 to-white rounded-xl border border-slate-100 flex items-center justify-center overflow-hidden">
              <svg 
                className="w-full h-full max-w-[560px]" 
                viewBox="0 0 520 340"
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
              >
                {/* Defs for gradients & filters */}
                <defs>
                  <filter id="nodeGlow" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="2" stdDeviation="3" floodOpacity="0.15" />
                  </filter>
                  <filter id="pulseGlow" x="-30%" y="-30%" width="160%" height="160%">
                    <feDropShadow dx="0" dy="0" stdDeviation="6" floodColor="#3B82F6" floodOpacity="0.4" />
                  </filter>
                </defs>

                {/* Confirmed Edges */}
                {edges.map((edge, idx) => {
                  const source = nodes.find(n => n.id === edge.from);
                  const target = nodes.find(n => n.id === edge.to);
                  if (!source || !target) return null;

                  const isHighlighted = (selectedNode && (selectedNode.id === source.id || selectedNode.id === target.id)) ||
                                        (hoveredNode && (hoveredNode.id === source.id || hoveredNode.id === target.id));

                  return (
                    <line
                      key={`edge-${idx}`}
                      x1={source.x}
                      y1={source.y}
                      x2={target.x}
                      y2={target.y}
                      stroke={isHighlighted ? "#2563EB" : "#94A3B8"}
                      strokeWidth={isHighlighted ? 3 : 2}
                      strokeOpacity={isHighlighted ? 0.9 : 0.65}
                      strokeLinecap="round"
                      className="transition-all duration-300"
                    />
                  );
                })}

                {/* Candidate Link (Dashed Line between Person A and Vehicle 7 through Phone X) */}
                {insightStatus !== 'REJECTED' && (
                  <path
                    d="M 130 130 Q 250 100 375 140"
                    fill="none"
                    stroke={insightStatus === 'ACCEPTED' ? "#10B981" : "#3B82F6"}
                    strokeWidth={insightStatus === 'ACCEPTED' ? 2.5 : 2}
                    strokeDasharray={insightStatus === 'ACCEPTED' ? "none" : "5,5"}
                    strokeOpacity={0.8}
                    className={insightStatus === 'PENDING' ? "animate-pulse" : ""}
                  />
                )}

                {/* Candidate Badge if Pending */}
                {insightStatus === 'PENDING' && (
                  <g transform="translate(252, 102)">
                    <rect x="-42" y="-10" width="84" height="20" rx="10" fill="#EFF6FF" stroke="#93C5FD" strokeWidth="1" />
                    <text x="0" y="3" textAnchor="middle" fontSize="9" fontWeight="600" fill="#1E40AF">
                      Candidate Link
                    </text>
                  </g>
                )}

                {/* Candidate Badge if Accepted */}
                {insightStatus === 'ACCEPTED' && (
                  <g transform="translate(252, 102)">
                    <rect x="-42" y="-10" width="84" height="20" rx="10" fill="#ECFDF5" stroke="#6EE7B7" strokeWidth="1" />
                    <text x="0" y="3" textAnchor="middle" fontSize="9" fontWeight="700" fill="#047857">
                      ✓ Verified Link
                    </text>
                  </g>
                )}

                {/* Render Nodes */}
                {nodes.map((node) => {
                  const isSelected = selectedNode?.id === node.id;
                  const isHovered = hoveredNode?.id === node.id;

                  return (
                    <g
                      key={node.id}
                      className="cursor-pointer group"
                      onClick={() => {
                        soundEffects.playClick();
                        setSelectedNode(node);
                        onSelectEntity?.(node);
                      }}
                      onMouseEnter={() => setHoveredNode(node)}
                      onMouseLeave={() => setHoveredNode(null)}
                    >
                      {/* Active Ring */}
                      {(isSelected || isHovered) && (
                        <circle
                          cx={node.x}
                          cy={node.y}
                          r={node.r + 6}
                          fill="none"
                          stroke={node.color}
                          strokeWidth="2"
                          strokeOpacity="0.4"
                          className="animate-pulse"
                        />
                      )}

                      {/* Main Node Circle */}
                      <circle
                        cx={node.x}
                        cy={node.y}
                        r={node.r}
                        fill={node.color}
                        filter="url(#nodeGlow)"
                        className="transition-transform duration-200 transform origin-center group-hover:scale-110"
                      />

                      {/* Inner Highlight for Depth */}
                      <circle
                        cx={node.x - 4}
                        cy={node.y - 4}
                        r={node.r * 0.4}
                        fill="#FFFFFF"
                        fillOpacity="0.25"
                      />

                      {/* Pill Label Beneath Node */}
                      <g transform={`translate(${node.x}, ${node.y + node.r + 14})`}>
                        <rect
                          x={-node.label.length * 4.2}
                          y="-10"
                          width={node.label.length * 8.4}
                          height="18"
                          rx="9"
                          fill="#FFFFFF"
                          stroke="#E2E8F0"
                          strokeWidth="1"
                          filter="url(#nodeGlow)"
                        />
                        <text
                          x="0"
                          y="3"
                          textAnchor="middle"
                          fontSize="10"
                          fontWeight="600"
                          fill="#1E293B"
                          className="select-none"
                        >
                          {node.label}
                        </text>
                      </g>
                    </g>
                  );
                })}
              </svg>
            </div>
          </div>

          {/* Node Detail Bar (When selected) */}
          <div className="mt-3 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs">
            {selectedNode ? (
              <div className="flex items-center gap-2 text-slate-700">
                <span className="font-semibold text-slate-900">{selectedNode.label}:</span>
                <span className="text-slate-600">{selectedNode.details}</span>
              </div>
            ) : (
              <div className="flex items-center gap-2 text-slate-400 text-[11px]">
                <Info className="w-3.5 h-3.5 text-slate-400" />
                <span>Tip: Click any node to inspect evidence traceability, or click candidate buttons to verify with Gemini.</span>
              </div>
            )}

            <div className="flex items-center gap-2">
              <span className="text-[11px] text-slate-400">Entities: 6 shown</span>
            </div>
          </div>
        </div>

        {/* Right Column: Gemini Insight Card */}
        <div className="lg:col-span-4 bg-white rounded-2xl p-5 md:p-6 border border-slate-200/90 shadow-[0_2px_12px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
                <span>Gemini insight</span>
                <Sparkles className="w-4 h-4 text-blue-600" />
              </h2>

              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                AI Inference
              </span>
            </div>

            {/* Blue Tinted Callout Container */}
            <div className="bg-[#EFF6FF] rounded-2xl p-4 md:p-5 border border-blue-100/80 transition-all">
              <h3 className="font-bold text-sm text-[#1E40AF] tracking-tight">
                {currentInsight.title}
              </h3>
              
              <p className="text-xs text-slate-700 mt-2 leading-relaxed font-normal">
                {currentInsight.description}
              </p>

              <div className="mt-4 pt-3 border-t border-blue-200/60 space-y-1.5 text-xs text-slate-600">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-500">Evidence:</span>
                  <span className="font-semibold text-slate-800">{currentInsight.evidence}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-500">Confidence:</span>
                  <span className="font-semibold text-orange-700 bg-orange-100/70 px-2 py-0.5 rounded-full text-[11px]">
                    {currentInsight.confidence}
                  </span>
                </div>
              </div>

              {/* Status Outcome Banner if Clicked */}
              {insightStatus === 'ACCEPTED' && (
                <div className="mt-4 p-2.5 rounded-xl bg-emerald-100/80 border border-emerald-300 text-emerald-900 text-xs font-semibold flex items-center gap-2 animate-fadeIn">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                  <span>Link verified by investigator. Appended to judicial dossier.</span>
                </div>
              )}

              {insightStatus === 'REJECTED' && (
                <div className="mt-4 p-2.5 rounded-xl bg-rose-100/80 border border-rose-300 text-rose-900 text-xs font-semibold flex items-center gap-2 animate-fadeIn">
                  <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
                  <span>Candidate link dismissed from active case hypothesis.</span>
                </div>
              )}
            </div>
          </div>

          {/* Action Buttons: Accept / Reject Link */}
          <div className="mt-5 space-y-2">
            {insightStatus === 'PENDING' ? (
              <div className="grid grid-cols-2 gap-3">
                {/* Accept Button */}
                <button
                  onClick={handleAcceptLink}
                  className="w-full py-2.5 px-3 rounded-xl text-xs font-semibold bg-[#DCFCE7] text-[#15803D] hover:bg-[#BBF7D0] transition-colors flex items-center justify-center gap-1.5 shadow-sm border border-emerald-200"
                >
                  <Check className="w-4 h-4 stroke-[2.5]" />
                  <span>Accept link</span>
                </button>

                {/* Reject Button */}
                <button
                  onClick={handleRejectLink}
                  className="w-full py-2.5 px-3 rounded-xl text-xs font-semibold bg-[#FEE2E2] text-[#991B1B] hover:bg-[#FECDD3] transition-colors flex items-center justify-center gap-1.5 shadow-sm border border-rose-200"
                >
                  <X className="w-4 h-4 stroke-[2.5]" />
                  <span>Reject link</span>
                </button>
              </div>
            ) : (
              <button
                onClick={handleResetReview}
                className="w-full py-2 px-3 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors flex items-center justify-center gap-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Evaluate Next Candidate Insight</span>
              </button>
            )}

            <div className="text-center">
              <span className="text-[11px] text-slate-400">
                Requires human sign-off per Responsible AI charter
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Card: Evidence Traceability */}
      <div className="bg-white rounded-2xl p-5 md:p-6 border border-slate-200/90 shadow-[0_2px_12px_rgba(0,0,0,0.03)]">
        <h2 className="text-base font-bold text-slate-900 tracking-tight">
          Evidence traceability
        </h2>

        <div className="mt-3 space-y-2 text-xs md:text-sm text-slate-600">
          <div className="flex flex-wrap items-center gap-2 py-1">
            <span className="font-semibold text-slate-800 bg-slate-100 px-2 py-0.5 rounded text-xs">
              Record 03
            </span>
            <span className="text-slate-400">•</span>
            <span className="font-medium text-slate-700">"Phone X contacted Person A"</span>
            <span className="text-slate-400">•</span>
            <span className="text-slate-500 font-mono text-xs">12 Aug 2026</span>
            <button 
              onClick={() => onOpenEvidenceReview?.('audio')}
              className="text-blue-600 hover:underline inline-flex items-center gap-1 text-xs font-semibold ml-auto"
            >
              <span>Play Wiretap Audio</span>
              <ExternalLink className="w-3 h-3" />
            </button>
          </div>

          <div className="flex flex-wrap items-center gap-2 py-1">
            <span className="font-semibold text-slate-800 bg-slate-100 px-2 py-0.5 rounded text-xs">
              Record 07
            </span>
            <span className="text-slate-400">•</span>
            <span className="font-medium text-slate-700">"Vehicle 7 observed near Location B"</span>
            <span className="text-slate-400">•</span>
            <span className="text-slate-500 font-mono text-xs">14 Aug 2026</span>
            <button 
              onClick={() => onOpenEvidenceReview?.('cctv')}
              className="text-blue-600 hover:underline inline-flex items-center gap-1 text-xs font-semibold ml-auto"
            >
              <span>View CCTV ANPR Hit</span>
              <ExternalLink className="w-3 h-3" />
            </button>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-400 flex items-center justify-between">
          <span>All links are suggestions only; investigators verify the original source before action.</span>
          <span className="font-medium text-slate-500">BSA 2023 / Section 65B Audit Compliant</span>
        </div>
      </div>
    </div>
  );
}
