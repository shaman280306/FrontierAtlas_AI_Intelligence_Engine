# FrontierAtlas AI — Global AI Ecosystem Intelligence Platform

[![CI Pipeline](https://github.com/shaman280306/FrontierAtlas_AI_Intelligence_Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/shaman280306/FrontierAtlas_AI_Intelligence_Engine/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org/)
[![React 18](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![Automated Tests](https://img.shields.io/badge/pytest-42%2F42%20passed-35c98a.svg)](tests/)
[![Data Quality](https://img.shields.io/badge/quality%20score-99.4%25%20(Grade%20A+)-35c98a.svg)](data/exports/)

> **Navigate the Intelligence Frontier.**  
> *The Intelligence Layer for the Global AI Ecosystem: An enterprise-grade platform connecting startups, commercial products, breakthrough research, engineering opportunities, and emerging technology trends.*

---

## 🚀 Live Demo & Cloud Deployment

| Component | Target URL / Status | Description |
| :--- | :--- | :--- |
| **Frontend Web Workspace** | **[Live Web App (Vercel)](https://frontieratlas-frontend.vercel.app/)** *(or `http://localhost:3000`)* | Next.js 14 App Router, Recharts, SVG Graph, 12 Modules |
| **Backend REST API** | **[FastAPI Service (Render)](https://frontieratlas-api.onrender.com)** *(or `http://localhost:8000`)* | 22 REST Endpoints, OpenAPI / Swagger Docs, CORS Enabled |
| **Interactive API Docs** | **[`/docs` (Swagger UI)](http://localhost:8000/docs)** | Interactive schema explorer and request testing console |
| **Continuous Integration** | **[GitHub Actions](https://github.com/shaman280306/FrontierAtlas_AI_Intelligence_Engine/actions)** | Automated Pytest (42 tests) & Next.js production build |

*Deployment blueprints for Render (`render.yaml`), Vercel (`frontend/vercel.json`), and Docker Compose are included directly in the repository for one-click reproducibility.*

---

## 📸 Application Showcase

The platform features an executive dark-mode analytical interface designed for high-density information exploration:

### 1. Executive Analytics & Overview Dashboard
![Overview Dashboard](docs/screenshots/dashboard_overview.png)
*Real-time ecosystem metrics: 1,000 startups, 1,000 products, 1,000 research breakthroughs, funding distribution, and research-to-code ratio.*

### 2. Interactive SVG Entity Relationship Graph
![Entity Relationship Graph](docs/screenshots/entity_graph.png)
*Real-time SVG network visualizer linking Startups ↔ Products ↔ Research Papers ↔ Jobs ↔ News, with degree-weighted node sizing.*

### 3. AI Startups Directory & Detailed Intelligence Dossier
![Startups Directory](docs/screenshots/startups_directory.png)
*Multi-field search, funding stage filters (Seed through Series C+), employee counts, and provenance tracking.*

### 4. AI Products Explorer & Side-by-Side Comparison Matrix
![Products Comparison](docs/screenshots/products_comparison.png)
*Commercial AI product directory with pricing model filters (`Free`, `Freemium`, `Paid`, `Enterprise`, `Open Source`) and side-by-side comparison.*

### 5. Research Intelligence & Code Implementation Link
![Research Intelligence](docs/screenshots/research_intelligence.png)
*arXiv research tracker establishing the explicit research-to-code link with verified GitHub repositories and live star counts.*

### 6. Engineering Opportunities & Remote Filter
![Jobs Opportunities](docs/screenshots/jobs_opportunities.png)
*Engineering openings across 5 major technical job boards with remote status toggle and category breakdowns.*

### 7. Frontier Signals & Trend Intelligence
![Trend Signals](docs/screenshots/trend_signals.png)
*Emerging technology trajectory, research velocity, and market segment momentum.*

### 8. Data Quality & Trust Center (99.4% Grade A+)
![Data Quality Center](docs/screenshots/data_quality.png)
*Empirical transparency: field completeness, null-rate audits, and deterministic resolution logs.*

### 9. Deliverables & Reports Export Center
![Reports Exports](docs/screenshots/reports_exports.png)
*One-click direct streaming downloads for Master Excel (6 sheets, 294 KB), CSVs, and the 3-page Architecture PDF.*

---

## 📚 Deep-Dive Technical Documentation

For engineering recruiters and technical leads, exhaustive specifications are available in [`docs/engineering/`](docs/engineering/):

1. **[System Architecture Specification](docs/engineering/SYSTEM_ARCHITECTURE.md)** — Architectural layers, request flow, and path to 500,000+ records.
2. **[Data Pipeline & Ingestion Engine](docs/engineering/DATA_PIPELINE.md)** — Rate limiting, 413 semantic chunking, 429 jitter backoff, and hierarchical LLM fallback.
3. **[REST API Reference Catalog](docs/engineering/API_REFERENCE.md)** — Complete schemas, parameters, and payloads for all 22 REST endpoints.
4. **[Cloud Deployment & Production Ops](docs/engineering/DEPLOYMENT.md)** — Zero-friction setup for Vercel, Render, Docker, and Kubernetes.
5. **[Security, Governance & Ethical Web Practices](docs/engineering/SECURITY.md)** — Credential isolation, robots.txt compliance, and anti-abuse policies.
6. **[Architectural Decisions & Trade-offs](docs/engineering/ENGINEERING_DECISIONS.md)** — Documented justifications (SQLite vs. PostgreSQL, ReportLab vs. Print).
7. **[Known Limitations & Engineering Roadmap](docs/engineering/KNOWN_LIMITATIONS.md)** — Honest assessment of API boundaries (GitHub 60 req/hr) and future scale roadmap.

---

## 🏛️ Platform Architecture

```mermaid
graph TD
    subgraph Sources["Heterogeneous Ingestion Sources"]
        S1["Startup Registries & Directories"]
        S2["Commercial AI Product Feeds"]
        S3["ArXiv Research Feed (cs.AI, cs.LG, cs.CL)"]
        S4["GitHub REST API v3 (Repos & Stars)"]
        S5["AI Engineering Job Boards"]
        S6["Industry RSS & News Feeds"]
    end

    subgraph Pipeline["Ingestion & Resilience Engine"]
        C1["Async Scrapers (aiohttp / asyncio / Playwright)"]
        C2["Semantic Chunker (413 Payload Splitter)"]
        C3["LLM Extraction (Gemini Pro/Flash ➔ Claude ➔ GPT-4o ➔ DLQ)"]
        C4["429 Exponential Jitter Backoff"]
    end

    subgraph Resolution["Normalization & Resolution Cascade"]
        N1["Pydantic v2 Schema Validation"]
        N2["URL & Timestamp Normalization"]
        N3["Deterministic Resolution (Aliases / Legal Suffixes / Fuzzy)"]
        N4["Entity Relationship Graph Engine"]
    end

    subgraph Storage["Storage & Deliverable Artifacts"]
        DB[("Relational Store (SQLite / PostgreSQL)")]
        EXP["Automated Exporters (Master XLSX, CSVs, 3-Page PDF)"]
    end

    subgraph Backend["FastAPI Application Services (22 Endpoints)"]
        API1["Analytics & KPI Service"]
        API2["Graph & Degree Centrality Service"]
        API3["Frontier Trends & Topic Service"]
        API4["Data Quality & Audit Engine (99.4%)"]
        API5["Global Search & AI Query Assistant"]
    end

    subgraph Frontend["Next.js 14 Web Workspace (12 Modules)"]
        UI1["Overview & Market Analytics"]
        UI2["Directories (Startups, Products, Papers, Jobs, News)"]
        UI3["Interactive SVG Network Graph"]
        UI4["Command Palette (Ctrl+K) & Natural Language Assistant"]
        UI5["Data Trust & Export Hub"]
    end

    Sources --> Pipeline
    C1 --> C2 --> C3
    C3 -- 429 Rate Limit --> C4 --> C3
    C3 --> Resolution
    N1 --> N2 --> N3 --> N4
    N4 --> Storage
    Storage --> EXP
    Storage --> Backend
    Backend --> Frontend
```

---

## 💻 Monorepo Structure

```
FrontierAtlas_AI_Intelligence_Engine/
├── .github/
│   └── workflows/ci.yml         # GitHub Actions CI (Pytest 42/42 + Next.js build)
├── config/
│   ├── settings.py              # Pydantic BaseSettings with .env management
│   └── sources.yaml             # Crawl targets, URLs, concurrency, seeds
├── data/
│   ├── exports/                 # Verified submission deliverables
│   │   ├── frontier_atlas_intelligence.xlsx  # Master 6-tab Excel workbook (294 KB)
│   │   ├── startups.csv         # 1,000 verified startups
│   │   ├── products.csv         # 1,000 commercial AI products
│   │   ├── research_papers.csv  # 1,000 research papers (with GitHub stars)
│   │   ├── jobs.csv             # 317 verified jobs
│   │   ├── news.csv             # 72 verified news articles
│   │   └── entity_mapping_log.csv # 1,000 deterministic resolution logs
│   ├── frontier_atlas.db        # SQLite persistence database (4,389 records)
│   └── samples/                 # Sample payload schemas
├── docs/
│   ├── engineering/             # In-depth recruiter & architect documentation
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   ├── DATA_PIPELINE.md
│   │   ├── API_REFERENCE.md
│   │   ├── DEPLOYMENT.md
│   │   ├── SECURITY.md
│   │   ├── ENGINEERING_DECISIONS.md
│   │   └── KNOWN_LIMITATIONS.md
│   ├── screenshots/             # High-res application screenshots
│   ├── architecture.pdf         # Strictly 3-page production architecture document
│   └── AI Engineer_Nov 2026.pdf # Authoritative 9-page specification document
├── frontend/                    # Next.js 14 App Router Web Application
│   ├── src/
│   │   ├── app/                 # 12 Application Pages & Routes
│   │   ├── components/          # Sidebar, Header, GlobalSearchModal, Badges
│   │   ├── lib/api.ts           # Type-safe API client
│   │   └── types/index.ts       # TypeScript interfaces for all data models
│   ├── vercel.json              # Vercel deployment configuration
│   └── package.json             # Next 14, React 18, Tailwind, Lucide, Recharts
├── scripts/
│   ├── run_pipeline.py          # CLI pipeline execution script
│   ├── validate_data.py         # 6-step automated data quality validator
│   ├── generate_architecture_pdf.py # ReportLab 3-page PDF generator
│   ├── capture_screenshots.py   # Headless Chrome screenshot automation
│   └── final_audit.py           # 10-point independent verification script
├── src/
│   ├── crawlers/                # Async crawlers for Startups, Products, Papers, Jobs, News
│   ├── entity_resolution/       # Seed entities, normalization & fuzzy matching
│   ├── exports/                 # Excel multi-tab & CSV exporters
│   ├── llm/                     # Multi-tier fallback orchestrator & semantic chunker
│   ├── pipelines/               # Ingestion pipeline orchestration
│   ├── services/                # Analytics, Graph, Trends, Quality, Search, AI services
│   ├── storage/                 # Database connection, ORM models & repositories
│   └── main.py                  # FastAPI 2.0 server with 22 endpoints & CORS
├── tests/                       # 42 automated Pytest unit and integration tests
├── .env.example                 # Clean environment variable template
├── .gitignore                   # Safe Git rules (zero secrets or credentials)
├── Dockerfile                   # Backend production container build
├── docker-compose.yml           # Unified multi-service container orchestration
├── render.yaml                  # Render Blueprint for automated deployment
└── requirements.txt             # Python backend dependencies
```

---

## ⚡ Quickstart & Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (tested on Node 20 & 26)
- Git

### 1. Clone & Environment
```bash
git clone https://github.com/shaman280306/FrontierAtlas_AI_Intelligence_Engine.git
cd FrontierAtlas_AI_Intelligence_Engine

# Copy environment template
cp .env.example .env
```

### 2. Launch Backend (Terminal 1)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run FastAPI server
python -m uvicorn src.main:app --reload --port 8000
```
*API docs will be available at: `http://127.0.0.1:8000/docs`*

### 3. Launch Frontend (Terminal 2)
```bash
cd frontend

# Install Node dependencies
npm install

# Run Next.js in development mode
npm run dev
```
*Web application workspace will be available at: `http://localhost:3000`*

---

## 🧪 Testing & Verification

The project includes an automated test suite with **42 passing tests** across crawlers, chunking, schema validation, entity resolution, LLM fallback recovery, and API endpoints:

```bash
# Run the complete test suite
python -m pytest tests/ -v

# Run the independent data quality verification audit
python scripts/final_audit.py

# Verify Next.js frontend build
cd frontend && npm run build
```

---

## 📊 Summary of Required Assessment Deliverables

All seven deliverables mandated by the original internship specification are verified and preserved in the repository:

| Deliverable | File Path | Status |
| :--- | :--- | :--- |
| **1. Master Excel Workbook** | `data/exports/frontier_atlas_intelligence.xlsx` | 294 KB, 6 sheets with frozen headers & filters |
| **2. Startups Dataset** | `data/exports/startups.csv` | 1,000 verified AI startup records |
| **3. Products Dataset** | `data/exports/products.csv` | 1,000 commercial AI products |
| **4. Research Papers Dataset** | `data/exports/research_papers.csv` | 1,000 arXiv papers (with GitHub stars) |
| **5. AI Job Opportunities** | `data/exports/jobs.csv` | 317 verified job listings |
| **6. AI Industry News** | `data/exports/news.csv` | 72 verified news articles |
| **7. Entity Mapping Log** | `data/exports/entity_mapping_log.csv` | 1,000 deterministic resolution logs |
| **8. Architecture Specification** | `docs/architecture.pdf` | Exactly 3 pages, vector diagram, tables |

---

*Engineered with precision for GraphOne / FrontierAtlas Intelligence.*
