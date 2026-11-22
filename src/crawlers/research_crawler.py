import asyncio
import re
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Set, Tuple
from src.crawlers.base import BaseCrawler
from src.utils.dates import get_utc_now, to_iso8601_utc, parse_iso_or_relative_date
from src.utils.deduplication import normalize_url, compute_content_fingerprint
from src.utils.logging import app_logger
from config.settings import settings

class ResearchCrawler(BaseCrawler):
    """
    Concurrent Crawler for AI Research Papers.
    Acquires research papers from the official arXiv API (cs.AI, cs.LG, cs.CL, cs.CV).
    Scans for associated GitHub repository links in paper abstracts and comments,
    and dynamically queries the official GitHub API for live star counts and observation timestamps.
    """
    def __init__(self):
        super().__init__(name="ResearchCrawler", base_url="http://export.arxiv.org", rate_limit_per_second=2.0)
        self.gh_cache: Dict[str, Optional[int]] = {}
        self.gh_pattern = re.compile(r'https?://github\.com/([a-zA-Z0-9_\-\.]+)/([a-zA-Z0-9_\-\.]+)', re.IGNORECASE)

    async def _fetch_github_stars(self, gh_url: str) -> Tuple[Optional[int], Optional[str]]:
        """
        Queries official GitHub REST API to extract live star count.
        Returns (stars, retrieval_timestamp_iso).
        """
        match = self.gh_pattern.search(gh_url)
        if not match:
            return None, None
        
        owner, repo = match.group(1), match.group(2).rstrip('.').rstrip('/')
        repo_key = f"{owner}/{repo}".lower()

        if repo_key in self.gh_cache:
            return self.gh_cache[repo_key], to_iso8601_utc(get_utc_now())

        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "FrontierAtlas-Research-Tracker/1.0"
        }
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

        try:
            client = await self.get_client()
            res = await client.get(api_url, headers=headers, timeout=8.0)
            now_iso = to_iso8601_utc(get_utc_now())
            if res.status_code == 200:
                data = res.json()
                stars = data.get("stargazers_count")
                self.gh_cache[repo_key] = stars
                return stars, now_iso
            elif res.status_code == 404:
                self.gh_cache[repo_key] = None
                return None, None
            elif res.status_code == 403 or res.status_code == 429:
                app_logger.warning(f"[{self.name}] GitHub API rate limit reached fetching stars for {repo_key}")
                return None, None
        except Exception as e:
            app_logger.warning(f"[{self.name}] Failed to fetch GitHub stars for {repo_key}: {e}")

        return None, None

    async def crawl(self, limit: int = 1000) -> List[Dict[str, Any]]:
        app_logger.info(f"[{self.name}] Initiating acquisition of min {limit} unique AI research papers from arXiv...")
        collected: List[Dict[str, Any]] = []
        seen_fingerprints: Set[str] = set()

        batch_size = 250
        start_idx = 0
        total_queries = 0

        while len(collected) < limit and total_queries < 15:
            total_queries += 1
            arxiv_url = (
                f"http://export.arxiv.org/api/query?"
                f"search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.CV&"
                f"start={start_idx}&max_results={batch_size}&"
                f"sortBy=submittedDate&sortOrder=descending"
            )

            res = await self.fetch(arxiv_url)
            if not res or res.status_code != 200:
                app_logger.warning(f"[{self.name}] arXiv API request failed at offset {start_idx}. Backing off...")
                await asyncio.sleep(3.0)
                continue

            try:
                root = ET.fromstring(res.content)
            except Exception as e:
                app_logger.error(f"[{self.name}] Failed to parse arXiv XML response: {e}")
                break

            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            if not entries:
                app_logger.info(f"[{self.name}] No more entries returned by arXiv at offset {start_idx}.")
                break

            for entry in entries:
                # Title
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None and title_elem.text else "Untitled"
                title = re.sub(r'\s+', ' ', title)

                # Paper URL
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                paper_url = normalize_url(id_elem.text.strip()) if id_elem is not None and id_elem.text else ""

                fp = compute_content_fingerprint(title, paper_url)
                if fp in seen_fingerprints:
                    continue
                seen_fingerprints.add(fp)

                # Authors
                authors = []
                for author_elem in entry.findall('{http://www.w3.org/2005/Atom}author'):
                    name_elem = author_elem.find('{http://www.w3.org/2005/Atom}name')
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                # Published date
                pub_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                raw_pub = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else None
                pub_dt, _ = parse_iso_or_relative_date(raw_pub)
                pub_iso = to_iso8601_utc(pub_dt) if pub_dt else to_iso8601_utc(get_utc_now())

                # Scan summary and comment for associated GitHub repo
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                summary = summary_elem.text if summary_elem is not None and summary_elem.text else ""
                comment_elem = entry.find('{http://arxiv.org/schemas/atom}comment')
                comment = comment_elem.text if comment_elem is not None and comment_elem.text else ""
                combined_text = f"{summary} {comment}"

                gh_match = self.gh_pattern.search(combined_text)
                github_url = None
                github_stars = None
                stars_retrieved_at = None

                if gh_match:
                    raw_gh = gh_match.group(0).rstrip('.').rstrip(',').rstrip(')')
                    github_url = normalize_url(raw_gh)
                    # Query official GitHub API for verified stars
                    github_stars, stars_retrieved_at = await self._fetch_github_stars(github_url)

                collected.append({
                    "schema_version": "1.0",
                    "record_type": "RESEARCH_PAPER",
                    "title": title,
                    "authors_json": json.dumps(authors),
                    "paper_url": paper_url,
                    "github_url": github_url,
                    "github_stars": github_stars,
                    "github_stars_retrieved_at": stars_retrieved_at,
                    "published_date": pub_iso,
                    "fingerprint": fp
                })

                if len(collected) >= limit:
                    break

            start_idx += len(entries)
            app_logger.info(f"[{self.name}] Progress: {len(collected)}/{limit} research papers processed.")
            await asyncio.sleep(1.0)  # Respect arXiv polite crawl policy

        app_logger.info(f"[{self.name}] Successfully acquired {len(collected)} verified AI research paper records.")
        return collected
