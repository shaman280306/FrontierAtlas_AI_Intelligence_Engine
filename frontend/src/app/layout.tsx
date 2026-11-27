import "./globals.css";
import type { Metadata } from "next";
import Sidebar from "@/components/layout/Sidebar";

export const metadata: Metadata = {
  title: "FrontierAtlas AI — Navigate the Intelligence Frontier",
  description: "Enterprise AI Ecosystem Intelligence Platform connecting startups, products, research papers, engineering opportunities and emerging trends.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0B1020] text-[#F4F7FC] font-sans antialiased">
        <div className="flex">
          {/* Main Navigation Sidebar */}
          <Sidebar />

          {/* Page Content Shell with Left Margin for Fixed Sidebar */}
          <div className="flex-1 min-w-0 pl-20 sm:pl-64 transition-all duration-300">
            <main className="min-h-screen">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
