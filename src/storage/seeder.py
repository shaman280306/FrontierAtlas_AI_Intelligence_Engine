import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
from sqlalchemy.orm import Session

from config.settings import settings
from src.storage.models import (
    Base, StartupRecord, ProductRecord, ResearchPaperRecord, JobRecord, NewsRecord, EntityMappingLogRecord
)
from src.utils.deduplication import compute_content_fingerprint, normalize_url
from src.utils.logging import app_logger

logger = logging.getLogger("frontier_atlas.seeder")

def seed_database_if_empty(session: Session, force: bool = False) -> Dict[str, Any]:
    """
    Checks if database contains baseline canonical records.
    If database is uninitialized or has 0 startups, seeds all 4,389 records
    from canonical CSV exports in data/exports/.
    """
    existing_startups = session.query(StartupRecord).count()
    if existing_startups > 0 and not force:
        logger.info(f"Database already populated ({existing_startups} startups). Auto-seeding skipped.")
        return {
            "status": "already_populated",
            "startups": existing_startups,
            "products": session.query(ProductRecord).count(),
            "research_papers": session.query(ResearchPaperRecord).count(),
            "jobs": session.query(JobRecord).count(),
            "news": session.query(NewsRecord).count(),
            "entity_mapping_logs": session.query(EntityMappingLogRecord).count(),
        }

    logger.info("Database is empty or force=True. Starting automated canonical data restoration...")
    exports_dir = settings.EXPORTS_DIR
    if not exports_dir.exists():
        exports_dir = settings.BASE_DIR / "data" / "exports"

    counts = {
        "startups": 0,
        "products": 0,
        "research_papers": 0,
        "jobs": 0,
        "news": 0,
        "entity_mapping_logs": 0
    }

    # 1. Startups (1,000)
    startups_path = exports_dir / "startups.csv"
    if startups_path.exists():
        try:
            df_s = pd.read_csv(startups_path)
            for _, r in df_s.iterrows():
                name = str(r.get("content.entityName", "")).strip()
                url = str(r.get("source.url", "")).strip()
                if not name:
                    continue
                fp = compute_content_fingerprint(name, normalize_url(url))
                
                # Deduplication check
                if session.query(StartupRecord).filter_by(fingerprint=fp).first():
                    continue

                emp_val = r.get("content.data.employeeCount")
                emp_count = int(emp_val) if pd.notna(emp_val) else None

                rec = StartupRecord(
                    schema_version=str(r.get("schemaVersion", "1.0")),
                    record_type="STARTUP",
                    source_name=str(r.get("source.name", "FrontierAtlas")),
                    source_url=url,
                    raw_name=name,
                    canonical_name=name,
                    employee_count=emp_count,
                    website=str(r.get("website", "")) if pd.notna(r.get("website")) else None,
                    description=str(r.get("description", "")) if pd.notna(r.get("description")) else None,
                    fingerprint=fp,
                    collected_at=str(r.get("collectedAt", ""))
                )
                session.add(rec)
                counts["startups"] += 1
            session.commit()
            logger.info(f"Restored {counts['startups']} startups.")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to seed startups: {e}")

    # 2. Products (1,000)
    products_path = exports_dir / "products.csv"
    if products_path.exists():
        try:
            df_p = pd.read_csv(products_path)
            for _, r in df_p.iterrows():
                pname = str(r.get("content.productName", "")).strip()
                sname = str(r.get("content.startupName", "")).strip()
                url = str(r.get("source.url", "")).strip()
                if not pname:
                    continue
                fp = compute_content_fingerprint(sname, pname, normalize_url(url))
                
                if session.query(ProductRecord).filter_by(fingerprint=fp).first():
                    continue

                rec = ProductRecord(
                    schema_version=str(r.get("schemaVersion", "1.0")),
                    record_type="PRODUCT",
                    source_name=str(r.get("source.name", "FrontierAtlas")),
                    source_url=url,
                    startup_name=sname,
                    product_name=pname,
                    pricing_model=str(r.get("content.pricingModel", "")) if pd.notna(r.get("content.pricingModel")) else None,
                    description=str(r.get("description", "")) if pd.notna(r.get("description")) else None,
                    fingerprint=fp,
                    collected_at=str(r.get("collectedAt", ""))
                )
                session.add(rec)
                counts["products"] += 1
            session.commit()
            logger.info(f"Restored {counts['products']} products.")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to seed products: {e}")

    # 3. Research Papers (1,000 with GitHub links & stars)
    papers_path = exports_dir / "research_papers.csv"
    if papers_path.exists():
        try:
            df_r = pd.read_csv(papers_path)
            for _, r in df_r.iterrows():
                title = str(r.get("content.title", "")).strip()
                paper_url = str(r.get("content.paper_url", "")).strip()
                if not title:
                    continue
                fp = compute_content_fingerprint(title, normalize_url(paper_url))
                
                if session.query(ResearchPaperRecord).filter_by(fingerprint=fp).first():
                    continue

                authors_raw = str(r.get("content.authors", "[]"))
                if authors_raw.startswith("["):
                    authors_json = authors_raw
                else:
                    authors_json = json.dumps([a.strip() for a in authors_raw.split(";") if a.strip()])

                stars_val = r.get("content.github_stars")
                stars = int(stars_val) if pd.notna(stars_val) else None

                rec = ResearchPaperRecord(
                    schema_version=str(r.get("schemaVersion", "1.0")),
                    record_type="RESEARCH_PAPER",
                    title=title,
                    authors_json=authors_json,
                    paper_url=paper_url,
                    github_url=str(r["content.github_url"]) if pd.notna(r.get("content.github_url")) else None,
                    github_stars=stars,
                    github_stars_retrieved_at=str(r.get("github_stars_retrieved_at", "")) if pd.notna(r.get("github_stars_retrieved_at")) else None,
                    published_date=str(r.get("content.published_date", "")),
                    fingerprint=fp
                )
                session.add(rec)
                counts["research_papers"] += 1
            session.commit()
            logger.info(f"Restored {counts['research_papers']} research papers.")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to seed research papers: {e}")

    # 4. Jobs (317 verified openings across 5 boards)
    jobs_path = exports_dir / "jobs.csv"
    if jobs_path.exists():
        try:
            df_j = pd.read_csv(jobs_path)
            for _, r in df_j.iterrows():
                title = str(r.get("content.title", "")).strip()
                comp = str(r.get("content.company", "")).strip()
                url = str(r.get("source.url", "")).strip()
                if not title or not comp:
                    continue
                fp = compute_content_fingerprint(comp, title, normalize_url(url))
                
                if session.query(JobRecord).filter_by(fingerprint=fp).first():
                    continue

                rec = JobRecord(
                    schema_version=str(r.get("schemaVersion", "1.0")),
                    record_type="JOB",
                    source_name=str(r.get("source.name", "Board")),
                    source_url=url,
                    company=comp,
                    title=title,
                    date=str(r.get("content.date", "")),
                    is_remote=bool(r.get("content.is_remote", False)),
                    role_family=str(r.get("content.role_family", "Engineering")),
                    first_discovered_at=str(r.get("first_discovered_at", "")),
                    collected_at=str(r.get("collected_at", "")),
                    fingerprint=fp
                )
                session.add(rec)
                counts["jobs"] += 1
            session.commit()
            logger.info(f"Restored {counts['jobs']} jobs.")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to seed jobs: {e}")

    # 5. News (72 technology signals across 5 syndications)
    news_path = exports_dir / "news.csv"
    if news_path.exists():
        try:
            df_n = pd.read_csv(news_path)
            for _, r in df_n.iterrows():
                title = str(r.get("content.title", "")).strip()
                url = str(r.get("source.url", "")).strip()
                if not title:
                    continue
                fp = compute_content_fingerprint(title, normalize_url(url))
                
                if session.query(NewsRecord).filter_by(fingerprint=fp).first():
                    continue

                rec = NewsRecord(
                    schema_version=str(r.get("schemaVersion", "1.0")),
                    record_type="NEWS",
                    source_name=str(r.get("source.name", "News")),
                    source_url=url,
                    title=title,
                    published_at=str(r.get("content.published_at", "")),
                    summary=str(r.get("content.summary", "")) if pd.notna(r.get("content.summary")) else None,
                    full_text=str(r.get("content.full_text", "")) if pd.notna(r.get("content.full_text")) else None,
                    author=str(r.get("content.author", "")) if pd.notna(r.get("content.author")) else None,
                    primary_entity=str(r.get("content.primary_entity", "")) if pd.notna(r.get("content.primary_entity")) else None,
                    first_discovered_at=str(r.get("firstDiscoveredAt", "")),
                    collected_at=str(r.get("collectedAt", "")),
                    fingerprint=fp
                )
                session.add(rec)
                counts["news"] += 1
            session.commit()
            logger.info(f"Restored {counts['news']} news articles.")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to seed news: {e}")

    # 6. Entity Mapping Logs (1,000 deterministic resolutions)
    logs_path = exports_dir / "entity_mapping_log.csv"
    if logs_path.exists():
        try:
            df_m = pd.read_csv(logs_path)
            for _, r in df_m.iterrows():
                raw = str(r.get("raw_name", "")).strip()
                canonical = str(r.get("canonical_name", "")).strip()
                if not raw or not canonical:
                    continue

                rec = EntityMappingLogRecord(
                    raw_name=raw,
                    canonical_name=canonical,
                    matching_method=str(r.get("matching_method", "EXACT_CANONICAL")),
                    confidence_score=float(r.get("confidence_score", 1.0)),
                    source_url=str(r.get("source_url", "")),
                    resolution_timestamp=str(r.get("resolution_timestamp", ""))
                )
                session.add(rec)
                counts["entity_mapping_logs"] += 1
            session.commit()
            logger.info(f"Restored {counts['entity_mapping_logs']} entity mapping logs.")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to seed entity mapping logs: {e}")

    counts["status"] = "restored"
    counts["total"] = sum(v for k, v in counts.items() if isinstance(v, int))
    logger.info(f"Data recovery complete: {counts['total']} total records active.")
    return counts

if __name__ == "__main__":
    from src.storage.database import init_db, get_db_session
    init_db()
    with get_db_session() as s:
        res = seed_database_if_empty(s, force=True)
        print("Seed result:", res)
