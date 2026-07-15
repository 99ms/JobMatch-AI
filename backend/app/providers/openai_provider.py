import time

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AsyncOpenAI,
    AuthenticationError,
    RateLimitError,
)

from app.core.config import settings
from app.core.exceptions import (
    AITimeoutError,
    AIRateLimitError,
    InvalidAIResponseError,
    InvalidAPIKeyError,
    ProviderUnavailableError,
)
from app.providers.base_provider import BaseAIProvider
from app.schemas.ai import ProviderResponse, TokenUsage
from app.utils.token_utils import estimate_tokens

class OpenAIProvider(BaseAIProvider):
    """OpenAI implementation of the provider-agnostic AI interface."""
    
    def __init__(self):
        self.model = settings.AI_MODEL_NAME
        self.api_key = settings.OPENAI_API_KEY
        self._client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    async def generate(self, prompt: str) -> ProviderResponse:
        if not self.api_key or self._client is None:
            raise InvalidAPIKeyError("OPENAI_API_KEY is not configured.")

        start_time = time.monotonic()

        try:
            completion = await self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.AI_MAX_TOKENS,
            )
        except AuthenticationError as exc:
            raise InvalidAPIKeyError("OpenAI rejected the configured API key.") from exc
        except APITimeoutError as exc:
            raise AITimeoutError("OpenAI request timed out.") from exc
        except RateLimitError as exc:
            raise AIRateLimitError("OpenAI rate limit exceeded.") from exc
        except (APIConnectionError, APIStatusError) as exc:
            raise ProviderUnavailableError("OpenAI service is unavailable.") from exc

        content = self._extract_content(completion)
        usage = getattr(completion, "usage", None)
        prompt_tokens = getattr(usage, "prompt_tokens", None)
        completion_tokens = getattr(usage, "completion_tokens", None)

        if prompt_tokens is None:
            prompt_tokens = estimate_tokens(prompt)
        if completion_tokens is None:
            completion_tokens = estimate_tokens(content)

        return ProviderResponse(
            content=content,
            token_usage=TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            ),
            provider="openai",
            model=self.model,
            duration_ms=int((time.monotonic() - start_time) * 1000),
        )

    @staticmethod
    def _extract_content(completion: object) -> str:
        choices = getattr(completion, "choices", None)
        if not choices:
            raise InvalidAIResponseError("OpenAI returned no completion choices.")

        content = getattr(getattr(choices[0], "message", None), "content", None)
        if not isinstance(content, str) or not content.strip():
            raise InvalidAIResponseError("OpenAI returned an empty completion message.")

        return content
