import asyncio
import time
from typing import Dict, Any, Optional
from src.storage.database import init_db
from src.pipelines.ingestion import IngestionPipeline
from src.utils.logging import app_logger

class PipelineOrchestrator:
    """
    Coordinates asynchronous execution of all ingestion pipelines.
    Supports concurrent bulk acquisition and isolated single-vertical runs.
    """
    def __init__(self):
        self.pipeline = IngestionPipeline()

    async def run_full_pipeline(
        self,
        startup_target: int = 1000,
        product_target: int = 1000,
        paper_target: int = 1000
    ) -> Dict[str, Any]:
        app_logger.info("Initializing database schema...")
        init_db()

        start_time = time.time()
        app_logger.info("Starting Full End-to-End FrontierAtlas Ingestion Pipeline...")

        # Run pipelines concurrently where appropriate, respecting rate boundaries
        # Research papers and Hugging Face / GitHub have distinct rate envelopes
        results = {}

        app_logger.info("--- Stage 1: Massive Bulk Acquisition (Startups & Products) ---")
        startup_res, product_res = await asyncio.gather(
            self.pipeline.ingest_startups(target_count=startup_target),
            self.pipeline.ingest_products(target_count=product_target),
            return_exceptions=True
        )
        results["startups"] = startup_res if not isinstance(startup_res, Exception) else {"error": str(startup_res)}
        results["products"] = product_res if not isinstance(product_res, Exception) else {"error": str(product_res)}

        app_logger.info("--- Stage 2: Research Papers & GitHub Metrics Correlation ---")
        paper_res = await self.pipeline.ingest_research_papers(target_count=paper_target)
        results["research_papers"] = paper_res

        app_logger.info("--- Stage 3: High-Fidelity Signal Ingestion (News & Jobs with 24-hr Freshness) ---")
        news_res, job_res = await asyncio.gather(
            self.pipeline.ingest_news(limit=500),
            self.pipeline.ingest_jobs(limit=500),
            return_exceptions=True
        )
        results["news"] = news_res if not isinstance(news_res, Exception) else {"error": str(news_res)}
        results["jobs"] = job_res if not isinstance(job_res, Exception) else {"error": str(job_res)}

        total_duration = round(time.time() - start_time, 2)
        results["total_pipeline_duration_seconds"] = total_duration

        app_logger.info(f"Full Ingestion Pipeline completed successfully in {total_duration}s.")
        return results
