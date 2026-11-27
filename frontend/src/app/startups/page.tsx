"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { Startup, PaginatedResponse } from "@/types";
import {
  Building2,
  Search,
  Filter,
  ExternalLink,
  Users,
  Globe,
  Loader2,
  ChevronLeft,
  ChevronRight,
  X,
  ShieldCheck,
  Calendar
} from "lucide-react";

export default function StartupsPage() {
  const [data, setData] = useState<PaginatedResponse<Startup> | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [selectedSource, setSelectedSource] = useState("");
  const [employeeFilter, setEmployeeFilter] = useState<string>("all");
  const [sources, setSources] = useState<string[]>([]);
  const [selectedStartup, setSelectedStartup] = useState<Startup | null>(null);

  // Load sources
  useEffect(() => {
    api.getStartupSources().then((res) => setSources(res.sources)).catch(console.error);
  }, []);

  // Fetch startups on filter change
  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const hasEmp = employeeFilter === "yes" ? true : (employeeFilter === "no" ? false : undefined);
        const res = await api.getStartups({
          page,
          page_size: 20,
          search: search || undefined,
          source: selectedSource || undefined,
          has_employees: hasEmp
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
  }, [page, search, selectedSource, employeeFilter]);

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="AI Startups"
        subtitle="1,000 Verified AI Companies & Organizations"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Startups" }]}
      />

      <div className="px-6 py-6 space-y-6 max-w-7xl mx-auto">
        {/* Controls Header */}
        <div className="p-4 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] flex flex-col md:flex-row md:items-center justify-between gap-4">
          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-3 w-4 h-4 text-[#98A7BD]" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search canonical name, alias, description..."
              className="w-full pl-9 pr-4 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none focus:border-[#4F8CFF]"
            />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Source Filter */}
            <select
              value={selectedSource}
              onChange={(e) => {
                setSelectedSource(e.target.value);
                setPage(1);
              }}
              className="px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#4F8CFF]"
            >
              <option value="">All Ingestion Sources</option>
              {sources.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>

            {/* Employee Filter */}
            <select
              value={employeeFilter}
              onChange={(e) => {
                setEmployeeFilter(e.target.value);
                setPage(1);
              }}
              className="px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#4F8CFF]"
            >
              <option value="all">All Employee Sizes</option>
              <option value="yes">Known Employee Count</option>
              <option value="no">Unreported / Unspecified</option>
            </select>

            {/* Total Results Count */}
            <div className="text-xs font-mono text-[#98A7BD]">
              {data ? `${data.total.toLocaleString()} startups` : "Loading..."}
            </div>
          </div>
        </div>

        {/* Startups Table & Cards */}
        {loading ? (
          <div className="py-24 text-center">
            <Loader2 className="w-8 h-8 text-[#4F8CFF] animate-spin mx-auto mb-2" />
            <span className="text-xs font-mono text-[#98A7BD]">Loading startups directory...</span>
          </div>
        ) : (
          <div className="rounded-2xl bg-[#111A2E] border border-[#1E2D4A] overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#17233A] text-[#98A7BD] uppercase font-mono border-b border-[#1E2D4A]">
                  <tr>
                    <th className="py-3 px-4">Canonical Entity</th>
                    <th className="py-3 px-4">Raw Name</th>
                    <th className="py-3 px-4">Ingestion Source</th>
                    <th className="py-3 px-4">Employees</th>
                    <th className="py-3 px-4">Collection Date</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1E2D4A]/50">
                  {data?.items.map((startup) => (
                    <tr
                      key={startup.id}
                      onClick={() => setSelectedStartup(startup)}
                      className="hover:bg-[#17233A]/60 transition-colors cursor-pointer group"
                    >
                      <td className="py-3 px-4 font-semibold text-white flex items-center gap-2">
                        <Building2 className="w-4 h-4 text-[#4F8CFF] flex-shrink-0" />
                        <span className="group-hover:text-[#4F8CFF] transition-colors">{startup.canonical_name}</span>
                      </td>
                      <td className="py-3 px-4 text-[#98A7BD] font-mono">
                        {startup.raw_name}
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded bg-[#17233A] text-[11px] text-[#36D6E7] border border-[#1E2D4A]">
                          {startup.source_name}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-mono">
                        {startup.employee_count !== null ? (
                          <span className="text-[#35C98A] font-semibold">{startup.employee_count.toLocaleString()}</span>
                        ) : (
                          <span className="text-[#60728F] italic">Unknown</span>
                        )}
                      </td>
                      <td className="py-3 px-4 font-mono text-[#98A7BD]">
                        {new Date(startup.collected_at).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-4 text-right" onClick={(e) => e.stopPropagation()}>
                        <a
                          href={startup.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-[#4F8CFF] hover:underline"
                        >
                          Source <ExternalLink className="w-3 h-3" />
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            {data && data.total_pages > 1 && (
              <div className="p-4 bg-[#111A2E] border-t border-[#1E2D4A] flex items-center justify-between text-xs">
                <span className="text-[#98A7BD]">
                  Showing page <span className="text-white font-mono">{data.page}</span> of{" "}
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
        )}

        {/* Startup Detail Drawer / Modal */}
        {selectedStartup && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
            <div className="w-full max-w-xl rounded-2xl bg-[#0B1020] border border-[#1E2D4A] shadow-2xl p-6 relative space-y-4">
              <button
                onClick={() => setSelectedStartup(null)}
                className="absolute top-4 right-4 p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A]"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex items-center gap-3">
                <div className="p-3 rounded-xl bg-[#4F8CFF]/15 border border-[#4F8CFF]/30 text-[#4F8CFF]">
                  <Building2 className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">{selectedStartup.canonical_name}</h3>
                  <p className="text-xs font-mono text-[#98A7BD]">Raw Name: {selectedStartup.raw_name}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 py-3 border-y border-[#1E2D4A] text-xs">
                <div>
                  <span className="text-[#98A7BD] block mb-1">Ingestion Source</span>
                  <span className="font-semibold text-white">{selectedStartup.source_name}</span>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-1">Employee Count</span>
                  <span className="font-semibold text-white">
                    {selectedStartup.employee_count !== null
                      ? `${selectedStartup.employee_count} employees`
                      : "Unreported (preserves null)"}
                  </span>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-1">Fingerprint (SHA-256)</span>
                  <span className="font-mono text-[10px] text-[#98A7BD] break-all">{selectedStartup.fingerprint}</span>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-1">Collection Timestamp</span>
                  <span className="font-mono text-white">{new Date(selectedStartup.collected_at).toLocaleString()}</span>
                </div>
              </div>

              {selectedStartup.description && (
                <div>
                  <h4 className="text-xs font-semibold text-[#98A7BD] uppercase mb-1">Description</h4>
                  <p className="text-xs text-[#F4F7FC] leading-relaxed bg-[#111A2E] p-3 rounded-xl border border-[#1E2D4A]">
                    {selectedStartup.description}
                  </p>
                </div>
              )}

              <div className="flex items-center justify-between pt-2">
                <a
                  href={`/entities?name=${encodeURIComponent(selectedStartup.canonical_name)}`}
                  className="px-4 py-2 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs text-white"
                >
                  View in Entity Graph
                </a>
                <a
                  href={selectedStartup.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-xl bg-[#4F8CFF] hover:bg-[#3B7BE8] text-xs font-medium text-white flex items-center gap-1.5"
                >
                  Visit Verified Source <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
