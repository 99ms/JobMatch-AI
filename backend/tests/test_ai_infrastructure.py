import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from app.core.config import settings
from app.core.exceptions import (
    AIException,
    ProviderUnavailableError,
    InvalidAPIKeyError,
    AITimeoutError,
    AIRateLimitError,
    InvalidAIResponseError,
)
from app.utils.prompt_manager import PromptManager
from app.utils.token_utils import estimate_tokens
from app.providers.base_provider import BaseAIProvider
from app.providers.provider_factory import ProviderFactory
from app.providers.openai_provider import OpenAIProvider
from app.schemas.ai import (
    ProviderResponse,
    TokenUsage,
    ResumeFeedbackRequest,
    ResumeTailorRequest,
    CoverLetterRequest,
    InterviewQuestionsRequest,
)
from app.services.ai_service import AIService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_provider_response(content: str = "mock") -> ProviderResponse:
    return ProviderResponse(
        content=content,
        token_usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        provider="mock",
        model="mock-model",
        duration_ms=1,
    )


class MockProvider(BaseAIProvider):
    """In-process provider that never makes network calls."""

    def __init__(self, response_content: str = "mock response"):
        self.response_content = response_content
        self.model = "mock-model"

    async def generate(self, prompt: str) -> ProviderResponse:
        return make_provider_response(self.response_content)


class FailingProvider(BaseAIProvider):
    """Provider that always raises AIRateLimitError."""

    def __init__(self):
        self.model = "failing-model"

    async def generate(self, prompt: str) -> ProviderResponse:
        raise AIRateLimitError("Rate limit exceeded.")


# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------

class TestConfiguration:
    def test_project_name_default(self):
        assert settings.PROJECT_NAME == "JobMatch AI"

    def test_ai_provider_default(self):
        assert settings.AI_PROVIDER == "openai"

    def test_ai_model_name_set(self):
        assert settings.AI_MODEL_NAME  # must be a non-empty string

    def test_temperature_in_valid_range(self):
        assert 0.0 <= settings.AI_TEMPERATURE <= 2.0

    def test_max_tokens_positive(self):
        assert settings.AI_MAX_TOKENS > 0

    def test_api_key_optional_default_none(self):
        # If no .env is present, OPENAI_API_KEY defaults to None
        assert settings.OPENAI_API_KEY is None or isinstance(settings.OPENAI_API_KEY, str)


# ---------------------------------------------------------------------------
# 2. Prompt Manager
# ---------------------------------------------------------------------------

class TestPromptManager:
    def test_load_resume_feedback_prompt(self):
        content = PromptManager.get_prompt("resume_feedback", "v1")
        assert isinstance(content, str)
        assert len(content) > 0

    def test_load_tailor_resume_prompt(self):
        content = PromptManager.get_prompt("tailor_resume", "v1")
        assert isinstance(content, str)
        assert len(content) > 0

    def test_load_cover_letter_prompt(self):
        content = PromptManager.get_prompt("cover_letter", "v1")
        assert isinstance(content, str)
        assert len(content) > 0

    def test_load_interview_questions_prompt(self):
        content = PromptManager.get_prompt("interview_questions", "v1")
        assert isinstance(content, str)
        assert len(content) > 0

    def test_default_version_is_v1(self):
        # Calling without version should use v1
        content_explicit = PromptManager.get_prompt("resume_feedback", "v1")
        content_default = PromptManager.get_prompt("resume_feedback")
        assert content_explicit == content_default

    def test_missing_prompt_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            PromptManager.get_prompt("does_not_exist", "v99")

    def test_missing_version_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            PromptManager.get_prompt("resume_feedback", "v999")


# ---------------------------------------------------------------------------
# 3. Token Estimation Utility
# ---------------------------------------------------------------------------

class TestTokenEstimation:
    def test_empty_string_returns_zero(self):
        assert estimate_tokens("") == 0

    def test_single_word(self):
        result = estimate_tokens("hello")
        assert result >= 1

    def test_proportional_to_length(self):
        short = estimate_tokens("hello world")
        long = estimate_tokens("hello world foo bar baz qux")
        assert long > short

    def test_returns_integer(self):
        result = estimate_tokens("some text here")
        assert isinstance(result, int)

    def test_whitespace_only_returns_zero(self):
        assert estimate_tokens("   ") == 0


# ---------------------------------------------------------------------------
# 4. Provider Factory
# ---------------------------------------------------------------------------

class TestProviderFactory:
    def test_returns_openai_provider_by_default(self):
        provider = ProviderFactory.get_provider()
        assert isinstance(provider, OpenAIProvider)

    def test_unsupported_provider_raises_error(self):
        with patch.object(settings, "AI_PROVIDER", "unsupported_provider"):
            with pytest.raises(ProviderUnavailableError):
                ProviderFactory.get_provider()


# ---------------------------------------------------------------------------
# 5. Provider Abstraction
# ---------------------------------------------------------------------------

class TestProviderAbstraction:
    def test_mock_provider_implements_interface(self):
        provider = MockProvider()
        assert isinstance(provider, BaseAIProvider)

    def test_mock_provider_returns_provider_response(self):
        provider = MockProvider()
        response = asyncio.get_event_loop().run_until_complete(
            provider.generate("test prompt")
        )
        assert isinstance(response, ProviderResponse)
        assert response.provider == "mock"
        assert isinstance(response.content, str)
        assert response.token_usage.total_tokens > 0

    def test_provider_response_has_all_required_fields(self):
        r = make_provider_response("hello")
        assert r.content == "hello"
        assert r.provider == "mock"
        assert r.model == "mock-model"
        assert r.duration_ms >= 0
        assert r.token_usage.total_tokens == 15


# ---------------------------------------------------------------------------
# 6. AIService — mocked provider
# ---------------------------------------------------------------------------

class TestAIService:
    def test_service_instantiates_with_mock_provider(self):
        service = AIService(provider=MockProvider())
        assert service._provider is not None

    def test_generate_resume_feedback_returns_stub(self):
        service = AIService(provider=MockProvider())
        request = ResumeFeedbackRequest(
            job_description="Backend developer role",
            resume_stats={"match_score": 75.0, "total_matched_skills": 4},
        )
        response = asyncio.get_event_loop().run_until_complete(
            service.generate_resume_feedback(request)
        )
        assert response.overall_feedback  # non-empty stub string
        assert isinstance(response.improvements, list)

    def test_tailor_resume_returns_stub(self):
        service = AIService(provider=MockProvider())
        request = ResumeTailorRequest(
            job_description="Full stack developer",
            resume_stats={"match_score": 60.0},
        )
        response = asyncio.get_event_loop().run_until_complete(
            service.tailor_resume(request)
        )
        assert response.tailored_summary
        assert isinstance(response.tailored_bullet_points, list)

    def test_generate_cover_letter_returns_stub(self):
        service = AIService(provider=MockProvider())
        request = CoverLetterRequest(
            job_description="Engineer at Acme Corp",
            resume_stats={},
        )
        response = asyncio.get_event_loop().run_until_complete(
            service.generate_cover_letter(request)
        )
        assert response.cover_letter

    def test_generate_interview_questions_returns_stub(self):
        service = AIService(provider=MockProvider())
        request = InterviewQuestionsRequest(
            job_description="Senior Python developer",
            resume_stats={},
        )
        response = asyncio.get_event_loop().run_until_complete(
            service.generate_interview_questions(request)
        )
        assert isinstance(response.questions, list)

    def test_provider_exception_propagates(self):
        service = AIService(provider=FailingProvider())
        request = ResumeFeedbackRequest(
            job_description="any",
            resume_stats={},
        )
        with pytest.raises(AIRateLimitError):
            asyncio.get_event_loop().run_until_complete(
                service.generate_resume_feedback(request)
            )

    def test_service_logs_on_success(self, caplog):
        import logging
        service = AIService(provider=MockProvider())
        request = ResumeFeedbackRequest(
            job_description="any",
            resume_stats={},
        )
        with caplog.at_level(logging.INFO, logger="app.services.ai_service"):
            asyncio.get_event_loop().run_until_complete(
                service.generate_resume_feedback(request)
            )
        assert any("ai_operation" in r.message for r in caplog.records)

    def test_service_logs_on_failure(self, caplog):
        import logging
        service = AIService(provider=FailingProvider())
        request = ResumeFeedbackRequest(job_description="any", resume_stats={})
        with caplog.at_level(logging.ERROR, logger="app.services.ai_service"):
            with pytest.raises(AIRateLimitError):
                asyncio.get_event_loop().run_until_complete(
                    service.generate_resume_feedback(request)
                )
        assert any("ai_operation" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# 7. Custom Exception Hierarchy
# ---------------------------------------------------------------------------

class TestExceptions:
    def test_all_exceptions_are_ai_exception_subclasses(self):
        for exc_class in [
            ProviderUnavailableError,
            InvalidAPIKeyError,
            AITimeoutError,
            AIRateLimitError,
            InvalidAIResponseError,
        ]:
            assert issubclass(exc_class, AIException)

    def test_all_exceptions_are_python_exceptions(self):
        for exc_class in [
            AIException,
            ProviderUnavailableError,
            InvalidAPIKeyError,
            AITimeoutError,
            AIRateLimitError,
            InvalidAIResponseError,
        ]:
            assert issubclass(exc_class, Exception)

    def test_raise_and_catch_provider_unavailable(self):
        with pytest.raises(ProviderUnavailableError):
            raise ProviderUnavailableError("Provider is down")

    def test_raise_and_catch_via_base_class(self):
        with pytest.raises(AIException):
            raise AIRateLimitError("Rate limit hit")

    def test_exception_carries_message(self):
        exc = InvalidAPIKeyError("Key is wrong")
        assert str(exc) == "Key is wrong"
