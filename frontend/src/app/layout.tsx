import "./globals.css";
import type { Metadata, Viewport } from "next";
import { NavProvider } from "@/components/layout/NavContext";
import AppShell from "@/components/layout/AppShell";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  themeColor: "#0B1020",
};

export const metadata: Metadata = {
  metadataBase: new URL("https://frontieratlas-frontend.vercel.app"),
  title: "FrontierAtlas AI — Navigate the Intelligence Frontier",
  description: "Enterprise AI Ecosystem Intelligence Platform connecting startups, products, research papers, engineering opportunities and emerging trends.",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "FrontierAtlas AI — Navigate the Intelligence Frontier",
    description: "Enterprise AI Ecosystem Intelligence Platform connecting startups, products, research papers, engineering opportunities and emerging trends.",
    url: "https://frontieratlas-frontend.vercel.app",
    siteName: "FrontierAtlas AI",
    type: "website",
  },
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
      <body className="min-h-screen bg-[#0B1020] text-[#F4F7FC] font-sans antialiased overflow-x-hidden">
        <NavProvider>
          <AppShell>{children}</AppShell>
        </NavProvider>
      </body>
    </html>
  );
}
