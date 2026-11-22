import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.storage.database import get_db_session
from src.storage.repositories import (
    StartupRepository, ProductRepository, PaperRepository, JobRepository, NewsRepository, EntityMappingRepository
)
from src.utils.dates import parse_iso_or_relative_date, is_within_hours, get_utc_now
from src.utils.logging import app_logger

def validate_data() -> bool:
    app_logger.info("--- STARTING RIGOROUS DATA VALIDATION GATE ---")
    now = get_utc_now()
    all_passed = True

    with get_db_session() as session:
        startup_repo = StartupRepository(session)
        product_repo = ProductRepository(session)
        paper_repo = PaperRepository(session)
        job_repo = JobRepository(session)
        news_repo = NewsRepository(session)
        entity_repo = EntityMappingRepository(session)

        startups = startup_repo.get_all()
        products = product_repo.get_all()
        papers = paper_repo.get_all()
        jobs = job_repo.get_all()
        news = news_repo.get_all()
        entity_logs = entity_repo.get_all()

        # 1. Startups Validation
        app_logger.info(f"[1/6] Validating Startups: Count = {len(startups)}...")
        if len(startups) < 1000:
            app_logger.error(f"FAILURE: Startups count ({len(startups)}) is below the required 1,000 threshold!")
            all_passed = False
        else:
            app_logger.info(f"PASS: Minimum 1,000 startup target satisfied ({len(startups)} records).")

        startup_fps = set()
        for s in startups:
            if not s.canonical_name or not s.source_url:
                app_logger.error(f"FAILURE: Startup record #{s.id} missing name or source URL!")
                all_passed = False
            if s.fingerprint in startup_fps:
                app_logger.error(f"FAILURE: Duplicate startup fingerprint detected: {s.fingerprint}")
                all_passed = False
            startup_fps.add(s.fingerprint)

        # 2. Products Validation
        app_logger.info(f"[2/6] Validating Products: Count = {len(products)}...")
        if len(products) < 1000:
            app_logger.error(f"FAILURE: Products count ({len(products)}) is below the required 1,000 threshold!")
            all_passed = False
        else:
            app_logger.info(f"PASS: Minimum 1,000 product target satisfied ({len(products)} records).")

        allowed_pricing = {"FREE", "FREEMIUM", "PAID", "ENTERPRISE", None}
        product_fps = set()
        for p in products:
            if p.pricing_model not in allowed_pricing:
                app_logger.error(f"FAILURE: Invalid pricing model '{p.pricing_model}' on product #{p.id}")
                all_passed = False
            if p.fingerprint in product_fps:
                app_logger.error(f"FAILURE: Duplicate product fingerprint detected: {p.fingerprint}")
                all_passed = False
            product_fps.add(p.fingerprint)

        # 3. Research Papers Validation
        app_logger.info(f"[3/6] Validating Research Papers: Count = {len(papers)}...")
        if len(papers) < 1000:
            app_logger.error(f"FAILURE: Research papers count ({len(papers)}) is below the required 1,000 threshold!")
            all_passed = False
        else:
            app_logger.info(f"PASS: Minimum 1,000 research papers target satisfied ({len(papers)} records).")

        papers_with_github = sum(1 for p in papers if p.github_url)
        papers_with_stars = sum(1 for p in papers if p.github_stars is not None)
        app_logger.info(f"Research Papers Metrics: {papers_with_github} with GitHub repos, {papers_with_stars} with live stars.")

        paper_fps = set()
        for p in papers:
            if not p.title or not p.paper_url:
                app_logger.error(f"FAILURE: Paper record #{p.id} missing title or URL!")
                all_passed = False
            if p.fingerprint in paper_fps:
                app_logger.error(f"FAILURE: Duplicate paper fingerprint detected: {p.fingerprint}")
                all_passed = False
            paper_fps.add(p.fingerprint)

        # 4. Jobs Validation (Strict 24-hr freshness)
        app_logger.info(f"[4/6] Validating Jobs: Count = {len(jobs)}...")
        for j in jobs:
            dt, _ = parse_iso_or_relative_date(j.date, ref_time=now)
            if not is_within_hours(dt, hours=24, ref_time=now):
                app_logger.error(f"FAILURE: Job #{j.id} ('{j.title}' at '{j.company}') violated 24-hr freshness policy: {j.date}")
                all_passed = False

        # 5. News Validation (Strict 24-hr freshness)
        app_logger.info(f"[5/6] Validating News: Count = {len(news)}...")
        for n in news:
            dt, _ = parse_iso_or_relative_date(n.published_at, ref_time=now)
            if not is_within_hours(dt, hours=24, ref_time=now):
                app_logger.error(f"FAILURE: News #{n.id} ('{n.title}') violated 24-hr freshness policy: {n.published_at}")
                all_passed = False

        # 6. Entity Mapping Log Validation
        app_logger.info(f"[6/6] Validating Entity Mapping Logs: Count = {len(entity_logs)}...")
        if len(entity_logs) == 0:
            app_logger.warning("WARNING: No entity mapping logs recorded!")
        for e in entity_logs:
            if not (0.0 <= e.confidence_score <= 1.0):
                app_logger.error(f"FAILURE: Invalid confidence score {e.confidence_score} in mapping log #{e.id}")
                all_passed = False

    if all_passed:
        app_logger.info("SUCCESS: ALL DATA QUALITY GATES AND SCHEMAS FULLY PASSED AND VERIFIED!")
    else:
        app_logger.error("DATA VALIDATION FAILED: Review the errors above.")

    return all_passed

if __name__ == "__main__":
    success = validate_data()
    sys.exit(0 if success else 1)
