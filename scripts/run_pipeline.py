import argparse
import asyncio
import sys
from pathlib import Path

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.storage.database import init_db
from src.pipelines.ingestion import IngestionPipeline
from src.pipelines.orchestration import PipelineOrchestrator
from src.exports.sheets_export import GoogleSheetsExporter
from src.utils.logging import app_logger

async def main():
    parser = argparse.ArgumentParser(description="FrontierAtlas AI Intelligence Ingestion Engine CLI")
    parser.add_argument("--all", action="store_true", help="Run complete end-to-end ingestion pipeline")
    parser.add_argument("--startups", action="store_true", help="Run Startups ingestion")
    parser.add_argument("--products", action="store_true", help="Run Products ingestion")
    parser.add_argument("--papers", action="store_true", help="Run Research Papers ingestion")
    parser.add_argument("--news", action="store_true", help="Run 24-hr News ingestion")
    parser.add_argument("--jobs", action="store_true", help="Run 24-hr Jobs ingestion")
    parser.add_argument("--export", action="store_true", help="Run CSV and Excel / Sheets export")
    parser.add_argument("--target", type=int, default=1000, help="Target count for bulk verticals (default: 1000)")

    args = parser.parse_args()

    # If no flags passed, default to --all
    if not (args.all or args.startups or args.products or args.papers or args.news or args.jobs or args.export):
        args.all = True

    init_db()
    pipeline = IngestionPipeline()

    if args.all:
        app_logger.info("Starting Full End-to-End Pipeline Execution...")
        orchestrator = PipelineOrchestrator()
        results = await orchestrator.run_full_pipeline(
            startup_target=args.target,
            product_target=args.target,
            paper_target=args.target
        )
        app_logger.info(f"Pipeline Execution Summary: {results}")
        
        # Automatically run export after full pipeline
        app_logger.info("Executing automatic export...")
        exporter = GoogleSheetsExporter()
        export_res = exporter.publish_or_export()
        app_logger.info(f"Export Summary: {export_res}")
        return

    if args.startups:
        await pipeline.ingest_startups(target_count=args.target)
    if args.products:
        await pipeline.ingest_products(target_count=args.target)
    if args.papers:
        await pipeline.ingest_research_papers(target_count=args.target)
    if args.news:
        await pipeline.ingest_news(limit=500)
    if args.jobs:
        await pipeline.ingest_jobs(limit=500)
    if args.export:
        exporter = GoogleSheetsExporter()
        res = exporter.publish_or_export()
        app_logger.info(f"Export Results: {res}")

if __name__ == "__main__":
    asyncio.run(main())
