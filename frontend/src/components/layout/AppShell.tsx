"use client";

import React from "react";
import Sidebar from "./Sidebar";
import { useNav } from "./NavContext";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const { isCollapsed } = useNav();

  return (
    <div className="flex min-h-screen bg-[#0B1020] text-[#F4F7FC]">
      {/* Navigation Sidebar (Desktop persistent + Mobile slide-over drawer) */}
      <Sidebar />

      {/* Main Content Area: 0 left padding on mobile, dynamic padding on desktop */}
      <div
        className={`flex-1 min-w-0 transition-all duration-300 ease-in-out ${
          isCollapsed ? "md:pl-20" : "md:pl-64"
        }`}
      >
        <main className="min-h-screen w-full overflow-x-hidden">
          {children}
        </main>
      </div>
    </div>
  );
}
