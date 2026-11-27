# FrontierAtlas AI — Known Limitations, Edge Cases & Engineering Roadmap

## 1. Transparent Engineering Audit

In the spirit of rigorous software engineering and honest technical communication, this document outlines known constraints, edge cases, external API boundaries, and planned architectural evolutions for FrontierAtlas AI.

---

## 2. External API Boundaries & Rate Limits

### 2.1 GitHub Unauthenticated API Rate Limits
- **Constraint:** GitHub's public REST API v3 imposes an unauthenticated IP rate limit of **60 requests per hour**.
- **Impact:** When verifying GitHub stars for hundreds of ArXiv research papers without a Personal Access Token (`GITHUB_TOKEN`), crawlers will trigger HTTP 403 Forbidden after 60 requests.
- **Mitigation & Handling:** The crawler detects HTTP 403 / 429 status codes, preserves previously cached star counts, logs rate-limit boundaries, and gracefully flags repository links as verified while marking star counts pending authentication. Supplying a `GITHUB_TOKEN` in `.env` immediately expands capacity to 5,000 requests per hour.

### 2.2 ArXiv OAI-PMH Harvesting Delays
- **Constraint:** ArXiv's harvest guidelines request a polite 3-second delay between consecutive query batches.
- **Handling:** The crawler honors this constraint via `asyncio.sleep(3.0)`, meaning harvesting 1,000+ papers sequentially requires approximately 5 to 10 minutes of controlled ingestion time.

---

## 3. Data Freshness & Historical Assessment Window

- **Assessment Baseline (November 2026):**
  The original internship assessment dataset was harvested during the November 2026 evaluation window (e.g., job openings and news articles crawled on `2026-11-22`).
- **Freshness Evaluation:**
  When checking data freshness against real-time wall-clock time (`now()`), historical records correctly reflect their initial crawl date.
- **Continuous Crawling Mode:**
  The platform includes an automated scheduler (`python -m src.scheduler`) capable of executing periodic incremental crawls via cron to keep records dynamically synchronized with the current calendar day.

---

## 4. Scale Constraints & Single-Node Boundaries

| Dimension | Current Architecture | Upper Limit Before Sharding | Proposed Scale Solution |
| :--- | :--- | :--- | :--- |
| **Record Volume** | ~1,050 records | ~50,000 records on SQLite | Migrate to PostgreSQL with table partitioning and indexed B-trees. |
| **Concurrent Workers** | 10 asyncio workers | 100 coroutines / single core | Celery / Temporal distributed worker pools with Redis broker. |
| **Graph Network** | Top 50 degree nodes in UI | ~500 nodes in SVG canvas | WebGL / Canvas2D rendering via Pixi.js for 10,000+ nodes. |
| **Search Queries** | Multi-column SQL ILIKE | 100,000 text rows | Hybrid Elasticsearch / Meilisearch or PostgreSQL Full-Text Search. |

---

## 5. Engineering Roadmap (Next Iterations)

1. **RAG-Powered Entity Dossiers:** Embed company whitepapers and SEC filings using Google Gemini Embeddings to enable multi-hop question answering across corporate parentage and product lineages.
2. **Real-time Webhook Ingestion:** Ingest Hacker News, Techmeme, and Product Hunt signals via real-time webhooks rather than periodic polling.
3. **Automated Continuous Re-Verification:** Daily cron jobs to ping external startup homepages and product URLs, automatically flagging defunct domains or acquisitions.
