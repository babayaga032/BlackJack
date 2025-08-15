"""Deterministic comparison of seed and candidate signals."""

from __future__ import annotations


def compare_signals(seed_fp: dict, candidate: dict) -> dict:
    """Populate boolean comparison signals for a candidate."""
    signals = candidate.get("signals", {})
    result = {
        "gtm": bool(set(seed_fp.get("gtm_ids", [])) & set(signals.get("gtm", []))),
        "ga": bool(set(seed_fp.get("ga_ids", [])) & set(signals.get("ga", []))),
        "pixel": bool(set(seed_fp.get("fb_pixel_ids", [])) & set(signals.get("pixel", []))),
        "favicon_mmh3_equal": bool(signals.get("favicon_mmh3_equal")),
        "asset_overlap": bool(
            set(seed_fp.get("asset_paths", [])) & set(signals.get("asset_overlap", []))
        ),
        "ns_match": bool(signals.get("ns_match")),
        "ip_asn_match": bool(signals.get("ip_asn_match")),
        "footer_phrase_match": bool(
            set(seed_fp.get("footer_phrases", []))
            & set(signals.get("footer_phrase_match", []))
        ),
        "ssl_san_match": bool(signals.get("ssl_san_match")),
    }
    candidate["signals"] = result
    return candidate
