import asyncio
import re
from typing import List, Dict, Any, Optional, Set, Tuple
import feedparser
from bs4 import BeautifulSoup
from src.crawlers.base import BaseCrawler
from src.utils.dates import (
    get_utc_now, to_iso8601_utc, parse_iso_or_relative_date, is_within_hours
)
from src.utils.deduplication import normalize_url, compute_content_fingerprint
from src.utils.logging import app_logger

class BaseNewsAdapter:
    """Base interface for news source adapters."""
    def __init__(self, name: str, feed_url: str):
        self.name = name
        self.feed_url = feed_url

    async def fetch_and_parse(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        raise NotImplementedError


class RSSNewsAdapter(BaseNewsAdapter):
    """Adapter for standard RSS / Atom feeds."""
    async def fetch_and_parse(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        res = await crawler.fetch(self.feed_url)
        if not res or res.status_code != 200:
            return []

        feed = feedparser.parse(res.content)
        items = []
        for entry in feed.entries:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            raw_date = getattr(entry, "published", getattr(entry, "updated", None))
            
            summary = getattr(entry, "summary", "")
            if summary:
                # Strip HTML from summary
                soup = BeautifulSoup(summary, "html.parser")
                summary = soup.get_text(separator=" ").strip()

            author = getattr(entry, "author", None)
            
            # Content / full text if available in feed
            full_text = ""
            if hasattr(entry, "content"):
                full_text = " ".join([c.get("value", "") for c in entry.content])
                full_text = BeautifulSoup(full_text, "html.parser").get_text(separator=" ").strip()
            if not full_text:
                full_text = summary

            items.append({
                "source_name": self.name,
                "source_url": link,
                "title": title,
                "raw_date": raw_date,
                "summary": summary[:600] if summary else "",
                "full_text": full_text[:4000] if full_text else "",
                "author": author
            })
        return items


class HackerNewsAIAdapter(BaseNewsAdapter):
    """Adapter for Hacker News AI stories via Algolia API."""
    def __init__(self):
        super().__init__(
            name="Hacker News AI Signals",
            feed_url="https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI&hitsPerPage=40"
        )

    async def fetch_and_parse(self, crawler: BaseCrawler) -> List[Dict[str, Any]]:
        res = await crawler.fetch(self.feed_url)
        if not res or res.status_code != 200:
            return []

        data = res.json()
        hits = data.get("hits", [])
        items = []
        for h in hits:
            title = h.get("title", "").strip()
            link = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
            raw_date = h.get("created_at")
            author = h.get("author")
            story_text = h.get("story_text") or f"Discussion on Hacker News ({h.get('points', 0)} points, {h.get('num_comments', 0)} comments)"

            items.append({
                "source_name": self.name,
                "source_url": link,
                "title": title,
                "raw_date": raw_date,
                "summary": story_text[:600],
                "full_text": story_text[:2000],
                "author": author
            })
        return items


class NewsCrawler(BaseCrawler):
    """
    High-Fidelity Signal Ingestion for AI News.
    Monitors 5 distinct news sources:
      1. TechCrunch AI
      2. The Verge
      3. Engadget AI
      4. Hacker News AI Signals
      5. Ars Technica Tech Lab
    Enforces STRICT 24-hour freshness policy.
    Distinguishes published_at, first_discovered_at, and collected_at.
    """
    def __init__(self, adapters: Optional[List[BaseNewsAdapter]] = None):
        super().__init__(name="NewsCrawler", base_url="https://techcrunch.com", rate_limit_per_second=2.0)
        self.adapters = adapters or [
            RSSNewsAdapter("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
            RSSNewsAdapter("The Verge AI", "https://www.theverge.com/rss/index.xml"),
            RSSNewsAdapter("Engadget AI", "https://www.engadget.com/rss.xml"),
            HackerNewsAIAdapter(),
            RSSNewsAdapter("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab")
        ]

    async def crawl(self, limit: int = 500) -> List[Dict[str, Any]]:
        app_logger.info(f"[{self.name}] Initiating signal monitoring across {len(self.adapters)} news sources...")
        now = get_utc_now()
        now_iso = to_iso8601_utc(now)
        collected: List[Dict[str, Any]] = []
        seen_fingerprints: Set[str] = set()

        for adapter in self.adapters:
            app_logger.info(f"[{self.name}] Fetching news from: {adapter.name}")
            try:
                raw_items = await adapter.fetch_and_parse(self)
                app_logger.info(f"[{self.name}] {adapter.name} returned {len(raw_items)} raw entries.")

                for item in raw_items:
                    raw_date = item.get("raw_date")
                    pub_dt, confidence = parse_iso_or_relative_date(raw_date, ref_time=now)

                    # STRICT 24-HOUR FRESHNESS FILTER
                    if not is_within_hours(pub_dt, hours=24, ref_time=now):
                        # Filter out stale items
                        continue

                    # Must have sufficient date confidence to guarantee 24-hr freshness
                    if confidence < 0.70:
                        app_logger.warning(
                            f"[{self.name}] Rejected item '{item['title'][:40]}' due to low date confidence ({confidence})"
                        )
                        continue

                    canonical_url = normalize_url(item.get("source_url", ""))
                    fp = compute_content_fingerprint(item.get("title", ""), canonical_url)
                    if fp in seen_fingerprints:
                        continue
                    seen_fingerprints.add(fp)

                    pub_iso = to_iso8601_utc(pub_dt)

                    record = {
                        "schema_version": "1.0",
                        "record_type": "NEWS",
                        "source_name": item["source_name"],
                        "source_url": canonical_url,
                        "title": item["title"],
                        "published_at": pub_iso,
                        "summary": item.get("summary", ""),
                        "full_text": item.get("full_text", ""),
                        "author": item.get("author"),
                        "primary_entity": None,
                        "first_discovered_at": now_iso,
                        "collected_at": now_iso,
                        "date_confidence": confidence,
                        "fingerprint": fp
                    }
                    collected.append(record)

            except Exception as e:
                app_logger.error(f"[{self.name}] Error crawling source {adapter.name}: {e}")

        app_logger.info(
            f"[{self.name}] Completed crawl: {len(collected)} news articles passed strict 24-hour freshness filter."
        )
        return collected
