"""Tests for the base_score function."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.match.score import base_score


def test_base_score_sums_weights():
    signals = {"gtm": ["GTM-1"], "favicon_mmh3_equal": True}
    assert base_score(signals) == 65


def test_network_only_cap():
    signals = {
        "ns_match": True,
        "ip_asn_match": True,
        "footer_phrase_match": True,
        "ssl_san_match": True,
    }
    assert base_score(signals) == 35


def test_cap_at_100():
    signals = {
        "gtm": True,
        "ga": True,
        "pixel": True,
        "favicon_mmh3_equal": True,
        "asset_overlap": True,
        "ns_match": True,
        "ip_asn_match": True,
        "footer_phrase_match": True,
        "ssl_san_match": True,
    }
    assert base_score(signals) == 100
