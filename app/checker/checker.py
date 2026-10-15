"""Core website-checking logic for PulseCheck.

This module has no AWS dependencies, so it can be tested on any machine.
"""

import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse

DEFAULT_TIMEOUT_SECONDS = 5
MAX_URL_LENGTH = 2048
USER_AGENT = "PulseCheck/0.1 (+https://github.com/niraj199/pulsecheck)"


def validate_url(url):
    """Return an error message if the URL is not acceptable, otherwise None."""
    if not isinstance(url, str) or not url.strip():
        return "URL must be a non-empty string"
    if len(url) > MAX_URL_LENGTH:
        return f"URL must be at most {MAX_URL_LENGTH} characters"
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return "URL must start with http:// or https://"
    if not parsed.hostname:
        return "URL must include a hostname"
    return None


def check_url(url, timeout=DEFAULT_TIMEOUT_SECONDS):
    """Check one website and return a result dictionary.

    The result always has the same keys, whether the site is up or down,
    so the code that stores results never has to guess what it will get.
    """
    result = {
        "url": url,
        "status": "DOWN",
        "status_code": None,
        "response_time_ms": None,
        "error": None,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    error = validate_url(url)
    if error:
        result["error"] = error
        return result

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result["status_code"] = response.status
            if 200 <= response.status < 400:
                result["status"] = "UP"
            else:
                result["error"] = f"Unexpected status {response.status}"
    except urllib.error.HTTPError as exc:
        # The server answered, but with an error code such as 404 or 500.
        result["status_code"] = exc.code
        result["error"] = f"HTTP error {exc.code}"
    except TimeoutError:
        result["error"] = f"Timed out after {timeout} seconds"
    except urllib.error.URLError as exc:
        # No usable answer: bad domain, refused connection, SSL problem, etc.
        if isinstance(exc.reason, TimeoutError):
            result["error"] = f"Timed out after {timeout} seconds"
        else:
            result["error"] = f"Connection failed: {exc.reason}"
    finally:
        elapsed_seconds = time.perf_counter() - start
        result["response_time_ms"] = round(elapsed_seconds * 1000)

    return result


if __name__ == "__main__":
    # Lets you try it by hand: python app/checker/checker.py https://example.com
    import json
    import sys

    for target in sys.argv[1:] or ["https://example.com"]:
        print(json.dumps(check_url(target), indent=2))