from app.providers.base_provider import BaseAIProvider
from app.providers.openai_provider import OpenAIProvider
from app.core.config import settings
from app.core.exceptions import ProviderUnavailableError

class ProviderFactory:
    @staticmethod
    def get_provider() -> BaseAIProvider:
        provider_name = settings.AI_PROVIDER.lower()
        
        if provider_name == "openai":
            return OpenAIProvider()
        
        # Add future providers here (e.g., anthropic, ollama)
        
        raise ProviderUnavailableError(f"Provider '{provider_name}' is not supported.")
