"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { NewsArticle, PaginatedResponse } from "@/types";
import {
  Newspaper,
  Search,
  Filter,
  ExternalLink,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Clock,
  Radio,
  X
} from "lucide-react";

export default function NewsPage() {
  const [data, setData] = useState<PaginatedResponse<NewsArticle> | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [selectedSource, setSelectedSource] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [selectedArticle, setSelectedArticle] = useState<NewsArticle | null>(null);

  useEffect(() => {
    api.getNewsSources().then((res) => setSources(res.sources)).catch(console.error);
  }, []);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await api.getNews({
          page,
          page_size: 20,
          search: search || undefined,
          source: selectedSource || undefined
        });
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    const timer = setTimeout(load, 200);
    return () => clearTimeout(timer);
  }, [page, search, selectedSource]);

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Industry News"
        subtitle="72 Live AI Signals Across 5 Major Technology Sources"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "News" }]}
      />

      <div className="px-3 sm:px-6 py-4 sm:py-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto">
        {/* Controls Bar */}
        <div className="p-3 sm:p-4 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] flex flex-col md:flex-row md:items-center justify-between gap-3 sm:gap-4">
          <div className="relative flex-1 w-full md:max-w-md">
            <Search className="absolute left-3 top-3 w-4 h-4 text-[#98A7BD]" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search headline, company, topic..."
              className="w-full pl-9 pr-4 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none focus:border-[#F3B84B]"
            />
          </div>

          <div className="flex flex-col sm:flex-row flex-wrap items-stretch sm:items-center gap-2 sm:gap-3">
            {/* Source Filter */}
            <select
              value={selectedSource}
              onChange={(e) => {
                setSelectedSource(e.target.value);
                setPage(1);
              }}
              className="w-full sm:w-auto px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#F3B84B]"
            >
              <option value="">All 5 News Sources</option>
              {sources.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>

            <div className="text-xs font-mono text-[#98A7BD] text-center sm:text-left">
              {data ? `${data.total.toLocaleString()} articles` : "Loading..."}
            </div>
          </div>
        </div>

        {/* News Grid */}
        {loading ? (
          <div className="py-24 text-center">
            <Loader2 className="w-8 h-8 text-[#F3B84B] animate-spin mx-auto mb-2" />
            <span className="text-xs font-mono text-[#98A7BD]">Fetching verified news signals...</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data?.items.map((news) => (
              <div
                key={news.id}
                onClick={() => setSelectedArticle(news)}
                className="p-4 sm:p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#F3B84B]/60 transition-all flex flex-col justify-between cursor-pointer group"
              >
                <div>
                  <div className="flex flex-wrap items-center justify-between gap-1.5 mb-2">
                    <Badge variant="amber">{news.source_name}</Badge>
                    <span className="text-[11px] font-mono text-[#98A7BD] flex items-center gap-1">
                      <Clock className="w-3 h-3 text-[#F3B84B]" />
                      {new Date(news.published_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-white group-hover:text-[#F3B84B] transition-colors line-clamp-2 leading-snug">
                    {news.title}
                  </h3>

                  <p className="text-xs text-[#98A7BD] mt-2 line-clamp-3 leading-relaxed">
                    {news.summary || news.full_text || "Read full report on publisher website."}
                  </p>
                </div>

                <div className="pt-3 sm:pt-4 mt-3 sm:mt-4 border-t border-[#1E2D4A]/60 flex flex-wrap items-center justify-between gap-2">
                  <span className="text-[11px] font-mono text-[#98A7BD]">
                    {new Date(news.published_at).toLocaleDateString()}
                  </span>
                  <a
                    href={news.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="text-xs text-[#4F8CFF] hover:underline flex items-center gap-1 font-mono"
                  >
                    Read on {news.source_name} <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] flex items-center justify-between text-xs">
            <span className="text-[#98A7BD]">
              Page <span className="text-white font-mono">{data.page}</span> of{" "}
              <span className="text-white font-mono">{data.total_pages}</span>
            </span>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={data.page <= 1}
                className="p-1.5 rounded-lg bg-[#17233A] border border-[#1E2D4A] text-white disabled:opacity-30"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
                disabled={data.page >= data.total_pages}
                className="p-1.5 rounded-lg bg-[#17233A] border border-[#1E2D4A] text-white disabled:opacity-30"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Article Detail Modal */}
        {selectedArticle && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/70 backdrop-blur-sm">
            <div className="w-full max-w-xl max-h-[90vh] overflow-y-auto rounded-2xl bg-[#0B1020] border border-[#1E2D4A] shadow-2xl p-4 sm:p-6 relative space-y-4">
              <button
                onClick={() => setSelectedArticle(null)}
                className="absolute top-3 sm:top-4 right-3 sm:right-4 p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A]"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex flex-wrap items-center gap-2 pr-8">
                <Badge variant="amber">{selectedArticle.source_name}</Badge>
                <span className="text-xs font-mono text-[#98A7BD]">
                  Published: {new Date(selectedArticle.published_at).toLocaleString()}
                </span>
              </div>

              <h3 className="text-base font-bold text-white leading-snug">{selectedArticle.title}</h3>

              <div className="p-3 sm:p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] text-xs text-[#F4F7FC] leading-relaxed max-h-60 overflow-y-auto">
                {selectedArticle.summary || selectedArticle.full_text || "No summary provided by publisher."}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 py-2 border-t border-[#1E2D4A] text-xs">
                <div>
                  <span className="text-[#98A7BD] block mb-0.5">Author / Byline</span>
                  <span className="font-semibold text-white">{selectedArticle.author || "Staff Reporter"}</span>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-0.5">Primary Entity</span>
                  <span className="font-semibold text-white">{selectedArticle.primary_entity || "General AI"}</span>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-2">
                <span className="text-[11px] font-mono text-[#98A7BD] truncate">Fingerprint: {selectedArticle.fingerprint.slice(0, 16)}...</span>
                <a
                  href={selectedArticle.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-xl bg-[#F3B84B] hover:bg-[#DDA032] text-xs font-semibold text-black flex items-center justify-center gap-1.5"
                >
                  Read Full Article on {selectedArticle.source_name} <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
