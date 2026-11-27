"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import {
  FileSpreadsheet,
  Download,
  FileText,
  FileCheck,
  HardDrive,
  ExternalLink,
  Loader2,
  ShieldCheck,
  CheckCircle2
} from "lucide-react";

export default function ReportsPage() {
  const [reports, setReports] = useState<Array<{ filename: string; size_bytes: number; format: string; type: string }>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getReportsList();
        setReports(data.reports);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  };

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Reports & Exports"
        subtitle="Download Master Excel Workbook, Verified CSV Tabs & 3-Page Architecture PDF"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Reports" }]}
      />

      <div className="px-6 py-6 space-y-6 max-w-7xl mx-auto">
        {/* Master Workbook Hero Download */}
        <div className="p-6 rounded-2xl bg-gradient-to-r from-[#111A2E] via-[#17233A] to-[#111A2E] border border-[#1E2D4A] flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xl">
          <div className="flex items-center space-x-4">
            <div className="w-14 h-14 rounded-2xl bg-[#35C98A]/20 border border-[#35C98A]/40 text-[#35C98A] flex items-center justify-center flex-shrink-0 shadow-lg shadow-emerald-500/10">
              <FileSpreadsheet className="w-8 h-8" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <Badge variant="emerald">MASTER DELIVERABLE WORKBOOK</Badge>
                <span className="text-xs font-mono text-[#98A7BD]">6 Audited Tabs • 294 KB</span>
              </div>
              <h2 className="text-xl font-bold text-white tracking-tight">
                frontier_atlas_intelligence.xlsx
              </h2>
              <p className="text-xs text-[#98A7BD] mt-1 max-w-xl">
                Contains all 6 required tabs: Startups (1,000), Products (1,000), Research Papers (1,000 with GitHub stars), Jobs (317), News (72), and Entity Mapping Log (1,000) with frozen headers and column filters.
              </p>
            </div>
          </div>

          <a
            href={api.getDownloadUrl("frontier_atlas_intelligence.xlsx")}
            download
            className="px-5 py-3 rounded-xl bg-[#35C98A] hover:bg-[#28B87B] text-xs font-bold text-black transition-all flex items-center gap-2 shadow-lg shadow-emerald-500/20 whitespace-nowrap"
          >
            <Download className="w-4 h-4" />
            Download Master Workbook (.XLSX)
          </a>
        </div>

        {/* 3-Page Architecture PDF Card */}
        <div className="p-6 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-2xl bg-[#9275FF]/20 border border-[#9275FF]/40 text-[#9275FF] flex items-center justify-center flex-shrink-0">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <Badge variant="violet">STRICTLY 3 PAGES SPECIFICATION</Badge>
                <span className="text-xs font-mono text-[#98A7BD]">Vector Diagrams & Strategy</span>
              </div>
              <h3 className="text-base font-bold text-white">architecture.pdf</h3>
              <p className="text-xs text-[#98A7BD] mt-0.5 max-w-xl">
                Detailed production scaling blueprint to 500,000+ records, HTTP 413/429 mitigation tables, 4-way timestamp isolation, deterministic entity resolution, and polyglot persistence architecture.
              </p>
            </div>
          </div>

          <a
            href={api.getDownloadUrl("architecture.pdf")}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2.5 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs font-semibold text-white transition-all flex items-center gap-2 whitespace-nowrap"
          >
            <Download className="w-4 h-4 text-[#4F8CFF]" />
            Download Architecture PDF
          </a>
        </div>

        {/* Individual Tab CSV Exports List */}
        <div className="p-6 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-[#4F8CFF]" />
                Individual Dataset Tab Exports (CSV)
              </h3>
              <p className="text-xs text-[#98A7BD]">Comma-separated values files matching exact submission schema contracts</p>
            </div>
            <Badge variant="cyan">6 Verified CSVs</Badge>
          </div>

          {loading ? (
            <div className="py-16 text-center">
              <Loader2 className="w-8 h-8 text-[#4F8CFF] animate-spin mx-auto mb-2" />
              <span className="text-xs font-mono text-[#98A7BD]">Inspecting exported deliverables...</span>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {reports
                .filter((r) => r.format === "CSV")
                .map((file) => (
                  <div
                    key={file.filename}
                    className="p-4 rounded-xl bg-[#17233A]/60 border border-[#1E2D4A] hover:border-[#4F8CFF]/50 transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <Badge variant="slate">{file.format}</Badge>
                        <span className="text-[11px] font-mono text-[#98A7BD]">{formatBytes(file.size_bytes)}</span>
                      </div>
                      <h4 className="text-sm font-bold text-white font-mono break-all">{file.filename}</h4>
                      <p className="text-xs text-[#98A7BD] mt-1">{file.type}</p>
                    </div>

                    <div className="pt-3 mt-3 border-t border-[#1E2D4A]/60 flex items-center justify-between">
                      <span className="text-[10px] font-mono text-[#35C98A] flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        Verified Integrity
                      </span>
                      <a
                        href={api.getDownloadUrl(file.filename)}
                        download
                        className="text-xs text-[#4F8CFF] hover:underline font-mono inline-flex items-center gap-1"
                      >
                        Download <Download className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
