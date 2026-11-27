from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.storage.models import (
    StartupRecord, ProductRecord, ResearchPaperRecord, JobRecord, NewsRecord, EntityMappingLogRecord
)

class GlobalSearchService:
    def __init__(self, session: Session):
        self.session = session

    def search(self, query: str, limit_per_category: int = 5) -> Dict[str, Any]:
        """Performs multi-entity search across all 6 database tables."""
        if not query or len(query.strip()) < 2:
            return {
                "query": query,
                "total_matches": 0,
                "results": {
                    "startups": [],
                    "products": [],
                    "research_papers": [],
                    "jobs": [],
                    "news": [],
                    "entities": []
                }
            }

        clean = query.strip()
        term = f"%{clean}%"

        # 1. Startups
        startups = self.session.query(StartupRecord).filter(
            or_(
                StartupRecord.canonical_name.ilike(term),
                StartupRecord.raw_name.ilike(term),
                StartupRecord.description.ilike(term)
            )
        ).limit(limit_per_category).all()

        # 2. Products
        products = self.session.query(ProductRecord).filter(
            or_(
                ProductRecord.product_name.ilike(term),
                ProductRecord.startup_name.ilike(term),
                ProductRecord.description.ilike(term)
            )
        ).limit(limit_per_category).all()

        # 3. Research Papers
        papers = self.session.query(ResearchPaperRecord).filter(
            or_(
                ResearchPaperRecord.title.ilike(term),
                ResearchPaperRecord.authors_json.ilike(term)
            )
        ).limit(limit_per_category).all()

        # 4. Jobs
        jobs = self.session.query(JobRecord).filter(
            or_(
                JobRecord.title.ilike(term),
                JobRecord.company.ilike(term)
            )
        ).limit(limit_per_category).all()

        # 5. News
        news = self.session.query(NewsRecord).filter(
            or_(
                NewsRecord.title.ilike(term),
                NewsRecord.summary.ilike(term),
                NewsRecord.primary_entity.ilike(term)
            )
        ).limit(limit_per_category).all()

        # 6. Entity Mappings
        entities = self.session.query(EntityMappingLogRecord).filter(
            or_(
                EntityMappingLogRecord.raw_name.ilike(term),
                EntityMappingLogRecord.canonical_name.ilike(term)
            )
        ).limit(limit_per_category).all()

        total = len(startups) + len(products) + len(papers) + len(jobs) + len(news) + len(entities)

        return {
            "query": clean,
            "total_matches": total,
            "results": {
                "startups": [s.to_full_dict() for s in startups],
                "products": [p.to_full_dict() for p in products],
                "research_papers": [r.to_full_dict() for r in papers],
                "jobs": [j.to_full_dict() for j in jobs],
                "news": [n.to_full_dict() for n in news],
                "entities": [e.to_full_dict() for e in entities]
            }
        }
