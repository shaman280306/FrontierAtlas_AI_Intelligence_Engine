import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "blue" | "cyan" | "violet" | "emerald" | "amber" | "slate";
  className?: string;
}

export default function Badge({ children, variant = "slate", className = "" }: BadgeProps) {
  const variantStyles = {
    blue: "bg-[#4F8CFF]/15 text-[#4F8CFF] border-[#4F8CFF]/30",
    cyan: "bg-[#36D6E7]/15 text-[#36D6E7] border-[#36D6E7]/30",
    violet: "bg-[#9275FF]/15 text-[#9275FF] border-[#9275FF]/30",
    emerald: "bg-[#35C98A]/15 text-[#35C98A] border-[#35C98A]/30",
    amber: "bg-[#F3B84B]/15 text-[#F3B84B] border-[#F3B84B]/30",
    slate: "bg-[#17233A] text-[#98A7BD] border-[#1E2D4A]",
  };

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-mono font-medium border ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
