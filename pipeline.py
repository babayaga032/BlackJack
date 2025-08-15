"""Pipeline orchestrator entrypoint.

This implementation wires together the placeholder modules in ``core`` so the
project can be executed end‑to‑end without external API calls. It uses static
data to simulate discovery and Gemini steps, allowing unit tests and local runs
to validate the control flow.
"""

from __future__ import annotations

from core.discover.merge import merge_candidates
from core.match.adjudicate_gemini import adjudicate
from core.match.compare import compare_signals
from core.match.score import base_score
from core.match.softmatch_gemini import infer_soft_signals
from core.util.domain import normalize_domain


def _fingerprint(seed_url: str) -> dict:
    """Return a deterministic fingerprint for the provided seed URL."""
    domain = normalize_domain(seed_url)
    return {
        "domain": domain,
        "gtm_ids": ["GTM-XXXX"],
        "ga_ids": ["G-AAAA1111"],
        "fb_pixel_ids": ["1234567890"],
        "other_trackers": ["hotjar-12345"],
        "favicon_mmh3": 123456789,
        "asset_paths": ["/js/core-v2.js", "/assets/brandx/main.css"],
        "footer_phrases": ["© BrandX, Inc."],
        "meta_generator": "Next.js",
        "dns": {"ipv4": ["203.0.113.10"], "asn": "AS15169", "ns": ["ns1.brandxdns.com"]},
        "ssl": {
            "issuer": "Let's Encrypt",
            "sans": [f"{domain}", f"www.{domain}"],
        },
        "evidence": [f"view-source:{domain}", "/favicon.ico"],
    }


def _discovery_stub() -> list[list[dict]]:
    """Return stubbed discovery results for demonstration purposes."""
    candidate = {
        "domain": "brandx-markets.com",
        "signals": {
            "gtm": ["GTM-XXXX"],
            "ga": [],
            "pixel": [],
            "favicon_mmh3_equal": True,
            "asset_overlap": ["/js/core-v2.js"],
            "ns_match": True,
            "ip_asn_match": False,
            "footer_phrase_match": ["© BrandX, Inc."],
            "ssl_san_match": False,
        },
        "evidence_urls": ["https://brandx-markets.com"],
    }
    return [[candidate]]  # a list-of-lists as expected by merge_candidates


def run_tool(payload: dict) -> list[dict]:
    """Execute the placeholder pipeline and return sorted candidate matches."""

    seed_url = payload.get("seed_url", "")
    if not seed_url:
        raise ValueError("payload must include 'seed_url'")

    seed_fp = _fingerprint(seed_url)
    discovery = _discovery_stub()
    candidates = merge_candidates(discovery)

    compared = [compare_signals(seed_fp, c) for c in candidates]
    for c in compared:
        c["match_score"] = base_score(c["signals"])

    compared = infer_soft_signals(seed_fp, compared)

    prelim = [c for c in compared if c["match_score"] >= 35]
    decisions = adjudicate(prelim)

    final: list[dict] = []
    for c in prelim:
        d = next((x for x in decisions if x["domain"] == c["domain"]), None)
        if not d:
            continue
        c["match_score"] = max(0, min(100, c["match_score"] + d.get("score_adjustment", 0)))
        if d.get("keep") and c["match_score"] >= 40:
            final.append(c)

    return sorted(final, key=lambda x: x["match_score"], reverse=True)[:200]

