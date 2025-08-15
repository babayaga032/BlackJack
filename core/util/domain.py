"""Domain utilities for parsing and normalization.

This module will host helpers for public suffix parsing and other domain-related
logic used across the pipeline.
"""

from __future__ import annotations

from urllib.parse import urlparse


def normalize_domain(url: str) -> str:
    """Return a lowercase netloc for the given URL or domain string."""
    parsed = urlparse(url)
    host = parsed.netloc or parsed.path
    return host.strip().lower()
