import asyncio
import random
from typing import Type, TypeVar, Optional, List, Dict, Any, Tuple
from pydantic import BaseModel
from config.settings import settings
from src.llm.schemas import ExtractionBundle
from src.llm.chunking import SemanticChunker
from src.llm.providers import (
    BaseLLMProvider, GeminiFlashProvider, GroqLlamaProvider, DeepSeekProvider, LLMProviderError
)
from src.utils.logging import app_logger

T = TypeVar("T", bound=BaseModel)

class LLMOrchestrator:
    """
    Multi-tier LLM Orchestration Engine.
    Implements:
      1. Primary: Gemini Flash
      2. Secondary: Groq Llama 3
      3. Tertiary: DeepSeek
    Features:
      - Exponential backoff with jitter on HTTP 429 (Rate Limits)
      - Dynamic Semantic Chunking on HTTP 413 (Payload Too Large)
      - Transparent fallback progression
      - Dead-letter preservation on complete fallback exhaustion
    """
    def __init__(
        self,
        providers: Optional[List[BaseLLMProvider]] = None,
        max_retries_per_tier: int = 3,
        base_backoff_sec: float = 1.0,
        max_backoff_sec: float = 15.0
    ):
        if providers is not None:
            self.providers = providers
        else:
            self.providers = [
                GeminiFlashProvider(api_key=settings.GEMINI_API_KEY, model=settings.GEMINI_MODEL),
                GroqLlamaProvider(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL),
                DeepSeekProvider(
                    api_key=settings.DEEPSEEK_API_KEY,
                    model=settings.DEEPSEEK_MODEL,
                    base_url=settings.DEEPSEEK_BASE_URL
                )
            ]
        self.max_retries = max_retries_per_tier
        self.base_backoff = base_backoff_sec
        self.max_backoff = max_backoff_sec
        self.chunker = SemanticChunker(max_tokens_per_chunk=2500)

    async def extract_with_fallback(self, prompt: str, schema: Type[T], doc_title: Optional[str] = None) -> Tuple[Optional[T], Dict[str, Any]]:
        """
        Executes structured extraction through the fallback chain.
        Returns (result_model, audit_metadata).
        """
        audit_trail: List[Dict[str, Any]] = []

        for provider in self.providers:
            if not provider.is_configured:
                audit_trail.append({
                    "provider": provider.name,
                    "status": "SKIPPED",
                    "reason": "Missing API credentials"
                })
                continue

            app_logger.info(f"Attempting extraction with Tier: {provider.name}")
            
            # Tier execution with retry loop
            for attempt in range(1, self.max_retries + 1):
                try:
                    result = await provider.extract_structured(prompt, schema)
                    audit_trail.append({
                        "provider": provider.name,
                        "status": "SUCCESS",
                        "attempts": attempt
                    })
                    app_logger.info(f"Extraction successful using {provider.name} on attempt {attempt}")
                    return result, {"status": "SUCCESS", "provider": provider.name, "audit": audit_trail}

                except LLMProviderError as e:
                    audit_trail.append({
                        "provider": provider.name,
                        "attempt": attempt,
                        "error_code": e.status_code,
                        "error_message": str(e)
                    })

                    # Handle HTTP 413: Payload Too Large -> Chunk document and reconcile
                    if e.status_code == 413 and schema == ExtractionBundle:
                        app_logger.warning(
                            f"HTTP 413 Payload Too Large on {provider.name}. Triggering semantic chunking..."
                        )
                        chunked_result = await self._chunk_and_extract(prompt, provider, doc_title)
                        if chunked_result:
                            audit_trail.append({
                                "provider": provider.name,
                                "status": "SUCCESS_CHUNKED",
                                "note": "Reconciled multiple semantic chunks"
                            })
                            return chunked_result, {"status": "SUCCESS_CHUNKED", "provider": provider.name, "audit": audit_trail}

                    # Handle HTTP 429: Rate Limit -> Exponential backoff with random jitter
                    if e.status_code == 429 and attempt < self.max_retries:
                        backoff = min(self.max_backoff, self.base_backoff * (2 ** (attempt - 1)))
                        jittered_delay = backoff + random.uniform(0.1, 1.5)
                        app_logger.warning(
                            f"Rate limit (429) hit on {provider.name}. Backing off for {jittered_delay:.2f}s (attempt {attempt}/{self.max_retries})"
                        )
                        await asyncio.sleep(jittered_delay)
                        continue

                    # If other error or retries exhausted, break to next provider
                    app_logger.warning(f"Provider {provider.name} failed on attempt {attempt}: {e}. Proceeding to fallback...")
                    break

        app_logger.error("All configured LLM providers failed or were unconfigured. Preserving raw record in dead-letter state.")
        return None, {
            "status": "ALL_PROVIDERS_EXHAUSTED",
            "audit": audit_trail,
            "requires_reprocessing": True
        }

    async def _chunk_and_extract(self, full_text: str, provider: BaseLLMProvider, title: Optional[str]) -> Optional[ExtractionBundle]:
        """Splits full document into chunks, extracts from each, and reconciles results."""
        chunks = self.chunker.chunk_document(full_text, title=title)
        chunk_results: List[ExtractionBundle] = []

        for chunk in chunks:
            chunk_prompt = f"Extract all AI startups, products, jobs, and news signals from this section:\n\n{chunk.text}"
            try:
                sub_res = await provider.extract_structured(chunk_prompt, ExtractionBundle)
                chunk_results.append(sub_res)
            except Exception as e:
                app_logger.error(f"Error extracting from chunk {chunk.index} on {provider.name}: {e}")

        if chunk_results:
            return self.chunker.reconcile_chunk_extractions(chunk_results)
        return None
