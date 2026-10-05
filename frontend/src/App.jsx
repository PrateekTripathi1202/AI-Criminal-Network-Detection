import React, { useState, useEffect } from 'react';
import {
  ShieldAlert, Activity, Share2, Globe, Sparkles, Database, Brain, Video, Bot, 
  ChevronRight, RefreshCw, Radio, Lock, Radar, Target, Gauge, ShieldCheck, 
  Volume2, VolumeX, Eye, FileText, Search, Settings, HelpCircle
} from 'lucide-react';
import { api } from './services/api';
import { soundEffects } from './services/soundEffects';

// Views and Components
import CaseGraphNetworkOverview from './components/CaseGraphNetworkOverview';
import EvidenceReviewHub from './components/EvidenceReviewHub';
import DashboardOverview from './components/DashboardOverview';
import ThreeGraph3D from './components/ThreeGraph3D';
import TacticalGlobe3D from './components/TacticalGlobe3D';
import ChainExplorer3D from './components/ChainExplorer3D';
import DataIngestion from './components/DataIngestion';
import IntelligenceHub from './components/IntelligenceHub';
import CaseCopilot from './components/CaseCopilot';
import CaseDossierModal from './components/CaseDossierModal';

export default function App() {
  // Navigation State - Defaults to the user's requested 'network-graph' view!
  const [activeTab, setActiveTab] = useState('network-graph');
  const [graphData, setGraphData] = useState(null);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAudioOn, setIsAudioOn] = useState(true);
  const [evidenceInitialTab, setEvidenceInitialTab] = useState('cctv');

  useEffect(() => {
    loadGraph();
  }, []);

  const loadGraph = async () => {
    setIsLoading(true);
    try {
      const data = await api.getGraph();
      setGraphData(data);
    } catch (err) {
      console.warn('Backend graph load notice:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectNode = (node) => {
    if (!node) return;
    const id = typeof node === 'string' ? node : (node.id || node.suspect_id);
    setSelectedNodeId(id);
  };

  const handleOpenEvidence = (subTab = 'cctv') => {
    setEvidenceInitialTab(subTab);
    setActiveTab('evidence-review');
    soundEffects.playClick();
  };

  // Sidebar Workspace navigation items matching reference
  const workspaceNav = [
    { id: 'overview', label: 'Overview' },
    { id: 'case-explorer', label: 'Case Explorer' },
    { id: 'network-graph', label: 'Network Graph' },
    { id: 'timeline', label: 'Timeline' },
    { id: 'evidence-review', label: 'Evidence Review' },
    { id: 'audit-log', label: 'Audit Log' },
  ];

  return (
    <div className="min-h-screen bg-[#EDF2F7] text-slate-900 font-sans flex flex-col antialiased selection:bg-blue-100 selection:text-blue-900">
      
      {/* Top Application Bar */}
      <header className="bg-white border-b border-slate-200/90 px-4 md:px-6 py-3 sticky top-0 z-40 shadow-[0_1px_3px_rgba(0,0,0,0.03)]">
        <div className="max-w-[1600px] mx-auto flex items-center justify-between gap-4">
          
          {/* Logo & Application Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-base shadow-sm select-none">
              CN
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold tracking-tight text-slate-900 leading-none">
                  CaseGraph AI
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1 leading-none">
                Gemini-assisted criminal network analysis • Demo workspace
              </p>
            </div>
          </div>

          {/* Right Header Status / Badges */}
          <div className="flex items-center gap-3">
            {/* Audio SFX Toggle */}
            <button
              onClick={() => {
                const s = soundEffects.toggleSound();
                if (s) soundEffects.playClick();
                setIsAudioOn(s);
              }}
              className="p-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-600 text-xs flex items-center gap-1.5 transition-all"
              title="Toggle Tactical Audio Feedback"
            >
              {isAudioOn ? <Volume2 className="w-3.5 h-3.5 text-blue-600" /> : <VolumeX className="w-3.5 h-3.5 text-slate-400" />}
              <span className="hidden sm:inline text-[11px] font-medium">{isAudioOn ? 'SFX ON' : 'MUTED'}</span>
            </button>

            {/* AI Copilot shortcut */}
            <button
              onClick={() => {
                soundEffects.playClick();
                setActiveTab('copilot');
              }}
              className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-100 transition-all"
            >
              <Bot className="w-3.5 h-3.5 text-blue-600" />
              <span>Ask Copilot</span>
            </button>

            {/* Ingestion shortcut */}
            <button
              onClick={() => {
                soundEffects.playClick();
                setActiveTab('ingestion');
              }}
              className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200 transition-all"
            >
              <Database className="w-3.5 h-3.5 text-slate-600" />
              <span>Ingest FIR</span>
            </button>

            {/* DEMO DATA ONLY Badge matching screenshot */}
            <div className="casegraph-badge-demo">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>DEMO DATA ONLY</span>
            </div>
          </div>

        </div>
      </header>

      {/* Main Workspace Body with Left Sidebar & Right View Area */}
      <div className="flex-1 max-w-[1600px] w-full mx-auto p-4 md:p-6 flex flex-col md:flex-row gap-5 items-start">
        
        {/* Left Dark Navy Sidebar */}
        <aside className="w-full md:w-60 lg:w-64 bg-[#0E1B2E] rounded-2xl p-4 flex flex-col justify-between self-stretch flex-shrink-0 shadow-sm border border-slate-800">
          <div className="space-y-4">
            
            {/* WORKSPACE Category Title */}
            <div className="px-3 pt-2 text-[11px] font-bold text-slate-400 tracking-[0.14em] uppercase">
              WORKSPACE
            </div>

            {/* Navigation List */}
            <nav className="space-y-1">
              {workspaceNav.map((item) => {
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      soundEffects.playClick();
                      setActiveTab(item.id);
                    }}
                    className={`casegraph-nav-btn ${isActive ? 'active' : ''}`}
                  >
                    {isActive ? (
                      <span className="w-2 h-2 rounded-full bg-white flex-shrink-0" />
                    ) : (
                      <span className="w-2 h-2 rounded-full bg-transparent flex-shrink-0" />
                    )}
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </nav>

            {/* Direct Tool Links */}
            <div className="pt-3 border-t border-slate-800/80 px-2 space-y-1">
              <button
                onClick={() => {
                  soundEffects.playClick();
                  setActiveTab('copilot');
                }}
                className={`casegraph-nav-btn text-xs ${activeTab === 'copilot' ? 'active' : ''}`}
              >
                <Bot className="w-3.5 h-3.5 text-blue-400" />
                <span>Gemini Case Copilot</span>
              </button>

              <button
                onClick={() => {
                  soundEffects.playClick();
                  setActiveTab('ingestion');
                }}
                className={`casegraph-nav-btn text-xs ${activeTab === 'ingestion' ? 'active' : ''}`}
              >
                <Database className="w-3.5 h-3.5 text-emerald-400" />
                <span>FIR Ingestion & OCR</span>
              </button>
            </div>
          </div>

          {/* Bottom Sidebar Box: RESPONSIBLE AI */}
          <div className="mt-8 bg-[#16273F] border border-[#203657] rounded-xl p-3.5 space-y-1.5 text-left">
            <div className="text-[11px] font-bold text-emerald-400 tracking-wider uppercase">
              RESPONSIBLE AI
            </div>
            <div className="text-xs text-slate-300 font-medium leading-tight">
              Human review required
            </div>
            <div className="text-xs text-slate-300 font-medium leading-tight">
              Source-linked suggestions
            </div>
            <div className="text-xs text-slate-300 font-medium leading-tight">
              No automated accusations
            </div>
          </div>
        </aside>

        {/* Right Main Content Stage */}
        <main className="flex-1 w-full min-w-0">
          
          {/* 1. Network Graph (Primary view matching reference image) */}
          {activeTab === 'network-graph' && (
            <CaseGraphNetworkOverview
              onNavigate={setActiveTab}
              onSelectEntity={handleSelectNode}
              onOpenEvidenceReview={handleOpenEvidence}
            />
          )}

          {/* 2. Overview Tab */}
          {activeTab === 'overview' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6 animate-fadeIn">
              <div className="border-b border-slate-100 pb-4">
                <h1 className="text-2xl font-bold text-slate-900">
                  Criminal Ecosystem Intelligence Overview
                </h1>
                <p className="text-xs text-slate-500 mt-1">
                  Synthesized multi-jurisdiction telemetry and active law enforcement alerts
                </p>
              </div>

              <DashboardOverview
                graphData={graphData}
                onNavigate={setActiveTab}
                onSelectSuspect={handleSelectNode}
              />
            </div>
          )}

          {/* 3. Case Explorer Tab (3D Graph & Tactical Globe) */}
          {activeTab === 'case-explorer' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4 animate-fadeIn">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                <div>
                  <h1 className="text-2xl font-bold text-slate-900">
                    3D Interactive Case Explorer
                  </h1>
                  <p className="text-xs text-slate-500 mt-1">
                    Multi-dimensional force-directed physics graph with Gemini community clustering
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleSelectNode('P-101')}
                    className="px-3 py-1.5 rounded-xl text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100"
                  >
                    👑 Focus Kingpin (Amit Tyagi)
                  </button>
                </div>
              </div>

              <div className="rounded-xl overflow-hidden border border-slate-200">
                <ThreeGraph3D
                  graphData={graphData}
                  onSelectNode={handleSelectNode}
                  selectedNodeId={selectedNodeId}
                />
              </div>
            </div>
          )}

          {/* 4. Timeline Tab */}
          {activeTab === 'timeline' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4 animate-fadeIn">
              <div className="border-b border-slate-100 pb-4">
                <h1 className="text-2xl font-bold text-slate-900">
                  Chronological Crime Chain & Event Sequence
                </h1>
                <p className="text-xs text-slate-500 mt-1">
                  Step-by-step forensic progression from initial suspect contact to financial layering and CCTV interception
                </p>
              </div>

              <ChainExplorer3D />
            </div>
          )}

          {/* 5. Evidence Review Tab (CCTV, Live Webcam with face bounding box & ANPR, Audio Wiretaps) */}
          {activeTab === 'evidence-review' && (
            <EvidenceReviewHub
              defaultTab={evidenceInitialTab}
              onSelectSuspect={handleSelectNode}
            />
          )}

          {/* 6. Audit Log Tab */}
          {activeTab === 'audit-log' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4 animate-fadeIn">
              <div className="border-b border-slate-100 pb-4">
                <h1 className="text-2xl font-bold text-slate-900">
                  Judicial Audit Trail & Explainable AI (XAI)
                </h1>
                <p className="text-xs text-slate-500 mt-1">
                  Section 65B Indian Evidence Act / Section 63 BSA 2023 admissibility certifications & model audit logs
                </p>
              </div>

              <IntelligenceHub onGraphUpdate={loadGraph} />
            </div>
          )}

          {/* 7. Gemini Case Copilot */}
          {activeTab === 'copilot' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4 animate-fadeIn">
              <div className="border-b border-slate-100 pb-4">
                <h1 className="text-2xl font-bold text-slate-900">
                  Gemini AI Case Copilot
                </h1>
                <p className="text-xs text-slate-500 mt-1">
                  Ask investigative questions, request cross-case link discovery, and draft judicial raid orders
                </p>
              </div>

              <CaseCopilot onSelectEntity={handleSelectNode} />
            </div>
          )}

          {/* 8. Data Ingestion & OCR */}
          {activeTab === 'ingestion' && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4 animate-fadeIn">
              <div className="border-b border-slate-100 pb-4">
                <h1 className="text-2xl font-bold text-slate-900">
                  FIR & CDR Ingestion Engine
                </h1>
                <p className="text-xs text-slate-500 mt-1">
                  Extract entities, relationships, vehicles, and phone numbers from unstructured police case reports
                </p>
              </div>

              <DataIngestion
                onIngestionComplete={() => {
                  loadGraph();
                  setActiveTab('network-graph');
                }}
              />
            </div>
          )}

        </main>
      </div>

      {/* Case Dossier Modal (When an entity is clicked) */}
      <CaseDossierModal
        nodeId={selectedNodeId}
        onClose={() => setSelectedNodeId(null)}
        onSelectConnectedNode={handleSelectNode}
      />

      {/* Enterprise Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white px-4 py-3 text-center text-xs text-slate-500">
        <div className="max-w-[1600px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="text-slate-500 font-medium">
            CaseGraph AI • Gemini Criminal Network Intelligence Platform
          </div>
          <div className="text-[11px] text-slate-400">
            For Authorized Judicial & Law Enforcement Personnel Only • Section 65B Certified
          </div>
        </div>
      </footer>

    </div>
  );
}
