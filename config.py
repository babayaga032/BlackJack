"""Configuration for API keys and scoring weights.

The real pipeline integrates with a number of third‑party services. The
expected API keys are pulled from environment variables so users can provide
their own credentials when running the tool.
"""

from __future__ import annotations

import os

# Mapping of service name → key/id/secret. Empty strings indicate the key was
# not provided in the environment.
API_KEYS: dict[str, str] = {
    "BING_API_KEY": os.getenv("BING_API_KEY", ""),
    "GOOGLE_CSE_ID": os.getenv("GOOGLE_CSE_ID", ""),
    "GOOGLE_CSE_KEY": os.getenv("GOOGLE_CSE_KEY", ""),
    "SHODAN_API_KEY": os.getenv("SHODAN_API_KEY", ""),
    "CENSYS_API_ID": os.getenv("CENSYS_API_ID", ""),
    "CENSYS_API_SECRET": os.getenv("CENSYS_API_SECRET", ""),
    "SECURITYTRAILS_API_KEY": os.getenv("SECURITYTRAILS_API_KEY", ""),
    "WAPPALYZER_API_KEY": os.getenv("WAPPALYZER_API_KEY", ""),
    "BUILTWITH_API_KEY": os.getenv("BUILTWITH_API_KEY", ""),
    "SIMILARWEB_API_KEY": os.getenv("SIMILARWEB_API_KEY", ""),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
}

# Default deterministic weights mirrored from ``core.match.score``. Users can
# tweak these at runtime if desired.
WEIGHTS: dict[str, int] = {
    "gtm": 40,
    "ga": 40,
    "pixel": 40,
    "favicon": 25,
    "assets": 15,
    "ns": 10,
    "ip_asn": 10,
    "footer": 10,
    "ssl_san": 10,
}

