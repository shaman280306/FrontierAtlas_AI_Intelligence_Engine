import pytest
from src.crawlers.startup_crawler import StartupCrawler
from src.crawlers.product_crawler import ProductCrawler
from src.crawlers.research_crawler import ResearchCrawler
from src.crawlers.news_crawler import NewsCrawler
from src.crawlers.job_crawler import JobCrawler
from src.utils.deduplication import normalize_url, compute_content_fingerprint

def test_url_normalization():
    dirty_url = "https://www.example.com/company/profile/?utm_source=twitter&utm_medium=cpc&ref=homepage#contact"
    clean_url = normalize_url(dirty_url)
    assert "utm_source" not in clean_url
    assert "utm_medium" not in clean_url
    assert "ref" not in clean_url
    assert "#contact" not in clean_url
    assert clean_url == "https://www.example.com/company/profile"

def test_fingerprint_deterministic():
    fp1 = compute_content_fingerprint("OpenAI", "https://openai.com")
    fp2 = compute_content_fingerprint("openai", "https://openai.com")
    assert fp1 == fp2  # Case insensitive determinism

    fp3 = compute_content_fingerprint("Anthropic", "https://anthropic.com")
    assert fp1 != fp3

@pytest.mark.asyncio
async def test_startup_crawler_initialization():
    crawler = StartupCrawler()
    assert crawler.name == "StartupCrawler"
    await crawler.close()

@pytest.mark.asyncio
async def test_product_crawler_initialization():
    crawler = ProductCrawler()
    assert crawler.name == "ProductCrawler"
    await crawler.close()

@pytest.mark.asyncio
async def test_research_crawler_initialization():
    crawler = ResearchCrawler()
    assert crawler.name == "ResearchCrawler"
    await crawler.close()

@pytest.mark.asyncio
async def test_news_crawler_initialization():
    crawler = NewsCrawler()
    assert len(crawler.adapters) >= 5
    await crawler.close()

@pytest.mark.asyncio
async def test_job_crawler_initialization():
    crawler = JobCrawler()
    assert len(crawler.adapters) >= 5
    await crawler.close()
