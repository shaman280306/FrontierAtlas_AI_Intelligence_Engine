"use client";

import React, { useState } from "react";
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
  Sparkles,
  Compass
} from "lucide-react";

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
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`fixed top-0 left-0 z-40 h-screen transition-all duration-300 ease-in-out border-r border-[#1E2D4A] bg-[#0B1020] flex flex-col justify-between ${
        collapsed ? "w-20" : "w-64"
      }`}
    >
      {/* Brand Header */}
      <div>
        <div className="flex items-center justify-between h-16 px-4 border-b border-[#1E2D4A]">
          <Link href="/" className="flex items-center space-x-3 overflow-hidden">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-[#4F8CFF] to-[#9275FF] text-white shadow-lg shadow-blue-500/20 flex-shrink-0">
              <Compass className="w-6 h-6 animate-pulse" />
            </div>
            {!collapsed && (
              <div className="flex flex-col">
                <span className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
                  FrontierAtlas <span className="text-[#36D6E7] text-xs font-mono uppercase bg-[#111A2E] px-1.5 py-0.5 rounded border border-[#1E2D4A]">AI</span>
                </span>
                <span className="text-[10px] text-[#98A7BD] font-mono tracking-wider">ECOSYSTEM GRAPH</span>
              </div>
            )}
          </Link>
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A] transition-colors"
            title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-1 overflow-y-auto max-h-[calc(100vh-140px)]">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`group flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? "bg-[#17233A] text-[#4F8CFF] border border-[#1E2D4A] shadow-sm shadow-blue-900/10"
                    : "text-[#98A7BD] hover:text-[#F4F7FC] hover:bg-[#111A2E]"
                }`}
                title={collapsed ? item.name : undefined}
              >
                <Icon
                  className={`w-5 h-5 flex-shrink-0 transition-colors ${
                    isActive ? "text-[#4F8CFF]" : "text-[#98A7BD] group-hover:text-[#F4F7FC]"
                  }`}
                />
                {!collapsed && (
                  <span className="ml-3 truncate flex-1 text-left">{item.name}</span>
                )}
                {!collapsed && item.badge && (
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
        {!collapsed ? (
          <div className="p-2.5 rounded-xl bg-[#111A2E] border border-[#1E2D4A] flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#35C98A] animate-ping" />
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-white">Live Ingestion</span>
                <span className="text-[10px] text-[#98A7BD]">4,389 Entities</span>
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
  );
}
