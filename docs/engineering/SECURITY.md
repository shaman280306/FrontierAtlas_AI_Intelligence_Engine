# FrontierAtlas AI — Security, Governance & Ethical Web Practices

## 1. Security Architecture & Threat Model

FrontierAtlas AI is engineered according to the principle of least privilege, zero hardcoded credentials, and strict input validation. The platform processes large volumes of external web data and therefore maintains defensive perimeter controls to prevent data poisoning, injection attacks, and credential leakage.

```
       [External Web / User Requests]
                     │
                     ▼
           [TLS 1.3 Termination]
                     │
                     ▼
     [CORS Policy & Origin Filtering]
                     │
                     ▼
     [Pydantic v2 Schema Sanitization]
                     │
                     ▼
   [SQLAlchemy Parameterized Queries]
                     │
                     ▼
        [Encrypted / Isolated Store]
```

---

## 2. Credential Management & Zero-Secret Policy

1. **Environment Isolation:** Secrets, API tokens, and database credentials are strictly isolated from source code using `.env` files parsed via `python-dotenv` and Pydantic `BaseSettings`.
2. **Git Tracking Rules:** Root `.gitignore` explicitly prevents `.env`, `*.pem`, `*.key`, `secrets.json`, and credentials files from being committed.
3. **Auditing Verification:** Prior to any commit, automated checks run `git status` and scan repository files for accidental pattern leaks (regex match for `AIza...`, `sk-...`, `ghp_...`).
4. **Graceful Degraded Mode:** If external LLM API keys (`GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) are omitted or unavailable, the system safely falls back to local deterministic rule-based extractors rather than crashing or hanging.

---

## 3. Ethical Scraping & Anti-Abuse Compliance

FrontierAtlas AI adheres strictly to industry standards for responsible automated data collection:

- **Robots.txt Compliance:** Crawlers inspect `robots.txt` directives prior to initiating scrapes on target hostnames.
- **Identifiable User-Agent:** All HTTP requests emit a clear, contact-bearing User-Agent header:
  `Mozilla/5.0 (compatible; FrontierAtlasBot/2.0; +https://github.com/shaman280306/FrontierAtlas_AI_Intelligence_Engine)`
- **Concurrency & Politeness Delays:** Scrapers implement intentional rate-limiting delays (minimum 500ms to 2s between consecutive requests per domain) to prevent server overload on target domains.
- **No Access Control Bypasses:** The ingestion engine never attempts to bypass paywalls, solve CAPTCHAs, or spoof credentials. Only publicly accessible, indexable content is harvested.

---

## 4. Input Validation & Query Sanitization

- **SQL Injection Prevention:** All database operations are mediated exclusively through SQLAlchemy 2.0 ORM query builders with parameterized inputs. Raw string interpolation in SQL clauses is strictly forbidden.
- **Cross-Site Scripting (XSS) Mitigation:** The Next.js 14 frontend renders data using native React JSX string interpolation, which automatically escapes HTML entities. Rich markdown descriptions are passed through sanitized AST parsers.
- **Cross-Origin Resource Sharing (CORS):** The FastAPI service permits CORS headers only for configured origins in production, defaulting to explicit local developer hosts during development.
- **Parameter Bounds Enforcement:** Pagination query parameters (`page`, `limit`) are strictly clamped ($1 \le \text{limit} \le 100$) using FastAPI `Query(ge=1, le=100)` validators to prevent unbounded memory allocation denial-of-service.
