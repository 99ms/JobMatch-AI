import json
from typing import Any

from pydantic import ValidationError

from app.core.exceptions import AIOutputValidationError
from app.schemas.ai import ResumeFeedbackResponse


class ResponseParser:
    """Parses provider text into validated, provider-independent AI response models."""

    @staticmethod
    def parse_resume_feedback(content: str) -> ResumeFeedbackResponse:
        """Parse and validate a ResumeFeedbackResponse JSON object from provider text."""
        if not content or not content.strip():
            raise AIOutputValidationError("Resume feedback response is empty.")

        try:
            payload: Any = json.loads(content)
        except json.JSONDecodeError as exc:
            raise AIOutputValidationError(
                f"Resume feedback response is not valid JSON: {exc.msg}."
            ) from exc

        if not isinstance(payload, dict):
            raise AIOutputValidationError(
                "Resume feedback response must be a JSON object."
            )

        try:
            return ResumeFeedbackResponse.model_validate(payload)
        except ValidationError as exc:
            errors = exc.errors(include_url=False)
            raise AIOutputValidationError(
                f"Resume feedback response failed schema validation: {errors}"
            ) from exc
