import os
from typing import Optional, Dict, Any, List
from pathlib import Path
from fastapi import FastAPI, Depends, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.settings import settings
from src.storage.database import init_db, get_db
from src.storage.repositories import (
    StartupRepository, ProductRepository, PaperRepository, JobRepository, NewsRepository, EntityMappingRepository
)
from src.services.analytics import AnalyticsService
from src.services.graph import EntityGraphService
from src.services.trends import TrendIntelligenceService
from src.services.quality import DataQualityService
from src.services.search import GlobalSearchService
from src.services.ai_assistant import AIAssistantService
from src.pipelines.orchestration import PipelineOrchestrator
from src.exports.sheets_export import GoogleSheetsExporter
from src.utils.logging import app_logger

from src.storage.seeder import seed_database_if_empty

app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="Enterprise-grade AI Ecosystem Intelligence Platform for FrontierAtlas."
)

# Enable CORS with explicit origins & regex for Vercel production + preview deployments
allowed_origins = [
    "https://frontieratlas-frontend.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]
env_cors = os.getenv("CORS_ORIGINS", "")
if env_cors:
    for o in env_cors.split(","):
        clean_o = o.strip()
        if clean_o and clean_o not in allowed_origins:
            allowed_origins.append(clean_o)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    # Automated Canonical Data Seeder Check
    try:
        from src.storage.database import SessionLocal
        with SessionLocal() as db_session:
            counts = seed_database_if_empty(db_session)
            app_logger.info(f"Database readiness verified on startup: {counts}")
    except Exception as e:
        app_logger.error(f"Automated data restoration check failed during startup: {e}")
    app_logger.info("FrontierAtlas AI API initialized.")

# =========================================================================
# SYSTEM & HEALTH
# =========================================================================
@app.get("/", tags=["System"])
@app.head("/", tags=["System"])
def root_endpoint(db: Session = Depends(get_db)):
    """Production root endpoint with service metadata, live health status, and documentation links."""
    try:
        startup_count = StartupRepository(db).count()
        status = "operational" if startup_count > 0 else "degraded"
    except Exception:
        status = "unhealthy"

    return {
        "name": "FrontierAtlas AI",
        "description": "Global AI Ecosystem Intelligence Engine",
        "version": app.version,
        "status": status,
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/api/v1/health",
        "live_frontend": "https://frontieratlas-frontend.vercel.app"
    }

@app.get("/health", tags=["System"])
@app.head("/health", tags=["System"])
@app.get("/api/v1/health", tags=["System"])
@app.head("/api/v1/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """Verifies operational health, database connectivity, and record counts."""
    try:
        s_count = StartupRepository(db).count()
        p_count = ProductRepository(db).count()
        r_count = PaperRepository(db).count()
        j_count = JobRepository(db).count()
        n_count = NewsRepository(db).count()
        m_count = EntityMappingRepository(db).count()
        total = s_count + p_count + r_count + j_count + n_count + m_count

        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "database": "connected",
            "database_url": settings.DATABASE_URL.split("///")[-1] if "///" in settings.DATABASE_URL else "configured",
            "llm_tiers": {
                "tier_1_gemini": bool(settings.GEMINI_API_KEY),
                "tier_2_groq": bool(settings.GROQ_API_KEY),
                "tier_3_deepseek": bool(settings.DEEPSEEK_API_KEY)
            },
            "records_count": {
                "startups": s_count,
                "products": p_count,
                "research_papers": r_count,
                "jobs": j_count,
                "news": n_count,
                "entity_mapping_logs": m_count,
                "total_entities": total
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {e}")

# =========================================================================
# ANALYTICS & OVERVIEW KPIS
# =========================================================================
@app.get("/api/v1/stats", tags=["Intelligence"])
def get_stats(db: Session = Depends(get_db)):
    """Returns real-time record counts across all ingestion verticals."""
    s_count = StartupRepository(db).count()
    p_count = ProductRepository(db).count()
    r_count = PaperRepository(db).count()
    j_count = JobRepository(db).count()
    n_count = NewsRepository(db).count()
    m_count = EntityMappingRepository(db).count()
    return {
        "startups": s_count,
        "products": p_count,
        "research_papers": r_count,
        "jobs_24h_fresh": j_count,
        "news_24h_fresh": n_count,
        "entity_mapping_logs": m_count,
        "total_records": s_count + p_count + r_count + j_count + n_count + m_count
    }

@app.get("/api/v1/analytics/overview", tags=["Intelligence"])
def get_overview_analytics(db: Session = Depends(get_db)):
    """Provides full executive intelligence dashboard aggregates."""
    service = AnalyticsService(db)
    return service.get_overview_kpis()

# =========================================================================
# STARTUP INTELLIGENCE
# =========================================================================
@app.get("/api/v1/startups", tags=["Startups"])
def list_startups(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=500), # Backwards compatibility
    search: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    has_employees: Optional[bool] = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    repo = StartupRepository(db)
    # If legacy limit parameter is passed without page
    if limit is not None:
        records = repo.get_all(limit=limit)
        return {
            "total": repo.count(),
            "limit": limit,
            "data": [r.to_canonical_dict() for r in records]
        }
    return repo.paginate(
        page=page,
        page_size=page_size,
        search=search,
        source=source,
        has_employees=has_employees,
        sort_by=sort_by,
        order=order
    )

@app.get("/api/v1/startups/sources", tags=["Startups"])
def get_startup_sources(db: Session = Depends(get_db)):
    repo = StartupRepository(db)
    return {"sources": repo.get_sources()}

@app.get("/api/v1/startups/{startup_id}", tags=["Startups"])
def get_startup_detail(startup_id: int, db: Session = Depends(get_db)):
    repo = StartupRepository(db)
    startup = repo.get_by_id(startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup.to_full_dict()

# =========================================================================
# AI PRODUCT DISCOVERY
# =========================================================================
@app.get("/api/v1/products", tags=["Products"])
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=500), # Backwards compatibility
    search: Optional[str] = Query(None),
    pricing_model: Optional[str] = Query(None),
    startup_name: Optional[str] = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    repo = ProductRepository(db)
    if limit is not None:
        records = repo.get_all(limit=limit)
        return {
            "total": repo.count(),
            "limit": limit,
            "data": [p.to_canonical_dict() for p in records]
        }
    return repo.paginate(
        page=page,
        page_size=page_size,
        search=search,
        pricing_model=pricing_model,
        startup_name=startup_name,
        sort_by=sort_by,
        order=order
    )

@app.get("/api/v1/products/pricing-distribution", tags=["Products"])
def get_product_pricing_distribution(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return {"distribution": repo.get_pricing_distribution()}

@app.get("/api/v1/products/compare", tags=["Products"])
def compare_products(ids: str = Query(..., description="Comma-separated product IDs"), db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    try:
        id_list = [int(i.strip()) for i in ids.split(",") if i.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product IDs")
    products = repo.get_for_comparison(id_list)
    return {"products": [p.to_full_dict() for p in products]}

@app.get("/api/v1/products/{product_id}", tags=["Products"])
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.to_full_dict()

# =========================================================================
# RESEARCH INTELLIGENCE
# =========================================================================
@app.get("/api/v1/research-papers", tags=["Research"])
def list_research_papers(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=500), # Backwards compatibility
    search: Optional[str] = Query(None),
    has_github: Optional[bool] = Query(None),
    min_stars: Optional[int] = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    repo = PaperRepository(db)
    if limit is not None:
        records = repo.get_all(limit=limit)
        return {
            "total": repo.count(),
            "limit": limit,
            "data": [r.to_canonical_dict() for r in records]
        }
    return repo.paginate(
        page=page,
        page_size=page_size,
        search=search,
        has_github=has_github,
        min_stars=min_stars,
        sort_by=sort_by,
        order=order
    )

@app.get("/api/v1/research-papers/top-starred", tags=["Research"])
def get_top_starred_papers(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    repo = PaperRepository(db)
    top = repo.get_top_starred(limit=limit)
    return {"papers": [p.to_full_dict() for p in top]}

@app.get("/api/v1/research-papers/{paper_id}", tags=["Research"])
def get_paper_detail(paper_id: int, db: Session = Depends(get_db)):
    repo = PaperRepository(db)
    paper = repo.get_by_id(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Research paper not found")
    return paper.to_full_dict()

# =========================================================================
# ENGINEERING JOBS
# =========================================================================
@app.get("/api/v1/jobs", tags=["Jobs"])
def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=500), # Backwards compatibility
    search: Optional[str] = Query(None),
    is_remote: Optional[bool] = Query(None),
    role_family: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    repo = JobRepository(db)
    if limit is not None:
        records = repo.get_all(limit=limit)
        return {
            "total": repo.count(),
            "freshness_window": "24 hours",
            "data": [j.to_canonical_dict() for j in records]
        }
    return repo.paginate(
        page=page,
        page_size=page_size,
        search=search,
        is_remote=is_remote,
        role_family=role_family,
        source=source,
        sort_by=sort_by,
        order=order
    )

@app.get("/api/v1/jobs/sources", tags=["Jobs"])
def get_job_sources(db: Session = Depends(get_db)):
    repo = JobRepository(db)
    return {"sources": repo.get_sources()}

@app.get("/api/v1/jobs/{job_id}", tags=["Jobs"])
def get_job_detail(job_id: int, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    job = repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job opening not found")
    return job.to_full_dict()

# =========================================================================
# INDUSTRY NEWS
# =========================================================================
@app.get("/api/v1/news", tags=["News"])
def list_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=500), # Backwards compatibility
    search: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    repo = NewsRepository(db)
    if limit is not None:
        records = repo.get_all(limit=limit)
        return {
            "total": repo.count(),
            "freshness_window": "24 hours",
            "data": [n.to_canonical_dict() for n in records]
        }
    return repo.paginate(
        page=page,
        page_size=page_size,
        search=search,
        source=source,
        sort_by=sort_by,
        order=order
    )

@app.get("/api/v1/news/sources", tags=["News"])
def get_news_sources(db: Session = Depends(get_db)):
    repo = NewsRepository(db)
    return {"sources": list(repo.get_source_distribution().keys())}

@app.get("/api/v1/news/{news_id}", tags=["News"])
def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    repo = NewsRepository(db)
    item = repo.get_by_id(news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News article not found")
    return item.to_full_dict()

# =========================================================================
# ENTITY RESOLUTION & GRAPH EXPLORER
# =========================================================================
@app.get("/api/v1/entity-mappings", tags=["Entity Resolution"])
def list_entity_mappings(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    limit: Optional[int] = Query(None, ge=1, le=500), # Backwards compatibility
    search: Optional[str] = Query(None),
    method: Optional[str] = Query(None),
    min_confidence: Optional[float] = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    repo = EntityMappingRepository(db)
    if limit is not None:
        records = repo.get_all(limit=limit)
        return {
            "total": repo.count(),
            "data": [m.to_canonical_dict() for m in records]
        }
    return repo.paginate(
        page=page,
        page_size=page_size,
        search=search,
        method=method,
        min_confidence=min_confidence,
        sort_by=sort_by,
        order=order
    )

@app.get("/api/v1/entities/top-connected", tags=["Entity Resolution"])
def get_top_connected_entities(limit: int = Query(15, ge=1, le=50), db: Session = Depends(get_db)):
    service = EntityGraphService(db)
    return {"entities": service.list_top_connected_entities(limit=limit)}

@app.get("/api/v1/entities/{entity_name}/graph", tags=["Entity Resolution"])
def get_entity_relationship_graph(entity_name: str, db: Session = Depends(get_db)):
    service = EntityGraphService(db)
    return service.get_entity_graph(entity_name=entity_name)

# =========================================================================
# TREND INTELLIGENCE (FRONTIER SIGNALS)
# =========================================================================
@app.get("/api/v1/trends", tags=["Trends"])
def get_frontier_signals(db: Session = Depends(get_db)):
    service = TrendIntelligenceService(db)
    return service.get_frontier_signals()

# =========================================================================
# DATA QUALITY & AUDIT
# =========================================================================
@app.get("/api/v1/quality/metrics", tags=["Data Quality"])
def get_quality_metrics(db: Session = Depends(get_db)):
    service = DataQualityService(db)
    return service.get_quality_report()

# =========================================================================
# GLOBAL MULTI-ENTITY SEARCH
# =========================================================================
@app.get("/api/v1/search", tags=["Search"])
def global_search(q: str = Query(..., min_length=2), limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    service = GlobalSearchService(db)
    return service.search(query=q, limit_per_category=limit)

# =========================================================================
# AI ASSISTANT & GROUNDED DISCOVERY
# =========================================================================
class AIQueryRequest(BaseModel):
    prompt: str

@app.post("/api/v1/ai/query", tags=["AI Assistant"])
def query_ai_assistant(req: AIQueryRequest, db: Session = Depends(get_db)):
    service = AIAssistantService(db)
    return service.query_intelligence(user_prompt=req.prompt)

# =========================================================================
# REPORTS & EXPORTS
# =========================================================================
@app.get("/api/v1/reports/list", tags=["Reports"])
def list_available_reports():
    exports_dir = settings.EXPORTS_DIR
    docs_dir = settings.DOCS_DIR
    files = []

    if exports_dir.exists():
        for f in exports_dir.iterdir():
            if f.is_file() and not f.name.startswith("."):
                files.append({
                    "filename": f.name,
                    "size_bytes": f.stat().st_size,
                    "format": f.suffix.replace(".", "").upper(),
                    "type": "Data Workbook" if f.suffix == ".xlsx" else "CSV Tab Export"
                })

    arch_pdf = docs_dir / "architecture.pdf"
    if arch_pdf.exists():
        files.append({
            "filename": "architecture.pdf",
            "size_bytes": arch_pdf.stat().st_size,
            "format": "PDF",
            "type": "Architecture Specification (3 Pages)"
        })

    return {"reports": files}

@app.get("/api/v1/reports/download/{filename}", tags=["Reports"])
def download_report(filename: str):
    # Security check: prevent directory traversal
    clean_name = os.path.basename(filename)
    
    # Check in exports dir
    target_path = settings.EXPORTS_DIR / clean_name
    if not target_path.exists():
        # Check in docs dir
        target_path = settings.DOCS_DIR / clean_name

    if not target_path.exists() or not target_path.is_file():
        raise HTTPException(status_code=404, detail="Requested file not found")

    return FileResponse(
        path=str(target_path),
        filename=clean_name,
        media_type="application/octet-stream"
    )

# =========================================================================
# PIPELINE & INGESTION RUNNER (PRESERVED)
# =========================================================================
@app.get("/api/v1/ingestion/status", tags=["Pipeline"])
def get_ingestion_status(db: Session = Depends(get_db)):
    return {
        "status": "READY",
        "worker_concurrency": settings.MAX_CONCURRENT_REQUESTS,
        "per_domain_concurrency": settings.PER_DOMAIN_CONCURRENCY,
        "active_sources": {
            "startups": ["Hugging Face Organizations", "GitHub AI Orgs"],
            "products": ["Hugging Face Models", "Hugging Face Spaces"],
            "research": ["arXiv CS.AI/CS.LG/CS.CL", "Papers with Code"],
            "jobs": ["Remotive", "Arbeitnow", "Jobicy", "Himalayas", "WeWorkRemotely"],
            "news": ["TechCrunch AI", "The Verge", "Engadget", "HackerNews Algolia", "Ars Technica"]
        },
        "records_ingested": {
            "startups": StartupRepository(db).count(),
            "products": ProductRepository(db).count(),
            "research_papers": PaperRepository(db).count(),
            "jobs": JobRepository(db).count(),
            "news": NewsRepository(db).count()
        }
    }

@app.post("/api/v1/pipeline/run", tags=["Pipeline"])
async def trigger_pipeline(
    background_tasks: BackgroundTasks,
    startup_target: int = Query(1000, ge=10),
    product_target: int = Query(1000, ge=10),
    paper_target: int = Query(1000, ge=10)
):
    orchestrator = PipelineOrchestrator()
    background_tasks.add_task(
        orchestrator.run_full_pipeline,
        startup_target=startup_target,
        product_target=product_target,
        paper_target=paper_target
    )
    return {
        "status": "QUEUED",
        "message": f"Pipeline triggered with targets: startups={startup_target}, products={product_target}, papers={paper_target}"
    }

@app.post("/api/v1/pipeline/export", tags=["Exports"])
def trigger_export():
    exporter = GoogleSheetsExporter()
    result = exporter.publish_or_export()
    return result
