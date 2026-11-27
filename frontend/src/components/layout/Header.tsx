"use client";

import React, { useState } from "react";
import { Search, Sparkles, Activity, ShieldCheck } from "lucide-react";
import GlobalSearchModal from "../common/GlobalSearchModal";
import AIAssistantModal from "../common/AIAssistantModal";

interface HeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: Array<{ label: string; href?: string }>;
}

export default function Header({ title, subtitle, breadcrumbs }: HeaderProps) {
  const [searchOpen, setSearchOpen] = useState(false);
  const [aiOpen, setAiOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-30 h-16 border-b border-[#1E2D4A] bg-[#0B1020]/80 backdrop-blur-md px-6 flex items-center justify-between">
        {/* Title & Breadcrumbs */}
        <div className="flex flex-col">
          {breadcrumbs && breadcrumbs.length > 0 && (
            <div className="flex items-center space-x-1.5 text-xs text-[#98A7BD] font-mono">
              {breadcrumbs.map((b, idx) => (
                <React.Fragment key={idx}>
                  {idx > 0 && <span>/</span>}
                  <span className={idx === breadcrumbs.length - 1 ? "text-[#F4F7FC]" : "hover:text-[#4F8CFF]"}>
                    {b.label}
                  </span>
                </React.Fragment>
              ))}
            </div>
          )}
          <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            {title}
            {subtitle && <span className="text-xs font-normal text-[#98A7BD] hidden sm:inline">— {subtitle}</span>}
          </h1>
        </div>

        {/* Global Controls */}
        <div className="flex items-center space-x-3">
          {/* Global Search Button */}
          <button
            onClick={() => setSearchOpen(true)}
            className="flex items-center space-x-2.5 px-3.5 py-1.5 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#4F8CFF]/50 text-[#98A7BD] hover:text-[#F4F7FC] text-xs transition-all shadow-sm"
          >
            <Search className="w-4 h-4 text-[#4F8CFF]" />
            <span className="hidden md:inline">Quick search...</span>
            <kbd className="hidden md:inline-flex items-center px-1.5 py-0.5 text-[10px] font-mono bg-[#17233A] text-[#98A7BD] rounded border border-[#1E2D4A]">
              Ctrl K
            </kbd>
          </button>

          {/* AI Intelligence Assistant */}
          <button
            onClick={() => setAiOpen(true)}
            className="flex items-center space-x-2 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-[#4F8CFF]/20 to-[#9275FF]/20 hover:from-[#4F8CFF]/30 hover:to-[#9275FF]/30 border border-[#4F8CFF]/40 text-[#F4F7FC] text-xs font-medium transition-all shadow-sm"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#36D6E7]" />
            <span className="hidden sm:inline">AI Assistant</span>
          </button>

          {/* Freshness Badge */}
          <div className="hidden lg:flex items-center space-x-1.5 px-3 py-1 rounded-xl bg-[#111A2E] border border-[#1E2D4A] text-xs font-mono text-[#35C98A]">
            <Activity className="w-3.5 h-3.5 text-[#35C98A] animate-pulse" />
            <span>24h Verified Freshness</span>
          </div>
        </div>
      </header>

      {/* Modals */}
      <GlobalSearchModal isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
      <AIAssistantModal isOpen={aiOpen} onClose={() => setAiOpen(false)} />
    </>
  );
}
