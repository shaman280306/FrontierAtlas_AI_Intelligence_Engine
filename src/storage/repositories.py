from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
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
            # Update fields if new data has employee count
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
