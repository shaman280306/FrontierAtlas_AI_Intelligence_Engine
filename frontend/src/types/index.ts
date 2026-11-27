export interface Startup {
  id: number;
  canonical_name: string;
  raw_name: string;
  source_name: string;
  source_url: string;
  website: string | null;
  description: string | null;
  employee_count: number | null;
  fingerprint: string;
  collected_at: string;
}

export interface Product {
  id: number;
  product_name: string;
  startup_name: string;
  pricing_model: "FREE" | "FREEMIUM" | "PAID" | "ENTERPRISE" | null;
  source_name: string;
  source_url: string;
  description: string | null;
  fingerprint: string;
  collected_at: string;
}

export interface ResearchPaper {
  id: number;
  title: string;
  authors: string[];
  paper_url: string;
  github_url: string | null;
  github_stars: number | null;
  github_stars_retrieved_at: string | null;
  published_date: string;
  fingerprint: string;
}

export interface JobListing {
  id: number;
  title: string;
  company: string;
  source_name: string;
  source_url: string;
  date: string;
  is_remote: boolean;
  role_family: string;
  first_discovered_at: string;
  collected_at: string;
  fingerprint: string;
}

export interface NewsArticle {
  id: number;
  title: string;
  source_name: string;
  source_url: string;
  published_at: string;
  summary: string | null;
  full_text: string | null;
  author: string | null;
  primary_entity: string | null;
  first_discovered_at: string;
  collected_at: string;
  fingerprint: string;
}

export interface EntityMappingLog {
  id: number;
  raw_name: string;
  canonical_name: string;
  matching_method: string;
  confidence_score: number;
  source_url: string;
  resolution_timestamp: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface OverviewAnalytics {
  counts: {
    startups: number;
    products: number;
    research_papers: number;
    jobs: number;
    news: number;
    mapped_entities: number;
    papers_with_github: number;
    github_open_source_ratio: number;
    total_github_stars_indexed: number;
    remote_jobs_percentage: number;
  };
  distributions: {
    pricing: Record<string, number>;
    job_roles: Record<string, number>;
    news_sources: Record<string, number>;
    resolution_methods: Record<string, number>;
  };
  top_starred_papers: ResearchPaper[];
  recent_news: NewsArticle[];
  recent_jobs: JobListing[];
  health: {
    database_connected: boolean;
    data_integrity: string;
    last_audit_status: string;
  };
}

export interface GraphNode {
  id: string;
  label: string;
  type: "entity" | "startup" | "product" | "paper" | "job" | "news";
  metadata: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  relationship: string;
}

export interface EntityGraph {
  entity: string;
  node_count: number;
  edge_count: number;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface FrontierSignals {
  research_signals: Array<{
    topic: string;
    occurrences: number;
    share_percentage: number;
    trend: string;
    methodology: string;
  }>;
  pricing_signals: Array<{
    tier: string;
    count: number;
    share: number;
    insight: string;
  }>;
  job_demand_signals: Array<{
    role_family: string;
    openings: number;
    share: number;
    demand_indicator: string;
  }>;
  open_source_velocity: {
    total_papers: number;
    with_code_repository: number;
    open_source_ratio: number;
    with_live_stars_indexed: number;
    status: string;
    interpretation: string;
  };
  methodology_note: string;
}

export interface QualityReport {
  audited_at: string;
  overall_quality_score: number;
  system_grade: string;
  total_entities_audited: number;
  datasets: Array<{
    name: string;
    total_records: number;
    url_coverage: string;
    uniqueness: string;
    missing_urls: number;
    schema_violations: number;
    attribute_completeness: string;
    status: string;
    grade: string;
  }>;
  guarantees: Record<string, string>;
}

export interface GlobalSearchResults {
  query: string;
  total_matches: number;
  results: {
    startups: Startup[];
    products: Product[];
    research_papers: ResearchPaper[];
    jobs: JobListing[];
    news: NewsArticle[];
    entities: EntityMappingLog[];
  };
}

export interface AIQueryResponse {
  query: string;
  response: string;
  provider: string;
  grounding: {
    referenced_papers: ResearchPaper[];
    referenced_products: Product[];
    referenced_startups: Startup[];
    referenced_jobs: JobListing[];
    referenced_news: NewsArticle[];
  };
}
