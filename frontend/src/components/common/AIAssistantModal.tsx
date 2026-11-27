"use client";

import React, { useState } from "react";
import { Sparkles, X, Send, Loader2, BookOpen, Package, Building2, ExternalLink } from "lucide-react";
import { api } from "@/lib/api";
import { AIQueryResponse } from "@/types";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function AIAssistantModal({ isOpen, onClose }: Props) {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<Array<{ q: string; a: AIQueryResponse }>>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || loading) return;

    const userQ = prompt.trim();
    setPrompt("");
    setLoading(true);

    try {
      const res = await api.queryAI(userQ);
      setHistory((prev) => [...prev, { q: userQ, a: res }]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-3xl rounded-2xl bg-[#0B1020] border border-[#1E2D4A] shadow-2xl overflow-hidden flex flex-col h-[94vh] sm:h-[85vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-3 sm:px-6 py-3 sm:py-4 border-b border-[#1E2D4A] bg-[#111A2E] gap-2">
          <div className="flex items-center space-x-2 sm:space-x-3 min-w-0">
            <div className="p-1.5 sm:p-2 rounded-xl bg-gradient-to-br from-[#4F8CFF] to-[#9275FF] text-white shadow-md flex-shrink-0">
              <Sparkles className="w-4 h-4 sm:w-5 sm:h-5" />
            </div>
            <div className="min-w-0">
              <h2 className="text-xs sm:text-base font-bold text-white flex items-center gap-1.5 truncate">
                <span className="truncate">Frontier Assistant</span>
                <span className="text-[9px] sm:text-[10px] font-mono px-1.5 sm:px-2 py-0.5 rounded-full bg-[#9275FF]/20 text-[#9275FF] border border-[#9275FF]/30 flex-shrink-0">
                  Grounding Mode
                </span>
              </h2>
              <p className="text-[10px] sm:text-xs text-[#98A7BD] truncate hidden min-[360px]:block">Grounded in 4,389 verified database records</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A] flex-shrink-0"
            aria-label="Close Assistant Modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Conversation Body */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6">
          {history.length === 0 && (
            <div className="py-12 flex flex-col items-center justify-center text-center">
              <div className="w-12 h-12 rounded-2xl bg-[#17233A] border border-[#1E2D4A] flex items-center justify-center text-[#4F8CFF] mb-4">
                <Sparkles className="w-6 h-6 animate-pulse" />
              </div>
              <h3 className="text-sm font-semibold text-white">Ask anything about the AI ecosystem</h3>
              <p className="text-xs text-[#98A7BD] max-w-md mt-1 mb-6">
                Queries synthesize real research papers, open-source repositories, pricing models, and engineering roles.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg w-full text-left">
                {[
                  "Which AI research papers have open-source GitHub code?",
                  "What startups offer freemium AI products?",
                  "What engineering opportunities exist in robotics?",
                  "Explain connections around OpenAI & Mistral AI",
                ].map((sample) => (
                  <button
                    key={sample}
                    onClick={() => {
                      setPrompt(sample);
                    }}
                    className="p-2.5 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#4F8CFF]/50 text-xs text-[#98A7BD] hover:text-[#F4F7FC] transition-colors"
                  >
                    &quot;{sample}&quot;
                  </button>
                ))}
              </div>
            </div>
          )}

          {history.map((item, idx) => (
            <div key={idx} className="space-y-4">
              {/* User Prompt */}
              <div className="flex justify-end">
                <div className="max-w-[80%] px-4 py-2.5 rounded-2xl rounded-tr-sm bg-[#4F8CFF] text-white text-sm">
                  {item.q}
                </div>
              </div>

              {/* Engine Response */}
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 rounded-lg bg-[#9275FF]/20 border border-[#9275FF]/40 text-[#9275FF] flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div className="flex-1 p-4 rounded-2xl rounded-tl-sm bg-[#111A2E] border border-[#1E2D4A] text-sm text-[#F4F7FC] space-y-3">
                  <div className="prose prose-invert max-w-none text-xs leading-relaxed whitespace-pre-wrap">
                    {item.a.response}
                  </div>

                  {/* Grounding Attribution Chips */}
                  <div className="pt-2 border-t border-[#1E2D4A]/60 flex flex-wrap gap-1.5 items-center">
                    <span className="text-[10px] font-mono text-[#98A7BD] uppercase mr-1">Verified Grounding:</span>
                    {item.a.grounding.referenced_papers.slice(0, 2).map((p) => (
                      <a
                        key={p.id}
                        href={p.paper_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-[#17233A] text-[10px] font-mono text-[#9275FF] border border-[#9275FF]/30 hover:bg-[#9275FF]/20"
                      >
                        <BookOpen className="w-3 h-3" />
                        <span className="truncate max-w-[140px]">{p.title}</span>
                        <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    ))}
                    {item.a.grounding.referenced_products.slice(0, 2).map((pr) => (
                      <a
                        key={pr.id}
                        href={pr.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-[#17233A] text-[10px] font-mono text-[#36D6E7] border border-[#36D6E7]/30 hover:bg-[#36D6E7]/20"
                      >
                        <Package className="w-3 h-3" />
                        <span className="truncate max-w-[120px]">{pr.product_name}</span>
                        <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    ))}
                    {item.a.grounding.referenced_startups.slice(0, 2).map((st) => (
                      <a
                        key={st.id}
                        href={st.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-[#17233A] text-[10px] font-mono text-[#4F8CFF] border border-[#4F8CFF]/30 hover:bg-[#4F8CFF]/20"
                      >
                        <Building2 className="w-3 h-3" />
                        <span className="truncate max-w-[120px]">{st.canonical_name}</span>
                        <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center space-x-3 text-[#98A7BD] text-xs font-mono">
              <Loader2 className="w-4 h-4 animate-spin text-[#4F8CFF]" />
              <span>Querying FrontierAtlas graph & synthesizing grounded answer...</span>
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="p-3 sm:p-4 border-t border-[#1E2D4A] bg-[#111A2E] flex items-center gap-2 sm:gap-3">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask FrontierAtlas intelligence..."
            className="flex-1 min-w-0 bg-[#17233A] border border-[#1E2D4A] rounded-xl px-3 sm:px-4 py-2 sm:py-2.5 text-xs sm:text-sm text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none focus:border-[#4F8CFF]"
          />
          <button
            type="submit"
            disabled={!prompt.trim() || loading}
            className="p-2 sm:p-2.5 rounded-xl bg-[#4F8CFF] hover:bg-[#3B7BE8] disabled:opacity-50 text-white transition-colors flex-shrink-0"
            aria-label="Send Query"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
