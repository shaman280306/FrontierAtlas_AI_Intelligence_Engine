import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://frontieratlas-frontend.vercel.app";
  const routes = [
    "",
    "/startups",
    "/products",
    "/research",
    "/jobs",
    "/news",
    "/entities",
    "/trends",
    "/quality",
    "/ingestion",
    "/reports",
    "/settings",
  ];

  return routes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: "daily",
    priority: route === "" ? 1.0 : 0.8,
  }));
}
