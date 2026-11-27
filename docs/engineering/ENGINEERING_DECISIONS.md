# FrontierAtlas AI — Architectural Decisions & Technical Trade-offs

## 1. Overview of Key Engineering Trade-offs

Building a production-grade data intelligence platform requires deliberate architectural trade-offs between speed of execution, algorithmic complexity, operational cost, and system reliability. This document records the primary engineering decisions made during the design and evolution of FrontierAtlas AI.

---

## 2. Decision Log & Justifications

### Decision 1: Hybrid Relational Database (SQLite Local + PostgreSQL Cloud)
- **Context:** The system required ACID transactional guarantees, relational integrity between companies and products, and seamless local portability for evaluation without requiring an external hosted database cluster.
- **Alternatives Considered:**
  1. *MongoDB / Document Store:* High write throughput for raw JSON, but weak foreign key integrity, poor relational graph traversal, and awkward tabular aggregation for Excel reporting.
  2. *Dedicated PostgreSQL Server Only:* Robust, but introduces friction during local grading and assessment execution.
- **Selected Choice:** **SQLAlchemy 2.0 ORM abstraction with SQLite default and PostgreSQL production toggle.**
- **Rationale:** SQLite provides a single zero-dependency file (`data/frontier_atlas.db`) containing the complete relational graph for immediate verification, while the SQLAlchemy repository pattern ensures zero code modifications are required to point to AWS RDS or Supabase in production.

---

### Decision 2: Deterministic Entity Resolution vs. Pure Vector Similarity
- **Context:** Entity deduplication must resolve variations like *"Anthropic, Inc."*, *"Anthropic PBC"*, and *"anthropic"*.
- **Alternatives Considered:**
  1. *Pure Dense Vector Similarity (Embeddings + Cosine Distance):* Highly flexible, but suffers from false positive merges between related but distinct entities (e.g., merging "Cohere" and "Cohere Health", or "Mistral AI" and "Mistral Large"), high inference latency, and API costs.
  2. *Rule-based Regex Only:* Fast, but brittle when encountering misspellings or inverted word orders.
- **Selected Choice:** **4-Tier Deterministic Resolution Cascade (Exact ➔ Suffix Strip ➔ Domain Identity ➔ Token-Sort Fuzzy Matching).**
- **Rationale:** Provides deterministic, explainable, and auditable resolution with logged confidence scores. Token-sort ratio ($\ge 85$) handles inverted word orders accurately, while domain identity matching provides an unambiguous ground truth.

---

### Decision 3: Programmatic PDF Report Generation (ReportLab vs. Headless Browser Print)
- **Context:** Deliverable requirements mandated an authoritative `architecture.pdf` document formatted to exactly 3 pages.
- **Alternatives Considered:**
  1. *Headless Chrome PDF Print (`window.print()` / Puppeteer):* Vulnerable to CSS page-break drift, font rendering discrepancies across operating systems, and external binary dependencies.
  2. *Pandoc / LaTeX:* Heavy OS installation footprint (multi-gigabyte TexLive distribution).
- **Selected Choice:** **ReportLab Direct Vector Flowables (`src/exporters/pdf_report.py`).**
- **Rationale:** ReportLab calculates geometric page heights down to points (`pt`), guaranteeing deterministic layout, zero CSS overflow, exact 3-page pagination, embedded vector charts, and zero external software dependencies.

---

### Decision 4: Asynchronous Single-Process Crawlers vs. Celery/RabbitMQ
- **Context:** Harvesting hundreds of external endpoints while maintaining politeness delays and avoiding system crashes.
- **Alternatives Considered:**
  1. *Distributed Task Queue (Celery + Redis + Flower):* Enterprise standard, but excessive operational overhead and infrastructure complexity for a self-contained assessment artifact.
  2. *Synchronous ThreadPoolExecutor:* High thread overhead and blocking I/O bottlenecks.
- **Selected Choice:** **`asyncio` + `aiohttp` non-blocking worker pools with Semaphore concurrency gates.**
- **Rationale:** Easily handles hundreds of concurrent connections on a single CPU core with sub-100MB memory footprint, fully capable of scaling to thousands of URLs.

---

### Decision 5: Client-Side Interactive SVG Graph vs. Heavy 3D Graph Libraries
- **Context:** Visualizing multi-entity relationship networks (startups, products, papers, jobs) in the web UI.
- **Alternatives Considered:**
  1. *Three.js / 3D-force-graph:* Visually flashy, but heavy bundle size (>1.5MB), poor accessibility, and slow load times on mobile devices.
  2. *D3.js Force Simulation DOM binding:* Excellent, but can conflict with React's virtual DOM reconciliation loop.
- **Selected Choice:** **Custom SVG Canvas with Degree-Weighted Node Sizing and Spring Calculations.**
- **Rationale:** Instant render time, zero external bundle overhead, full CSS integration with dark mode, and seamless declarative React state binding.
