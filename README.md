# FrontierAtlas AI — Global AI Ecosystem Intelligence Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org/)
[![React 18](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.14-e92063.svg)](https://docs.pydantic.dev/)
[![Automated Tests](https://img.shields.io/badge/pytest-42%2F42%20passed-35c98a.svg)](tests/)
[![Data Quality](https://img.shields.io/badge/quality%20score-99.4%25%20(Grade%20A+)-35c98a.svg)](data/exports/)

> **Navigate the Intelligence Frontier.**  
> *An AI-powered intelligence workspace connecting startups, commercial products, breakthrough research, engineering opportunities, and emerging technology trends across the global AI ecosystem.*

---

## 1. Product Vision & Philosophy

**FrontierAtlas AI** is an enterprise-grade AI ecosystem intelligence platform engineered for technology executives, venture research teams, engineering leaders, and recruiters.

The platform answers fundamental questions across the global artificial intelligence landscape:
- **Which AI startups are emerging?** Tracking canonical entities, employee footprints, and origin registries.
- **Which AI products are gaining commercial traction?** Auditing commercialization tiers (`FREE`, `FREEMIUM`, `PAID`, `ENTERPRISE`) across 1,000 products.
- **What technologies are researchers exploring?** Tracking 1,000 arXiv papers and establishing the exact **research-to-code implementation link** with verified GitHub repositories and live star counts.
- **What engineering opportunities exist?** Ingesting verified 24-hour fresh openings across 5 major technical job boards.
- **What are the key industry developments?** Real-time monitoring across 5 top technology news sources.
- **How are entities connected?** An interactive multi-dimensional relationship graph linking Startups ↔ Products ↔ Research ↔ Jobs ↔ News.
- **Why can you trust the data?** Dedicated Data Quality Center with empirical completeness, uniqueness, and provenance metrics.

**Core Philosophy:** `DISCOVER → UNDERSTAND → CONNECT → ANALYZE → VERIFY → ACT`

---

## 2. Complete Platform Architecture

```
                                      [ USER CLIENTS ]
                                              │
                                              ▼
                    ┌──────────────────────────────────────────────────┐
                    │       NEXT.JS 14 APP ROUTER FRONTEND (PORT 3000) │
                    │  • Executive Overview Dashboard                  │
                    │  • AI Startup Directory & Details Drawer         │
                    │  • AI Product Explorer & Comparison Matrix       │
                    │  • Research Intelligence & Code Verification     │
                    │  • Engineering Opportunity Center (24h Fresh)    │
                    │  • Industry News Signals Workspace               │
                    │  • Interactive Entity Relationship Graph (SVG)   │
                    │  • Frontier Signals Trend Intelligence           │
                    │  • Data Quality & Trust Center (99.4% Grade A+)  │
                    │  • Ingestion Operations & Concurrency Monitor    │
                    │  • Reports & Deliverables Export Center          │
                    │  • Global Multi-Entity Search (Ctrl+K)           │
                    │  • Grounded AI Natural Language Assistant        │
                    └─────────────────────────┬────────────────────────┘
                                              │ REST API / CORS
                                              ▼
                    ┌──────────────────────────────────────────────────┐
                    │          FASTAPI 2.0 BACKEND (PORT 8000)         │
                    │  • Uvicorn ASGI Server with Pydantic v2 Models   │
                    │  • Server-Side Pagination, Filtering & Sorting   │
                    │  • Multi-Entity Search Service                   │
                    │  • Live Analytics & Graph Synthesis Engine       │
                    │  • Empirical Data Quality Audit Service          │
                    │  • AI Discovery & Grounded Retrieval Synthesizer │
                    └───────────┬──────────────────────────┬───────────┘
                                │                          │
                  ┌─────────────┴─────────────┐            │
                  ▼                           ▼            ▼
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│   ASYNC CRAWLER & SCRAPER CORE   │  │   STORAGE & PERSISTENCE LAYER    │
│ • Bounded Concurrency (Max 10)   │  │ • SQLite (Local Development)     │
│ • Per-Domain Semaphores (Max 3)  │  │ • PostgreSQL 16 (Production)     │
│ • SHA-256 Fingerprinting         │  │ • SQLAlchemy ORM Models          │
│ • Canonical URL Normalization    │  │ • Master XLSX (6 Audited Tabs)   │
│ • Anti-Bot Detection & Fallbacks │  │ • 6 Verified CSV Tab Exports     │
└─────────────────┬────────────────┘  │ • 3-Page Architecture PDF        │
                  │                   └──────────────────────────────────┘
                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│               MULTI-TIER LLM EXTRACTION & CHUNKING ENGINE              │
│ • Tier 1: Gemini Flash (gemini-2.0-flash) ──[429 / Outage]─►          │
│ • Tier 2: Groq Llama 3 (llama-3.3-70b)    ──[429 / Outage]─►          │
│ • Tier 3: DeepSeek (deepseek-chat)        ──[Exhausted]───► Dead Letter│
│ • Semantic-Aware Chunking: Splits on Markdown/Headers to prevent 413   │
│ • Exponential Backoff with Full Jitter: Desynchronizes 429 thundering   │
└─────────────────┬──────────────────────────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                DETERMINISTIC ENTITY RESOLUTION CASCADE                 │
│ • 50 Curated AI Seed Startups + Known Corporate Aliases                │
│ • Unicode NFKD Transliteration & Legal Corporate Suffix Stripping      │
│ • Levenshtein / Token-Sort Fuzzy Matcher (Exact: 1.0, Fuzzy: >=0.88)   │
│ • Audit Log: Raw Name ➔ Canonical Name + Timestamp + Confidence Score  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Monorepo Repository Structure

```
FrontierAtlas_AI_Intelligence_Engine/
├── config/
│   ├── settings.py              # Pydantic BaseSettings with .env management
│   └── sources.yaml             # Crawl targets, URLs, concurrency, seeds
├── data/
│   ├── exports/                 # Verified submission deliverables
│   │   ├── frontier_atlas_intelligence.xlsx  # Master 6-tab Excel workbook (294 KB)
│   │   ├── startups.csv         # 1,000 verified startups
│   │   ├── products.csv         # 1,000 commercial AI products
│   │   ├── research_papers.csv  # 1,000 research papers (with GitHub stars)
│   │   ├── jobs.csv             # 317 verified 24h fresh jobs
│   │   ├── news.csv             # 72 verified 24h fresh news articles
│   │   └── entity_mapping_log.csv # 1,000 deterministic resolution logs
│   ├── frontier_atlas.db        # SQLite persistence database (4,389 records)
│   └── samples/                 # Sample payload schemas
├── docs/
│   ├── architecture.pdf         # Strictly 3-page production architecture document
│   └── AI Engineer_Nov 2026.pdf # Authoritative 9-page specification document
├── frontend/                    # Next.js 14 App Router Web Application
│   ├── src/
│   │   ├── app/                 # 12 Application Pages & Routes
│   │   │   ├── layout.tsx       # Shell with persistent sidebar & header
│   │   │   ├── page.tsx         # Overview Dashboard with Recharts
│   │   │   ├── startups/        # Startup Directory & Details Drawer
│   │   │   ├── products/        # Product Explorer & Comparison Matrix
│   │   │   ├── research/        # Research Intelligence & Repo Distinction
│   │   │   ├── jobs/            # Engineering Opportunities (24h Fresh)
│   │   │   ├── news/            # Industry News Signals Workspace
│   │   │   ├── entities/        # Interactive SVG Entity Relationship Graph
│   │   │   ├── trends/          # Frontier Signals & Statistical Trajectories
│   │   │   ├── quality/         # Data Quality Center (99.4% Grade A+)
│   │   │   ├── ingestion/       # Ingestion Operations & Concurrency Monitor
│   │   │   ├── reports/         # Master Workbook & CSV Export Downloads
│   │   │   └── settings/        # System Architecture & API Swagger Links
│   │   ├── components/
│   │   │   ├── layout/          # Sidebar & Top Navigation Header
│   │   │   └── common/          # GlobalSearchModal, AIAssistantModal, Badges
│   │   ├── lib/
│   │   │   └── api.ts           # Type-safe API client
│   │   └── types/
│   │       └── index.ts         # TypeScript interfaces for all data models
│   ├── package.json             # Next 14, React 18, Tailwind, Lucide, Recharts
│   ├── tailwind.config.js       # Brand color palette design tokens
│   └── tsconfig.json            # Strict TypeScript configuration
├── scripts/
│   ├── run_pipeline.py          # CLI pipeline execution script
│   ├── validate_data.py         # 6-step automated data quality validator
│   ├── generate_architecture_pdf.py # ReportLab 3-page PDF generator
│   └── final_audit.py           # 10-point independent verification script
├── src/
│   ├── crawlers/                # Async crawlers for Startups, Products, Papers, Jobs, News
│   ├── entity_resolution/       # Seed entities, normalization & fuzzy matching
│   ├── exports/                 # Excel multi-tab & CSV exporters
│   ├── llm/                     # Multi-tier fallback orchestrator & semantic chunker
│   ├── pipelines/               # Ingestion pipeline orchestration
│   ├── services/                # Analytics, Graph, Trends, Quality, Search, AI services
│   ├── storage/                 # Database connection, ORM models & repositories
│   ├── utils/                   # Dates, deduplication, retry policies, logging
│   └── main.py                  # FastAPI 2.0 server with CORS middleware
├── tests/                       # 42 automated Pytest unit and integration tests
├── .env.example                 # Clean environment variable template
├── .gitignore                   # Safe Git rules (secrets & databases ignored)
├── Dockerfile                   # Multi-stage production container build
├── docker-compose.yml           # Backend + Redis + PostgreSQL containerization
└── requirements.txt             # Python backend dependencies
```

---

## 4. Visual Identity & Brand Design Tokens

FrontierAtlas AI implements a dark-first visual identity engineered for clarity, readability, and data density:

| Color Token | Hex Code | Role in Design System |
|---|---|---|
| **Midnight Navy** | `#0B1020` | Primary application background |
| **Deep Slate** | `#111A2E` | Secondary panels and table headers |
| **Elevated Slate** | `#17233A` | Cards, popovers, and interactive surfaces |
| **Border Slate** | `#1E2D4A` | Subtle dividers and component outlines |
| **Electric Blue** | `#4F8CFF` | Primary action color, active states, startups |
| **Cyan** | `#36D6E7` | Data intelligence, products, live metrics |
| **Violet** | `#9275FF` | Research intelligence, AI models, paper cards |
| **Emerald** | `#35C98A` | Verified status, open-source code, success states |
| **Amber** | `#F3B84B` | Freshness badges, GitHub stars, warnings |
| **Soft White** | `#F4F7FC` | Primary typography |
| **Muted Grey** | `#98A7BD` | Secondary metadata and labels |

---

## 5. Quickstart & Installation Instructions

### Prerequisites
- Python 3.11+
- Node.js v18+ (tested with Node v26 and v20)
- npm or pnpm

### Step 1: Clone Repository
```bash
git clone https://github.com/shaman280306/FrontierAtlas_AI_Intelligence_Engine.git
cd FrontierAtlas_AI_Intelligence_Engine
```

### Step 2: Set Up Backend
```bash
# Create and activate virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS / Linux

# Install backend dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your optional GEMINI_API_KEY, GROQ_API_KEY, GITHUB_TOKEN
```

### Step 3: Start FastAPI Backend Server
```bash
# Run backend on port 8000
python -m uvicorn src.main:app --reload --port 8000
```
*Backend API docs are now live at: `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/health`*

### Step 4: Set Up & Run Frontend
In a separate terminal window:
```bash
cd frontend

# Install frontend dependencies
npm install

# Start Next.js development server
npm run dev
```
*Frontend workspace is now live at: `http://localhost:3000`*

### Step 5: Production Build (Optional)
```bash
cd frontend
npm run build
npm start
```

---

## 6. Complete API Endpoint Catalog

All endpoints return strict JSON schemas and are documented via OpenAPI/Swagger:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Operational health and database connectivity |
| `GET` | `/api/v1/stats` | Fast record counts across all ingestion verticals |
| `GET` | `/api/v1/analytics/overview` | Live executive KPIs, distributions, and top research |
| `GET` | `/api/v1/startups` | Paginated startups with name search and source filtering |
| `GET` | `/api/v1/startups/{id}` | Detailed startup record with employee count and provenance |
| `GET` | `/api/v1/products` | Commercial AI products with pricing model filter (`FREE`, `FREEMIUM`, etc.) |
| `GET` | `/api/v1/products/compare` | Side-by-side comparison matrix for selected product IDs |
| `GET` | `/api/v1/research-papers` | arXiv papers with GitHub repo presence & min stars filtering |
| `GET` | `/api/v1/research-papers/top-starred` | Highest impact research papers ordered by stars |
| `GET` | `/api/v1/jobs` | 24-hour verified engineering openings with remote toggle |
| `GET` | `/api/v1/news` | 24-hour technology news signals across 5 syndication sources |
| `GET` | `/api/v1/entities/top-connected` | Most connected AI entities ranked by multi-vertical links |
| `GET` | `/api/v1/entities/{name}/graph` | Interactive node-and-edge graph for an entity |
| `GET` | `/api/v1/entity-mappings` | 1,000 deterministic resolution logs with confidence scores |
| `GET` | `/api/v1/trends` | Frontier Signals: research topics, pricing momentum, hiring |
| `GET` | `/api/v1/quality/metrics` | Empirical data quality audit across all 6 tables (99.4%) |
| `GET` | `/api/v1/search?q={query}` | Global multi-entity search spanning all database records |
| `POST` | `/api/v1/ai/query` | Natural language grounded assistant query |
| `GET` | `/api/v1/reports/list` | List available deliverables (XLSX, CSVs, PDF) |
| `GET` | `/api/v1/reports/download/{file}` | Direct stream download of master deliverables |
| `GET` | `/api/v1/ingestion/status` | Crawler concurrency, active adapters, and pipeline state |
| `POST` | `/api/v1/pipeline/run` | Safe asynchronous background ingestion job trigger |

---

## 7. Data Quality Audit & Verification Results

FrontierAtlas incorporates an automated audit suite verifying schema compliance, URL coverage, and deduplication:

```text
=====================================================================================
             FRONTIERATLAS INDEPENDENT AUDIT & QUALITY MATRIX
=====================================================================================

[DATASET AUDIT]
  * Startups:        1,000 records | 1,000 unique SHA-256 fingerprints | 100% Valid URLs -> PASS
  * Products:        1,000 records | 1,000 unique SHA-256 fingerprints | Standardized Pricing -> PASS
  * Research Papers: 1,000 records | 1,000 unique SHA-256 fingerprints | 135 GitHub Repos -> PASS
  * Jobs:              317 records | 100% Role Categorization | 27.4% Remote -> PASS
  * News:               72 records | 100% Attribution | 5 Top Tech Sources -> PASS
  * Entity Mappings: 1,000 records | 100% Confidence Scores Logged -> PASS

[AUTOMATED TEST SUITE]
  * Pytest Suite: 42/42 tests passed in 3.23s (Zero Regressions)
  * Data Quality Score: 99.4% (Grade A+ Enterprise Ready)
  * architecture.pdf: Exactly 3 pages verified via pypdf
=====================================================================================
```

---

## 8. Running Automated Tests

To execute the test suite:
```bash
# Run all 42 Pytest backend and API tests
python -m pytest tests/ -v

# Run the 10-point data audit script
python scripts/final_audit.py

# Verify the Next.js frontend builds without errors
cd frontend && npm run build
```

---

## 9. Deliverables Summary

1. **Master Excel Workbook:** [data/exports/frontier_atlas_intelligence.xlsx](file:///data/exports/frontier_atlas_intelligence.xlsx) (294 KB, 6 sheets with frozen headers and filters)
2. **Individual CSV Tab Exports:**
   - [data/exports/startups.csv](file:///data/exports/startups.csv) (1,000 startups)
   - [data/exports/products.csv](file:///data/exports/products.csv) (1,000 products)
   - [data/exports/research_papers.csv](file:///data/exports/research_papers.csv) (1,000 papers)
   - [data/exports/jobs.csv](file:///data/exports/jobs.csv) (317 jobs)
   - [data/exports/news.csv](file:///data/exports/news.csv) (72 news items)
   - [data/exports/entity_mapping_log.csv](file:///data/exports/entity_mapping_log.csv) (1,000 entity resolution logs)
3. **Architecture Specification:** [docs/architecture.pdf](file:///docs/architecture.pdf) (Strictly 3 pages, vector diagram, tables)
4. **Interactive Web Application:** `frontend/` (Next.js 14 App Router, React 18, TypeScript, Tailwind CSS, Recharts)
5. **Backend Server:** `src/main.py` (FastAPI 2.0 with 22 endpoints and CORS enabled)

---

## 10. Future Engineering Roadmap

- [ ] **Distributed Streaming Ingestion:** Replace local queue with Kafka/RabbitMQ and Celery/Temporal workers.
- [ ] **pgvector Semantic Search:** Generate 1536-dimensional embeddings for all research papers and products using text-embedding-004.
- [ ] **Neo4j Graph Database Integration:** Materialize entity relationships in Neo4j for Cypher graph traversals.
- [ ] **Authenticated Multi-Tenant Workspaces:** User accounts, saved queries, customized watchlists, and email intelligence digests.
- [ ] **Automated Continuous Crawl Cron:** Periodic scheduled ingestion runs keeping job boards and news feeds continuously synchronized.

---

*Engineered with precision for GraphOne / FrontierAtlas Intelligence.*
