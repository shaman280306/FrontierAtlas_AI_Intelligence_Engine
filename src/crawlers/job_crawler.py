import asyncio
from typing import List, Dict, Any, Optional, Set
import feedparser
from src.crawlers.base import BaseCrawler
from src.entity_resolution.resolver import EntityResolver
from src.utils.dates import (
    get_utc_now, to_iso8601_utc, parse_iso_or_relative_date, is_within_hours
)
from src.utils.deduplication import normalize_url, compute_content_fingerprint
from src.utils.logging import app_logger

class BaseJobAdapter:
    """Base interface for job source adapters."""
    def __init__(self, name: str, endpoint: str):
        self.name = name
        self.endpoint = endpoint

    async def fetch_jobs(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        raise NotImplementedError


class RemotiveJobAdapter(BaseJobAdapter):
    def __init__(self):
        super().__init__("Remotive", "https://remotive.com/api/remote-jobs?category=software-dev")

    async def fetch_jobs(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        res = await crawler.fetch(self.endpoint)
        if not res or res.status_code != 200:
            return []
        data = res.json()
        jobs = []
        for j in data.get("jobs", []):
            jobs.append({
                "source_name": self.name,
                "source_url": j.get("url", ""),
                "company": j.get("company_name", "Unknown"),
                "title": j.get("title", ""),
                "raw_date": j.get("publication_date"),
                "is_remote": True,
                "role_family": "Engineering"
            })
        return jobs


class ArbeitnowJobAdapter(BaseJobAdapter):
    def __init__(self):
        super().__init__("Arbeitnow", "https://www.arbeitnow.com/api/job-board-api")

    async def fetch_jobs(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        res = await crawler.fetch(self.endpoint)
        if not res or res.status_code != 200:
            return []
        data = res.json()
        jobs = []
        for j in data.get("data", []):
            # created_at is a unix timestamp integer
            jobs.append({
                "source_name": self.name,
                "source_url": j.get("url", ""),
                "company": j.get("company_name", "Unknown"),
                "title": j.get("title", ""),
                "raw_date": j.get("created_at"),
                "is_remote": bool(j.get("remote", False)),
                "role_family": "Engineering"
            })
        return jobs


class JobicyJobAdapter(BaseJobAdapter):
    def __init__(self):
        super().__init__("Jobicy", "https://jobicy.com/api/v2/remote-jobs?count=50&tag=ai")

    async def fetch_jobs(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        res = await crawler.fetch(self.endpoint)
        if not res or res.status_code != 200:
            return []
        data = res.json()
        jobs = []
        for j in data.get("jobs", []):
            jobs.append({
                "source_name": self.name,
                "source_url": j.get("url", ""),
                "company": j.get("companyName", "Unknown"),
                "title": j.get("jobTitle", ""),
                "raw_date": j.get("pubDate"),
                "is_remote": True,
                "role_family": "Engineering"
            })
        return jobs


class HimalayasJobAdapter(BaseJobAdapter):
    def __init__(self):
        super().__init__("Himalayas", "https://himalayas.app/jobs/api?limit=50")

    async def fetch_jobs(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        res = await crawler.fetch(self.endpoint)
        if not res or res.status_code != 200:
            return []
        data = res.json()
        jobs = []
        for j in data.get("jobs", []):
            jobs.append({
                "source_name": self.name,
                "source_url": f"https://himalayas.app/jobs/{j.get('slug', '')}",
                "company": j.get("companyName", "Unknown"),
                "title": j.get("title", ""),
                "raw_date": j.get("pubDate"),
                "is_remote": True,
                "role_family": "Engineering"
            })
        return jobs


class WeWorkRemotelyJobAdapter(BaseJobAdapter):
    def __init__(self):
        super().__init__("WeWorkRemotely", "https://weworkremotely.com/categories/remote-programming-jobs.rss")

    async def fetch_jobs(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        res = await crawler.fetch(self.endpoint)
        if not res or res.status_code != 200:
            return []
        feed = feedparser.parse(res.content)
        jobs = []
        for e in feed.entries:
            title_parts = getattr(e, "title", "").split(":", 1)
            company = title_parts[0].strip() if len(title_parts) > 1 else "Unknown"
            job_title = title_parts[1].strip() if len(title_parts) > 1 else getattr(e, "title", "")
            
            jobs.append({
                "source_name": self.name,
                "source_url": getattr(e, "link", ""),
                "company": company,
                "title": job_title,
                "raw_date": getattr(e, "published", None),
                "is_remote": True,
                "role_family": "Engineering"
            })
        return jobs


class JobCrawler(BaseCrawler):
    """
    High-Fidelity Signal Ingestion for AI & Engineering Jobs.
    Monitors 5 distinct job boards:
      1. Remotive API
      2. Arbeitnow API
      3. Jobicy API
      4. Himalayas API
      5. WeWorkRemotely RSS
    Enforces STRICT 24-hour freshness policy.
    Canonicalizes company names using EntityResolver.
    """
    def __init__(self, resolver: Optional[EntityResolver] = None, adapters: Optional[List[BaseJobAdapter]] = None):
        super().__init__(name="JobCrawler", base_url="https://remotive.com", rate_limit_per_second=2.0)
        self.resolver = resolver or EntityResolver()
        self.adapters = adapters or [
            RemotiveJobAdapter(),
            ArbeitnowJobAdapter(),
            JobicyJobAdapter(),
            HimalayasJobAdapter(),
            WeWorkRemotelyJobAdapter()
        ]

    async def crawl(self, limit: int = 500) -> List[Dict[str, Any]]:
        app_logger.info(f"[{self.name}] Initiating signal monitoring across {len(self.adapters)} job boards...")
        now = get_utc_now()
        now_iso = to_iso8601_utc(now)
        collected: List[Dict[str, Any]] = []
        seen_fingerprints: Set[str] = set()

        for adapter in self.adapters:
            app_logger.info(f"[{self.name}] Fetching jobs from: {adapter.name}")
            try:
                raw_jobs = await adapter.fetch_jobs(self)
                app_logger.info(f"[{self.name}] {adapter.name} returned {len(raw_jobs)} raw jobs.")

                for job in raw_jobs:
                    raw_date = job.get("raw_date")
                    pub_dt, confidence = parse_iso_or_relative_date(raw_date, ref_time=now)

                    # STRICT 24-HOUR FRESHNESS FILTER
                    if not is_within_hours(pub_dt, hours=24, ref_time=now):
                        continue

                    if confidence < 0.70:
                        continue

                    raw_company = job.get("company", "Unknown").strip()
                    res = self.resolver.resolve(raw_company, source_url=job.get("source_url", ""))
                    canonical_company = res.canonical_name

                    source_url = normalize_url(job.get("source_url", ""))
                    fp = compute_content_fingerprint(canonical_company, job.get("title", ""), source_url)

                    if fp in seen_fingerprints:
                        continue
                    seen_fingerprints.add(fp)

                    pub_iso = to_iso8601_utc(pub_dt)

                    # Classify role family
                    title_lower = job.get("title", "").lower()
                    if any(w in title_lower for w in ("research", "scientist", "phd")):
                        role_family = "Research"
                    elif any(w in title_lower for w in ("product", "pm")):
                        role_family = "Product"
                    elif any(w in title_lower for w in ("data", "analytics", "bi")):
                        role_family = "Data"
                    else:
                        role_family = "Engineering"

                    record = {
                        "schema_version": "1.0",
                        "record_type": "JOB",
                        "source_name": adapter.name,
                        "source_url": source_url,
                        "company": canonical_company,
                        "title": job.get("title", ""),
                        "date": pub_iso,
                        "is_remote": job.get("is_remote", True),
                        "role_family": role_family,
                        "first_discovered_at": now_iso,
                        "collected_at": now_iso,
                        "date_confidence": confidence,
                        "fingerprint": fp
                    }
                    collected.append(record)

            except Exception as e:
                app_logger.error(f"[{self.name}] Error crawling job board {adapter.name}: {e}")

        app_logger.info(
            f"[{self.name}] Completed crawl: {len(collected)} job postings passed strict 24-hour freshness filter."
        )
        return collected
