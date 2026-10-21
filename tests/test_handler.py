"""Tests for the Lambda handler. check_url is replaced with a fake,
so these tests never touch the network or AWS."""

import handler


def fake_check(url):
    return {"url": url, "status": "DOWN" if "down" in url else "UP"}


def test_uses_urls_from_event(monkeypatch):
    monkeypatch.setattr(handler, "check_url", fake_check)

    result = handler.lambda_handler({"urls": ["https://a.example", "https://b.example"]}, None)

    assert [r["url"] for r in result["results"]] == ["https://a.example", "https://b.example"]
    assert result["checked"] == 2


def test_falls_back_to_environment_variable(monkeypatch):
    monkeypatch.setattr(handler, "check_url", fake_check)
    monkeypatch.setenv("TARGET_URLS", "https://a.example, https://b.example ,")

    result = handler.lambda_handler({}, None)

    assert [r["url"] for r in result["results"]] == ["https://a.example", "https://b.example"]


def test_counts_up_and_down(monkeypatch):
    monkeypatch.setattr(handler, "check_url", fake_check)

    result = handler.lambda_handler({"urls": ["https://up.example", "https://down.example"]}, None)

    assert result["up"] == 1
    assert result["down"] == 1


def test_caps_number_of_urls(monkeypatch):
    monkeypatch.setattr(handler, "check_url", fake_check)
    many = [f"https://site{i}.example" for i in range(25)]

    result = handler.lambda_handler({"urls": many}, None)

    assert result["checked"] == handler.MAX_URLS_PER_RUN


def test_no_urls_returns_empty_summary(monkeypatch):
    monkeypatch.setattr(handler, "check_url", fake_check)
    monkeypatch.delenv("TARGET_URLS", raising=False)

    result = handler.lambda_handler({}, None)

    assert result == {"checked": 0, "up": 0, "down": 0, "results": []}
