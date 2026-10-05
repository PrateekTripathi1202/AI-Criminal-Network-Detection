import React, { useState } from 'react';
import { Video, Radio, Shield, Eye, Camera, Mic, Volume2, Sparkles } from 'lucide-react';
import CctvSurveillance from './CctvSurveillance';
import AudioWiretapPlayer from './AudioWiretapPlayer';
import { soundEffects } from '../services/soundEffects';

export default function EvidenceReviewHub({ defaultTab = 'cctv', onSelectSuspect }) {
  const [activeEvidenceTab, setActiveEvidenceTab] = useState(defaultTab);

  return (
    <div className="w-full space-y-5 animate-fadeIn">
      {/* Evidence Sub-Navigation Header */}
      <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl md:text-2xl font-bold text-slate-900">
              Evidence Review Vault
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
              Sec. 65B Telemetry
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time optical CCTV streams, local AI webcam surveillance, and forensic wiretap intercepts
          </p>
        </div>

        {/* Tab switchers */}
        <div className="flex items-center p-1 rounded-xl bg-slate-100 border border-slate-200">
          <button
            onClick={() => {
              soundEffects.playClick();
              setActiveEvidenceTab('cctv');
            }}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all ${
              activeEvidenceTab === 'cctv'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Video className="w-4 h-4" />
            <span>CCTV & Live Webcam Grid</span>
          </button>

          <button
            onClick={() => {
              soundEffects.playClick();
              setActiveEvidenceTab('wiretap');
            }}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all ${
              activeEvidenceTab === 'wiretap'
                ? 'bg-white text-purple-600 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Radio className="w-4 h-4" />
            <span>Audio Wiretap Intercepts</span>
          </button>
        </div>
      </div>

      {/* Render selected evidence viewer */}
      {activeEvidenceTab === 'cctv' ? (
        <div className="rounded-2xl overflow-hidden border border-slate-200 shadow-sm">
          <CctvSurveillance onSelectSuspect={onSelectSuspect} />
        </div>
      ) : (
        <div className="rounded-2xl overflow-hidden border border-slate-200 shadow-sm">
          <AudioWiretapPlayer />
        </div>
      )}
    </div>
  );
}
