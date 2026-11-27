import math
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc, asc
from src.storage.models import (
    StartupRecord, ProductRecord, ResearchPaperRecord, JobRecord, NewsRecord, EntityMappingLogRecord
)
from src.utils.logging import app_logger

class StartupRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, record_data: Dict[str, Any]) -> Tuple[StartupRecord, bool]:
        """Upsert a startup record based on fingerprint."""
        existing = self.session.query(StartupRecord).filter_by(fingerprint=record_data["fingerprint"]).first()
        if existing:
            if record_data.get("employee_count") is not None:
                existing.employee_count = record_data["employee_count"]
            return existing, False
        
        record = StartupRecord(**record_data)
        self.session.add(record)
        return record, True

    def count(self) -> int:
        return self.session.query(func.count(StartupRecord.id)).scalar() or 0

    def get_all(self, limit: Optional[int] = None) -> List[StartupRecord]:
        query = self.session.query(StartupRecord).order_by(StartupRecord.id.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_id(self, item_id: int) -> Optional[StartupRecord]:
        return self.session.query(StartupRecord).filter_by(id=item_id).first()

    def get_by_name(self, name: str) -> Optional[StartupRecord]:
        return self.session.query(StartupRecord).filter(
            or_(
                StartupRecord.canonical_name.ilike(name.strip()),
                StartupRecord.raw_name.ilike(name.strip())
            )
        ).first()

    def get_sources(self) -> List[str]:
        rows = self.session.query(StartupRecord.source_name).distinct().all()
        return sorted([r[0] for r in rows if r[0]])

    def paginate(
        self,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        source: Optional[str] = None,
        has_employees: Optional[bool] = None,
        sort_by: str = "id",
        order: str = "asc"
    ) -> Dict[str, Any]:
        query = self.session.query(StartupRecord)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    StartupRecord.canonical_name.ilike(term),
                    StartupRecord.raw_name.ilike(term),
                    StartupRecord.description.ilike(term)
                )
            )

        if source and source.strip():
            query = query.filter(StartupRecord.source_name == source.strip())

        if has_employees is True:
            query = query.filter(StartupRecord.employee_count.isnot(None))
        elif has_employees is False:
            query = query.filter(StartupRecord.employee_count.is_(None))

        total = query.count()
        total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

        sort_col = getattr(StartupRecord, sort_by, StartupRecord.id)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_col))
        else:
            query = query.order_by(asc(sort_col))

        offset = (max(1, page) - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "items": [item.to_full_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, record_data: Dict[str, Any]) -> Tuple[ProductRecord, bool]:
        existing = self.session.query(ProductRecord).filter_by(fingerprint=record_data["fingerprint"]).first()
        if existing:
            return existing, False
        
        record = ProductRecord(**record_data)
        self.session.add(record)
        return record, True

    def count(self) -> int:
        return self.session.query(func.count(ProductRecord.id)).scalar() or 0

    def get_all(self, limit: Optional[int] = None) -> List[ProductRecord]:
        query = self.session.query(ProductRecord).order_by(ProductRecord.id.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_id(self, item_id: int) -> Optional[ProductRecord]:
        return self.session.query(ProductRecord).filter_by(id=item_id).first()

    def get_pricing_distribution(self) -> Dict[str, int]:
        rows = self.session.query(ProductRecord.pricing_model, func.count(ProductRecord.id)).group_by(ProductRecord.pricing_model).all()
        return {r[0] or "UNKNOWN": r[1] for r in rows}

    def get_for_comparison(self, ids: List[int]) -> List[ProductRecord]:
        return self.session.query(ProductRecord).filter(ProductRecord.id.in_(ids)).all()

    def paginate(
        self,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        pricing_model: Optional[str] = None,
        startup_name: Optional[str] = None,
        sort_by: str = "id",
        order: str = "asc"
    ) -> Dict[str, Any]:
        query = self.session.query(ProductRecord)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    ProductRecord.product_name.ilike(term),
                    ProductRecord.startup_name.ilike(term),
                    ProductRecord.description.ilike(term)
                )
            )

        if pricing_model and pricing_model.strip():
            query = query.filter(ProductRecord.pricing_model == pricing_model.strip().upper())

        if startup_name and startup_name.strip():
            query = query.filter(ProductRecord.startup_name.ilike(f"%{startup_name.strip()}%"))

        total = query.count()
        total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

        sort_col = getattr(ProductRecord, sort_by, ProductRecord.id)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_col))
        else:
            query = query.order_by(asc(sort_col))

        offset = (max(1, page) - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "items": [item.to_full_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }


class PaperRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, record_data: Dict[str, Any]) -> Tuple[ResearchPaperRecord, bool]:
        existing = self.session.query(ResearchPaperRecord).filter_by(fingerprint=record_data["fingerprint"]).first()
        if existing:
            if record_data.get("github_stars") is not None:
                existing.github_stars = record_data["github_stars"]
                existing.github_stars_retrieved_at = record_data.get("github_stars_retrieved_at")
            return existing, False
        
        record = ResearchPaperRecord(**record_data)
        self.session.add(record)
        return record, True

    def count(self) -> int:
        return self.session.query(func.count(ResearchPaperRecord.id)).scalar() or 0

    def get_all(self, limit: Optional[int] = None) -> List[ResearchPaperRecord]:
        query = self.session.query(ResearchPaperRecord).order_by(ResearchPaperRecord.id.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_id(self, item_id: int) -> Optional[ResearchPaperRecord]:
        return self.session.query(ResearchPaperRecord).filter_by(id=item_id).first()

    def get_top_starred(self, limit: int = 10) -> List[ResearchPaperRecord]:
        return self.session.query(ResearchPaperRecord).filter(
            ResearchPaperRecord.github_stars.isnot(None)
        ).order_by(desc(ResearchPaperRecord.github_stars)).limit(limit).all()

    def paginate(
        self,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        has_github: Optional[bool] = None,
        min_stars: Optional[int] = None,
        sort_by: str = "id",
        order: str = "asc"
    ) -> Dict[str, Any]:
        query = self.session.query(ResearchPaperRecord)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    ResearchPaperRecord.title.ilike(term),
                    ResearchPaperRecord.authors_json.ilike(term)
                )
            )

        if has_github is True:
            query = query.filter(ResearchPaperRecord.github_url.isnot(None))
        elif has_github is False:
            query = query.filter(ResearchPaperRecord.github_url.is_(None))

        if min_stars is not None:
            query = query.filter(ResearchPaperRecord.github_stars >= min_stars)

        total = query.count()
        total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

        sort_col = getattr(ResearchPaperRecord, sort_by, ResearchPaperRecord.id)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_col))
        else:
            query = query.order_by(asc(sort_col))

        offset = (max(1, page) - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "items": [item.to_full_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }


class JobRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, record_data: Dict[str, Any]) -> Tuple[JobRecord, bool]:
        existing = self.session.query(JobRecord).filter_by(fingerprint=record_data["fingerprint"]).first()
        if existing:
            return existing, False
        
        record = JobRecord(**record_data)
        self.session.add(record)
        return record, True

    def count(self) -> int:
        return self.session.query(func.count(JobRecord.id)).scalar() or 0

    def get_all(self, limit: Optional[int] = None) -> List[JobRecord]:
        query = self.session.query(JobRecord).order_by(JobRecord.id.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_id(self, item_id: int) -> Optional[JobRecord]:
        return self.session.query(JobRecord).filter_by(id=item_id).first()

    def get_role_distribution(self) -> Dict[str, int]:
        rows = self.session.query(JobRecord.role_family, func.count(JobRecord.id)).group_by(JobRecord.role_family).all()
        return {r[0] or "Other": r[1] for r in rows}

    def get_sources(self) -> List[str]:
        rows = self.session.query(JobRecord.source_name).distinct().all()
        return sorted([r[0] for r in rows if r[0]])

    def paginate(
        self,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        is_remote: Optional[bool] = None,
        role_family: Optional[str] = None,
        source: Optional[str] = None,
        sort_by: str = "id",
        order: str = "desc"
    ) -> Dict[str, Any]:
        query = self.session.query(JobRecord)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    JobRecord.title.ilike(term),
                    JobRecord.company.ilike(term)
                )
            )

        if is_remote is not None:
            query = query.filter(JobRecord.is_remote == is_remote)

        if role_family and role_family.strip():
            query = query.filter(JobRecord.role_family == role_family.strip())

        if source and source.strip():
            query = query.filter(JobRecord.source_name == source.strip())

        total = query.count()
        total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

        sort_col = getattr(JobRecord, sort_by, JobRecord.id)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_col))
        else:
            query = query.order_by(asc(sort_col))

        offset = (max(1, page) - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "items": [item.to_full_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }


class NewsRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, record_data: Dict[str, Any]) -> Tuple[NewsRecord, bool]:
        existing = self.session.query(NewsRecord).filter_by(fingerprint=record_data["fingerprint"]).first()
        if existing:
            return existing, False
        
        record = NewsRecord(**record_data)
        self.session.add(record)
        return record, True

    def count(self) -> int:
        return self.session.query(func.count(NewsRecord.id)).scalar() or 0

    def get_all(self, limit: Optional[int] = None) -> List[NewsRecord]:
        query = self.session.query(NewsRecord).order_by(NewsRecord.id.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_id(self, item_id: int) -> Optional[NewsRecord]:
        return self.session.query(NewsRecord).filter_by(id=item_id).first()

    def get_source_distribution(self) -> Dict[str, int]:
        rows = self.session.query(NewsRecord.source_name, func.count(NewsRecord.id)).group_by(NewsRecord.source_name).all()
        return {r[0] or "Unknown": r[1] for r in rows}

    def paginate(
        self,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        source: Optional[str] = None,
        sort_by: str = "id",
        order: str = "desc"
    ) -> Dict[str, Any]:
        query = self.session.query(NewsRecord)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    NewsRecord.title.ilike(term),
                    NewsRecord.summary.ilike(term),
                    NewsRecord.primary_entity.ilike(term)
                )
            )

        if source and source.strip():
            query = query.filter(NewsRecord.source_name == source.strip())

        total = query.count()
        total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

        sort_col = getattr(NewsRecord, sort_by, NewsRecord.id)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_col))
        else:
            query = query.order_by(asc(sort_col))

        offset = (max(1, page) - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "items": [item.to_full_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }


class EntityMappingRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_log(self, log_data: Dict[str, Any]) -> EntityMappingLogRecord:
        record = EntityMappingLogRecord(**log_data)
        self.session.add(record)
        return record

    def count(self) -> int:
        return self.session.query(func.count(EntityMappingLogRecord.id)).scalar() or 0

    def get_all(self, limit: Optional[int] = None) -> List[EntityMappingLogRecord]:
        query = self.session.query(EntityMappingLogRecord).order_by(EntityMappingLogRecord.id.asc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_id(self, item_id: int) -> Optional[EntityMappingLogRecord]:
        return self.session.query(EntityMappingLogRecord).filter_by(id=item_id).first()

    def get_method_distribution(self) -> Dict[str, int]:
        rows = self.session.query(EntityMappingLogRecord.matching_method, func.count(EntityMappingLogRecord.id)).group_by(EntityMappingLogRecord.matching_method).all()
        return {r[0] or "Unknown": r[1] for r in rows}

    def paginate(
        self,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        method: Optional[str] = None,
        min_confidence: Optional[float] = None,
        sort_by: str = "id",
        order: str = "asc"
    ) -> Dict[str, Any]:
        query = self.session.query(EntityMappingLogRecord)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    EntityMappingLogRecord.raw_name.ilike(term),
                    EntityMappingLogRecord.canonical_name.ilike(term)
                )
            )

        if method and method.strip():
            query = query.filter(EntityMappingLogRecord.matching_method == method.strip())

        if min_confidence is not None:
            query = query.filter(EntityMappingLogRecord.confidence_score >= min_confidence)

        total = query.count()
        total_pages = max(1, math.ceil(total / page_size)) if total > 0 else 1

        sort_col = getattr(EntityMappingLogRecord, sort_by, EntityMappingLogRecord.id)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_col))
        else:
            query = query.order_by(asc(sort_col))

        offset = (max(1, page) - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "items": [item.to_full_dict() for item in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
