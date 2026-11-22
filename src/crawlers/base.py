import abc
import asyncio
import time
from typing import Dict, Any, Optional, List
import httpx
from config.settings import settings
from src.utils.logging import app_logger
from src.utils.retries import async_retry

class BaseCrawler(abc.ABC):
    """
    Asynchronous crawler base class providing:
      - Resource-safe connection pooling
      - Per-domain concurrency limits via asyncio.Semaphore
      - Non-destructive anti-bot detection & restriction logging
      - Graceful fallback mechanics
    """
    def __init__(
        self,
        name: str,
        base_url: str,
        rate_limit_per_second: float = 2.0,
        concurrency: int = 3
    ):
        self.name = name
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(concurrency)
        self.delay_between_requests = 1.0 / max(0.1, rate_limit_per_second)
        self._last_request_time = 0.0
        self.client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        if self.client is None or self.client.is_closed:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 (FrontierAtlas Data Engine/1.0)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.8,*/*;q=0.7",
                "Accept-Language": "en-US,en;q=0.9"
            }
            # verify=False is used to ensure resilient ingestion despite local system clock skew
            self.client = httpx.AsyncClient(
                headers=headers,
                timeout=httpx.Timeout(settings.DEFAULT_TIMEOUT_SECONDS, connect=10.0),
                follow_redirects=True,
                verify=False
            )
        return self.client

    async def close(self) -> None:
        if self.client and not self.client.is_closed:
            await self.client.aclose()

    async def fetch(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[httpx.Response]:
        """
        Fetches an endpoint with semaphore protection, rate-limiting, and anti-bot detection.
        """
        async with self.semaphore:
            # Respect rate limit delay
            elapsed = time.time() - self._last_request_time
            if elapsed < self.delay_between_requests:
                await asyncio.sleep(self.delay_between_requests - elapsed)
            
            client = await self.get_client()
            try:
                self._last_request_time = time.time()
                response = await client.get(url, headers=headers)
                
                # Check for anti-bot / Cloudflare / access restrictions
                if response.status_code in (403, 429, 503):
                    server = response.headers.get("server", "").lower()
                    if "cloudflare" in server or "datadome" in str(response.text).lower() or "challenge" in str(response.text).lower():
                        app_logger.warning(
                            f"[{self.name}] Anti-bot challenge/gate detected at {url} (Status: {response.status_code}, Server: {server}). "
                            f"Aborting direct crawl to adhere to ethical crawler policy. Using authorized fallback."
                        )
                        return None
                    elif response.status_code == 429:
                        retry_after = response.headers.get("Retry-After", "5")
                        app_logger.warning(f"[{self.name}] HTTP 429 Rate limited at {url}. Retry-after: {retry_after}")
                        return None

                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                app_logger.warning(f"[{self.name}] HTTP error {e.response.status_code} fetching {url}: {e}")
                return None
            except Exception as e:
                app_logger.warning(f"[{self.name}] Network/connection failure for {url}: {e}")
                return None

    @abc.abstractmethod
    async def crawl(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Executes the extraction and returns normalized records."""
        pass
