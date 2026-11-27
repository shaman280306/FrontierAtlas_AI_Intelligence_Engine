"use client";

import React, { useState, useEffect } from "react";
import { Search, X, Building2, Package, BookOpen, Briefcase, Newspaper, Network, ExternalLink, Loader2 } from "lucide-react";
import { api } from "@/lib/api";
import { GlobalSearchResults } from "@/types";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function GlobalSearchModal({ isOpen, onClose }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<GlobalSearchResults | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        if (isOpen) onClose();
        else setQuery("");
      }
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  useEffect(() => {
    if (!query || query.trim().length < 2) {
      setResults(null);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await api.searchGlobal(query.trim());
        setResults(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [query]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-3xl rounded-2xl bg-[#0B1020] border border-[#1E2D4A] shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
        {/* Search Bar Input */}
        <div className="flex items-center px-4 py-3.5 border-b border-[#1E2D4A] bg-[#111A2E]">
          <Search className="w-5 h-5 text-[#4F8CFF] mr-3 flex-shrink-0" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search AI startups, products, papers, jobs, news, entities..."
            autoFocus
            className="w-full bg-transparent text-sm text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none"
          />
          {loading && <Loader2 className="w-4 h-4 text-[#36D6E7] animate-spin mr-2" />}
          <button onClick={onClose} className="p-1 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A]">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results Container */}
        <div className="p-4 overflow-y-auto space-y-5">
          {!results && !loading && (
            <div className="py-12 text-center text-[#98A7BD] text-xs">
              Type at least 2 characters to search across 4,389 verified AI records.
              <div className="mt-2 text-[11px] font-mono text-[#60728F]">
                Try &quot;Vision&quot;, &quot;Reasoning&quot;, &quot;OpenAI&quot;, &quot;Mistral&quot;, &quot;Robotics&quot;
              </div>
            </div>
          )}

          {results && results.total_matches === 0 && !loading && (
            <div className="py-12 text-center text-[#98A7BD] text-xs">
              No entities found matching &quot;{query}&quot;.
            </div>
          )}

          {/* Startups */}
          {results && results.results.startups.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold text-[#4F8CFF] uppercase tracking-wider mb-2">
                <Building2 className="w-3.5 h-3.5" />
                <span>Startups ({results.results.startups.length})</span>
              </div>
              <div className="space-y-1.5">
                {results.results.startups.map((s) => (
                  <div key={s.id} className="p-2.5 rounded-lg bg-[#111A2E] border border-[#1E2D4A] hover:border-[#4F8CFF]/50 transition-colors flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-sm text-[#F4F7FC]">{s.canonical_name}</div>
                      <div className="text-xs text-[#98A7BD] line-clamp-1">{s.description || `Source: ${s.source_name}`}</div>
                    </div>
                    <a href={s.source_url} target="_blank" rel="noopener noreferrer" className="p-1.5 text-[#98A7BD] hover:text-[#4F8CFF]">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Products */}
          {results && results.results.products.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold text-[#36D6E7] uppercase tracking-wider mb-2">
                <Package className="w-3.5 h-3.5" />
                <span>Products ({results.results.products.length})</span>
              </div>
              <div className="space-y-1.5">
                {results.results.products.map((p) => (
                  <div key={p.id} className="p-2.5 rounded-lg bg-[#111A2E] border border-[#1E2D4A] hover:border-[#36D6E7]/50 transition-colors flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-sm text-[#F4F7FC]">
                        {p.product_name} <span className="text-xs text-[#98A7BD]">by {p.startup_name}</span>
                      </div>
                      <div className="text-xs text-[#98A7BD] flex items-center gap-2 mt-0.5">
                        <span className="font-mono text-[#36D6E7]">{p.pricing_model || "TIER UNKNOWN"}</span>
                        <span>•</span>
                        <span className="line-clamp-1">{p.description || p.source_name}</span>
                      </div>
                    </div>
                    <a href={p.source_url} target="_blank" rel="noopener noreferrer" className="p-1.5 text-[#98A7BD] hover:text-[#36D6E7]">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Research Papers */}
          {results && results.results.research_papers.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold text-[#9275FF] uppercase tracking-wider mb-2">
                <BookOpen className="w-3.5 h-3.5" />
                <span>Research Papers ({results.results.research_papers.length})</span>
              </div>
              <div className="space-y-1.5">
                {results.results.research_papers.map((r) => (
                  <div key={r.id} className="p-2.5 rounded-lg bg-[#111A2E] border border-[#1E2D4A] hover:border-[#9275FF]/50 transition-colors flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-sm text-[#F4F7FC] line-clamp-1">{r.title}</div>
                      <div className="text-xs text-[#98A7BD] flex items-center gap-2 mt-0.5">
                        {r.github_stars !== null && (
                          <span className="font-mono text-[#F3B84B]">★ {r.github_stars}</span>
                        )}
                        <span>•</span>
                        <span className="line-clamp-1">{r.authors.join(", ")}</span>
                      </div>
                    </div>
                    <a href={r.paper_url} target="_blank" rel="noopener noreferrer" className="p-1.5 text-[#98A7BD] hover:text-[#9275FF]">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Jobs */}
          {results && results.results.jobs.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold text-[#35C98A] uppercase tracking-wider mb-2">
                <Briefcase className="w-3.5 h-3.5" />
                <span>Engineering Opportunities ({results.results.jobs.length})</span>
              </div>
              <div className="space-y-1.5">
                {results.results.jobs.map((j) => (
                  <div key={j.id} className="p-2.5 rounded-lg bg-[#111A2E] border border-[#1E2D4A] hover:border-[#35C98A]/50 transition-colors flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-sm text-[#F4F7FC]">{j.title}</div>
                      <div className="text-xs text-[#98A7BD]">{j.company} • {j.role_family} {j.is_remote ? "(Remote)" : ""}</div>
                    </div>
                    <a href={j.source_url} target="_blank" rel="noopener noreferrer" className="p-1.5 text-[#98A7BD] hover:text-[#35C98A]">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* News */}
          {results && results.results.news.length > 0 && (
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold text-[#F3B84B] uppercase tracking-wider mb-2">
                <Newspaper className="w-3.5 h-3.5" />
                <span>Industry News ({results.results.news.length})</span>
              </div>
              <div className="space-y-1.5">
                {results.results.news.map((n) => (
                  <div key={n.id} className="p-2.5 rounded-lg bg-[#111A2E] border border-[#1E2D4A] hover:border-[#F3B84B]/50 transition-colors flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-sm text-[#F4F7FC] line-clamp-1">{n.title}</div>
                      <div className="text-xs text-[#98A7BD]">{n.source_name} • {new Date(n.published_at).toLocaleDateString()}</div>
                    </div>
                    <a href={n.source_url} target="_blank" rel="noopener noreferrer" className="p-1.5 text-[#98A7BD] hover:text-[#F3B84B]">
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer shortcuts */}
        <div className="px-4 py-2 bg-[#111A2E] border-t border-[#1E2D4A] text-[11px] text-[#98A7BD] flex items-center justify-between font-mono">
          <span>Search spans 6 intelligence verticals</span>
          <span>ESC to close</span>
        </div>
      </div>
    </div>
  );
}
