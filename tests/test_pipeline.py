import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pipeline import run_tool


def test_run_tool_outputs_candidate():
    payload = {
        "seed_url": "https://brandx.com",
        "market": "United States",
        "competitor": "BrandX",
        "keywords": ["crm"],
    }
    results = run_tool(payload)
    assert isinstance(results, list)
    assert results
    first = results[0]
    assert first["domain"] == "brandx-markets.com"
    assert first["match_score"] > 0
