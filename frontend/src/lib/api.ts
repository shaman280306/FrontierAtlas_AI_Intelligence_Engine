import {
  Startup, Product, ResearchPaper, JobListing, NewsArticle, EntityMappingLog,
  PaginatedResponse, OverviewAnalytics, EntityGraph, FrontierSignals,
  QualityReport, GlobalSearchResults, AIQueryResponse
} from "../types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
      },
      ...options,
    });
    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }
    return await res.json();
  } catch (error) {
    console.error(`Failed to fetch ${url}:`, error);
    throw error;
  }
}

export const api = {
  // System
  getHealth: () => fetchJson<{ status: string; environment: string; database: string }>("/health"),

  // Overview Analytics
  getOverviewAnalytics: () => fetchJson<OverviewAnalytics>("/api/v1/analytics/overview"),
  getStats: () => fetchJson<Record<string, number>>("/api/v1/stats"),

  // Startups
  getStartups: (params: { page?: number; page_size?: number; search?: string; source?: string; has_employees?: boolean }) => {
    const sp = new URLSearchParams();
    if (params.page) sp.set("page", params.page.toString());
    if (params.page_size) sp.set("page_size", params.page_size.toString());
    if (params.search) sp.set("search", params.search);
    if (params.source) sp.set("source", params.source);
    if (params.has_employees !== undefined) sp.set("has_employees", params.has_employees.toString());
    return fetchJson<PaginatedResponse<Startup>>(`/api/v1/startups?${sp.toString()}`);
  },
  getStartupDetail: (id: number) => fetchJson<Startup>(`/api/v1/startups/${id}`),
  getStartupSources: () => fetchJson<{ sources: string[] }>("/api/v1/startups/sources"),

  // Products
  getProducts: (params: { page?: number; page_size?: number; search?: string; pricing_model?: string; startup_name?: string }) => {
    const sp = new URLSearchParams();
    if (params.page) sp.set("page", params.page.toString());
    if (params.page_size) sp.set("page_size", params.page_size.toString());
    if (params.search) sp.set("search", params.search);
    if (params.pricing_model) sp.set("pricing_model", params.pricing_model);
    if (params.startup_name) sp.set("startup_name", params.startup_name);
    return fetchJson<PaginatedResponse<Product>>(`/api/v1/products?${sp.toString()}`);
  },
  getProductDetail: (id: number) => fetchJson<Product>(`/api/v1/products/${id}`),
  compareProducts: (ids: number[]) => fetchJson<{ products: Product[] }>(`/api/v1/products/compare?ids=${ids.join(",")}`),

  // Research Papers
  getResearchPapers: (params: { page?: number; page_size?: number; search?: string; has_github?: boolean; min_stars?: number }) => {
    const sp = new URLSearchParams();
    if (params.page) sp.set("page", params.page.toString());
    if (params.page_size) sp.set("page_size", params.page_size.toString());
    if (params.search) sp.set("search", params.search);
    if (params.has_github !== undefined) sp.set("has_github", params.has_github.toString());
    if (params.min_stars !== undefined) sp.set("min_stars", params.min_stars.toString());
    return fetchJson<PaginatedResponse<ResearchPaper>>(`/api/v1/research-papers?${sp.toString()}`);
  },
  getPaperDetail: (id: number) => fetchJson<ResearchPaper>(`/api/v1/research-papers/${id}`),
  getTopStarredPapers: (limit: number = 10) => fetchJson<{ papers: ResearchPaper[] }>(`/api/v1/research-papers/top-starred?limit=${limit}`),

  // Jobs
  getJobs: (params: { page?: number; page_size?: number; search?: string; is_remote?: boolean; role_family?: string; source?: string }) => {
    const sp = new URLSearchParams();
    if (params.page) sp.set("page", params.page.toString());
    if (params.page_size) sp.set("page_size", params.page_size.toString());
    if (params.search) sp.set("search", params.search);
    if (params.is_remote !== undefined) sp.set("is_remote", params.is_remote.toString());
    if (params.role_family) sp.set("role_family", params.role_family);
    if (params.source) sp.set("source", params.source);
    return fetchJson<PaginatedResponse<JobListing>>(`/api/v1/jobs?${sp.toString()}`);
  },
  getJobDetail: (id: number) => fetchJson<JobListing>(`/api/v1/jobs/${id}`),
  getJobSources: () => fetchJson<{ sources: string[] }>("/api/v1/jobs/sources"),

  // News
  getNews: (params: { page?: number; page_size?: number; search?: string; source?: string }) => {
    const sp = new URLSearchParams();
    if (params.page) sp.set("page", params.page.toString());
    if (params.page_size) sp.set("page_size", params.page_size.toString());
    if (params.search) sp.set("search", params.search);
    if (params.source) sp.set("source", params.source);
    return fetchJson<PaginatedResponse<NewsArticle>>(`/api/v1/news?${sp.toString()}`);
  },
  getNewsDetail: (id: number) => fetchJson<NewsArticle>(`/api/v1/news/${id}`),
  getNewsSources: () => fetchJson<{ sources: string[] }>("/api/v1/news/sources"),

  // Entities & Graph
  getEntityMappings: (params: { page?: number; page_size?: number; search?: string; method?: string }) => {
    const sp = new URLSearchParams();
    if (params.page) sp.set("page", params.page.toString());
    if (params.page_size) sp.set("page_size", params.page_size.toString());
    if (params.search) sp.set("search", params.search);
    if (params.method) sp.set("method", params.method);
    return fetchJson<PaginatedResponse<EntityMappingLog>>(`/api/v1/entity-mappings?${sp.toString()}`);
  },
  getTopConnectedEntities: (limit: number = 15) => fetchJson<{ entities: Array<{ entity: string; products: number; papers: number; jobs: number; news: number; total_connections: number }> }>(`/api/v1/entities/top-connected?limit=${limit}`),
  getEntityGraph: (name: string) => fetchJson<EntityGraph>(`/api/v1/entities/${encodeURIComponent(name)}/graph`),

  // Trend Intelligence (Frontier Signals)
  getFrontierSignals: () => fetchJson<FrontierSignals>("/api/v1/trends"),

  // Data Quality
  getQualityMetrics: () => fetchJson<QualityReport>("/api/v1/quality/metrics"),

  // Ingestion Monitor
  getIngestionStatus: () => fetchJson<any>("/api/v1/ingestion/status"),
  triggerIngestion: (targets: { startup_target?: number; product_target?: number; paper_target?: number }) => {
    const sp = new URLSearchParams();
    if (targets.startup_target) sp.set("startup_target", targets.startup_target.toString());
    if (targets.product_target) sp.set("product_target", targets.product_target.toString());
    if (targets.paper_target) sp.set("paper_target", targets.paper_target.toString());
    return fetchJson<{ status: string; message: string }>(`/api/v1/pipeline/run?${sp.toString()}`, { method: "POST" });
  },

  // Reports
  getReportsList: () => fetchJson<{ reports: Array<{ filename: string; size_bytes: number; format: string; type: string }> }>("/api/v1/reports/list"),
  getDownloadUrl: (filename: string) => `${API_BASE}/api/v1/reports/download/${filename}`,

  // Global Search
  searchGlobal: (query: string) => fetchJson<GlobalSearchResults>(`/api/v1/search?q=${encodeURIComponent(query)}`),

  // AI Assistant Query
  queryAI: (prompt: string) => fetchJson<AIQueryResponse>("/api/v1/ai/query", {
    method: "POST",
    body: JSON.stringify({ prompt }),
  }),
};
