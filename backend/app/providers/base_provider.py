from abc import ABC, abstractmethod
from app.schemas.ai import ProviderResponse

class BaseAIProvider(ABC):
    """Abstract base class for all AI providers."""
    
    @abstractmethod
    async def generate(self, prompt: str) -> ProviderResponse:
        """
        Executes a prompt against the AI provider.
        Returns a structured ProviderResponse.
        """
        pass
