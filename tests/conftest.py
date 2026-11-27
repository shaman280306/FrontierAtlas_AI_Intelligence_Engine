import os
import sys
import json
from pathlib import Path
from typing import Generator
import pytest
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.storage.models import (
    Base, StartupRecord, ProductRecord, ResearchPaperRecord, JobRecord, NewsRecord, EntityMappingLogRecord
)
from src.storage.database import get_db
import src.storage.database as db_module
from src.main import app
from src.utils.deduplication import compute_content_fingerprint, normalize_url

# Isolated in-memory SQLite database with StaticPool to share connection across sessions/threads
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def seed_test_database(session: Session) -> None:
    """Populates the isolated test database with canonical baseline records from data/exports/."""
    exports_dir = ROOT_DIR / "data" / "exports"

    # 1. Startups
    startups_path = exports_dir / "startups.csv"
    if startups_path.exists():
        df_s = pd.read_csv(startups_path)
        for _, r in df_s.iterrows():
            name = str(r["content.entityName"])
            url = str(r.get("source.url", ""))
            fp = compute_content_fingerprint(name, normalize_url(url))
            rec = StartupRecord(
                schema_version=str(r.get("schemaVersion", "1.0")),
                record_type="STARTUP",
                source_name=str(r.get("source.name", "FrontierAtlas")),
                source_url=url,
                raw_name=name,
                canonical_name=name,
                employee_count=int(r["content.data.employeeCount"]) if pd.notna(r.get("content.data.employeeCount")) else None,
                fingerprint=fp,
                collected_at=str(r.get("collectedAt", ""))
            )
            session.add(rec)
        session.commit()

    # 2. Products
    products_path = exports_dir / "products.csv"
    if products_path.exists():
        df_p = pd.read_csv(products_path)
        for _, r in df_p.iterrows():
            pname = str(r["content.productName"])
            sname = str(r["content.startupName"])
            url = str(r.get("source.url", ""))
            fp = compute_content_fingerprint(sname, pname, normalize_url(url))
            rec = ProductRecord(
                schema_version=str(r.get("schemaVersion", "1.0")),
                record_type="PRODUCT",
                source_name=str(r.get("source.name", "FrontierAtlas")),
                source_url=url,
                startup_name=sname,
                product_name=pname,
                pricing_model=str(r.get("content.pricingModel", "")) if pd.notna(r.get("content.pricingModel")) else None,
                fingerprint=fp,
                collected_at=str(r.get("collectedAt", ""))
            )
            session.add(rec)
        session.commit()

    # 3. Research Papers
    papers_path = exports_dir / "research_papers.csv"
    if papers_path.exists():
        df_r = pd.read_csv(papers_path)
        for _, r in df_r.iterrows():
            title = str(r["content.title"])
            paper_url = str(r.get("content.paper_url", ""))
            authors_raw = str(r.get("content.authors", "[]"))
            if authors_raw.startswith("["):
                authors_json = authors_raw
            else:
                authors_json = json.dumps([a.strip() for a in authors_raw.split(";") if a.strip()])
            fp = compute_content_fingerprint(title, normalize_url(paper_url))
            rec = ResearchPaperRecord(
                schema_version=str(r.get("schemaVersion", "1.0")),
                record_type="RESEARCH_PAPER",
                title=title,
                authors_json=authors_json,
                paper_url=paper_url,
                github_url=str(r["content.github_url"]) if pd.notna(r.get("content.github_url")) else None,
                github_stars=int(r["content.github_stars"]) if pd.notna(r.get("content.github_stars")) else None,
                github_stars_retrieved_at=str(r.get("github_stars_retrieved_at", "")) if pd.notna(r.get("github_stars_retrieved_at")) else None,
                published_date=str(r.get("content.published_date", "")),
                fingerprint=fp
            )
            session.add(rec)
        session.commit()

    # 4. Jobs
    jobs_path = exports_dir / "jobs.csv"
    if jobs_path.exists():
        df_j = pd.read_csv(jobs_path)
        for _, r in df_j.iterrows():
            title = str(r.get("content.title", ""))
            comp = str(r.get("content.company", ""))
            url = str(r.get("source.url", ""))
            fp = compute_content_fingerprint(comp, title, normalize_url(url))
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
        session.commit()

    # 5. News
    news_path = exports_dir / "news.csv"
    if news_path.exists():
        df_n = pd.read_csv(news_path)
        for _, r in df_n.iterrows():
            title = str(r.get("content.title", ""))
            url = str(r.get("source.url", ""))
            fp = compute_content_fingerprint(title, normalize_url(url))
            rec = NewsRecord(
                schema_version=str(r.get("schemaVersion", "1.0")),
                record_type="NEWS",
                source_name=str(r.get("source.name", "News")),
                source_url=url,
                title=title,
                published_at=str(r.get("content.published_at", "")),
                summary=str(r.get("content.summary", "")),
                author=str(r.get("content.author", "")) if pd.notna(r.get("content.author")) else None,
                first_discovered_at=str(r.get("firstDiscoveredAt", "")),
                collected_at=str(r.get("collectedAt", "")),
                fingerprint=fp
            )
            session.add(rec)
        session.commit()

    # 6. Entity Mapping Logs
    logs_path = exports_dir / "entity_mapping_log.csv"
    if logs_path.exists():
        df_m = pd.read_csv(logs_path)
        for _, r in df_m.iterrows():
            rec = EntityMappingLogRecord(
                raw_name=str(r.get("raw_name", "")),
                canonical_name=str(r.get("canonical_name", "")),
                matching_method=str(r.get("matching_method", "EXACT")),
                confidence_score=float(r.get("confidence_score", 1.0)),
                source_url=str(r.get("source_url", "")),
                resolution_timestamp=str(r.get("resolution_timestamp", ""))
            )
            session.add(rec)
        session.commit()

# Ensure schema is created and seeded immediately upon import
Base.metadata.create_all(bind=test_engine)
with TestingSessionLocal() as _init_session:
    seed_test_database(_init_session)

# Patch storage database module engine and SessionLocal
db_module.engine = test_engine
db_module.SessionLocal = TestingSessionLocal

def _override_get_db() -> Generator[Session, None, None]:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# Wire dependency override for FastAPI
app.dependency_overrides[get_db] = _override_get_db

@pytest.fixture(scope="session", autouse=True)
def test_db_session():
    """Provides session-wide isolated database guarantees for all tests."""
    yield
