import abc
import json
import os
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel
from src.utils.logging import app_logger

T = TypeVar("T", bound=BaseModel)

class LLMProviderError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, provider: str = "Unknown"):
        super().__init__(message)
        self.status_code = status_code
        self.provider = provider


class BaseLLMProvider(abc.ABC):
    """Abstract base provider for multi-tier extraction engine."""
    def __init__(self, api_key: Optional[str], model: str, name: str):
        self.api_key = api_key
        self.model = model
        self.name = name

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    @abc.abstractmethod
    async def extract_structured(self, prompt: str, schema: Type[T]) -> T:
        """Extract structured data adhering to Pydantic schema."""
        pass


class GeminiFlashProvider(BaseLLMProvider):
    """Tier 1: Google Gemini Flash provider."""
    def __init__(self, api_key: Optional[str], model: str = "gemini-2.0-flash"):
        super().__init__(api_key, model, name="Gemini Flash")
        self._client = None
        if self.is_configured:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                app_logger.warning(f"Could not initialize Google GenAI SDK: {e}")

    async def extract_structured(self, prompt: str, schema: Type[T]) -> T:
        if not self.is_configured:
            raise LLMProviderError("Gemini API key not configured", status_code=401, provider=self.name)

        try:
            # Generate structured response with Gemini
            response = self._client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                }
            )
            raw_text = response.text
            parsed_json = json.loads(raw_text)
            return schema.model_validate(parsed_json)
        except Exception as e:
            err_str = str(e).lower()
            status_code = 429 if "429" in err_str or "quota" in err_str or "rate" in err_str else 500
            if "413" in err_str or "too large" in err_str:
                status_code = 413
            raise LLMProviderError(f"Gemini error: {e}", status_code=status_code, provider=self.name) from e


class GroqLlamaProvider(BaseLLMProvider):
    """Tier 2: Groq Llama 3 provider."""
    def __init__(self, api_key: Optional[str], model: str = "llama-3.3-70b-versatile"):
        super().__init__(api_key, model, name="Groq Llama 3")
        self._client = None
        if self.is_configured:
            try:
                from groq import AsyncGroq
                self._client = AsyncGroq(api_key=self.api_key)
            except Exception as e:
                app_logger.warning(f"Could not initialize Groq SDK: {e}")

    async def extract_structured(self, prompt: str, schema: Type[T]) -> T:
        if not self.is_configured or not self._client:
            raise LLMProviderError("Groq API key not configured", status_code=401, provider=self.name)

        system_instruction = (
            f"You are a precise data extraction engine. Extract data and return strictly valid JSON matching this schema:\n"
            f"{json.dumps(schema.model_json_schema())}\nDo not wrap output in markdown code blocks."
        )

        try:
            completion = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            raw_text = completion.choices[0].message.content
            parsed_json = json.loads(raw_text)
            return schema.model_validate(parsed_json)
        except Exception as e:
            err_str = str(e).lower()
            status_code = 429 if "429" in err_str or "rate limit" in err_str else 500
            if "413" in err_str or "too large" in err_str or "context length" in err_str:
                status_code = 413
            raise LLMProviderError(f"Groq error: {e}", status_code=status_code, provider=self.name) from e


class DeepSeekProvider(BaseLLMProvider):
    """Tier 3: DeepSeek provider (OpenAI compatible)."""
    def __init__(self, api_key: Optional[str], model: str = "deepseek-chat", base_url: str = "https://api.deepseek.com/v1"):
        super().__init__(api_key, model, name="DeepSeek")
        self.base_url = base_url
        self._client = None
        if self.is_configured:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
            except Exception as e:
                app_logger.warning(f"Could not initialize DeepSeek OpenAI client: {e}")

    async def extract_structured(self, prompt: str, schema: Type[T]) -> T:
        if not self.is_configured or not self._client:
            raise LLMProviderError("DeepSeek API key not configured", status_code=401, provider=self.name)

        system_instruction = (
            f"You are a high-fidelity data extraction engine. Extract data and return ONLY a JSON object matching this schema:\n"
            f"{json.dumps(schema.model_json_schema())}"
        )

        try:
            completion = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            raw_text = completion.choices[0].message.content
            parsed_json = json.loads(raw_text)
            return schema.model_validate(parsed_json)
        except Exception as e:
            err_str = str(e).lower()
            status_code = 429 if "429" in err_str or "rate limit" in err_str else 500
            if "413" in err_str or "context length" in err_str or "payload too large" in err_str:
                status_code = 413
            raise LLMProviderError(f"DeepSeek error: {e}", status_code=status_code, provider=self.name) from e
