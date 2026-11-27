import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, Enum as SAEnum, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class StartupRecord(Base):
    __tablename__ = "startups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    schema_version = Column(String(16), default="1.0", nullable=False)
    record_type = Column(String(32), default="STARTUP", nullable=False)
    
    # Source provenance
    source_name = Column(String(128), nullable=False)
    source_url = Column(Text, nullable=False)
    
    # Content
    raw_name = Column(String(255), nullable=False)
    canonical_name = Column(String(255), nullable=False)
    employee_count = Column(Integer, nullable=True)  # Strictly null if unknown
    website = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    
    # Deduplication & Timestamps
    fingerprint = Column(String(64), unique=True, nullable=False, index=True)
    collected_at = Column(String(64), nullable=False)  # ISO-8601 string
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_canonical_dict(self) -> Dict[str, Any]:
        """Converts to exact specification schema."""
        return {
            "schemaVersion": self.schema_version,
            "recordType": self.record_type,
            "source": {
                "name": self.source_name,
                "url": self.source_url
            },
            "content": {
                "entityName": self.canonical_name,
                "data": {
                    "employeeCount": self.employee_count
                }
            },
            "collectedAt": self.collected_at
        }

    def to_full_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "canonical_name": self.canonical_name,
            "raw_name": self.raw_name,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "website": self.website,
            "description": self.description,
            "employee_count": self.employee_count,
            "fingerprint": self.fingerprint,
            "collected_at": self.collected_at
        }


class ProductRecord(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    schema_version = Column(String(16), default="1.0", nullable=False)
    record_type = Column(String(32), default="PRODUCT", nullable=False)
    
    # Source provenance
    source_name = Column(String(128), nullable=False)
    source_url = Column(Text, nullable=False)
    
    # Content
    startup_name = Column(String(255), nullable=False)
    product_name = Column(String(255), nullable=False)
    pricing_model = Column(String(32), nullable=True)  # FREE, FREEMIUM, PAID, ENTERPRISE or null
    description = Column(Text, nullable=True)
    
    # Deduplication & Timestamps
    fingerprint = Column(String(64), unique=True, nullable=False, index=True)
    collected_at = Column(String(64), nullable=False)  # ISO-8601 string
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_canonical_dict(self) -> Dict[str, Any]:
        """Converts to exact specification schema."""
        return {
            "schemaVersion": self.schema_version,
            "recordType": self.record_type,
            "source": {
                "name": self.source_name,
                "url": self.source_url
            },
            "content": {
                "startupName": self.startup_name,
                "pricingModel": self.pricing_model
            },
            "collectedAt": self.collected_at
        }

    def to_full_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_name": self.product_name,
            "startup_name": self.startup_name,
            "pricing_model": self.pricing_model,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "description": self.description,
            "fingerprint": self.fingerprint,
            "collected_at": self.collected_at
        }


class ResearchPaperRecord(Base):
    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    schema_version = Column(String(16), default="1.0", nullable=False)
    record_type = Column(String(32), default="RESEARCH_PAPER", nullable=False)
    
    # Content
    title = Column(Text, nullable=False)
    authors_json = Column(Text, nullable=False)  # JSON-encoded array of author strings
    paper_url = Column(Text, nullable=False)
    github_url = Column(Text, nullable=True)
    github_stars = Column(Integer, nullable=True)
    github_stars_retrieved_at = Column(String(64), nullable=True)  # Exact traceable observation timestamp
    published_date = Column(String(64), nullable=False)  # ISO-8601 format
    
    # Deduplication & Timestamps
    fingerprint = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @property
    def authors(self) -> List[str]:
        try:
            return json.loads(self.authors_json)
        except Exception:
            return []

    def to_canonical_dict(self) -> Dict[str, Any]:
        """Converts to exact specification schema."""
        return {
            "schemaVersion": self.schema_version,
            "recordType": self.record_type,
            "content": {
                "title": self.title,
                "authors": self.authors,
                "paper_url": self.paper_url,
                "github_url": self.github_url,
                "github_stars": self.github_stars,
                "published_date": self.published_date
            }
        }

    def to_full_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "paper_url": self.paper_url,
            "github_url": self.github_url,
            "github_stars": self.github_stars,
            "github_stars_retrieved_at": self.github_stars_retrieved_at,
            "published_date": self.published_date,
            "fingerprint": self.fingerprint
        }


class JobRecord(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    schema_version = Column(String(16), default="1.0", nullable=False)
    record_type = Column(String(32), default="JOB", nullable=False)
    
    # Provenance
    source_name = Column(String(128), nullable=False)
    source_url = Column(Text, nullable=False)
    
    # Content
    company = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    date = Column(String(64), nullable=False)  # ISO-8601 publication date
    is_remote = Column(Boolean, default=False, nullable=False)
    role_family = Column(String(64), default="Engineering", nullable=False)
    
    # Freshness audit timestamps
    first_discovered_at = Column(String(64), nullable=False)
    collected_at = Column(String(64), nullable=False)
    date_confidence = Column(Float, default=1.0)
    
    fingerprint = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_canonical_dict(self) -> Dict[str, Any]:
        """Converts to exact specification schema."""
        return {
            "schemaVersion": self.schema_version,
            "recordType": self.record_type,
            "content": {
                "company": self.company,
                "date": self.date,
                "is_remote": self.is_remote,
                "role_family": self.role_family
            }
        }

    def to_full_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "date": self.date,
            "is_remote": self.is_remote,
            "role_family": self.role_family,
            "first_discovered_at": self.first_discovered_at,
            "collected_at": self.collected_at,
            "fingerprint": self.fingerprint
        }


class NewsRecord(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    schema_version = Column(String(16), default="1.0", nullable=False)
    record_type = Column(String(32), default="NEWS", nullable=False)
    
    # Provenance
    source_name = Column(String(128), nullable=False)
    source_url = Column(Text, nullable=False)
    
    # Content (Documented Schema Extension)
    title = Column(Text, nullable=False)
    published_at = Column(String(64), nullable=False)  # ISO-8601
    summary = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)
    primary_entity = Column(String(255), nullable=True)
    
    # Freshness audit
    first_discovered_at = Column(String(64), nullable=False)
    collected_at = Column(String(64), nullable=False)
    date_confidence = Column(Float, default=1.0)
    
    fingerprint = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_canonical_dict(self) -> Dict[str, Any]:
        """Converts to documented news extension schema."""
        return {
            "schemaVersion": self.schema_version,
            "recordType": self.record_type,
            "source": {
                "name": self.source_name,
                "url": self.source_url
            },
            "content": {
                "title": self.title,
                "published_at": self.published_at,
                "summary": self.summary,
                "full_text": self.full_text,
                "author": self.author,
                "primary_entity": self.primary_entity
            },
            "collectedAt": self.collected_at,
            "firstDiscoveredAt": self.first_discovered_at
        }

    def to_full_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "published_at": self.published_at,
            "summary": self.summary,
            "full_text": self.full_text,
            "author": self.author,
            "primary_entity": self.primary_entity,
            "first_discovered_at": self.first_discovered_at,
            "collected_at": self.collected_at,
            "fingerprint": self.fingerprint
        }


class EntityMappingLogRecord(Base):
    __tablename__ = "entity_mapping_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_name = Column(String(255), nullable=False, index=True)
    canonical_name = Column(String(255), nullable=False, index=True)
    matching_method = Column(String(64), nullable=False)  # EXACT_CANONICAL, SEED_ALIAS, NORMALIZED_MATCH, FUZZY_TOKEN_SORT, MANUAL_REVIEW_FLAGGED
    confidence_score = Column(Float, nullable=False)
    source_url = Column(Text, nullable=False)
    resolution_timestamp = Column(String(64), nullable=False)  # ISO-8601
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_canonical_dict(self) -> Dict[str, Any]:
        return {
            "rawName": self.raw_name,
            "canonicalName": self.canonical_name,
            "matchingMethod": self.matching_method,
            "confidenceScore": self.confidence_score,
            "sourceUrl": self.source_url,
            "resolutionTimestamp": self.resolution_timestamp
        }

    def to_full_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "raw_name": self.raw_name,
            "canonical_name": self.canonical_name,
            "matching_method": self.matching_method,
            "confidence_score": self.confidence_score,
            "source_url": self.source_url,
            "resolution_timestamp": self.resolution_timestamp
        }
