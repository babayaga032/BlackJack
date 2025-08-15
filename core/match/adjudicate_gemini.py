"""Gemini-assisted adjudication and clustering of candidates."""

from __future__ import annotations


def adjudicate(candidates: list[dict]) -> list[dict]:
    """Placeholder for Gemini adjudication."""
    return [{"domain": c.get("domain"), "score_adjustment": 0, "keep": True} for c in candidates]
