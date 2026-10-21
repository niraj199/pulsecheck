"""AWS Lambda entry point for the PulseCheck website checker.

This is a thin adapter: it decides which URLs to check, calls the tested
check_url() function, and logs the results. All checking logic lives in
checker.py.
"""

import json
import logging
import os

from checker import check_url

MAX_URLS_PER_RUN = 10

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


def get_target_urls(event):
    """Use URLs from the invoke event if given, otherwise from TARGET_URLS."""
    urls = None
    if isinstance(event, dict):
        urls = event.get("urls")
    if not urls:
        urls = os.environ.get("TARGET_URLS", "").split(",")
    cleaned = [u.strip() for u in urls if isinstance(u, str) and u.strip()]
    return cleaned[:MAX_URLS_PER_RUN]


def lambda_handler(event, context):
    urls = get_target_urls(event)
    results = [check_url(url) for url in urls]

    for result in results:
        logger.info(json.dumps(result))

    up = sum(1 for r in results if r["status"] == "UP")
    summary = {"checked": len(results), "up": up, "down": len(results) - up}
    logger.info(json.dumps({"summary": summary}))

    return {**summary, "results": results}
