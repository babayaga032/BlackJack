"""Merge candidate domains from multiple discovery sources."""

from __future__ import annotations


def merge_candidates(sources: list[list[dict]]) -> list[dict]:
    """Merge lists of candidate dictionaries, de-duplicating by domain."""
    merged: dict[str, dict] = {}
    for source in sources:
        for cand in source:
            domain = cand.get("domain")
            if not domain:
                continue
            if domain not in merged:
                merged[domain] = {**cand}
            else:
                existing = merged[domain]
                # Merge signal dictionaries
                signals = existing.setdefault("signals", {})
                for k, v in cand.get("signals", {}).items():
                    if isinstance(v, list):
                        signals.setdefault(k, []).extend(v)
                    else:
                        signals[k] = v or signals.get(k)
                # Merge evidence URLs
                existing.setdefault("evidence_urls", [])
                existing["evidence_urls"].extend(cand.get("evidence_urls", []))
    # Deduplicate evidence URLs and list-based signals
    for cand in merged.values():
        if "evidence_urls" in cand:
            cand["evidence_urls"] = sorted(set(cand["evidence_urls"]))
        signals = cand.get("signals", {})
        for key, value in list(signals.items()):
            if isinstance(value, list):
                signals[key] = sorted(set(value))
    return list(merged.values())
