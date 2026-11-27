# FrontierAtlas AI — REST API Reference Specification

## 1. Overview & Base Configuration

The FrontierAtlas AI backend is built on **FastAPI (Python 3.11+)** and follows RESTful conventions. It provides 22 structured endpoints for data exploration, entity resolution, graph traversal, market trends, quality validation, and administrative ingestion monitoring.

- **Base URL (Local):** `http://localhost:8000`
- **Base URL (Production):** Configurable via `NEXT_PUBLIC_API_BASE_URL`
- **Interactive Documentation:**
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`
  - OpenAPI JSON Specification: `http://localhost:8000/openapi.json`
- **Protocol:** HTTP/1.1 & HTTP/2 over TLS in production
- **Response Format:** `application/json; charset=utf-8`

---

## 2. Standard Response Envelope & Error Codes

### Standard Success Envelope
For paginated list queries:
```json
{
  "total": 315,
  "page": 1,
  "limit": 25,
  "items": [ ... ]
}
```

### Standard Error Envelope
FastAPI utilizes standard HTTP status codes accompanied by detailed JSON exception structures:
```json
{
  "detail": "Entity with ID 'startup_999' not found"
}
```

| HTTP Code | Description | Scenario |
| :--- | :--- | :--- |
| `200 OK` | Request succeeded | Successful data retrieval or calculation |
| `400 Bad Request` | Client error | Malformed query parameter or invalid filter enum |
| `404 Not Found` | Resource missing | Requested entity, paper, or file does not exist |
| `422 Unprocessable` | Validation error | Pydantic validation failure on request payload |
| `500 Server Error` | Internal error | Unhandled runtime exception |

---

## 3. Complete Endpoint Reference (22 Endpoints)

### 3.1 Core System & Health
#### `GET /api/v1/health`
Returns the operational health, database connectivity, and engine version.
- **Query Parameters:** None
- **Response `200 OK`:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "database": "connected",
  "records_indexed": 1045,
  "timestamp": "2026-11-27T14:55:00Z"
}
```

---

### 3.2 Analytics & Overview
#### `GET /api/v1/analytics/overview`
Returns high-level platform KPIs, entity category counts, funding totals, and remote job percentages.
- **Query Parameters:** None
- **Response `200 OK`:**
```json
{
  "total_entities": 1045,
  "startups_count": 315,
  "products_count": 218,
  "research_papers_count": 204,
  "jobs_count": 236,
  "news_count": 72,
  "total_funding_tracked_usd": 48200000000,
  "papers_with_code_percentage": 52.9,
  "remote_jobs_percentage": 68.2,
  "data_quality_score": 99.4
}
```

---

### 3.3 Startups Intelligence
#### `GET /api/v1/startups`
List and filter AI startups with multi-field search and pagination.
- **Query Parameters:**
  - `page` (int, default: 1): Page number.
  - `limit` (int, default: 25, max: 100): Records per page.
  - `search` (str, optional): Search keyword against name, market, description.
  - `stage` (str, optional): Filter by funding stage (`Seed`, `Series A`, `Series B`, `Series C+`, `Public`).
  - `market` (str, optional): Filter by market sector (e.g. `Healthcare`, `Developer Tools`).
  - `sort_by` (str, default: `valuation`): Sort field (`valuation`, `funding`, `employees`, `name`).
  - `sort_order` (str, default: `desc`): `asc` or `desc`.

#### `GET /api/v1/startups/{startup_id}`
Retrieve a single startup's complete dossier including connected products and founders.

#### `GET /api/v1/startups/stages/distribution`
Returns funding stage distribution aggregation across all indexed startups.

---

### 3.4 Products Intelligence
#### `GET /api/v1/products`
List commercial AI products with filtering by pricing model and target audience.
- **Query Parameters:**
  - `page`, `limit`, `search`
  - `pricing_model` (str, optional): `Free`, `Freemium`, `Paid`, `Enterprise`, `Open Source`.
  - `target_audience` (str, optional): Filter by user persona (e.g. `Developers`, `Enterprise`).

#### `GET /api/v1/products/{product_id}`
Retrieve detailed product specification, features, and parent company mapping.

#### `GET /api/v1/products/compare`
Side-by-side comparison matrix for two or more products.
- **Query Parameters:**
  - `ids` (str, required): Comma-separated product IDs (e.g., `?ids=prod_1,prod_2`).

---

### 3.5 Research Papers Intelligence
#### `GET /api/v1/research`
Explore peer-reviewed AI breakthroughs with repository cross-referencing.
- **Query Parameters:**
  - `page`, `limit`, `search`
  - `has_github` (bool, optional): Filter papers with linked open-source repositories.
  - `category` (str, optional): ArXiv primary category (`cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`).
  - `sort_by` (str, default: `stars`): Sort by GitHub stars or publication date.

#### `GET /api/v1/research/{paper_id}`
Retrieve complete abstract, author list, ArXiv DOI, and associated GitHub repository metadata.

---

### 3.6 Engineering Opportunities
#### `GET /api/v1/jobs`
Query AI job listings with location and remote status filtering.
- **Query Parameters:**
  - `page`, `limit`, `search`
  - `is_remote` (bool, optional): Filter remote-eligible roles (`true` or `false`).
  - `company` (str, optional): Filter by hiring entity.

#### `GET /api/v1/jobs/roles/distribution`
Aggregated breakdown of job openings categorized by specialization (LLM Research, MLOps, Data Engineering, Agent Architect).

---

### 3.7 Industry News & Signals
#### `GET /api/v1/news`
Chronological news feed covering breakthroughs, funding rounds, and partnerships.
- **Query Parameters:**
  - `page`, `limit`, `search`
  - `source` (str, optional): Filter by publishing outlet.
  - `sentiment` (str, optional): `positive`, `neutral`, `negative`.

#### `GET /api/v1/news/sources`
List of distinct, verified news publication outlets indexed in the database.

---

### 3.8 Entity Graph & Relationships
#### `GET /api/v1/entities/graph`
Returns nodes and directed edges for the interactive SVG relationship network.
- **Query Parameters:**
  - `max_nodes` (int, default: 50): Number of top degree-centrality nodes to return.
  - `entity_type` (str, optional): Restrict graph to specific node types.
- **Response Structure:**
```json
{
  "nodes": [
    { "id": "ent_1", "label": "OpenAI", "type": "startup", "degree": 14 }
  ],
  "edges": [
    { "source": "ent_1", "target": "prod_1", "relationship": "develops" }
  ]
}
```

#### `GET /api/v1/entities/resolution-logs`
Audit log of entity resolution events, including fuzzy matches and confidence scores.

---

### 3.9 Market Trends & Frontier Signals
#### `GET /api/v1/trends/frontier`
Top emerging technology keywords, breakthrough velocity, and category momentum.

#### `GET /api/v1/trends/funding-timeline`
Monthly funding trajectory across the ecosystem.

---

### 3.10 Data Quality & Trust Center
#### `GET /api/v1/quality/metrics`
Overall trust index, field completeness ratios, null-rate breakdowns, and provenance stats.

---

### 3.11 Search & AI Assistant
#### `GET /api/v1/search`
Unified cross-entity search across startups, products, papers, jobs, and news.

#### `POST /api/v1/ai/assistant`
Natural language query assistant answering ecosystem questions with citations.
- **Request Body:**
```json
{
  "query": "Which startups in Healthcare have raised more than $50M?",
  "temperature": 0.2
}
```

---

### 3.12 Deliverables & Reports
#### `GET /api/v1/reports/files`
List available downloadable deliverables with verified file sizes, hashes, and download endpoints.
