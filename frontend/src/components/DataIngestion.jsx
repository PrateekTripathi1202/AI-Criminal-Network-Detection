import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Sparkles, Database, Plus, RefreshCw, FileCode } from 'lucide-react';
import { api } from '../services/api';
import confetti from 'canvas-confetti';

const SAMPLE_FIRS = {
  fir_delhi: `FIRST INFORMATION REPORT (Under Section 173 BNS / 154 CrPC)
Police Station: Connaught Place, New Delhi District
FIR No: FIR-2026-DEL-102 | Date: 14/08/2026
Complainant: Ashok Khurana, Prop. Khurana Jewellers, CP

Incident Summary:
On 14/08/2026 at approx 20:45 hrs, complainant received armed extortion demand of ₹ 2,00,00,000/-. Suspect identifying as 'Munna Delhi' claimed allegiance to Vicky Malhotra gang. Caller threatened fatal harm if money was not handed over. Two armed accomplices arrived in a black SUV bearing registration DL-01-AB-9821. CCTV footage confirms prime accused Amit 'Rana' Tyagi entering the vehicle. Call was placed from burner SIM +91 98110-XXXX1. Suspects fled towards Barakhamba Road.`,

  fir_mumbai: `ENFORCEMENT DIRECTORATE & CYBER POLICE CRIME REPORT
Police Station: Bandra Kurla Complex Cyber Police, Mumbai
FIR No: FIR-2025-MUM-844 | Date: 20/11/2025
Complainant: FIU-IND / Sub-Divisional Officer

Incident Summary:
Large-scale Hawala laundering scheme detected in HDFC Account #...8819 under shell entity 'Apex Global Impex' (CIN U51909MH2021PTC368291). Funds exceeding ₹ 45 Crores received via structured smurfing from ICICI Account #...1102 (signatory Rajesh Sharma). Suspect Pooja Deshmukh absconding. Entity owns luxury vehicles including Fortuner DL-01-AB-9821 used in inter-state extortion crimes. Ultimate beneficiary traced to Vikram 'Vicky' Malhotra.`,

  cdr_log: `CDR Telecom Extraction:
Source IMEI: 864291040182910 | SIM: +91 98110-XXXX1 (Burner)
2026-09-18 01:14:02 | INCOMING | +91 99200-XXXX8 (Encrypted Satellite VoIP - Dubai) | 480s | Cell Tower: Rohini Sector 14
2026-09-18 02:40:11 | OUTGOING | +91 97118-XXXX4 (Accomplice SIM) | 120s | Cell Tower: Connaught Outer
2026-09-18 20:30:19 | SMS INTERCEPT | "Fortuner at CP Block B. Cash packet ready."`
};

export default function DataIngestion({ onIngestionComplete }) {
  const [sourceType, setSourceType] = useState('fir');
  const [rawText, setRawText] = useState(SAMPLE_FIRS.fir_delhi);
  const [isProcessing, setIsProcessing] = useState(false);
  const [ingestionResult, setIngestionResult] = useState(null);

  const handleLoadSample = (key) => {
    setRawText(SAMPLE_FIRS[key]);
    if (key === 'cdr_log') setSourceType('cdr');
    else setSourceType('fir');
  };

  const handleIngest = async () => {
    if (!rawText.trim()) return;
    setIsProcessing(true);
    try {
      const res = await api.ingestData({
        source_type: sourceType,
        raw_text: rawText,
        file_name: sourceType === 'fir' ? 'FIR-DOCUMENT-UPLOAD.pdf' : 'CDR-RECORD-EXPORT.csv'
      });
      setIngestionResult(res);
      confetti({ particleCount: 50, spread: 60, origin: { y: 0.7 } });
      if (onIngestionComplete) onIngestionComplete();
    } catch (err) {
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-5">
      {/* Header Banner */}
      <div className="glass-panel p-4 flex flex-wrap items-center justify-between gap-3 border-l-4 border-cyan-400">
          <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">
            DIGITAL EVIDENCE INGESTION & OCR // CCTNS STANDARD
          </span>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Database className="w-4 h-4 text-cyan-400" />
            Ingest & Standardize Diverse Law Enforcement Records (FIR, CDR, Bank Statements, CCTV)
          </h2>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Load Template:</span>
          <button 
            onClick={() => handleLoadSample('fir_delhi')}
            className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-300 rounded border border-slate-700 font-medium"
          >
            Delhi Extortion FIR
          </button>
          <button 
            onClick={() => handleLoadSample('fir_mumbai')}
            className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-amber-300 rounded border border-slate-700 font-medium"
          >
            Mumbai Hawala FIR
          </button>
          <button 
            onClick={() => handleLoadSample('cdr_log')}
            className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-emerald-300 rounded border border-slate-700 font-medium"
          >
            CDR Call Intercept
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Editor & Upload Form */}
        <div className="lg:col-span-7 glass-panel p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
              <FileCode className="w-4 h-4 text-cyan-400" /> Document & Forensic Stream Input
            </div>
            <div className="flex items-center gap-1.5 text-xs">
              {['fir', 'cdr', 'bank_statement', 'cctv_log'].map(type => (
                <button
                  key={type}
                  onClick={() => setSourceType(type)}
                  className={`px-2.5 py-1 rounded transition-all ${
                    sourceType === type 
                      ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/50 font-semibold' 
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {type.toUpperCase().replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1.5">
              Paste Police FIR Text, Intercept Transcript, or CSV Records:
            </label>
            <textarea
              rows={11}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 focus:border-cyan-400/60 rounded-lg p-3 text-xs text-slate-200 font-mono leading-relaxed focus:outline-none"
              placeholder="Paste raw police FIR, CDR transcripts, or bank statements..."
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <span className="text-[11px] text-slate-400 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              Automated NLP Entity Extraction, De-duplication & Graph Insertion
            </span>
            <button
              onClick={handleIngest}
              disabled={isProcessing}
              className="btn-primary text-xs"
            >
              {isProcessing ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" /> Extracting Entities...
                </>
              ) : (
                <>
                  <UploadCloud className="w-4 h-4" /> Run AI Entity Extraction & Link
                </>
              )}
            </button>
          </div>
        </div>

        {/* Extraction Output & Graph Status */}
        <div className="lg:col-span-5 glass-panel p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
            <h3 className="font-display font-bold text-sm text-slate-100 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Extracted Entities & Graph Linkage
            </h3>
            {ingestionResult && (
              <span className="badge badge-verified text-[10px]">
                {ingestionResult.entities_extracted_count} ENTITIES LINKED
              </span>
            )}
          </div>

          {ingestionResult ? (
            <div className="space-y-3">
              <div className="p-3 rounded-lg bg-emerald-950/20 border border-emerald-500/30 text-xs text-emerald-300">
                Data processed successfully! Entities integrated into active 3D Knowledge Graph and Cross-Case correlation engine.
              </div>

              <div className="space-y-2">
                <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider block">
                  Discovered Graph Nodes:
                </span>
                {ingestionResult.entities.map((ent, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2.5 rounded bg-slate-900/70 border border-slate-800 text-xs">
                    <div>
                      <div className="font-bold text-slate-200">{ent.label}</div>
                      <div className="text-[11px] text-slate-400 capitalize">Type: {ent.type} • {ent.role}</div>
                    </div>
                    <span className="badge badge-cyber text-[10px]">{ent.id}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-[280px] flex flex-col items-center justify-center text-center p-6 text-slate-500 text-xs space-y-2">
              <UploadCloud className="w-10 h-10 text-slate-600 mb-1" />
              <p className="font-medium text-slate-400">Ready for Document Ingestion</p>
              <p className="text-[11px] max-w-xs">
                Select a sample FIR above and click "Run AI Entity Extraction" to parse suspects, vehicles, and phones into the 3D Graph.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
