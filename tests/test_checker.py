"""Automated tests for the PulseCheck website checker.

These tests never touch the real internet. We replace the network call with
fakes so every scenario (up, down, timeout, bad input) is fast and repeatable.
"""

import urllib.error

import pytest

import checker


class FakeResponse:
    """Pretends to be the object urlopen() returns for a successful request."""

    def __init__(self, status):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def returns_status(status):
    def fake_urlopen(request, timeout):
        return FakeResponse(status)
    return fake_urlopen


def raises(exception):
    def fake_urlopen(request, timeout):
        raise exception
    return fake_urlopen


def test_site_that_responds_200_is_up(monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", returns_status(200))

    result = checker.check_url("https://example.com")

    assert result["status"] == "UP"
    assert result["status_code"] == 200
    assert result["error"] is None
    assert result["response_time_ms"] >= 0


@pytest.mark.parametrize("code", [404, 500, 503])
def test_http_error_codes_are_down(monkeypatch, code):
    error = urllib.error.HTTPError(
        "https://example.com", code, "error", hdrs=None, fp=None
    )
    monkeypatch.setattr("urllib.request.urlopen", raises(error))

    result = checker.check_url("https://example.com")

    assert result["status"] == "DOWN"
    assert result["status_code"] == code
    assert str(code) in result["error"]


@pytest.mark.parametrize(
    "exception",
    [TimeoutError("timed out"), urllib.error.URLError(TimeoutError("timed out"))],
)
def test_timeouts_are_down(monkeypatch, exception):
    monkeypatch.setattr("urllib.request.urlopen", raises(exception))

    result = checker.check_url("https://example.com", timeout=3)

    assert result["status"] == "DOWN"
    assert result["error"] == "Timed out after 3 seconds"


def test_unreachable_site_is_down(monkeypatch):
    error = urllib.error.URLError("Name or service not known")
    monkeypatch.setattr("urllib.request.urlopen", raises(error))

    result = checker.check_url("https://no-such-site.invalid")

    assert result["status"] == "DOWN"
    assert result["status_code"] is None
    assert result["error"].startswith("Connection failed")


@pytest.mark.parametrize(
    "bad_url",
    [
        "",
        None,
        "example.com",
        "ftp://example.com",
        "file:///etc/passwd",
        "https://",
        "https://" + "a" * 2050 + ".com",
    ],
)
def test_invalid_urls_are_rejected_without_network_call(monkeypatch, bad_url):
    # If validation fails to stop a bad URL, this fake makes the test fail loudly.
    monkeypatch.setattr(
        "urllib.request.urlopen",
        raises(AssertionError("network should not be called")),
    )

    result = checker.check_url(bad_url)

    assert result["status"] == "DOWN"
    assert result["error"] is not None
    assert result["response_time_ms"] is None