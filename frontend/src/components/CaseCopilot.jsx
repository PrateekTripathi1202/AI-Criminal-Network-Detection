import React, { useState } from 'react';
import { Bot, Send, User, Sparkles, Shield, AlertCircle, ArrowRight, CornerDownLeft, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

const QUICK_PROMPTS = [
  "Who is the syndicate kingpin and how does he communicate?",
  "Trace vehicle DL-01-AB-9821 and its legal ownership.",
  "Explain how extortion money was laundered via Hawala.",
  "Summarize cross-case evidence between Delhi and Mumbai FIRs."
];

export default function CaseCopilot({ onSelectEntity }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Greetings, Investigator. I am your **AI Case Copilot**, grounded in the CCTNS criminal database, CDR transcripts, Hawala transaction ledgers, and ANPR surveillance logs.

You can ask me questions in plain English to uncover hidden connections, trace criminal money flows, or summarize cross-case evidence.`
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (queryText = input) => {
    const q = queryText.trim();
    if (!q || isLoading) return;

    const userMsg = { role: 'user', content: q };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await api.queryCopilot(q);
      const assistantMsg = {
        role: 'assistant',
        content: res.answer,
        entities: res.entities_involved || [],
        confidence: res.confidence,
        suggested_actions: res.suggested_actions || []
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Apologies, an error occurred while connecting to the intelligence reasoning core.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Header Banner */}
      <div className="glass-panel p-4 flex flex-wrap items-center justify-between gap-3 border-l-4 border-cyan-400">
        <div>
          <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">
            AI COPILOT // RAG INVESTIGATION ASSISTANT // CCTNS GROUNDED
          </span>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Bot className="w-4 h-4 text-cyan-400" />
            Natural Language Case Copilot (LLM / RAG / Graph Knowledge Grounding)
          </h2>
        </div>
        <span className="badge badge-cyber text-xs">
          CCTNS KNOWLEDGE RETRIEVAL READY
        </span>
      </div>

      <div className="glass-panel p-5 h-[580px] flex flex-col justify-between space-y-4">
        {/* Messages Stream */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex gap-3 text-xs leading-relaxed ${
                m.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {m.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-cyan-950 border border-cyan-500/40 flex items-center justify-center text-cyan-300 flex-shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-2xl p-4 rounded-xl space-y-2.5 ${
                  m.role === 'user'
                    ? 'bg-cyan-600 text-slate-950 font-medium ml-12 rounded-tr-none'
                    : 'bg-slate-900/90 border border-slate-800 text-slate-200 mr-12 rounded-tl-none'
                }`}
              >
                <div className="whitespace-pre-line">{m.content}</div>

                {/* Entities pill tags */}
                {m.entities && m.entities.length > 0 && (
                  <div className="pt-2 border-t border-slate-800/80 flex flex-wrap items-center gap-1.5">
                    <span className="text-[10px] text-slate-400 font-semibold">Referenced Entities:</span>
                    {m.entities.map(eId => (
                      <button
                        key={eId}
                        onClick={() => onSelectEntity && onSelectEntity(eId)}
                        className="badge badge-cyber text-[10px] cursor-pointer hover:bg-cyan-500/30"
                      >
                        {eId} ➔
                      </button>
                    ))}
                  </div>
                )}

                {/* Recommended Actions */}
                {m.suggested_actions && m.suggested_actions.length > 0 && (
                  <div className="pt-1 text-[11px] text-amber-300">
                    <span className="font-semibold block text-[10px] uppercase text-amber-400">Advisory:</span>
                    {m.suggested_actions.join(' • ')}
                  </div>
                )}
              </div>

              {m.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 flex-shrink-0">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex items-center gap-2 text-xs text-cyan-400 p-2">
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              <span>Synthesizing intelligence from knowledge graph & CCTNS documents...</span>
            </div>
          )}
        </div>

        {/* Quick Prompts */}
        <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-800">
          <span className="text-[11px] text-slate-400 self-center mr-1">Quick Inquiries:</span>
          {QUICK_PROMPTS.map((qp, i) => (
            <button
              key={i}
              onClick={() => handleSend(qp)}
              className="text-[11px] px-2.5 py-1 rounded bg-slate-800/70 hover:bg-slate-700 text-slate-300 hover:text-cyan-300 transition-all border border-slate-700/60"
            >
              {qp}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Copilot about suspects, phone intercept dates, vehicle ownership, money trails..."
            className="flex-1 bg-slate-950/80 border border-slate-800 focus:border-cyan-400/60 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="btn-primary text-xs py-2.5 px-4 disabled:opacity-40"
          >
            <Send className="w-3.5 h-3.5" /> Send
          </button>
        </form>
      </div>
    </div>
  );
}
