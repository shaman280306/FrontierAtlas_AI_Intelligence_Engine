import asyncio
from typing import Optional, Dict, Any
from fastapi import FastAPI, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from config.settings import settings
from src.storage.database import init_db, get_db
from src.storage.repositories import (
    StartupRepository, ProductRepository, PaperRepository, JobRepository, NewsRepository, EntityMappingRepository
)
from src.pipelines.orchestration import PipelineOrchestrator
from src.exports.sheets_export import GoogleSheetsExporter
from src.utils.logging import app_logger

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Scalable, fault-tolerant AI data intelligence ingestion engine for GraphOne / FrontierAtlas."
)

@app.on_event("startup")
def on_startup():
    init_db()
    app_logger.info("Application initialized.")

@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """Verifies operational health and database connectivity."""
    try:
        # Check database connectivity
        startup_count = StartupRepository(db).count()
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "database": "connected",
            "llm_tiers": {
                "tier_1_gemini": bool(settings.GEMINI_API_KEY),
                "tier_2_groq": bool(settings.GROQ_API_KEY),
                "tier_3_deepseek": bool(settings.DEEPSEEK_API_KEY)
            },
            "records_count": {
                "startups": startup_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {e}")

@app.get("/api/v1/stats", tags=["Intelligence"])
def get_stats(db: Session = Depends(get_db)):
    """Returns real-time record counts across all ingestion verticals."""
    return {
        "startups": StartupRepository(db).count(),
        "products": ProductRepository(db).count(),
        "research_papers": PaperRepository(db).count(),
        "jobs_24h_fresh": JobRepository(db).count(),
        "news_24h_fresh": NewsRepository(db).count(),
        "entity_mapping_logs": EntityMappingRepository(db).count()
    }

@app.get("/api/v1/startups", tags=["Entities"])
def list_startups(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    repo = StartupRepository(db)
    records = repo.get_all(limit=limit)
    return {
        "total": repo.count(),
        "limit": limit,
        "offset": offset,
        "data": [r.to_canonical_dict() for r in records]
    }

@app.get("/api/v1/products", tags=["Entities"])
def list_products(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    records = repo.get_all(limit=limit)
    return {
        "total": repo.count(),
        "limit": limit,
        "data": [p.to_canonical_dict() for p in records]
    }

@app.get("/api/v1/research-papers", tags=["Intelligence"])
def list_research_papers(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)):
    repo = PaperRepository(db)
    records = repo.get_all(limit=limit)
    return {
        "total": repo.count(),
        "limit": limit,
        "data": [r.to_canonical_dict() for r in records]
    }

@app.get("/api/v1/jobs", tags=["Signals"])
def list_jobs(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)):
    repo = JobRepository(db)
    records = repo.get_all(limit=limit)
    return {
        "total": repo.count(),
        "freshness_window": "24 hours",
        "data": [j.to_canonical_dict() for j in records]
    }

@app.get("/api/v1/news", tags=["Signals"])
def list_news(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)):
    repo = NewsRepository(db)
    records = repo.get_all(limit=limit)
    return {
        "total": repo.count(),
        "freshness_window": "24 hours",
        "data": [n.to_canonical_dict() for n in records]
    }

@app.get("/api/v1/entity-mappings", tags=["Entity Resolution"])
def list_entity_mappings(limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    repo = EntityMappingRepository(db)
    records = repo.get_all(limit=limit)
    return {
        "total": repo.count(),
        "data": [m.to_canonical_dict() for m in records]
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
