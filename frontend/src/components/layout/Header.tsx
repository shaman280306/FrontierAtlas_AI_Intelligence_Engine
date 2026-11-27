"use client";

import React, { useState } from "react";
import { Search, Sparkles, Activity, Menu } from "lucide-react";
import GlobalSearchModal from "../common/GlobalSearchModal";
import AIAssistantModal from "../common/AIAssistantModal";
import { useNav } from "./NavContext";

interface HeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: Array<{ label: string; href?: string }>;
}

export default function Header({ title, subtitle, breadcrumbs }: HeaderProps) {
  const [searchOpen, setSearchOpen] = useState(false);
  const [aiOpen, setAiOpen] = useState(false);
  const { toggleMobileMenu } = useNav();

  return (
    <>
      <header className="sticky top-0 z-30 h-14 sm:h-16 border-b border-[#1E2D4A] bg-[#0B1020]/90 backdrop-blur-md px-3 sm:px-6 flex items-center justify-between gap-2">
        {/* Left: Mobile Hamburger & Page Title */}
        <div className="flex items-center space-x-2 sm:space-x-3 min-w-0">
          {/* Mobile Hamburger Button */}
          <button
            onClick={toggleMobileMenu}
            className="p-2 -ml-1 rounded-xl text-[#98A7BD] hover:text-white hover:bg-[#17233A] md:hidden flex-shrink-0 transition-colors"
            aria-label="Open Navigation Drawer"
          >
            <Menu className="w-5 h-5 text-white" />
          </button>

          <div className="flex flex-col min-w-0">
            {breadcrumbs && breadcrumbs.length > 0 && (
              <div className="hidden sm:flex items-center space-x-1.5 text-[11px] text-[#98A7BD] font-mono truncate">
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
            <h1 className="text-sm sm:text-base md:text-lg font-bold text-white tracking-tight flex items-center gap-1.5 truncate">
              <span className="truncate">{title}</span>
              {subtitle && (
                <span className="text-xs font-normal text-[#98A7BD] hidden lg:inline truncate">
                  — {subtitle}
                </span>
              )}
            </h1>
          </div>
        </div>

        {/* Right: Global Controls */}
        <div className="flex items-center space-x-2 sm:space-x-3 flex-shrink-0">
          {/* Global Search Button */}
          <button
            onClick={() => setSearchOpen(true)}
            className="flex items-center space-x-2 p-2 sm:px-3 sm:py-1.5 rounded-xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#4F8CFF]/50 text-[#98A7BD] hover:text-[#F4F7FC] text-xs transition-all shadow-sm"
            aria-label="Search Ecosystem"
            title="Search Ecosystem (Ctrl+K)"
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
            className="flex items-center space-x-1.5 p-2 sm:px-3.5 sm:py-1.5 rounded-xl bg-gradient-to-r from-[#4F8CFF]/20 to-[#9275FF]/20 hover:from-[#4F8CFF]/30 hover:to-[#9275FF]/30 border border-[#4F8CFF]/40 text-[#F4F7FC] text-xs font-medium transition-all shadow-sm"
            aria-label="AI Intelligence Assistant"
            title="AI Intelligence Assistant"
          >
            <Sparkles className="w-4 h-4 text-[#36D6E7]" />
            <span className="hidden sm:inline">AI Assistant</span>
          </button>

          {/* Freshness Badge */}
          <div className="hidden xl:flex items-center space-x-1.5 px-3 py-1 rounded-xl bg-[#111A2E] border border-[#1E2D4A] text-xs font-mono text-[#35C98A]">
            <Activity className="w-3.5 h-3.5 text-[#35C98A] animate-pulse" />
            <span>24h Verified Freshness</span>
          </div>
        </div>
      </header>

      {/* Global Modals */}
      <GlobalSearchModal isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
      <AIAssistantModal isOpen={aiOpen} onClose={() => setAiOpen(false)} />
    </>
  );
}
