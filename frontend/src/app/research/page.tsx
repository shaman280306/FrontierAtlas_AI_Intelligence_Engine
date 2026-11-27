"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { ResearchPaper, PaginatedResponse } from "@/types";
import {
  BookOpen,
  Search,
  Filter,
  ExternalLink,
  Loader2,
  ChevronLeft,
  ChevronRight,
  GitBranch,
  Star,
  Clock,
  Code2,
  X,
  Sparkles
} from "lucide-react";

export default function ResearchPage() {
  const [data, setData] = useState<PaginatedResponse<ResearchPaper> | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [githubFilter, setGithubFilter] = useState<string>("all");
  const [minStars, setMinStars] = useState<number | undefined>(undefined);
  const [selectedPaper, setSelectedPaper] = useState<ResearchPaper | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const hasGit = githubFilter === "yes" ? true : (githubFilter === "no" ? false : undefined);
        const res = await api.getResearchPapers({
          page,
          page_size: 20,
          search: search || undefined,
          has_github: hasGit,
          min_stars: minStars
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
  }, [page, search, githubFilter, minStars]);

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Research Intelligence"
        subtitle="1,000 AI Research Papers & Open-Source Code Repositories"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Research" }]}
      />

      <div className="px-6 py-6 space-y-6 max-w-7xl mx-auto">
        {/* Controls Bar */}
        <div className="p-4 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-3 w-4 h-4 text-[#98A7BD]" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search title, author, model, dataset..."
              className="w-full pl-9 pr-4 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none focus:border-[#9275FF]"
            />
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* GitHub Repo Presence Filter */}
            <select
              value={githubFilter}
              onChange={(e) => {
                setGithubFilter(e.target.value);
                setPage(1);
              }}
              className="px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#9275FF]"
            >
              <option value="all">All Research Papers (1,000)</option>
              <option value="yes">With Associated GitHub Code (135)</option>
              <option value="no">Without Code Repository (865)</option>
            </select>

            {/* Min Stars Filter */}
            <select
              value={minStars !== undefined ? minStars.toString() : ""}
              onChange={(e) => {
                setMinStars(e.target.value ? parseInt(e.target.value) : undefined);
                setPage(1);
              }}
              className="px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#9275FF]"
            >
              <option value="">Any Star Count</option>
              <option value="5">★ 5+ Stars</option>
              <option value="10">★ 10+ Stars</option>
              <option value="25">★ 25+ Stars</option>
              <option value="50">★ 50+ Stars</option>
            </select>

            <div className="text-xs font-mono text-[#98A7BD]">
              {data ? `${data.total.toLocaleString()} papers` : "Loading..."}
            </div>
          </div>
        </div>

        {/* Papers List */}
        {loading ? (
          <div className="py-24 text-center">
            <Loader2 className="w-8 h-8 text-[#9275FF] animate-spin mx-auto mb-2" />
            <span className="text-xs font-mono text-[#98A7BD]">Querying research papers index...</span>
          </div>
        ) : (
          <div className="space-y-3">
            {data?.items.map((paper) => {
              const hasRepo = Boolean(paper.github_url);
              return (
                <div
                  key={paper.id}
                  onClick={() => setSelectedPaper(paper)}
                  className={`p-4 rounded-2xl bg-[#111A2E] border transition-all cursor-pointer group flex flex-col md:flex-row md:items-center justify-between gap-4 ${
                    hasRepo
                      ? "border-[#1E2D4A] hover:border-[#9275FF]/60 shadow-sm"
                      : "border-[#1E2D4A]/60 opacity-90 hover:opacity-100 hover:border-[#1E2D4A]"
                  }`}
                >
                  <div className="space-y-1.5 flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      {hasRepo ? (
                        <Badge variant="emerald" className="gap-1">
                          <Code2 className="w-3 h-3" />
                          Code Available
                        </Badge>
                      ) : (
                        <Badge variant="slate">Theory / No Code</Badge>
                      )}
                      <span className="text-[11px] font-mono text-[#98A7BD]">
                        Published {new Date(paper.published_date).toLocaleDateString()}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white group-hover:text-[#9275FF] transition-colors leading-snug">
                      {paper.title}
                    </h3>

                    <p className="text-xs text-[#98A7BD] truncate">
                      {paper.authors.length > 0 ? paper.authors.join(", ") : "Unspecified Authors"}
                    </p>
                  </div>

                  {/* GitHub Metrics & Links */}
                  <div className="flex items-center gap-4 flex-shrink-0" onClick={(e) => e.stopPropagation()}>
                    {paper.github_stars !== null && (
                      <div className="text-right">
                        <div className="flex items-center gap-1 font-mono font-bold text-sm text-[#F3B84B]">
                          <Star className="w-4 h-4 fill-[#F3B84B]" />
                          <span>{paper.github_stars.toLocaleString()}</span>
                        </div>
                        {paper.github_stars_retrieved_at && (
                          <div className="text-[10px] text-[#98A7BD] font-mono" title={`Retrieved: ${paper.github_stars_retrieved_at}`}>
                            Observed {new Date(paper.github_stars_retrieved_at).toLocaleDateString()}
                          </div>
                        )}
                      </div>
                    )}

                    <div className="flex items-center gap-2">
                      <a
                        href={paper.paper_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-3 py-1.5 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs font-medium text-white flex items-center gap-1"
                      >
                        Paper <ExternalLink className="w-3 h-3 text-[#4F8CFF]" />
                      </a>
                      {paper.github_url && (
                        <a
                          href={paper.github_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-3 py-1.5 rounded-xl bg-[#35C98A]/15 hover:bg-[#35C98A]/25 border border-[#35C98A]/40 text-xs font-semibold text-[#35C98A] flex items-center gap-1"
                        >
                          <GitBranch className="w-3 h-3" />
                          Code <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
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

        {/* Paper Detail Modal */}
        {selectedPaper && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
            <div className="w-full max-w-2xl rounded-2xl bg-[#0B1020] border border-[#1E2D4A] shadow-2xl p-6 relative space-y-4">
              <button
                onClick={() => setSelectedPaper(null)}
                className="absolute top-4 right-4 p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A]"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex items-center gap-2">
                {selectedPaper.github_url ? (
                  <Badge variant="emerald">Open-Source Code Verified</Badge>
                ) : (
                  <Badge variant="slate">Theory Document</Badge>
                )}
                <span className="text-xs font-mono text-[#98A7BD]">arXiv Discovery</span>
              </div>

              <h3 className="text-base font-bold text-white leading-snug">{selectedPaper.title}</h3>

              <div className="text-xs text-[#98A7BD]">
                <span className="font-semibold text-white block mb-0.5">Authors:</span>
                {selectedPaper.authors.join(", ")}
              </div>

              <div className="grid grid-cols-2 gap-3 py-3 border-y border-[#1E2D4A] text-xs">
                <div>
                  <span className="text-[#98A7BD] block mb-1">Publication Date</span>
                  <span className="font-mono text-white">{new Date(selectedPaper.published_date).toLocaleDateString()}</span>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-1">GitHub Stars</span>
                  <span className="font-mono font-bold text-[#F3B84B]">
                    {selectedPaper.github_stars !== null ? `★ ${selectedPaper.github_stars}` : "Not applicable (No repository)"}
                  </span>
                </div>
                {selectedPaper.github_stars_retrieved_at && (
                  <div className="col-span-2">
                    <span className="text-[#98A7BD] block mb-0.5">Observation Timestamp (Traceability Guarantee):</span>
                    <span className="font-mono text-[#35C98A] text-[11px]">{selectedPaper.github_stars_retrieved_at}</span>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between pt-2">
                <a
                  href={selectedPaper.paper_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs text-white flex items-center gap-1.5"
                >
                  Read on arXiv <ExternalLink className="w-3.5 h-3.5" />
                </a>
                {selectedPaper.github_url && (
                  <a
                    href={selectedPaper.github_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-4 py-2 rounded-xl bg-[#35C98A] hover:bg-[#28B87B] text-xs font-semibold text-black flex items-center gap-1.5"
                  >
                    View Repository on GitHub <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
