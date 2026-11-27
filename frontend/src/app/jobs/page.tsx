"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { JobListing, PaginatedResponse } from "@/types";
import {
  Briefcase,
  Search,
  Filter,
  ExternalLink,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Globe2,
  Clock,
  Building,
  CheckCircle2
} from "lucide-react";

export default function JobsPage() {
  const [data, setData] = useState<PaginatedResponse<JobListing> | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [roleFamily, setRoleFamily] = useState("");
  const [selectedSource, setSelectedSource] = useState("");
  const [sources, setSources] = useState<string[]>([]);

  useEffect(() => {
    api.getJobSources().then((res) => setSources(res.sources)).catch(console.error);
  }, []);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await api.getJobs({
          page,
          page_size: 20,
          search: search || undefined,
          is_remote: remoteOnly ? true : undefined,
          role_family: roleFamily || undefined,
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
  }, [page, search, remoteOnly, roleFamily, selectedSource]);

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Engineering Opportunities"
        subtitle="317 Verified AI Roles Ingested Across 5 Job Boards"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Jobs" }]}
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
              placeholder="Search title, company, technology..."
              className="w-full pl-9 pr-4 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none focus:border-[#35C98A]"
            />
          </div>

          <div className="flex flex-col sm:flex-row flex-wrap items-stretch sm:items-center gap-2 sm:gap-3">
            {/* Role Family */}
            <select
              value={roleFamily}
              onChange={(e) => {
                setRoleFamily(e.target.value);
                setPage(1);
              }}
              className="w-full sm:w-auto px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#35C98A]"
            >
              <option value="">All Role Specializations</option>
              <option value="Engineering">Engineering</option>
              <option value="Machine Learning">Machine Learning</option>
              <option value="Data & Analytics">Data & Analytics</option>
              <option value="Product">Product</option>
              <option value="Research">Research</option>
              <option value="Other">Other</option>
            </select>

            {/* Source Job Board */}
            <select
              value={selectedSource}
              onChange={(e) => {
                setSelectedSource(e.target.value);
                setPage(1);
              }}
              className="w-full sm:w-auto px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#35C98A]"
            >
              <option value="">All 5 Job Boards</option>
              {sources.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>

            {/* Remote Toggle */}
            <label className="flex items-center justify-center sm:justify-start space-x-2 text-xs text-[#98A7BD] cursor-pointer bg-[#17233A] px-3 py-2 rounded-xl border border-[#1E2D4A]">
              <input
                type="checkbox"
                checked={remoteOnly}
                onChange={(e) => {
                  setRemoteOnly(e.target.checked);
                  setPage(1);
                }}
                className="rounded border-[#1E2D4A] text-[#35C98A] focus:ring-0"
              />
              <span className="text-[#F4F7FC]">Remote Only</span>
            </label>

            <div className="text-xs font-mono text-[#98A7BD] text-center sm:text-left">
              {data ? `${data.total.toLocaleString()} openings` : "Loading..."}
            </div>
          </div>
        </div>

        {/* Jobs List */}
        {loading ? (
          <div className="py-24 text-center">
            <Loader2 className="w-8 h-8 text-[#35C98A] animate-spin mx-auto mb-2" />
            <span className="text-xs font-mono text-[#98A7BD]">Filtering engineering opportunities...</span>
          </div>
        ) : (
          <div className="space-y-3">
            {data?.items.map((job) => (
              <div
                key={job.id}
                className="p-3.5 sm:p-4 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#35C98A]/50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4"
              >
                <div className="space-y-1 flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
                    <Badge variant={job.is_remote ? "emerald" : "slate"}>
                      {job.is_remote ? "Remote" : "On-site / Hybrid"}
                    </Badge>
                    <Badge variant="blue">{job.role_family}</Badge>
                    <span className="text-[11px] font-mono text-[#98A7BD]">
                      Board: {job.source_name}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-white hover:text-[#35C98A] transition-colors leading-snug">
                    {job.title}
                  </h3>

                  <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs text-[#98A7BD]">
                    <span className="text-white font-semibold flex items-center gap-1">
                      <Building className="w-3.5 h-3.5 text-[#98A7BD]" />
                      {job.company}
                    </span>
                    <span className="hidden sm:inline">•</span>
                    <span className="font-mono text-[#35C98A]">
                      Published: {new Date(job.date).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-3 flex-shrink-0 w-full sm:w-auto pt-2 sm:pt-0 border-t sm:border-t-0 border-[#1E2D4A]/60">
                  <a
                    href={job.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full sm:w-auto px-4 py-2 rounded-xl bg-[#35C98A] hover:bg-[#28B87B] text-xs font-semibold text-black transition-all flex items-center justify-center gap-1.5 shadow-md shadow-emerald-500/10"
                  >
                    Apply on {job.source_name} <ExternalLink className="w-3.5 h-3.5" />
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
      </div>
    </div>
  );
}
