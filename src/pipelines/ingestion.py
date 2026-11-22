import time
from typing import Dict, Any, List, Optional
from src.storage.database import get_db_session
from src.storage.repositories import (
    StartupRepository, ProductRepository, PaperRepository, JobRepository, NewsRepository, EntityMappingRepository
)
from src.crawlers.startup_crawler import StartupCrawler
from src.crawlers.product_crawler import ProductCrawler
from src.crawlers.research_crawler import ResearchCrawler
from src.crawlers.news_crawler import NewsCrawler
from src.crawlers.job_crawler import JobCrawler
from src.entity_resolution.resolver import EntityResolver
from src.utils.logging import app_logger

class IngestionPipeline:
    """
    Core Ingestion Pipeline.
    Coordinates crawler execution, schema transformation, deterministic entity resolution,
    atomic database upserts, and provenance logging.
    """
    def __init__(self):
        self.resolver = EntityResolver()

    async def ingest_startups(self, target_count: int = 1000) -> Dict[str, Any]:
        start_time = time.time()
        crawler = StartupCrawler(resolver=self.resolver)
        try:
            records = await crawler.crawl(limit=target_count)
            inserted, updated = 0, 0
            
            with get_db_session() as session:
                repo = StartupRepository(session)
                map_repo = EntityMappingRepository(session)
                
                for r in records:
                    res_meta = r.pop("resolution_meta", None)
                    _, is_new = repo.upsert(r)
                    if is_new:
                        inserted += 1
                    else:
                        updated += 1
                        
                    if res_meta:
                        map_repo.add_log(res_meta)
                        
            with get_db_session() as session:
                total_in_db = StartupRepository(session).count()

            duration = round(time.time() - start_time, 2)
            app_logger.info(f"Ingested {len(records)} startups ({inserted} new, {updated} updated) in {duration}s. Total in DB: {total_in_db}")
            return {
                "vertical": "STARTUPS",
                "collected": len(records),
                "inserted": inserted,
                "updated": updated,
                "total_in_db": total_in_db,
                "duration_seconds": duration
            }
        finally:
            await crawler.close()

    async def ingest_products(self, target_count: int = 1000) -> Dict[str, Any]:
        start_time = time.time()
        crawler = ProductCrawler(resolver=self.resolver)
        try:
            records = await crawler.crawl(limit=target_count)
            inserted, updated = 0, 0
            
            with get_db_session() as session:
                repo = ProductRepository(session)
                for r in records:
                    _, is_new = repo.upsert(r)
                    if is_new:
                        inserted += 1
                    else:
                        updated += 1
            with get_db_session() as session:
                total_in_db = ProductRepository(session).count()

            duration = round(time.time() - start_time, 2)
            app_logger.info(f"Ingested {len(records)} products ({inserted} new, {updated} updated) in {duration}s. Total in DB: {total_in_db}")
            return {
                "vertical": "PRODUCTS",
                "collected": len(records),
                "inserted": inserted,
                "updated": updated,
                "total_in_db": total_in_db,
                "duration_seconds": duration
            }
        finally:
            await crawler.close()

    async def ingest_research_papers(self, target_count: int = 1000) -> Dict[str, Any]:
        start_time = time.time()
        crawler = ResearchCrawler()
        try:
            records = await crawler.crawl(limit=target_count)
            inserted, updated = 0, 0
            
            with get_db_session() as session:
                repo = PaperRepository(session)
                for r in records:
                    _, is_new = repo.upsert(r)
                    if is_new:
                        inserted += 1
                    else:
                        updated += 1
            with get_db_session() as session:
                total_in_db = PaperRepository(session).count()

            duration = round(time.time() - start_time, 2)
            app_logger.info(f"Ingested {len(records)} papers ({inserted} new, {updated} updated) in {duration}s. Total in DB: {total_in_db}")
            return {
                "vertical": "RESEARCH_PAPERS",
                "collected": len(records),
                "inserted": inserted,
                "updated": updated,
                "total_in_db": total_in_db,
                "duration_seconds": duration
            }
        finally:
            await crawler.close()

    async def ingest_news(self, limit: int = 500) -> Dict[str, Any]:
        start_time = time.time()
        crawler = NewsCrawler()
        try:
            records = await crawler.crawl(limit=limit)
            inserted, updated = 0, 0
            
            with get_db_session() as session:
                repo = NewsRepository(session)
                for r in records:
                    _, is_new = repo.upsert(r)
                    if is_new:
                        inserted += 1
                    else:
                        updated += 1
            with get_db_session() as session:
                total_in_db = NewsRepository(session).count()

            duration = round(time.time() - start_time, 2)
            app_logger.info(f"Ingested {len(records)} 24-hr fresh news ({inserted} new, {updated} updated) in {duration}s. Total in DB: {total_in_db}")
            return {
                "vertical": "NEWS",
                "collected": len(records),
                "inserted": inserted,
                "updated": updated,
                "total_in_db": total_in_db,
                "duration_seconds": duration
            }
        finally:
            await crawler.close()

    async def ingest_jobs(self, limit: int = 500) -> Dict[str, Any]:
        start_time = time.time()
        crawler = JobCrawler(resolver=self.resolver)
        try:
            records = await crawler.crawl(limit=limit)
            inserted, updated = 0, 0
            
            with get_db_session() as session:
                repo = JobRepository(session)
                for r in records:
                    _, is_new = repo.upsert(r)
                    if is_new:
                        inserted += 1
                    else:
                        updated += 1
            with get_db_session() as session:
                total_in_db = JobRepository(session).count()

            duration = round(time.time() - start_time, 2)
            app_logger.info(f"Ingested {len(records)} 24-hr fresh jobs ({inserted} new, {updated} updated) in {duration}s. Total in DB: {total_in_db}")
            return {
                "vertical": "JOBS",
                "collected": len(records),
                "inserted": inserted,
                "updated": updated,
                "total_in_db": total_in_db,
                "duration_seconds": duration
            }
        finally:
            await crawler.close()
