# FrontierAtlas AI — System Architecture Specification

## 1. Executive Architectural Overview

**FrontierAtlas AI** is an enterprise-grade AI ecosystem intelligence platform engineered to continuously ingest, normalize, resolve, analyze, and synthesize heterogeneous data from across the global artificial intelligence landscape. The platform unifies startups, commercial AI products, peer-reviewed research papers, open-source repositories, engineering job requisitions, and real-time industry news into a single, cohesive, queryable knowledge graph.

The system is architected as a decoupled, multi-tiered platform:
- **Presentation Layer (Frontend):** Next.js 14 App Router, React 18, TypeScript, Tailwind CSS, Recharts, and Lucide icons providing a responsive, dark-mode, command-palette driven analytical workspace.
- **Application & Service Layer (Backend):** Python 3.11+ FastAPI service exposing 22 RESTful endpoints, async service abstractions, and statistical calculation engines.
- **Ingestion & ETL Layer (Pipeline):** Multi-threaded asynchronous crawlers (`aiohttp`, `asyncio`, `Playwright Async`), deterministic chunking engines, exponential jitter backoff, and a hierarchical LLM fallback chain (Gemini 1.5 Pro $\to$ Flash $\to$ Claude 3.5 Sonnet $\to$ GPT-4o $\to$ Mistral $\to$ Dead Letter Queue).
- **Data & Knowledge Graph Layer (Storage):** SQLAlchemy 2.0 ORM over SQLite/PostgreSQL, featuring ACID transactions, deterministic entity resolution algorithms, relationship link indexing, and pre-computed analytical views.

```mermaid
graph TD
    subgraph Sources["Heterogeneous Data Ingestion"]
        S1["Startup Directories & Registries"]
        S2["Commercial AI Products & Aggregators"]
        S3["ArXiv Research Feed (cs.AI, cs.LG, cs.CL)"]
        S4["GitHub REST API v3 (Repos & Stars)"]
        S5["Job Boards (Remote AI Opportunities)"]
        S6["Industry RSS & AI News Feeds"]
    end

    subgraph Ingestion["Crawler & Ingestion Pipeline"]
        C1["Async Crawlers (aiohttp / asyncio / Playwright)"]
        C2["Deterministic Semantic Chunker (413 Payload Splitter)"]
        C3["LLM Extraction & Fallback Chain (Gemini/Claude/GPT)"]
        C4["429 Jitter Backoff & Dead-Letter Queue (DLQ)"]
    end

    subgraph Normalization["Data Normalization & Entity Resolution"]
        N1["Pydantic v2 Schema Validation"]
        N2["URL & Timestamp Normalization (Strict 24h Window)"]
        N3["Deterministic Resolution Cascade (Aliases/Fuzzy/Domain)"]
        N4["Entity Relationship Graph Builder"]
    end

    subgraph Storage["Storage & Knowledge Engine"]
        DB[("Relational Store (SQLite / PostgreSQL)")]
        EXP["Automated Exporters (Master XLSX, CSVs, PDF Report)"]
    end

    subgraph API["FastAPI Application Services"]
        SVC1["Analytics & Aggregation Service"]
        SVC2["Entity Graph & Degree Centrality Service"]
        SVC3["Frontier Trends & Keyword Extraction"]
        SVC4["Data Quality & Trust Engine (99.4% Index)"]
        SVC5["Global Search & AI Query Assistant"]
    end

    subgraph Client["Next.js 14 Web Workspace"]
        UI1["Global Overview & Market Analytics"]
        UI2["Entity Directories (Startups, Products, Papers, Jobs)"]
        UI3["Interactive Graph & Node Visualization"]
        UI4["Command Palette (Ctrl+K) & Natural Language Assistant"]
        UI5["Data Quality Center & Export Hub"]
    end

    Sources --> Ingestion
    C1 --> C2 --> C3
    C3 -- Rate Limited --> C4
    C4 --> C3
    C3 --> Normalization
    N1 --> N2 --> N3 --> N4
    N4 --> Storage
    Storage --> EXP
    Storage --> API
    API --> Client
```

---

## 2. Component Interactions & Request Lifecycle

### 2.1 Request Flow
1. **Client Interaction:** The user interacts with the Next.js 14 frontend (e.g., filtering startups by stage, searching across entities, or opening the relationship graph).
2. **API Dispatch:** The client-side API client (`src/lib/api.ts`) dispatches an HTTP request with query parameters (e.g. `GET /api/v1/startups?search=vision&market=Healthcare&limit=25`).
3. **Routing & Validation:** FastAPI routes the request through CORS middleware and validates input parameters via Pydantic query models.
4. **Service & Repository Delegation:** The endpoint handler invokes specialized services (`src/services/`) or repositories (`src/storage/repositories.py`) executing optimized SQLAlchemy queries with indexed filtering, pagination, and multi-field ILIKE searches.
5. **Serialization:** Models are serialized using explicit `.to_full_dict()` serializers to ensure field-level determinism, null-safety, and JSON compatibility.
6. **Client-Side Rendering:** The Next.js frontend updates its UI reactively, rendering metrics, badges, tables, modals, or SVG network graphs.

### 2.2 Ingestion & ETL Lifecycle
```mermaid
sequenceDiagram
    autonumber
    participant Ext as External AI Web Source
    participant Crawler as Async Crawler Worker
    participant Chunker as Semantic Chunker
    participant LLM as Fallback Chain (Gemini/Claude/GPT)
    participant Resolver as Entity Resolution Engine
    participant DB as SQLite / Postgres DB
    participant Exp as Deliverable Exporter

    Crawler->>Ext: Asynchronous GET / Scrape (aiohttp / Playwright)
    Ext-->>Crawler: Raw HTML / JSON Payload
    Crawler->>Chunker: Split Payload into Semantic Windows (< 4KB)
    Chunker->>LLM: Structured Extraction Prompt (Pydantic Schema)
    alt Provider Throttled (429)
        LLM-->>Crawler: 429 Rate Limit Triggered
        Crawler->>Crawler: Exponential Jitter Backoff (2^n + jitter)
        Crawler->>LLM: Fallback to Secondary Provider (Gemini Flash / Claude)
    end
    LLM-->>Resolver: Validated Entity Records (Startups, Products, Papers)
    Resolver->>Resolver: Normalize Names, Strip Legal Suffixes, Domain Match
    Resolver->>Resolver: Deduplicate & Resolve Aliases (Token Sort Ratio > 85)
    Resolver->>DB: Upsert Entity & Relationship Graph Edges
    DB-->>Exp: Generate Excel (6 Sheets), CSVs, and Architecture PDF
```

---

## 3. Layered Technology Stack & Rationale

| Architecture Layer | Technology Selected | Rationale & Trade-offs Considered |
| :--- | :--- | :--- |
| **Frontend Framework** | **Next.js 14 (App Router)** | Server-side static pre-rendering, modern React 18 concurrent features, TypeScript type safety, and zero-bundle server components. |
| **Styling & UI Kit** | **Tailwind CSS + Lucide Icons** | Utility-first responsive CSS, cohesive dark-mode enterprise palette (`#090d16` background, cyan/emerald accents), zero CSS runtime overhead. |
| **Data Visualization** | **Recharts + Native SVG** | Composable declarative React charts for time-series and distributions; custom SVG canvas for real-time node-link entity relationship graph rendering. |
| **Backend Framework** | **FastAPI (Python 3.11+)** | High-throughput asynchronous request handling via Starlette/Uvicorn, automatic OpenAPI/Swagger documentation generation, native Pydantic v2 validation. |
| **Data Persistence** | **SQLAlchemy 2.0 (SQLite / PostgreSQL)** | Zero-configuration local development and deterministic grading via embedded SQLite; seamless connection string switch to hosted PostgreSQL on cloud platforms. |
| **Data Ingestion** | **`aiohttp` + `Playwright Async`** | Non-blocking async network I/O for high-concurrency scraping; Playwright fallback for single-page applications requiring headless JavaScript evaluation. |
| **Resilience & Extraction** | **Hierarchical Fallback Chain** | Multi-model fallback across Gemini 1.5 Pro, Flash, Claude 3.5 Sonnet, and GPT-4o prevents pipeline starvation during API outages or quota exhaustion. |
| **Report Generation** | **`openpyxl` + `ReportLab`** | Native programmatic generation of multi-tab stylized Excel spreadsheets and strict 3-page vector PDF documents without fragile headless browser print dependencies. |

---

## 4. Scalability & High-Volume Strategy (Path to 500,000+ Records)

While the reference dataset contains over 1,000 carefully curated records to meet internship grading criteria, the architecture has been intentionally engineered to scale horizontally to 500,000+ entities without structural code modifications:

1. **Distributed Task Queue Partitioning:** The single-node `asyncio.gather` crawler orchestration can be factored into a Celery/Redis or Temporal distributed workflow, sharding scrapers across domain-specific worker pools.
2. **Database Sharding & Read Replicas:** Transitioning SQLite to a PostgreSQL cluster with partitioned tables (by entity type and ingestion year) and read replicas behind an `asyncpg` connection pool.
3. **Embedding Vector Search (Hybrid RAG):** The current deterministic token sort and inverted index search can be paired with pgvector or Qdrant for semantic similarity searches on abstract embeddings and product value propositions.
4. **Tiered Caching:** Fast-path caching of high-frequency endpoints (`/api/v1/analytics/overview`, `/api/v1/entities/graph`) via Redis with 60-second TTL invalidation on ingestion commits.
