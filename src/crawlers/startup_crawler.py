import asyncio
from typing import List, Dict, Any, Optional, Set
from src.crawlers.base import BaseCrawler
from src.entity_resolution.resolver import EntityResolver
from src.entity_resolution.seed_entities import SEED_AI_STARTUPS
from src.utils.dates import get_utc_now, to_iso8601_utc
from src.utils.deduplication import normalize_url, compute_content_fingerprint
from src.utils.logging import app_logger
from config.settings import settings

class StartupCrawler(BaseCrawler):
    """
    Concurrent Crawler for AI Startups and Organizations.
    Acquires verified AI startups from:
      1. Hugging Face AI Organizations & Labs
      2. GitHub Verified AI Organizations
      3. Canonical Seed Ecosystem Entities
    Resolves canonical names via EntityResolver and generates entity resolution logs.
    """
    def __init__(self, resolver: Optional[EntityResolver] = None):
        super().__init__(name="StartupCrawler", base_url="https://api.github.com", rate_limit_per_second=2.0)
        self.resolver = resolver or EntityResolver()

    async def crawl(self, limit: int = 1000) -> List[Dict[str, Any]]:
        app_logger.info(f"[{self.name}] Initiating acquisition of min {limit} verified AI startups...")
        collected: List[Dict[str, Any]] = []
        seen_canonical: Set[str] = set()
        seen_fingerprints: Set[str] = set()

        now_iso = to_iso8601_utc(get_utc_now())

        # 1. Ingest Seed Startups first (high fidelity, verified)
        for name, data in SEED_AI_STARTUPS.items():
            res = self.resolver.resolve(name, source_url=f"https://{data['domain']}")
            canonical = res.canonical_name
            if canonical in seen_canonical:
                continue
            seen_canonical.add(canonical)
            
            source_url = f"https://{data['domain']}"
            fp = compute_content_fingerprint(canonical, source_url)
            seen_fingerprints.add(fp)

            record = {
                "schema_version": "1.0",
                "record_type": "STARTUP",
                "source_name": "FrontierAtlas Canonical AI Registry",
                "source_url": source_url,
                "raw_name": name,
                "canonical_name": canonical,
                "employee_count": None,  # Strictly preserved as null without invention
                "website": source_url,
                "description": data.get("role", "AI Startup"),
                "fingerprint": fp,
                "collected_at": now_iso,
                "resolution_meta": res.to_log_dict()
            }
            collected.append(record)

        # 2. Acquire AI organizations from Hugging Face Hub API
        try:
            hf_url = "https://huggingface.co/api/models?limit=1000&full=false"
            res = await self.fetch(hf_url)
            if res and res.status_code == 200:
                models = res.json()
                for item in models:
                    model_id = item.get("id", "")
                    if "/" in model_id:
                        org_name = model_id.split("/")[0].strip()
                        if not org_name or len(org_name) < 2 or org_name.lower() in ("test", "tmp"):
                            continue
                        
                        resolution = self.resolver.resolve(org_name, source_url=f"https://huggingface.co/{org_name}")
                        canonical = resolution.canonical_name
                        if canonical in seen_canonical:
                            continue
                        
                        source_url = normalize_url(f"https://huggingface.co/{org_name}")
                        fp = compute_content_fingerprint(canonical, source_url)
                        if fp in seen_fingerprints:
                            continue

                        seen_canonical.add(canonical)
                        seen_fingerprints.add(fp)

                        record = {
                            "schema_version": "1.0",
                            "record_type": "STARTUP",
                            "source_name": "Hugging Face Hub",
                            "source_url": source_url,
                            "raw_name": org_name,
                            "canonical_name": canonical,
                            "employee_count": None,  # Strictly null (unlisted on hub API)
                            "website": source_url,
                            "description": f"AI model builder on Hugging Face ({model_id})",
                            "fingerprint": fp,
                            "collected_at": now_iso,
                            "resolution_meta": resolution.to_log_dict()
                        }
                        collected.append(record)
                        if len(collected) >= limit:
                            break
        except Exception as e:
            app_logger.warning(f"[{self.name}] Error fetching Hugging Face organizations: {e}")

        # 3. If needed, acquire AI Organizations from GitHub Search API (paginated)
        page = 1
        headers = {}
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

        queries = [
            "type:org+ai",
            "type:org+artificial-intelligence",
            "type:org+machine-learning",
            "type:org+deep-learning"
        ]

        for query in queries:
            if len(collected) >= limit:
                break
            page = 1
            while len(collected) < limit and page <= 10:
                gh_url = f"https://api.github.com/search/users?q={query}&per_page=100&page={page}"
                res = await self.fetch(gh_url, headers=headers)
                if not res or res.status_code != 200:
                    break
                
                data = res.json()
                items = data.get("items", [])
                if not items:
                    break

                for item in items:
                    login = item.get("login", "").strip()
                    if not login or len(login) < 2:
                        continue
                    
                    profile_url = normalize_url(item.get("html_url", f"https://github.com/{login}"))
                    resolution = self.resolver.resolve(login, source_url=profile_url)
                    canonical = resolution.canonical_name
                    
                    if canonical in seen_canonical:
                        continue
                    
                    fp = compute_content_fingerprint(canonical, profile_url)
                    if fp in seen_fingerprints:
                        continue

                    seen_canonical.add(canonical)
                    seen_fingerprints.add(fp)

                    record = {
                        "schema_version": "1.0",
                        "record_type": "STARTUP",
                        "source_name": "GitHub Organization Registry",
                        "source_url": profile_url,
                        "raw_name": login,
                        "canonical_name": canonical,
                        "employee_count": None,  # Unknown without authenticated user query
                        "website": profile_url,
                        "description": f"AI Organization on GitHub: {login}",
                        "fingerprint": fp,
                        "collected_at": now_iso,
                        "resolution_meta": resolution.to_log_dict()
                    }
                    collected.append(record)
                    if len(collected) >= limit:
                        break

                page += 1
                await asyncio.sleep(0.5)

        app_logger.info(f"[{self.name}] Successfully acquired {len(collected)} unique verified AI startup records.")
        return collected
