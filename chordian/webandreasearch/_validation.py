"""Web & Research request validation."""

from typing import FrozenSet

_VALID_LLM_MODELS: FrozenSet[str] = frozenset(
    {
        "chordian-r1",
        "gpt-5.4 mini",
        "gemini 3 flash",
        "claude sonnet 4.6",
        "claude opus 4.6",
        "claude opus 4.7",
        "qwen3.5:cloud",
    }
)


def require_web_and_research_llm_model(llm_model: str) -> str:
    """Return a validated LLM model label."""
    if not isinstance(llm_model, str):
        raise ValueError("llm_model must be a string")
    stripped = llm_model.strip()
    if not stripped:
        raise ValueError("llm_model must not be empty")
    if stripped not in _VALID_LLM_MODELS:
        allowed = ", ".join(sorted(_VALID_LLM_MODELS))
        raise ValueError(f"llm_model must be one of: {allowed}; got {stripped!r}")
    return stripped
