import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.discover.merge import merge_candidates


def test_merge_deduplicates_signals_and_evidence():
    sources = [
        [
            {
                "domain": "example.com",
                "signals": {"gtm": ["GTM-1"]},
                "evidence_urls": ["https://example.com"],
            }
        ],
        [
            {
                "domain": "example.com",
                "signals": {"gtm": ["GTM-1", "GTM-2"]},
                "evidence_urls": [
                    "https://example.com",
                    "https://example.com/about",
                ],
            }
        ],
    ]

    merged = merge_candidates(sources)
    assert len(merged) == 1
    candidate = merged[0]
    assert candidate["signals"]["gtm"] == ["GTM-1", "GTM-2"]
    assert candidate["evidence_urls"] == [
        "https://example.com",
        "https://example.com/about",
    ]
