from app.providers.base_provider import BaseAIProvider
from app.schemas.ai import ProviderResponse, TokenUsage
from app.core.config import settings
from app.utils.token_utils import estimate_tokens
import time

class OpenAIProvider(BaseAIProvider):
    """Stub implementation of OpenAI provider for Milestone 2.75."""
    
    def __init__(self):
        self.model = settings.AI_MODEL_NAME
        self.api_key = settings.OPENAI_API_KEY
        
    async def generate(self, prompt: str) -> ProviderResponse:
        start_time = time.time()
        
        # Simulate network delay for stub
        # await asyncio.sleep(0.5)
        
        # In the future, this will call the OpenAI API.
        mock_content = "This is a mock response from the OpenAI provider."
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        prompt_tokens = estimate_tokens(prompt)
        completion_tokens = estimate_tokens(mock_content)
        
        return ProviderResponse(
            content=mock_content,
            token_usage=TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            ),
            provider="openai",
            model=self.model,
            duration_ms=duration_ms
        )
