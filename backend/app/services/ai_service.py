import logging
import time
import uuid
from typing import Any, Dict

from app.core.exceptions import AIException
from app.providers.base_provider import BaseAIProvider
from app.providers.provider_factory import ProviderFactory
from app.schemas.ai import (
    ResumeFeedbackRequest,
    ResumeFeedbackResponse,
    ResumeTailorRequest,
    ResumeTailorResponse,
    CoverLetterRequest,
    CoverLetterResponse,
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
)
from app.utils.prompt_manager import PromptManager
from app.utils.response_parser import ResponseParser

logger = logging.getLogger(__name__)


def _log_operation(
    *,
    operation: str,
    provider: str,
    model: str,
    request_id: str,
    duration_ms: int,
    success: bool,
    error: str | None = None,
) -> None:
    """
    Emits a single structured log line for every AI operation.
    Fields are explicit and do not contain prompts, resume text, job descriptions,
    API keys, or any personally identifiable information.
    """
    log_record: Dict[str, Any] = {
        "event": "ai_operation",
        "operation": operation,
        "provider": provider,
        "model": model,
        "request_id": request_id,
        "duration_ms": duration_ms,
        "success": success,
    }
    if error:
        log_record["error"] = error

    if success:
        logger.info(log_record)
    else:
        logger.error(log_record)


class AIService:
    """
    Provider-agnostic AI service.

    Responsibilities:
      - Accept structured ATS request models as input.
      - Delegate prompt loading to PromptManager.
      - Delegate generation to an injected BaseAIProvider.
      - Emit structured operational logs.
      - Return provider-independent response models.

    This service is intentionally decoupled from the deterministic ATS engine.
    The engine produces structured JSON; this service consumes it.
    """

    def __init__(self, provider: BaseAIProvider | None = None) -> None:
        self._provider: BaseAIProvider = provider or ProviderFactory.get_provider()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _call_provider(self, operation: str, prompt: str) -> str:
        """
        Executes a prompt against the injected provider and returns raw content.
        Handles timing, logging, and exception normalisation.
        """
        request_id = str(uuid.uuid4())
        start = time.monotonic()
        success = True
        error_msg: str | None = None

        try:
            response = await self._provider.generate(prompt)
            return response.content
        except AIException as exc:
            success = False
            error_msg = type(exc).__name__
            raise
        finally:
            duration_ms = int((time.monotonic() - start) * 1000)
            _log_operation(
                operation=operation,
                provider=self._provider.__class__.__name__,
                model=getattr(self._provider, "model", "unknown"),
                request_id=request_id,
                duration_ms=duration_ms,
                success=success,
                error=error_msg,
            )

    # ------------------------------------------------------------------
    # Public interface — infrastructure stubs
    # ------------------------------------------------------------------

    async def generate_resume_feedback(
        self, request: ResumeFeedbackRequest
    ) -> ResumeFeedbackResponse:
        """
        Loads the feedback prompt, delegates generation, and returns validated output.
        """
        prompt = PromptManager.get_prompt("resume_feedback", "v1")
        # Milestone 3: format prompt with request.resume_stats / request.job_description
        content = await self._call_provider("generate_resume_feedback", prompt)
        return ResponseParser.parse_resume_feedback(content)

    async def tailor_resume(
        self, request: ResumeTailorRequest
    ) -> ResumeTailorResponse:
        """Stub."""
        prompt = PromptManager.get_prompt("tailor_resume", "v1")
        _ = await self._call_provider("tailor_resume", prompt)
        return ResumeTailorResponse(
            tailored_summary="[Stub] Summary will be generated in Milestone 4.",
            tailored_bullet_points=[],
        )

    async def generate_cover_letter(
        self, request: CoverLetterRequest
    ) -> CoverLetterResponse:
        """Stub."""
        prompt = PromptManager.get_prompt("cover_letter", "v1")
        _ = await self._call_provider("generate_cover_letter", prompt)
        return CoverLetterResponse(
            cover_letter="[Stub] Cover letter will be generated in Milestone 5."
        )

    async def generate_interview_questions(
        self, request: InterviewQuestionsRequest
    ) -> InterviewQuestionsResponse:
        """Stub."""
        prompt = PromptManager.get_prompt("interview_questions", "v1")
        _ = await self._call_provider("generate_interview_questions", prompt)
        return InterviewQuestionsResponse(questions=[])


# Module-level singleton, using the default provider from settings.
# Tests should instantiate AIService(provider=MockProvider()) directly.
ai_service = AIService()
