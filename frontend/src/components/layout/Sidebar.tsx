"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Building2,
  Package,
  BookOpen,
  Briefcase,
  Newspaper,
  Network,
  TrendingUp,
  ShieldCheck,
  Cpu,
  FileSpreadsheet,
  Settings,
  ChevronLeft,
  ChevronRight,
  Compass,
  X
} from "lucide-react";
import { useNav } from "./NavContext";
import { api } from "@/lib/api";

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const navItems: NavItem[] = [
  { name: "Overview", href: "/", icon: LayoutDashboard },
  { name: "AI Startups", href: "/startups", icon: Building2 },
  { name: "AI Products", href: "/products", icon: Package },
  { name: "Research Intelligence", href: "/research", icon: BookOpen },
  { name: "Engineering Jobs", href: "/jobs", icon: Briefcase },
  { name: "Industry News", href: "/news", icon: Newspaper },
  { name: "Entity Explorer", href: "/entities", icon: Network },
  { name: "Trend Intelligence", href: "/trends", icon: TrendingUp, badge: "Signals" },
  { name: "Data Quality", href: "/quality", icon: ShieldCheck, badge: "99.4%" },
  { name: "Ingestion Monitor", href: "/ingestion", icon: Cpu },
  { name: "Reports & Exports", href: "/reports", icon: FileSpreadsheet },
  { name: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { isMobileOpen, setIsMobileOpen, isCollapsed, toggleCollapsed } = useNav();
  const [liveTotal, setLiveTotal] = React.useState<number | null>(4389);

  React.useEffect(() => {
    api.getStats()
      .then((res: any) => {
        const total =
          (res.startups || 0) +
          (res.products || 0) +
          (res.research_papers || 0) +
          (res.jobs_24h_fresh || 0) +
          (res.news_24h_fresh || 0) +
          (res.entity_mapping_logs || 0);
        if (total > 0) setLiveTotal(total);
      })
      .catch(() => {});
  }, []);

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/75 backdrop-blur-sm md:hidden transition-opacity duration-300"
          onClick={() => setIsMobileOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Main Navigation Sidebar Drawer */}
      <aside
        className={`fixed top-0 left-0 z-50 h-screen bg-[#0B1020] border-r border-[#1E2D4A] flex flex-col justify-between transition-all duration-300 ease-in-out ${
          // Mobile state: off-canvas drawer
          isMobileOpen
            ? "translate-x-0 w-72 max-w-[85vw] shadow-2xl"
            : "-translate-x-full md:translate-x-0"
        } ${
          // Desktop state: responsive width
          isCollapsed ? "md:w-20" : "md:w-64"
        }`}
        aria-label="Sidebar Navigation"
      >
        {/* Brand Header */}
        <div>
          <div className="flex items-center justify-between h-16 px-4 border-b border-[#1E2D4A]">
            <Link
              href="/"
              onClick={() => setIsMobileOpen(false)}
              className="flex items-center space-x-3 overflow-hidden"
            >
              <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-[#4F8CFF] to-[#9275FF] text-white shadow-lg shadow-blue-500/20 flex-shrink-0">
                <Compass className="w-6 h-6 animate-pulse" />
              </div>
              {(!isCollapsed || isMobileOpen) && (
                <div className="flex flex-col">
                  <span className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
                    FrontierAtlas{" "}
                    <span className="text-[#36D6E7] text-xs font-mono uppercase bg-[#111A2E] px-1.5 py-0.5 rounded border border-[#1E2D4A]">
                      AI
                    </span>
                  </span>
                  <span className="text-[10px] text-[#98A7BD] font-mono tracking-wider">
                    ECOSYSTEM GRAPH
                  </span>
                </div>
              )}
            </Link>

            {/* Desktop Collapse Button */}
            <button
              onClick={toggleCollapsed}
              className="hidden md:flex p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A] transition-colors"
              title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
              aria-label={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
            >
              {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>

            {/* Mobile Close Button */}
            <button
              onClick={() => setIsMobileOpen(false)}
              className="flex md:hidden p-2 rounded-xl text-[#98A7BD] hover:text-white hover:bg-[#17233A] transition-colors"
              aria-label="Close Navigation Drawer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation Items */}
          <nav className="p-3 space-y-1 overflow-y-auto max-h-[calc(100vh-140px)]">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;
              const showText = !isCollapsed || isMobileOpen;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsMobileOpen(false)}
                  className={`group flex items-center px-3 py-3 md:py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? "bg-[#17233A] text-[#4F8CFF] border border-[#1E2D4A] shadow-sm shadow-blue-900/10"
                      : "text-[#98A7BD] hover:text-[#F4F7FC] hover:bg-[#111A2E]"
                  }`}
                  title={!showText ? item.name : undefined}
                >
                  <Icon
                    className={`w-5 h-5 flex-shrink-0 transition-colors ${
                      isActive ? "text-[#4F8CFF]" : "text-[#98A7BD] group-hover:text-[#F4F7FC]"
                    }`}
                  />
                  {showText && (
                    <span className="ml-3 truncate flex-1 text-left">{item.name}</span>
                  )}
                  {showText && item.badge && (
                    <span className="ml-auto text-[10px] font-mono px-1.5 py-0.5 rounded bg-[#111A2E] text-[#36D6E7] border border-[#1E2D4A]">
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Footer System Status */}
        <div className="p-3 border-t border-[#1E2D4A]">
          {!isCollapsed || isMobileOpen ? (
            <div className="p-2.5 rounded-xl bg-[#111A2E] border border-[#1E2D4A] flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="w-2.5 h-2.5 rounded-full bg-[#35C98A] animate-ping" />
                <div className="flex flex-col">
                  <span className="text-xs font-semibold text-white">Live Ingestion</span>
                  <span className="text-[10px] text-[#98A7BD]">
                    {liveTotal !== null ? `${liveTotal.toLocaleString()} Entities` : "4,389 Entities"}
                  </span>
                </div>
              </div>
              <span className="text-[10px] font-mono text-[#35C98A] bg-[#35C98A]/10 px-1.5 py-0.5 rounded">
                A+
              </span>
            </div>
          ) : (
            <div className="flex justify-center py-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#35C98A]" title="Engine Connected" />
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
