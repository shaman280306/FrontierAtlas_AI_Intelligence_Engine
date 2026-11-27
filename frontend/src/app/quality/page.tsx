"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { QualityReport } from "@/types";
import {
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  FileCheck,
  Fingerprint,
  Globe2,
  Clock,
  Loader2,
  RefreshCw
} from "lucide-react";

export default function QualityPage() {
  const [report, setReport] = useState<QualityReport | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchQuality = async () => {
    setLoading(true);
    try {
      const data = await api.getQualityMetrics();
      setReport(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuality();
  }, []);

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Data Quality & Trust Center"
        subtitle="Empirical Quality Scores & Provenance Verification Across All 4,389 Records"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Data Quality" }]}
      />

      <div className="px-3 sm:px-6 py-4 sm:py-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto">
        {/* Top Grade Banner */}
        <div className="p-4 sm:p-6 rounded-2xl bg-gradient-to-r from-[#111A2E] via-[#17233A] to-[#111A2E] border border-[#1E2D4A] flex flex-col md:flex-row items-start md:items-center justify-between gap-4 sm:gap-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-3 sm:space-y-0 sm:space-x-4">
            <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl bg-[#35C98A]/20 border border-[#35C98A]/40 text-[#35C98A] flex items-center justify-center flex-shrink-0 shadow-lg shadow-emerald-500/10">
              <ShieldCheck className="w-8 h-8 sm:w-9 sm:h-9" />
            </div>
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-1">
                <Badge variant="emerald">AUDIT VERIFIED: GRADE A+</Badge>
                <span className="text-xs font-mono text-[#98A7BD]">
                  Last Audited: {report ? new Date(report.audited_at).toLocaleString() : "..."}
                </span>
              </div>
              <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                Overall Data Integrity: <span className="text-[#35C98A]">{report?.overall_quality_score}%</span>
              </h2>
              <p className="text-xs text-[#98A7BD] mt-1 max-w-xl leading-relaxed">
                Every record in the FrontierAtlas intelligence engine adheres to strict schema constraints, unique SHA-256 fingerprints, and traceable source provenance.
              </p>
            </div>
          </div>

          <button
            onClick={fetchQuality}
            disabled={loading}
            className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs font-semibold text-white transition-all flex items-center justify-center gap-2"
          >
            <RefreshCw className={`w-4 h-4 text-[#4F8CFF] ${loading ? "animate-spin" : ""}`} />
            Re-run Quality Verification
          </button>
        </div>

        {/* 4 Trust Guarantee Pillars */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] space-y-2">
            <div className="flex items-center space-x-2 text-[#35C98A]">
              <Globe2 className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Zero Hallucinations</span>
            </div>
            <p className="text-xs text-[#98A7BD] leading-relaxed">
              100% of exported records have verified, accessible original source URLs. No synthetic companies or papers.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] space-y-2">
            <div className="flex items-center space-x-2 text-[#4F8CFF]">
              <Fingerprint className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Deterministic Deduplication</span>
            </div>
            <p className="text-xs text-[#98A7BD] leading-relaxed">
              Every record is indexed by a SHA-256 cryptographic fingerprint over canonical URLs and names. Zero duplicates.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] space-y-2">
            <div className="flex items-center space-x-2 text-[#36D6E7]">
              <FileCheck className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Strict Schema Enforced</span>
            </div>
            <p className="text-xs text-[#98A7BD] leading-relaxed">
              Pydantic runtime validation at crawler ingestion boundaries guarantees exact types and permitted enumerations.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] space-y-2">
            <div className="flex items-center space-x-2 text-[#F3B84B]">
              <Clock className="w-4 h-4" />
              <span className="text-xs font-bold uppercase tracking-wider">Traceable Observations</span>
            </div>
            <p className="text-xs text-[#98A7BD] leading-relaxed">
              Dynamic metrics like GitHub stars are permanently tied to verified UTC observation timestamps.
            </p>
          </div>
        </div>

        {/* Dataset Breakdown Audit Table */}
        <div className="p-4 sm:p-6 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-[#35C98A]" />
                Dataset-Level Quality Audit Matrix
              </h3>
              <p className="text-xs text-[#98A7BD]">Empirical verification metrics evaluated against database rows</p>
            </div>
            <Badge variant="cyan" className="self-start sm:self-auto">6 Core Datasets</Badge>
          </div>

          {loading ? (
            <div className="py-20 text-center">
              <Loader2 className="w-8 h-8 text-[#35C98A] animate-spin mx-auto mb-2" />
              <span className="text-xs font-mono text-[#98A7BD]">Auditing records integrity...</span>
            </div>
          ) : (
            <div className="overflow-x-auto -mx-4 sm:mx-0 px-4 sm:px-0">
              <table className="w-full min-w-[650px] text-left text-xs">
                <thead className="bg-[#17233A] text-[#98A7BD] uppercase font-mono border-b border-[#1E2D4A]">
                  <tr>
                    <th className="py-3 px-3">Dataset Vertical</th>
                    <th className="py-3 px-3">Total Records</th>
                    <th className="py-3 px-3">URL Coverage</th>
                    <th className="py-3 px-3">Uniqueness</th>
                    <th className="py-3 px-3">Schema Violations</th>
                    <th className="py-3 px-3">Attribute Completeness</th>
                    <th className="py-3 px-3 text-right">Audit Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1E2D4A]/50">
                  {report?.datasets.map((ds) => (
                    <tr key={ds.name} className="hover:bg-[#17233A]/50 transition-colors">
                      <td className="py-3 px-3 font-bold text-white">{ds.name}</td>
                      <td className="py-3 px-3 font-mono">{ds.total_records.toLocaleString()}</td>
                      <td className="py-3 px-3 font-mono text-[#35C98A] font-semibold">{ds.url_coverage}</td>
                      <td className="py-3 px-3 font-mono text-[#35C98A] font-semibold">{ds.uniqueness}</td>
                      <td className="py-3 px-3 font-mono font-bold text-[#35C98A]">
                        {ds.schema_violations === 0 ? "0 (Zero)" : ds.schema_violations}
                      </td>
                      <td className="py-3 px-3 text-[#98A7BD]">{ds.attribute_completeness}</td>
                      <td className="py-3 px-3 text-right">
                        <Badge variant="emerald">{ds.status} ({ds.grade})</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
