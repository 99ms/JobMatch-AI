class AIException(Exception):
    """Base exception for all AI infrastructure errors."""
    pass

class ProviderUnavailableError(AIException):
    """Raised when the AI provider service is down or unreachable."""
    pass

class InvalidAPIKeyError(AIException):
    """Raised when the provided API key is invalid or rejected by the provider."""
    pass

class AITimeoutError(AIException):
    """Raised when an AI generation request times out."""
    pass

class AIRateLimitError(AIException):
    """Raised when the provider's rate limit is exceeded."""
    pass

class InvalidAIResponseError(AIException):
    """Raised when the provider returns a malformed or unexpected response."""
    pass


class AIOutputValidationError(AIException):
    """Raised when a successful provider response fails output parsing or validation."""
    pass
