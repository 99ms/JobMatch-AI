# AI Architecture — JobMatch AI

This document describes the AI infrastructure introduced in **Milestone 2.75**. No user-facing AI generation exists yet. This layer exists solely to prepare the application for clean, maintainable, provider-independent AI integration in Milestone 3 and beyond.

---

## Design Rationale

### Why the ATS engine remains the source of truth

The deterministic ATS engine (`analysis_service.py`) produces structured, auditable results: match scores, matched skills per category, missing skills, section mappings, and points breakdowns. This output is:

- **Reproducible** — the same inputs always produce the same outputs.
- **Explainable** — every number has a traceable cause.
- **Fast** — no network call required.
- **Zero-cost** — no tokens consumed.

The AI layer augments this structured output. It never replaces it. An LLM is never asked to calculate scores, detect skills, or parse resumes. Instead, it receives a structured `Dict` from the ATS engine and is asked to generate human-readable text from it.

This separation means:
- The ATS engine can be tested, versioned, and validated independently.
- AI quality can be improved by updating prompts without touching core logic.
- Providers can be swapped without touching business logic.

---

## Directory Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          ← centralised settings (pydantic-settings)
│   │   ├── exceptions.py      ← typed AI exception hierarchy
│   │   └── skills.json
│   ├── providers/
│   │   ├── base_provider.py   ← abstract interface all providers implement
│   │   ├── openai_provider.py ← stubbed OpenAI implementation
│   │   └── provider_factory.py ← instantiates the correct provider from settings
│   ├── schemas/
│   │   ├── ai.py              ← ProviderResponse, TokenUsage, operation request/response models
│   │   └── resume.py          ← ATS response schemas (unchanged)
│   ├── services/
│   │   ├── ai_service.py      ← async AI service (provider injection, structured logging)
│   │   ├── analysis_service.py
│   │   ├── section_service.py
│   │   └── pdf_service.py
│   └── utils/
│       ├── prompt_manager.py  ← versioned prompt loader
│       └── token_utils.py     ← lightweight token estimation
├── prompts/
│   ├── resume_feedback_v1.txt
│   ├── tailor_resume_v1.txt
│   ├── cover_letter_v1.txt
│   └── interview_questions_v1.txt
└── tests/
    ├── test_ai_infrastructure.py
    ├── test_analysis_service.py
    └── test_section_service.py
```

---

## Components

### 1. Configuration (`app/core/config.py`)

All AI settings are stored in a single `Settings` class built with `pydantic-settings`. Values are loaded from environment variables or `.env`. Nothing is hardcoded.

| Field | Description | Default |
|---|---|---|
| `AI_PROVIDER` | Which provider to use | `"openai"` |
| `OPENAI_API_KEY` | Provider API key (secret) | `None` |
| `AI_MODEL_NAME` | Model to use | `"gpt-4o"` |
| `AI_TEMPERATURE` | Sampling temperature | `0.7` |
| `AI_MAX_TOKENS` | Maximum generation tokens | `1500` |

To add a new provider, add its settings here. No other file needs to change for configuration.

### 2. Exception Hierarchy (`app/core/exceptions.py`)

All AI errors extend a single `AIException` base class, allowing callers to catch broadly or specifically.

```
Exception
└── AIException
    ├── ProviderUnavailableError  — provider is down or unreachable
    ├── InvalidAPIKeyError        — API key rejected
    ├── AITimeoutError            — request timed out
    ├── AIRateLimitError          — rate limit exceeded
    └── InvalidAIResponseError    — malformed provider response
```

### 3. Provider Abstraction (`app/providers/`)

#### `BaseAIProvider` (abstract)

Defines the only contract every provider must fulfil:

```python
async def generate(self, prompt: str) -> ProviderResponse
```

All providers return `ProviderResponse` — a provider-independent Pydantic model. Business logic never sees raw SDK objects.

#### `OpenAIProvider`

Reads model name and API key from `settings`. Currently stubbed. Milestone 3 will replace the stub body with the real SDK call without changing any other file.

#### `ProviderFactory`

Reads `settings.AI_PROVIDER` and returns the correct `BaseAIProvider` instance. To add Anthropic or Ollama, add one `elif` branch here. Nothing else changes.

### 4. Provider Response Models (`app/schemas/ai.py`)

#### `ProviderResponse`
The shared envelope returned by every provider. Fields:

| Field | Type | Description |
|---|---|---|
| `content` | `str` | Generated text |
| `token_usage` | `TokenUsage` | Prompt, completion, and total token counts |
| `provider` | `str` | Name of the provider |
| `model` | `str` | Model used |
| `duration_ms` | `int` | Round-trip latency in milliseconds |

#### Operation Schemas
Each future AI operation has typed request and response models:

| Operation | Request | Response |
|---|---|---|
| Resume Feedback | `ResumeFeedbackRequest` | `ResumeFeedbackResponse` |
| Resume Tailoring | `ResumeTailorRequest` | `ResumeTailorResponse` |
| Cover Letter | `CoverLetterRequest` | `CoverLetterResponse` |
| Interview Questions | `InterviewQuestionsRequest` | `InterviewQuestionsResponse` |

All requests extend `BaseAIRequest`:
```python
class BaseAIRequest(BaseModel):
    job_description: str
    resume_stats: Dict[str, Any]  # Structured ATS output — never raw resume text
```

This enforces the separation boundary at the type level.

### 5. Prompt Management (`app/utils/prompt_manager.py`)

Prompts are stored as plain `.txt` files on disk. They are never embedded in Python source files.

```python
PromptManager.get_prompt("resume_feedback", "v1")
# loads: backend/prompts/resume_feedback_v1.txt
```

**Versioning convention:** `{prompt_name}_{version}.txt`. To ship an improved prompt without breaking existing behaviour, create `resume_feedback_v2.txt` and update the caller to request `"v2"`. Both versions coexist on disk.

### 6. Token Estimation (`app/utils/token_utils.py`)

A lightweight, dependency-free heuristic:

```python
estimated_tokens = int(word_count * 1.3)
```

This is suitable for budget checks before calling an API. It is not a replacement for a tokenizer. When Milestone 3 adds real API calls, prompt size validation can use this utility before dispatching.

### 7. AIService (`app/services/ai_service.py`)

The single entry point for all AI operations.

**Responsibilities:**
- Accept typed `*Request` models as input.
- Load the correct prompt from `PromptManager`.
- Delegate generation to the injected `BaseAIProvider`.
- Emit structured operational logs.
- Return typed `*Response` models.

**What it does NOT do:**
- Parse PDFs.
- Calculate ATS scores.
- Detect skills.
- Handle HTTP requests.
- Return raw strings or SDK objects.

**Structured logging:** Every operation produces exactly one log record containing:

```json
{
  "event": "ai_operation",
  "operation": "generate_resume_feedback",
  "provider": "OpenAIProvider",
  "model": "gpt-4o",
  "request_id": "uuid-v4",
  "duration_ms": 423,
  "success": true
}
```

The following are **never** logged: resume text, job descriptions, prompts, API keys, or any personally identifiable information.

**Provider injection:** The service accepts an optional `provider` in its constructor. The module-level singleton uses `ProviderFactory.get_provider()`. Tests inject `MockProvider` directly, which means tests never touch network or configuration.

---

## Future Extension Points

### Adding a new provider

1. Create `app/providers/anthropic_provider.py` implementing `BaseAIProvider`.
2. Add one `elif` in `ProviderFactory.get_provider()`.
3. Add `ANTHROPIC_API_KEY` to `Settings`.
4. No other file changes required.

### Adding a new operation

1. Add `NewOperationRequest` / `NewOperationResponse` to `app/schemas/ai.py`.
2. Add `new_operation_v1.txt` to `backend/prompts/`.
3. Add `async def new_operation(request: NewOperationRequest)` to `AIService`.
4. Add an endpoint in `app/api/` when ready to expose it.

### Upgrading a prompt

1. Create `resume_feedback_v2.txt` in `backend/prompts/`.
2. Update the `PromptManager.get_prompt("resume_feedback", "v2")` call in `AIService`.
3. `v1` remains on disk for rollback.

### Switching models per operation

Extend `Settings` with per-operation model overrides:

```python
AI_FEEDBACK_MODEL: str = "gpt-4o"
AI_COVER_LETTER_MODEL: str = "gpt-4o-mini"
```

Read the appropriate setting inside each `AIService` method.
