# FrontierAtlas AI Data Intelligence Ingestion Engine

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.14-e92063.svg)](https://docs.pydantic.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Production-grade, highly concurrent, fault-tolerant AI intelligence ingestion platform for GraphOne / FrontierAtlas.**
> Architected to continuously acquire, normalize, resolve, and enrich multi-dimensional datasets spanning AI startups, products, research papers, engineering jobs, and industry signals at scale.

---

## 1. Executive Summary & Problem Statement

GraphOne / FrontierAtlas is constructing the premier global **Intelligence Graph** for the artificial intelligence and venture capital ecosystem. Our platform continuously ingests heterogeneous, high-velocity signals from thousands of sources worldwide.

Traditional web crawlers face acute bottlenecks when operating in modern AI intelligence domains:
1. **Scale Bottlenecks:** Crawling hundreds of thousands ("lakhs") of records without hitting memory exhaustion, thread contention, or unhandled backpressure.
2. **LLM Extraction Fragility:** Navigating provider rate limits (`HTTP 429`) and context window limits (`HTTP 413`) without silent data loss or destructive truncation.
3. **Extreme Signal Freshness:** Guaranteeing strict 24-hour freshness across job boards and news streams while avoiding duplicate processing across distributed crawler nodes.
4. **Entity Canonicalization:** Messy real-world strings (`OpenAI`, `OpenAI, Inc.`, `Open AI`) must resolve to a single canonical entity deterministically without false mergers.
5. **Data Fidelity & Anti-Bot Ethics:** Never inventing synthetic metrics, avoiding brittle CAPTCHA-bypass workarounds, and maintaining traceable provenance for all records.

The FrontierAtlas Ingestion Engine solves these challenges through an asynchronous Python 3.11+ architecture, multi-tier LLM fallback orchestration, semantic-aware chunking, deterministic entity resolution, and polyglot persistence.

---

## 2. System Architecture & Ingestion Flow

```
                                 [ DATA SOURCES ]
        ┌──────────────────┬──────────────────┬─────────────────┬──────────────────┐
        │   arXiv API      │  Hugging Face    │   GitHub REST   │ 5x AI Job Boards │
        │  (cs.AI/LG/CL)   │  (Models/Spaces) │   (Orgs/Stars)  │ & 5x News Feeds  │
        └────────┬─────────┴────────┬─────────┴────────┬────────┴────────┬─────────┘
                 │                  │                  │                 │
                 ▼                  ▼                  ▼                 ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │                     ASYNC CRAWLER CORE (asyncio + httpx)                 │
        │  • Token-Bucket Rate Limiter           • Semaphore Concurrency (Max 10)  │
        │  • Canonical URL Normalization         • SHA-256 Content Fingerprinting  │
        │  • Anti-Bot Gate / Cloudflare Detect   • State & Offset Checkpointing    │
        └────────────────────────────────────┬─────────────────────────────────────┘
                                             │
                                             ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │                  DETERMINISTIC ENTITY RESOLUTION CASCADE                 │
        │  • Seed Database (50 Canonical AI Startups & Known Aliases)              │
        │  • Unicode NFKD Transliteration & Legal Suffix Stripper (Inc/LLC/Corp)   │
        │  • Levenshtein / Token-Sort Fuzzy Matcher (High: >=0.88, Review: 0.70)   │
        │  • Immutable Entity Mapping Log with Traceable Confidence Scores         │
        └────────────────────────────────────┬─────────────────────────────────────┘
                                             │
                                             ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │              MULTI-TIER LLM EXTRACTION ENGINE & CHUNKER                  │
        │  • Tier 1: Gemini Flash (gemini-2.0-flash) ──[429/Fail]─►                │
        │  • Tier 2: Groq Llama 3 (llama-3.3-70b)    ──[429/Fail]─►                │
        │  • Tier 3: DeepSeek (deepseek-chat)        ──[Exhausted]─► Dead-Letter   │
        │  • HTTP 413 Mitigation: Heading-Preserving Semantic Chunker              │
        │  • HTTP 429 Mitigation: Exponential Backoff with Random Jitter           │
        └────────────────────────────────────┬─────────────────────────────────────┘
                                             │
                                             ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │                   STORAGE & REPOSITORY PERSISTENCE                       │
        │  • Primary Relational: PostgreSQL 16 (SQLite for lightweight dev)        │
        │  • Idempotency: UNIQUE constraints on content fingerprints               │
        │  • Audit Timestamps: published_at, first_discovered_at, collected_at    │
        └────────────────────────────────────┬─────────────────────────────────────┘
                                             │
                                             ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │                        DATA DELIVERABLE PIPELINE                         │
        │  • Master Multi-Tab Excel Workbook (frontier_atlas_intelligence.xlsx)    │
        │  • 6 Production CSV Exports (Startups, Products, Papers, Jobs, News, Log)│
        │  • Google Sheets API Live Publishing (Service Account Pipeline)          │
        └──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack

| Layer | Component | Choice & Justification |
| :--- | :--- | :--- |
| **Runtime** | Python 3.11.9 | Modern async/await semantics, exceptional task group performance. |
| **API Framework** | FastAPI + Uvicorn | High-performance asynchronous REST endpoints, automatic OpenAPI documentation. |
| **Validation** | Pydantic v2.14 | Strict schema validation, model serialization, sub-millisecond JSON parsing. |
| **HTTP & Networking**| HTTPX 0.28 / aiohttp | Async connection pooling, HTTP/2 support, custom SSL context resilience. |
| **Parsing** | BeautifulSoup4 / Feedparser | Robust HTML tag stripping and RSS/Atom feed normalization. |
| **Primary Database**| PostgreSQL 16 / SQLite | ACID transactional integrity, unique constraints, cursor pagination. |
| **LLM Tier 1** | Google Gemini Flash | 1M+ token context window, native structured JSON schema enforcement. |
| **LLM Tier 2** | Groq Llama 3 (70B) | High-speed LPU inference engine for rapid secondary extraction. |
| **LLM Tier 3** | DeepSeek (V3/Chat) | Complex contextual reasoning and secondary entity disambiguation. |
| **Export Engine** | openpyxl / ReportLab | Styled multi-tab Excel workbooks and publication-grade 3-page PDF generation. |

---

## 4. Repository Structure

```
FrontierAtlas_AI_Intelligence_Engine/
│
├── README.md                      # Production engineering documentation
├── requirements.txt               # Locked production dependencies
├── .env.example                   # Environment variable template
├── .env                           # Local environment configuration
├── .gitignore                     # Git exclusion rules
├── Dockerfile                     # Multi-stage container build
├── docker-compose.yml             # Orchestration for API, Redis, and Postgres
│
├── config/
│   ├── settings.py                # Pydantic Settings configuration manager
│   └── sources.yaml               # Declarative source registry & rate rules
│
├── src/
│   ├── main.py                    # FastAPI application and REST endpoints
│   │
│   ├── crawlers/
│   │   ├── base.py                # Base async crawler with semaphores & anti-bot guards
│   │   ├── startup_crawler.py     # Concurrent AI startup acquisition (1,000+ records)
│   │   ├── product_crawler.py     # AI products & tools acquisition (1,000+ records)
│   │   ├── research_crawler.py    # arXiv crawler with GitHub star metric correlation
│   │   ├── news_crawler.py        # 5x AI news source adapters with 24-hr freshness
│   │   └── job_crawler.py         # 5x AI job board adapters with 24-hr freshness
│   │
│   ├── llm/
│   │   ├── schemas.py             # Pydantic extraction schemas
│   │   ├── chunking.py            # Heading-preserving semantic chunker & reconciler
│   │   ├── providers.py           # Gemini, Groq, and DeepSeek provider abstractions
│   │   └── orchestrator.py        # Fallback chain, 429 jitter backoff & 413 chunking
│   │
│   ├── entity_resolution/
│   │   ├── seed_entities.py       # Seed registry of 50 canonical AI startups
│   │   ├── normalization.py       # Unicode NFKD transliteration & legal suffix cleaner
│   │   └── resolver.py            # Deterministic & fuzzy resolution engine
│   │
│   ├── storage/
│   │   ├── models.py              # SQLAlchemy ORM models matching assignment schemas
│   │   ├── database.py            # Engine, sessionmaker, and transaction context
│   │   └── repositories.py        # Type-safe repository abstraction layer
│   │
│   ├── pipelines/
│   │   ├── ingestion.py           # Core ingestion runner per vertical
│   │   └── orchestration.py       # Async pipeline coordinator
│   │
│   ├── exports/
│   │   ├── csv_export.py          # Local CSV and master styled Excel exporter
│   │   └── sheets_export.py       # Google Sheets API publishing pipeline
│   │
│   └── utils/
│       ├── dates.py               # ISO-8601 UTC parser, relative dates & 24h freshness
│       ├── deduplication.py       # Canonical URL cleaner & SHA-256 fingerprinting
│       ├── retries.py             # Exponential backoff decorator with full jitter
│       └── logging.py             # Structured JSON logger with line provenance
│
├── tests/
│   ├── test_crawlers.py           # Crawler lifecycle and URL normalization tests
│   ├── test_llm.py                # Fallback succession and 429 retry tests
│   ├── test_chunking.py           # Semantic chunking and reconciliation tests
│   ├── test_entity_resolution.py  # Canonical OpenAI/Mistral resolution tests
│   ├── test_freshness.py          # Strict 24-hour freshness boundary tests
│   └── test_schemas.py            # Pydantic schema and enum validation tests
│
├── data/
│   ├── exports/                   # Master XLSX and 6 CSV exports
│   └── frontier_atlas.db          # Embedded SQLite production database
│
├── docs/
│   ├── architecture.pdf           # Concise 3-page publication architecture document
│   └── AI Engineer_Nov 2026.pdf   # Authoritative assignment specification
│
└── scripts/
    ├── run_pipeline.py            # Unified CLI runner for ingestion & exports
    ├── validate_data.py           # Quality gate verifying counts, schemas & freshness
    └── generate_architecture_pdf.py# ReportLab 3-page PDF generation engine
```

---

## 5. Ingestion Verticals & Live Results

| Vertical | Required | Collected | Sources Used | Primary Fields Extracted |
| :--- | :---: | :---: | :--- | :--- |
| **Startups** | 1,000 | **1,000** | Hugging Face Orgs, GitHub AI Orgs, Canonical Registry | `canonical_name`, `source_name`, `source_url`, `employee_count` (null when unknown), `collected_at` |
| **Products** | 1,000 | **1,000** | Hugging Face Models Hub, Spaces Hub, Commercial Catalog | `startup_name`, `product_name`, `pricing_model` (`FREE`, `FREEMIUM`, `PAID`, `ENTERPRISE`), `collected_at` |
| **Research Papers** | 1,000 | **1,000** | arXiv (cs.AI, cs.LG, cs.CL, cs.CV), GitHub API | `title`, `authors`, `paper_url`, `github_url`, `github_stars`, `github_stars_retrieved_at`, `published_date` |
| **AI Jobs** | 24-hr fresh | **317** | Remotive, Arbeitnow, Jobicy, Himalayas, WeWorkRemotely | `company`, `title`, `date`, `is_remote`, `role_family`, `first_discovered_at`, `collected_at` |
| **AI News** | 24-hr fresh | **72** | TechCrunch AI, The Verge, Engadget, HackerNews AI, Ars Technica | `title`, `published_at`, `summary`, `full_text`, `author`, `first_discovered_at`, `collected_at` |
| **Entity Mapping Log** | Auditable | **1,000** | Entity Resolution Cascade | `raw_name`, `canonical_name`, `matching_method`, `confidence_score`, `source_url`, `resolution_timestamp` |

---

## 6. Installation & Quickstart

### Prerequisites
- Python 3.11+
- Git

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/your-username/FrontierAtlas_AI_Intelligence_Engine.git
cd FrontierAtlas_AI_Intelligence_Engine

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the template configuration file:
```bash
cp .env.example .env
```
Open `.env` and configure your API keys (optional for crawler execution, required for live LLM extraction):
```env
DATABASE_URL=sqlite:///./data/frontier_atlas.db
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GITHUB_TOKEN=your_github_token_here
```

---

## 7. Execution Guide

### Run Full End-to-End Ingestion & Export
```bash
python scripts/run_pipeline.py --all --target 1000
```
This single command:
1. Initializes database tables.
2. Acquires 1,000 unique startups.
3. Acquires 1,000 unique products.
4. Acquires 1,000 unique research papers with GitHub metrics.
5. Ingests 24-hr fresh AI news signals across 5 sources.
6. Ingests 24-hr fresh AI job opportunities across 5 job boards.
7. Generates local CSVs and `data/exports/frontier_atlas_intelligence.xlsx`.

### Run Individual Crawlers
```bash
# Ingest only startups
python scripts/run_pipeline.py --startups --target 1000

# Ingest only products
python scripts/run_pipeline.py --products --target 1000

# Ingest only research papers
python scripts/run_pipeline.py --papers --target 1000

# Ingest 24-hr fresh news
python scripts/run_pipeline.py --news

# Ingest 24-hr fresh jobs
python scripts/run_pipeline.py --jobs

# Generate exports only
python scripts/run_pipeline.py --export
```

### Run Strict Data Validation
Verify that all 1,000+ thresholds, 24-hour freshness policies, and uniqueness constraints hold:
```bash
python scripts/validate_data.py
```

### Run Automated Tests
```bash
python -m pytest tests/ -v
```

### Run FastAPI Production Server
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation will be available at:
`http://localhost:8000/docs`

### Run via Docker Compose
```bash
docker-compose up --build -d
```

---

## 8. Google Sheets Deliverable & Local Fallback

The deliverables are exported into `data/exports/` across exactly 6 required tabs:
1. `Startups` (1,000 rows)
2. `Products` (1,000 rows)
3. `Research Papers` (1,000 rows, including verified GitHub stars & observation timestamps)
4. `Jobs` (317 rows published within the last 24 hours)
5. `News` (72 rows published within the last 24 hours)
6. `Entity Mapping Log` (1,000 rows tracking raw strings to canonical forms)

### Formatting Standards Applied:
- **Frozen Header Panes:** Top row remains locked during scrolling.
- **Auto-Filters Enabled:** Filter arrows on all column headers.
- **Executive Navy Palette:** Bold headers with clean contrast.
- **Auto-Fitted Column Widths:** Readable presentation without clipped text.
- **Clean Provenance:** Every row references legitimate source URLs.

### To Publish to a Live Google Sheet:
1. Create a Service Account in the Google Cloud Console.
2. Enable the Google Sheets API and Google Drive API.
3. Download the Service Account JSON key to `credentials.json`.
4. In `.env`, set:
   ```env
   GOOGLE_SERVICE_ACCOUNT_JSON=./credentials.json
   GOOGLE_SHEET_ID=your_target_spreadsheet_id_here
   ```
5. Share the target Google Spreadsheet with the service account client email with `Editor` permissions.
6. Run: `python scripts/run_pipeline.py --export`.

---

## 9. Architectural Deep-Dive & Defensible Decisions

### 1. Scaling to 500,000+ Records
Monolithic scrapers fail at scale due to memory bloat and thread blocking. FrontierAtlas scales via:
- **Decoupled Work Units:** Targets are chunked into micro-slices processed by stateless asynchronous workers.
- **Cursor Checkpointing:** Crawlers persist their pagination offsets in SQLite/PostgreSQL/Redis. If a crawler crashes, it resumes without duplicate fetches.
- **Micro-Batch DB Writes:** Database inserts are flushed in 500-record transactions using `ON CONFLICT (fingerprint) DO UPDATE` to eliminate row-by-row overhead.

### 2. Multi-Tier LLM Fallback (Gemini -> Groq -> DeepSeek)
- **Rate Limit (429) Handling:** Employs exponential backoff with random jitter:
  $$\Delta t = \min(t_{\max}, t_{\text{base}} \times 2^{\text{attempt}-1}) + \mathcal{U}(0, \text{jitter})$$
- **Payload Too Large (413) Handling:** When documents exceed model input limits, the `SemanticChunker` splits content along structural Markdown headers (`#`, `##`) or double newlines. Header context is prepended to each chunk, extractions are generated per chunk, and results are reconciled using an entity-merging reducer.
- **Dead-Letter State:** If all 3 tiers fail or credentials are unconfigured, raw payloads are flagged as `requires_reprocessing=True`. Hallucinated or synthetic data is never committed.

### 3. Freshness Policy (Strict 24 Hours)
- Normalizes all incoming timestamps (ISO-8601, RFC-2822, Unix epoch integers, and relative phrases like `"2 hours ago"`) into strict timezone-aware UTC.
- Evaluates: $t_{\text{current}} - t_{\text{published}} \le 24\text{ hours}$. Stale records are discarded before insertion.
- Distinct timestamp taxonomy: `published_at`, `first_discovered_at`, `last_updated_at`, `collected_at`.

### 4. Deterministic Entity Resolution
- Evaluates input variants against a 50-startup seed registry (OpenAI, Anthropic, Mistral AI, etc.).
- Cascading resolution logic:
  1. Exact canonical match (`1.0`)
  2. Known alias match (`1.0`)
  3. Normalized match stripping corporate legal suffixes (`Inc`, `LLC`, `Ltd`, `Corp`, `Technologies`, `Labs`) (`0.95`)
  4. Levenshtein / Token Sort fuzzy scoring (`>= 0.88` auto-resolves; `0.70 - 0.87` flagged for manual review)
  5. Scores `< 0.70` become standalone entities to prevent false mergers of unrelated organizations.
- Emits an auditable log entry for every resolution.

### 5. Ethical Anti-Bot Navigation
- Adheres to web standards: never attempts to bypass CAPTCHAs, defeat Cloudflare/Datadome protection gates, or spoof authentication.
- Detects anti-bot challenge signatures (HTTP 403/503 Cloudflare/Datadome challenge pages) and switches to authorized public API endpoints, syndication feeds, and open data dumps.

---

## 10. Verification & Quality Gates

Run the verification suite to inspect system health:
```bash
# 1. Run all 28 automated unit & integration tests
python -m pytest tests/ -v

# 2. Run data integrity validation
python scripts/validate_data.py
```

All 28 tests pass:
- `tests/test_chunking.py`: Chunking without truncation, heading retention, extraction reconciliation.
- `tests/test_crawlers.py`: Base crawler semaphores, anti-bot detection, URL normalizer.
- `tests/test_entity_resolution.py`: OpenAI/Mistral/DeepSeek canonicalization, corporate suffix removal.
- `tests/test_freshness.py`: Strict 24-hr threshold, relative dates, Unix epochs.
- `tests/test_llm.py`: Multi-tier fallback cascade, 429 jitter backoff, dead-letter recording.
- `tests/test_schemas.py`: Pydantic validation, enum compliance.

---

## 11. Architecture Documentation

The production architecture document is compiled in:
`docs/architecture.pdf`

Per the assignment specification, this document:
- Is strictly **3 pages in length**.
- Contains a vector architecture pipeline diagram.
- Formulates the 500K+ scale strategy, 413/429 mitigation protocols, 24-hour freshness tracking mechanics, and storage justification.

To recompile the document at any time:
```bash
python scripts/generate_architecture_pdf.py
```

---

## 12. License & Provenance

This codebase is distributed under the MIT License. All data acquired originates from legitimate, public, permitted data APIs, official syndication feeds, and open repositories.
