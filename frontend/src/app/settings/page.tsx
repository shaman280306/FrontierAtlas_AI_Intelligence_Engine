"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api, API_BASE } from "@/lib/api";
import {
  Settings,
  Server,
  Database,
  Cpu,
  Shield,
  Key,
  ExternalLink,
  Code2,
  CheckCircle2,
  Loader2
} from "lucide-react";

export default function SettingsPage() {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getHealth()
      .then((data) => setHealth(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Settings & System Configuration"
        subtitle="Platform Architecture, API Integration & LLM Provider Chain"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Settings" }]}
      />

      <div className="px-3 sm:px-6 py-4 sm:py-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto">
        {/* Backend & Environment Status */}
        <div className="p-4 sm:p-6 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Server className="w-4 h-4 text-[#4F8CFF]" />
              Backend Service Architecture
            </h3>
            <Badge variant="emerald">Operational</Badge>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 text-xs">
            <div className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] space-y-1">
              <span className="text-[#98A7BD] block">FastAPI Runtime</span>
              <span className="font-semibold text-white text-sm">Python 3.11.9 (Asynchronous)</span>
              <span className="text-[11px] font-mono text-[#35C98A] block">Uvicorn ASGI Engine</span>
            </div>

            <div className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] space-y-1">
              <span className="text-[#98A7BD] block">Primary Persistence</span>
              <span className="font-semibold text-white text-sm">SQLite (Dev) / PostgreSQL (Prod)</span>
              <span className="text-[11px] font-mono text-[#36D6E7] block">SQLAlchemy ORM + Unique SHA-256 FP</span>
            </div>

            <div className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] space-y-1 sm:col-span-2 lg:col-span-1">
              <span className="text-[#98A7BD] block">Frontend Framework</span>
              <span className="font-semibold text-white text-sm">Next.js 14 (App Router) + React 18</span>
              <span className="text-[11px] font-mono text-[#9275FF] block">TypeScript Strict + Tailwind CSS</span>
            </div>
          </div>
        </div>

        {/* LLM Fallback Chain Configuration */}
        <div className="p-4 sm:p-6 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Cpu className="w-4 h-4 text-[#9275FF]" />
                Multi-Tier LLM Extraction Fallback Chain
              </h3>
              <p className="text-xs text-[#98A7BD]">Resilient 3-tier cascade with HTTP 413 chunking and 429 jittered backoff</p>
            </div>
            <Badge variant="violet" className="self-start sm:self-auto">Fault Tolerant</Badge>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
            <div className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#4F8CFF]">Tier 1 (Primary)</span>
                <span className="text-[10px] font-mono text-[#35C98A]">1M Context</span>
              </div>
              <div className="text-sm font-bold text-white">Gemini Flash</div>
              <p className="text-[11px] text-[#98A7BD]">Model: gemini-2.0-flash. High throughput structured JSON extraction.</p>
            </div>

            <div className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#36D6E7]">Tier 2 (Secondary)</span>
                <span className="text-[10px] font-mono text-[#36D6E7]">LPU Speed</span>
              </div>
              <div className="text-sm font-bold text-white">Groq Llama 3</div>
              <p className="text-[11px] text-[#98A7BD]">Model: llama-3.3-70b-versatile. Ultra low-latency fallback inference.</p>
            </div>

            <div className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#9275FF]">Tier 3 (Tertiary)</span>
                <span className="text-[10px] font-mono text-[#9275FF]">Deep Reasoning</span>
              </div>
              <div className="text-sm font-bold text-white">DeepSeek</div>
              <p className="text-[11px] text-[#98A7BD]">Model: deepseek-chat. Complex entity disambiguation and edge analysis.</p>
            </div>

            <div className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#35C98A]">Dead-Letter Storage</span>
                <span className="text-[10px] font-mono text-[#35C98A]">Zero Loss</span>
              </div>
              <div className="text-sm font-bold text-white">Local Queue</div>
              <p className="text-[11px] text-[#98A7BD]">Preserves raw document with requires_reprocessing=True flag.</p>
            </div>
          </div>
        </div>

        {/* API Documentation & Swagger */}
        <div className="p-4 sm:p-6 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Code2 className="w-4 h-4 text-[#35C98A]" />
                Interactive API Documentation & Contracts
              </h3>
              <p className="text-xs text-[#98A7BD]">Explore OpenAPI specifications and test live endpoints directly</p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <a
                href={`${API_BASE}/docs`}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1.5 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs font-mono text-[#4F8CFF] flex items-center gap-1.5"
              >
                Swagger UI <ExternalLink className="w-3 h-3" />
              </a>
              <a
                href={`${API_BASE}/redoc`}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1.5 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs font-mono text-[#36D6E7] flex items-center gap-1.5"
              >
                ReDoc <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          <div className="p-3 sm:p-4 rounded-xl bg-[#0B1020]/70 border border-[#1E2D4A] space-y-2 text-[11px] sm:text-xs font-mono overflow-x-auto">
            <div className="text-[#35C98A]">GET /api/v1/analytics/overview  — Live executive KPIs and distributions</div>
            <div className="text-[#4F8CFF]">GET /api/v1/startups            — Paginated and searchable startups directory</div>
            <div className="text-[#36D6E7]">GET /api/v1/products            — Commercial AI products with pricing filter</div>
            <div className="text-[#9275FF]">GET /api/v1/research-papers     — arXiv papers with verified GitHub stars</div>
            <div className="text-[#35C98A]">GET /api/v1/jobs                — 24-hour verified engineering openings</div>
            <div className="text-[#F3B84B]">GET /api/v1/news                — 24-hour technology news signals</div>
            <div className="text-[#36D6E7]">GET /api/v1/entities/{'{name}'}/graph — Node-and-edge entity graph</div>
            <div className="text-[#4F8CFF]">GET /api/v1/search?q={'{query}'}  — Global cross-entity search</div>
            <div className="text-[#9275FF]">POST /api/v1/ai/query           — Natural language grounded discovery</div>
          </div>
        </div>
      </div>
    </div>
  );
}
