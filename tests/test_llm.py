import pytest
import asyncio
from typing import Type, TypeVar
from pydantic import BaseModel
from src.llm.providers import BaseLLMProvider, LLMProviderError
from src.llm.orchestrator import LLMOrchestrator
from src.llm.schemas import ExtractionBundle, ExtractedStartup

T = TypeVar("T", bound=BaseModel)

class MockFailingProvider(BaseLLMProvider):
    def __init__(self, name: str, status_code: int = 500):
        super().__init__(api_key="mock_key", model="mock_model", name=name)
        self.status_code = status_code
        self.call_count = 0

    async def extract_structured(self, prompt: str, schema: Type[T]) -> T:
        self.call_count += 1
        raise LLMProviderError(f"Simulated error {self.status_code}", status_code=self.status_code, provider=self.name)

class MockRateLimitingThenSucceedingProvider(BaseLLMProvider):
    def __init__(self, name: str, fail_times: int = 2):
        super().__init__(api_key="mock_key", model="mock_model", name=name)
        self.fail_times = fail_times
        self.call_count = 0

    async def extract_structured(self, prompt: str, schema: Type[T]) -> T:
        self.call_count += 1
        if self.call_count <= self.fail_times:
            raise LLMProviderError("Simulated 429 Rate Limit", status_code=429, provider=self.name)
        return schema(startups=[ExtractedStartup(name="RecoveredAI", employee_count=42)])

class MockSuccessfulProvider(BaseLLMProvider):
    def __init__(self, name: str):
        super().__init__(api_key="mock_key", model="mock_model", name=name)
        self.call_count = 0

    async def extract_structured(self, prompt: str, schema: Type[T]) -> T:
        self.call_count += 1
        return schema(startups=[ExtractedStartup(name="FallbackSuccessAI", employee_count=100)])

@pytest.mark.asyncio
async def test_llm_fallback_chain_succession():
    # Tier 1 fails with 500, Tier 2 succeeds
    tier1 = MockFailingProvider("MockGemini", status_code=500)
    tier2 = MockSuccessfulProvider("MockGroq")
    tier3 = MockSuccessfulProvider("MockDeepSeek")

    orchestrator = LLMOrchestrator(providers=[tier1, tier2, tier3], max_retries_per_tier=1)
    result, meta = await orchestrator.extract_with_fallback("Extract AI startups", ExtractionBundle)

    assert result is not None
    assert meta["status"] == "SUCCESS"
    assert meta["provider"] == "MockGroq"
    assert result.startups[0].name == "FallbackSuccessAI"
    assert tier1.call_count == 1
    assert tier2.call_count == 1
    assert tier3.call_count == 0  # Did not need to invoke Tier 3

@pytest.mark.asyncio
async def test_llm_rate_limit_429_backoff_and_recovery():
    # Provider hits 429 once, then succeeds on retry 2
    recovering_tier = MockRateLimitingThenSucceedingProvider("MockRateLimitProvider", fail_times=1)
    orchestrator = LLMOrchestrator(
        providers=[recovering_tier],
        max_retries_per_tier=3,
        base_backoff_sec=0.01,
        max_backoff_sec=0.1
    )
    result, meta = await orchestrator.extract_with_fallback("Extract entities", ExtractionBundle)

    assert result is not None
    assert meta["status"] == "SUCCESS"
    assert recovering_tier.call_count == 2
    assert result.startups[0].name == "RecoveredAI"

@pytest.mark.asyncio
async def test_all_providers_exhausted_dead_letter():
    # All tiers fail -> system marks requires_reprocessing without inventing fake data
    tier1 = MockFailingProvider("Tier1", 500)
    tier2 = MockFailingProvider("Tier2", 500)
    tier3 = MockFailingProvider("Tier3", 500)

    orchestrator = LLMOrchestrator(providers=[tier1, tier2, tier3], max_retries_per_tier=1)
    result, meta = await orchestrator.extract_with_fallback("Extract data", ExtractionBundle)

    assert result is None
    assert meta["status"] == "ALL_PROVIDERS_EXHAUSTED"
    assert meta["requires_reprocessing"] is True
