"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { EntityGraph, EntityMappingLog, PaginatedResponse } from "@/types";
import {
  Network,
  Search,
  ExternalLink,
  Loader2,
  Building2,
  Package,
  BookOpen,
  Briefcase,
  Newspaper,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Info
} from "lucide-react";

export default function EntityExplorerPage() {
  const [selectedEntity, setSelectedEntity] = useState("OpenAI");
  const [graphData, setGraphData] = useState<EntityGraph | null>(null);
  const [graphLoading, setGraphLoading] = useState(false);
  const [topEntities, setTopEntities] = useState<Array<{ entity: string; products: number; papers: number; jobs: number; news: number; total_connections: number }>>([]);

  // Mapping Logs Table State
  const [activeTab, setActiveTab] = useState<"graph" | "logs">("graph");
  const [logData, setLogData] = useState<PaginatedResponse<EntityMappingLog> | null>(null);
  const [logPage, setLogPage] = useState(1);
  const [logSearch, setLogSearch] = useState("");
  const [logMethod, setLogMethod] = useState("");
  const [logsLoading, setLogsLoading] = useState(false);

  // Load top connected entities
  useEffect(() => {
    api.getTopConnectedEntities(20).then((res) => setTopEntities(res.entities)).catch(console.error);
  }, []);

  // Load graph for selected entity
  useEffect(() => {
    if (!selectedEntity) return;
    async function fetchGraph() {
      setGraphLoading(true);
      try {
        const data = await api.getEntityGraph(selectedEntity);
        setGraphData(data);
      } catch (err) {
        console.error(err);
      } finally {
        setGraphLoading(false);
      }
    }
    fetchGraph();
  }, [selectedEntity]);

  // Load mapping logs when on logs tab
  useEffect(() => {
    if (activeTab !== "logs") return;
    async function fetchLogs() {
      setLogsLoading(true);
      try {
        const data = await api.getEntityMappings({
          page: logPage,
          page_size: 20,
          search: logSearch || undefined,
          method: logMethod || undefined
        });
        setLogData(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLogsLoading(false);
      }
    }
    const timer = setTimeout(fetchLogs, 200);
    return () => clearTimeout(timer);
  }, [activeTab, logPage, logSearch, logMethod]);

  const getNodeColor = (type: string) => {
    switch (type) {
      case "entity":
        return "#4F8CFF"; // Electric blue
      case "startup":
        return "#36D6E7"; // Cyan
      case "product":
        return "#9275FF"; // Violet
      case "paper":
        return "#F3B84B"; // Amber
      case "job":
        return "#35C98A"; // Emerald
      case "news":
        return "#FF6B6B"; // Coral
      default:
        return "#98A7BD";
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="Global Entity Explorer"
        subtitle="Multi-Dimensional Graph of Connected Startups, Products, Research & Signals"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Entity Explorer" }]}
      />

      <div className="px-3 sm:px-6 py-4 sm:py-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto">
        {/* Navigation Tabs */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-[#1E2D4A] pb-3 gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setActiveTab("graph")}
              className={`px-3 sm:px-4 py-2 rounded-xl text-xs font-semibold transition-all flex items-center gap-2 ${
                activeTab === "graph"
                  ? "bg-[#4F8CFF] text-white shadow-lg shadow-blue-500/20"
                  : "bg-[#111A2E] text-[#98A7BD] hover:text-white border border-[#1E2D4A]"
              }`}
            >
              <Network className="w-4 h-4" />
              Interactive Relationship Graph
            </button>
            <button
              onClick={() => setActiveTab("logs")}
              className={`px-3 sm:px-4 py-2 rounded-xl text-xs font-semibold transition-all flex items-center gap-2 ${
                activeTab === "logs"
                  ? "bg-[#4F8CFF] text-white shadow-lg shadow-blue-500/20"
                  : "bg-[#111A2E] text-[#98A7BD] hover:text-white border border-[#1E2D4A]"
              }`}
            >
              <CheckCircle2 className="w-4 h-4" />
              Deterministic Resolution Logs (1,000)
            </button>
          </div>

          <Badge variant="cyan" className="self-start sm:self-auto">Multi-Vertical Graph Synthesis</Badge>
        </div>

        {activeTab === "graph" ? (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 sm:gap-6">
            {/* Left Sidebar: Top Connected Entities */}
            <div className="lg:col-span-1 space-y-4">
              <div className="p-3 sm:p-4 rounded-2xl bg-[#111A2E] border border-[#1E2D4A]">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-2 sm:mb-3">
                  Top Connected Entities
                </h3>
                <div className="flex flex-row overflow-x-auto gap-2 pb-2 lg:flex-col lg:overflow-x-visible lg:space-y-1.5 lg:pb-0 lg:max-h-[550px] lg:overflow-y-auto pr-1">
                  {topEntities.map((item) => {
                    const isSelected = selectedEntity.toLowerCase() === item.entity.toLowerCase();
                    return (
                      <button
                        key={item.entity}
                        onClick={() => setSelectedEntity(item.entity)}
                        className={`flex-shrink-0 lg:flex-shrink lg:w-full px-3 py-2 lg:p-2.5 rounded-xl text-left text-xs transition-all flex items-center justify-between gap-2 border ${
                          isSelected
                            ? "bg-[#17233A] text-white border-[#4F8CFF] shadow-sm shadow-blue-500/10"
                            : "bg-[#0B1020]/60 text-[#98A7BD] hover:text-white hover:bg-[#17233A]/50 border-transparent"
                        }`}
                      >
                        <span className="font-semibold truncate">{item.entity}</span>
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-[#111A2E] text-[#36D6E7] border border-[#1E2D4A]">
                          {item.total_connections} links
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Main Graph Canvas Area */}
            <div className="lg:col-span-3 space-y-4">
              <div className="p-4 sm:p-6 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] relative overflow-hidden flex flex-col justify-between min-h-[440px] sm:min-h-[550px]">
                {/* Graph Controls & Legend */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 sm:pb-4 border-b border-[#1E2D4A]/60 z-10">
                  <div>
                    <h3 className="text-base font-bold text-white flex items-center gap-2">
                      <Network className="w-5 h-5 text-[#4F8CFF]" />
                      Entity Graph: <span className="text-[#36D6E7]">{selectedEntity}</span>
                    </h3>
                    <p className="text-xs text-[#98A7BD]">
                      {graphData ? `${graphData.node_count} connected nodes across products, research, jobs and news` : "Computing links..."}
                    </p>
                  </div>

                  {/* Node Type Legend */}
                  <div className="flex flex-wrap items-center gap-2 text-[11px] font-mono text-[#98A7BD]">
                    <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-[#4F8CFF]" /> Entity</span>
                    <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-[#9275FF]" /> Product</span>
                    <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-[#F3B84B]" /> Research</span>
                    <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-[#35C98A]" /> Job</span>
                    <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-[#FF6B6B]" /> News</span>
                  </div>
                </div>

                {/* SVG Vector Graph Visualization */}
                {graphLoading ? (
                  <div className="flex-1 flex flex-col items-center justify-center py-20 space-y-2">
                    <Loader2 className="w-8 h-8 text-[#4F8CFF] animate-spin" />
                    <span className="text-xs font-mono text-[#98A7BD]">Traversing graph edges...</span>
                  </div>
                ) : (
                  <div className="flex-1 relative py-4 sm:py-6 flex items-center justify-center overflow-hidden">
                    <svg className="w-full h-[280px] sm:h-[400px]" viewBox="0 0 700 400" preserveAspectRatio="xMidYMid meet">
                      {/* Radial layout calculation */}
                      {(() => {
                        if (!graphData || graphData.nodes.length <= 1) return null;

                        const cx = 350;
                        const cy = 200;
                        const radius = 150;
                        const nonRootNodes = graphData.nodes.filter((n) => !n.metadata?.is_root);
                        const angleStep = (2 * Math.PI) / Math.max(1, nonRootNodes.length);

                        return (
                          <g>
                            {/* Render Edges */}
                            {nonRootNodes.map((node, i) => {
                              const angle = i * angleStep;
                              const x = cx + radius * Math.cos(angle);
                              const y = cy + radius * Math.sin(angle);
                              return (
                                <g key={`edge-${node.id}`}>
                                  <line
                                    x1={cx}
                                    y1={cy}
                                    x2={x}
                                    y2={y}
                                    stroke="#1E2D4A"
                                    strokeWidth="1.5"
                                    strokeDasharray="4 2"
                                  />
                                </g>
                              );
                            })}

                            {/* Center Root Entity Node */}
                            <g className="cursor-pointer">
                              <circle cx={cx} cy={cy} r="36" fill="#17233A" stroke="#4F8CFF" strokeWidth="3" />
                              <text
                                x={cx}
                                y={cy + 4}
                                textAnchor="middle"
                                fill="#FFFFFF"
                                fontSize="12"
                                fontWeight="bold"
                              >
                                {selectedEntity.slice(0, 10)}
                              </text>
                            </g>

                            {/* Surrounding Connected Nodes */}
                            {nonRootNodes.map((node, i) => {
                              const angle = i * angleStep;
                              const x = cx + radius * Math.cos(angle);
                              const y = cy + radius * Math.sin(angle);
                              const color = getNodeColor(node.type);

                              return (
                                <g key={`node-${node.id}`} className="cursor-pointer group">
                                  <circle
                                    cx={x}
                                    cy={y}
                                    r="22"
                                    fill="#111A2E"
                                    stroke={color}
                                    strokeWidth="2"
                                    className="hover:r-26 transition-all"
                                  />
                                  <text
                                    x={x}
                                    y={y + 3}
                                    textAnchor="middle"
                                    fill={color}
                                    fontSize="9"
                                    fontWeight="bold"
                                    fontFamily="monospace"
                                  >
                                    {node.type.slice(0, 4).toUpperCase()}
                                  </text>
                                  {/* Label tooltip underneath */}
                                  <text
                                    x={x}
                                    y={y + 32}
                                    textAnchor="middle"
                                    fill="#98A7BD"
                                    fontSize="10"
                                    className="group-hover:fill-white font-medium"
                                  >
                                    {node.label.length > 18 ? node.label.slice(0, 16) + "..." : node.label}
                                  </text>
                                </g>
                              );
                            })}
                          </g>
                        );
                      })()}
                    </svg>
                  </div>
                )}

                {/* Connected List Cards */}
                <div className="pt-4 border-t border-[#1E2D4A]/60">
                  <h4 className="text-xs font-semibold text-[#98A7BD] uppercase mb-2">Connected Records Breakdown:</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                    {graphData?.nodes
                      .filter((n) => !n.metadata?.is_root)
                      .slice(0, 6)
                      .map((node) => (
                        <div key={node.id} className="p-2.5 rounded-xl bg-[#0B1020]/70 border border-[#1E2D4A] flex items-center justify-between text-xs">
                          <div className="truncate pr-2">
                            <span className="font-semibold text-white block truncate">{node.label}</span>
                            <span className="text-[10px] font-mono text-[#98A7BD] uppercase">{node.type}</span>
                          </div>
                          {node.metadata?.url && (
                            <a href={node.metadata.url} target="_blank" rel="noopener noreferrer" className="p-1 text-[#4F8CFF] hover:text-white">
                              <ExternalLink className="w-3.5 h-3.5" />
                            </a>
                          )}
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Deterministic Resolution Logs Tab */
          <div className="rounded-2xl bg-[#111A2E] border border-[#1E2D4A] overflow-hidden space-y-4 p-4">
            {/* Filters */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
              <div className="relative flex-1 w-full sm:max-w-md">
                <Search className="absolute left-3 top-3 w-4 h-4 text-[#98A7BD]" />
                <input
                  type="text"
                  value={logSearch}
                  onChange={(e) => {
                    setLogSearch(e.target.value);
                    setLogPage(1);
                  }}
                  placeholder="Search raw name or canonical name..."
                  className="w-full pl-9 pr-4 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none focus:border-[#4F8CFF]"
                />
              </div>

              <select
                value={logMethod}
                onChange={(e) => {
                  setLogMethod(e.target.value);
                  setLogPage(1);
                }}
                className="w-full sm:w-auto px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#4F8CFF]"
              >
                <option value="">All Resolution Methods</option>
                <option value="EXACT_CANONICAL">EXACT_CANONICAL (1.0)</option>
                <option value="SEED_ALIAS">SEED_ALIAS (0.95)</option>
                <option value="NORMALIZED_MATCH">NORMALIZED_MATCH (0.92)</option>
                <option value="FUZZY_TOKEN_SORT">FUZZY_TOKEN_SORT (0.88)</option>
              </select>
            </div>

            {/* Table */}
            {logsLoading ? (
              <div className="py-20 text-center">
                <Loader2 className="w-6 h-6 text-[#4F8CFF] animate-spin mx-auto mb-2" />
                <span className="text-xs text-[#98A7BD]">Loading entity mapping logs...</span>
              </div>
            ) : (
              <div className="overflow-x-auto -mx-4 sm:mx-0 px-4 sm:px-0">
                <table className="w-full min-w-[650px] text-left text-xs">
                  <thead className="bg-[#17233A] text-[#98A7BD] uppercase font-mono border-b border-[#1E2D4A]">
                    <tr>
                      <th className="py-2.5 px-3">Raw Name</th>
                      <th className="py-2.5 px-3">Resolved Canonical Name</th>
                      <th className="py-2.5 px-3">Method</th>
                      <th className="py-2.5 px-3">Confidence Score</th>
                      <th className="py-2.5 px-3">Resolution Timestamp</th>
                      <th className="py-2.5 px-3 text-right">Source</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1E2D4A]/50">
                    {logData?.items.map((log) => (
                      <tr key={log.id} className="hover:bg-[#17233A]/50 transition-colors">
                        <td className="py-2.5 px-3 font-mono text-[#F4F7FC]">
                          {log.raw_name}
                        </td>
                        <td className="py-2.5 px-3 font-bold text-[#36D6E7]">
                          {log.canonical_name}
                        </td>
                        <td className="py-2.5 px-3">
                          <Badge variant={log.matching_method.includes("EXACT") ? "emerald" : "blue"}>
                            {log.matching_method}
                          </Badge>
                        </td>
                        <td className="py-2.5 px-3 font-mono font-bold text-[#35C98A]">
                          {log.confidence_score.toFixed(2)}
                        </td>
                        <td className="py-2.5 px-3 font-mono text-[#98A7BD]">
                          {log.resolution_timestamp}
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <a
                            href={log.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[#4F8CFF] hover:underline inline-flex items-center gap-1 font-mono"
                          >
                            URL <ExternalLink className="w-3 h-3" />
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Pagination */}
            {logData && logData.total_pages > 1 && (
              <div className="p-3 bg-[#17233A]/50 rounded-xl flex items-center justify-between text-xs">
                <span className="text-[#98A7BD]">
                  Page <span className="text-white font-mono">{logData.page}</span> of{" "}
                  <span className="text-white font-mono">{logData.total_pages}</span>
                </span>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setLogPage((p) => Math.max(1, p - 1))}
                    disabled={logData.page <= 1}
                    className="p-1 rounded bg-[#17233A] border border-[#1E2D4A] text-white disabled:opacity-30"
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setLogPage((p) => Math.min(logData.total_pages, p + 1))}
                    disabled={logData.page >= logData.total_pages}
                    className="p-1 rounded bg-[#17233A] border border-[#1E2D4A] text-white disabled:opacity-30"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
