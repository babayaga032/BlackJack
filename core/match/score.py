"""Scoring logic for candidate matches."""

from __future__ import annotations

from config import WEIGHTS


def base_score(signals: dict) -> int:
    """Compute deterministic base score from signal presence."""
    s = 0
    if signals.get("gtm"):
        s += WEIGHTS["gtm"]
    if signals.get("ga"):
        s += WEIGHTS["ga"]
    if signals.get("pixel"):
        s += WEIGHTS["pixel"]
    if signals.get("favicon_mmh3_equal"):
        s += WEIGHTS["favicon"]
    if signals.get("asset_overlap"):
        s += WEIGHTS["assets"]
    if signals.get("ns_match"):
        s += WEIGHTS["ns"]
    if signals.get("ip_asn_match"):
        s += WEIGHTS["ip_asn"]
    if signals.get("footer_phrase_match"):
        s += WEIGHTS["footer"]
    if signals.get("ssl_san_match"):
        s += WEIGHTS["ssl_san"]

    # Guardrail: network-only signals cannot exceed 35
    if s > 35 and not any(
        [
            signals.get("gtm"),
            signals.get("ga"),
            signals.get("pixel"),
            signals.get("favicon_mmh3_equal"),
            signals.get("asset_overlap"),
        ]
    ):
        s = 35
    return min(s, 100)
