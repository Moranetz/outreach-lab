"""Thin wrapper around the Anthropic Claude API."""

from __future__ import annotations

import os
import sys

try:
    import anthropic
except ImportError:  # pragma: no cover
    anthropic = None  # type: ignore


# Default to Sonnet 4.6 for speed/cost; Opus 4.7 for the resume-tailor pass.
MODEL_FAST = "claude-sonnet-4-6"
MODEL_DEEP = "claude-opus-4-7"


def _client() -> anthropic.Anthropic:
    if anthropic is None:
        sys.exit(
            "[outreach-lab] anthropic SDK not installed. Run: pip install anthropic"
        )
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit(
            "[outreach-lab] ANTHROPIC_API_KEY not set. "
            "export ANTHROPIC_API_KEY=sk-ant-..."
        )
    return anthropic.Anthropic(api_key=key)


def complete(
    system: str,
    user: str,
    *,
    model: str = MODEL_FAST,
    max_tokens: int = 4096,
) -> str:
    """Single-shot completion. Returns the text of the first content block."""
    client = _client()
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    return "".join(parts).strip()
