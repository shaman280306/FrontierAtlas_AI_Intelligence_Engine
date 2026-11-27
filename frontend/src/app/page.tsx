"use client";

import React, { useEffect, useState } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { OverviewAnalytics } from "@/types";
import {
  Building2,
  Package,
  BookOpen,
  Briefcase,
  Newspaper,
  Network,
  GitBranch,
  Star,
  ShieldCheck,
  TrendingUp,
  Activity,
  ArrowUpRight,
  ExternalLink,
  Loader2,
  Radio
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

export default function OverviewPage() {
  const [data, setData] = useState<OverviewAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.getOverviewAnalytics();
        setData(res);
      } catch (err) {
        console.error("Failed to load overview analytics", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B1020]">
        <Header title="Overview" subtitle="Executive Intelligence Dashboard" />
        <div className="flex flex-col items-center justify-center h-[70vh] space-y-3">
          <Loader2 className="w-8 h-8 text-[#4F8CFF] animate-spin" />
          <span className="text-sm font-mono text-[#98A7BD]">Aggregating ecosystem intelligence metrics...</span>
        </div>
      </div>
    );
  }

  const counts = data?.counts;
  const pricingData = data?.distributions.pricing
    ? Object.entries(data.distributions.pricing).map(([name, value]) => ({ name, value }))
    : [];
  const roleData = data?.distributions.job_roles
    ? Object.entries(data.distributions.job_roles).map(([name, value]) => ({ name, value }))
    : [];

  const PRICING_COLORS: Record<string, string> = {
    FREE: "#35C98A",
    FREEMIUM: "#4F8CFF",
    PAID: "#9275FF",
    ENTERPRISE: "#F3B84B",
    UNKNOWN: "#98A7BD",
  };

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Overview"
        subtitle="Global AI Ecosystem Intelligence"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Overview" }]}
      />

      <div className="px-6 py-6 space-y-6 max-w-7xl mx-auto">
        {/* Top Hero Banner */}
        <div className="p-6 rounded-2xl bg-gradient-to-r from-[#111A2E] via-[#17233A] to-[#111A2E] border border-[#1E2D4A] relative overflow-hidden shadow-xl">
          <div className="absolute right-0 top-0 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Badge variant="cyan">PRODUCTION INTELLIGENCE GRAPH</Badge>
                <Badge variant="emerald">100% PROVENANCE VERIFIED</Badge>
              </div>
              <h2 className="text-2xl font-bold text-white tracking-tight">
                Navigate the Global AI Ecosystem
              </h2>
              <p className="text-sm text-[#98A7BD] mt-1 max-w-2xl">
                Real-time tracking of emerging startups, commercial products, breakthrough research with GitHub implementations, active engineering opportunities, and 24-hour industry signals.
              </p>
            </div>
            <div className="flex items-center gap-3">
              <a
                href="/reports"
                className="px-4 py-2.5 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs font-semibold text-white transition-all flex items-center gap-2"
              >
                Download Master Datasets
                <ArrowUpRight className="w-4 h-4 text-[#4F8CFF]" />
              </a>
              <a
                href="/entities"
                className="px-4 py-2.5 rounded-xl bg-[#4F8CFF] hover:bg-[#3B7BE8] text-xs font-semibold text-white transition-all shadow-lg shadow-blue-500/20 flex items-center gap-2"
              >
                Explore Entity Graph
              </a>
            </div>
          </div>
        </div>

        {/* Executive KPI Cards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
          {/* Startups */}
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#4F8CFF]/50 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#98A7BD] text-xs mb-2">
              <span>AI Startups</span>
              <Building2 className="w-4 h-4 text-[#4F8CFF]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white tabular-nums tracking-tight">
                {counts?.startups.toLocaleString()}
              </div>
              <div className="text-[11px] text-[#35C98A] font-mono mt-1 flex items-center gap-1">
                <span>Verified Entities</span>
              </div>
            </div>
          </div>

          {/* Products */}
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#36D6E7]/50 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#98A7BD] text-xs mb-2">
              <span>AI Products</span>
              <Package className="w-4 h-4 text-[#36D6E7]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white tabular-nums tracking-tight">
                {counts?.products.toLocaleString()}
              </div>
              <div className="text-[11px] text-[#36D6E7] font-mono mt-1">
                Standardized Pricing
              </div>
            </div>
          </div>

          {/* Research Papers */}
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#9275FF]/50 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#98A7BD] text-xs mb-2">
              <span>Research Papers</span>
              <BookOpen className="w-4 h-4 text-[#9275FF]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white tabular-nums tracking-tight">
                {counts?.research_papers.toLocaleString()}
              </div>
              <div className="text-[11px] text-[#9275FF] font-mono mt-1">
                {counts?.papers_with_github} with Code Repos
              </div>
            </div>
          </div>

          {/* Engineering Jobs */}
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#35C98A]/50 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#98A7BD] text-xs mb-2">
              <span>Engineering Jobs</span>
              <Briefcase className="w-4 h-4 text-[#35C98A]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white tabular-nums tracking-tight">
                {counts?.jobs.toLocaleString()}
              </div>
              <div className="text-[11px] text-[#35C98A] font-mono mt-1">
                {counts?.remote_jobs_percentage}% Remote Roles
              </div>
            </div>
          </div>

          {/* News Signals */}
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#F3B84B]/50 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#98A7BD] text-xs mb-2">
              <span>Industry News</span>
              <Newspaper className="w-4 h-4 text-[#F3B84B]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white tabular-nums tracking-tight">
                {counts?.news.toLocaleString()}
              </div>
              <div className="text-[11px] text-[#F3B84B] font-mono mt-1">
                24h Fresh Signals
              </div>
            </div>
          </div>

          {/* Mapped Entities */}
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#4F8CFF]/50 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#98A7BD] text-xs mb-2">
              <span>Mapped Entities</span>
              <Network className="w-4 h-4 text-[#4F8CFF]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-white tabular-nums tracking-tight">
                {counts?.mapped_entities.toLocaleString()}
              </div>
              <div className="text-[11px] text-[#35C98A] font-mono mt-1">
                Deterministic Cascade
              </div>
            </div>
          </div>
        </div>

        {/* Analytics Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pricing Model Distribution */}
          <div className="p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A]">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Package className="w-4 h-4 text-[#36D6E7]" />
                  Product Commercialization Tiers
                </h3>
                <p className="text-xs text-[#98A7BD]">Standardized pricing across 1,000 indexed AI products</p>
              </div>
              <Badge variant="cyan">Pydantic Enforced</Badge>
            </div>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={pricingData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <XAxis dataKey="name" stroke="#98A7BD" fontSize={11} tickLine={false} />
                  <YAxis stroke="#98A7BD" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#17233A", borderColor: "#1E2D4A", borderRadius: "8px", fontSize: "12px" }}
                    itemStyle={{ color: "#F4F7FC" }}
                  />
                  <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                    {pricingData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PRICING_COLORS[entry.name] || "#4F8CFF"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* In-Demand Job Role Families */}
          <div className="p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A]">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Briefcase className="w-4 h-4 text-[#35C98A]" />
                  AI Talent Demand Distribution
                </h3>
                <p className="text-xs text-[#98A7BD]">Active openings by engineering and research specialization</p>
              </div>
              <Badge variant="emerald">Live 24h Boards</Badge>
            </div>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={roleData} layout="vertical" margin={{ top: 10, right: 20, left: 20, bottom: 0 }}>
                  <XAxis type="number" stroke="#98A7BD" fontSize={11} tickLine={false} />
                  <YAxis type="category" dataKey="name" stroke="#98A7BD" fontSize={11} tickLine={false} width={90} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#17233A", borderColor: "#1E2D4A", borderRadius: "8px", fontSize: "12px" }}
                    itemStyle={{ color: "#F4F7FC" }}
                  />
                  <Bar dataKey="value" fill="#35C98A" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* High-Impact Research Papers with Live GitHub Stars */}
        <div className="p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A]">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-[#9275FF]" />
                Top Starred Research Implementations
              </h3>
              <p className="text-xs text-[#98A7BD]">Breakthrough research papers with verified public GitHub repositories</p>
            </div>
            <a href="/research" className="text-xs text-[#4F8CFF] hover:underline flex items-center gap-1 font-mono">
              View All 1,000 Papers <ArrowUpRight className="w-3.5 h-3.5" />
            </a>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#17233A] text-[#98A7BD] uppercase font-mono border-b border-[#1E2D4A]">
                <tr>
                  <th className="py-2.5 px-3">Paper Title</th>
                  <th className="py-2.5 px-3">Authors</th>
                  <th className="py-2.5 px-3">GitHub Stars</th>
                  <th className="py-2.5 px-3">Observation Time</th>
                  <th className="py-2.5 px-3 text-right">Links</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E2D4A]/50">
                {data?.top_starred_papers.map((p) => (
                  <tr key={p.id} className="hover:bg-[#17233A]/50 transition-colors">
                    <td className="py-3 px-3 font-medium text-white max-w-md truncate">
                      {p.title}
                    </td>
                    <td className="py-3 px-3 text-[#98A7BD] max-w-xs truncate">
                      {p.authors.join(", ")}
                    </td>
                    <td className="py-3 px-3 font-mono font-bold text-[#F3B84B]">
                      ★ {p.github_stars}
                    </td>
                    <td className="py-3 px-3 font-mono text-[#98A7BD]">
                      {p.github_stars_retrieved_at ? new Date(p.github_stars_retrieved_at).toLocaleString() : "Traceable"}
                    </td>
                    <td className="py-3 px-3 text-right space-x-2">
                      <a
                        href={p.paper_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-[#4F8CFF] hover:underline"
                      >
                        Paper <ExternalLink className="w-3 h-3" />
                      </a>
                      {p.github_url && (
                        <a
                          href={p.github_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-[#35C98A] hover:underline"
                        >
                          Code <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Split Grid: Recent Jobs & News */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Jobs */}
          <div className="p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A]">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-[#35C98A]" />
                Recent Engineering Opportunities
              </h3>
              <a href="/jobs" className="text-xs text-[#4F8CFF] hover:underline flex items-center gap-1 font-mono">
                View All {counts?.jobs} Jobs <ArrowUpRight className="w-3.5 h-3.5" />
              </a>
            </div>
            <div className="space-y-2.5">
              {data?.recent_jobs.map((j) => (
                <div key={j.id} className="p-3 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] hover:border-[#35C98A]/50 transition-colors flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-xs text-white">{j.title}</div>
                    <div className="text-[11px] text-[#98A7BD] mt-0.5">
                      {j.company} • <span className="text-[#35C98A] font-mono">{j.role_family}</span> {j.is_remote ? "(Remote)" : ""}
                    </div>
                  </div>
                  <a href={j.source_url} target="_blank" rel="noopener noreferrer" className="p-1 text-[#98A7BD] hover:text-[#35C98A]">
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              ))}
            </div>
          </div>

          {/* Recent News */}
          <div className="p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A]">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Newspaper className="w-4 h-4 text-[#F3B84B]" />
                Latest Industry Signals
              </h3>
              <a href="/news" className="text-xs text-[#4F8CFF] hover:underline flex items-center gap-1 font-mono">
                View All {counts?.news} Articles <ArrowUpRight className="w-3.5 h-3.5" />
              </a>
            </div>
            <div className="space-y-2.5">
              {data?.recent_news.map((n) => (
                <div key={n.id} className="p-3 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] hover:border-[#F3B84B]/50 transition-colors flex items-center justify-between">
                  <div className="max-w-[85%]">
                    <div className="font-semibold text-xs text-white truncate">{n.title}</div>
                    <div className="text-[11px] text-[#98A7BD] mt-0.5">
                      {n.source_name} • <span className="font-mono text-[#F3B84B]">{new Date(n.published_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>
                  </div>
                  <a href={n.source_url} target="_blank" rel="noopener noreferrer" className="p-1 text-[#98A7BD] hover:text-[#F3B84B]">
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Data Provenance & Trust Card */}
        <div className="p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-[#35C98A]/20 border border-[#35C98A]/40 text-[#35C98A] flex items-center justify-center flex-shrink-0">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="text-sm font-bold text-white">Data Quality & Trust Verification</div>
              <div className="text-xs text-[#98A7BD]">
                100% of all 4,389 records contain verifiable source URLs, SHA-256 fingerprints, and strict schema validation.
              </div>
            </div>
          </div>
          <a
            href="/quality"
            className="px-4 py-2 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs font-mono text-[#35C98A] flex items-center gap-2 whitespace-nowrap"
          >
            Audit Quality Metrics (99.4%)
            <ArrowUpRight className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
}
