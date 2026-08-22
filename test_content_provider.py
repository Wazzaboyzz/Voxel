#!/usr/bin/env python3
"""
test_content_provider.py - minimal smoke test for content_provider.py.

Mocks the OpenRouter HTTP call so this runs with no API key, no network,
no cost. Proves generate_outline() and generate_manuscript() still return
the schema make_lesson.py / build_book.py depend on, so refactors in
content_provider.py can't silently break both callers.

Run:
    pip install pytest --break-system-packages
    OPENROUTER_API_KEY=dummy python -m pytest test_content_provider.py -v
"""

import os
import json
from unittest.mock import patch, MagicMock

os.environ.setdefault("OPENROUTER_API_KEY", "dummy-key-for-tests")

import content_provider


def _mock_response(payload):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {
        "choices": [{"message": {"content": json.dumps(payload)}}]
    }
    return mock_resp


def test_generate_outline_schema():
    fake_slides = [
        {
            "title": "Intro",
            "body": ["point one", "point two"],
            "narration": "Welcome to the lesson.",
            "mood": "calm focused",
            "image_prompt": "a classroom with a chalkboard",
        }
    ]
    with patch("content_provider.requests.post", return_value=_mock_response(fake_slides)):
        slides = content_provider.generate_outline("test topic")

    assert isinstance(slides, list)
    assert len(slides) == 1
    slide = slides[0]
    for key in ("title", "body", "narration", "mood", "image_prompt"):
        assert key in slide


def test_generate_manuscript_schema():
    fake_pages = [
        {"page_number": 1, "text": "Once upon a time.", "image_prompt": "a small dragon in a forest"}
    ]
    with patch("content_provider.requests.post", return_value=_mock_response(fake_pages)):
        pages = content_provider.generate_manuscript("test concept", page_count=1)

    assert isinstance(pages, list)
    assert len(pages) == 1
    page = pages[0]
    for key in ("page_number", "text", "image_prompt"):
        assert key in page


def test_missing_api_key_raises():
    old_key = content_provider.OPENROUTER_API_KEY
    content_provider.OPENROUTER_API_KEY = ""
    try:
        try:
            content_provider.generate_outline("test topic")
            assert False, "expected RuntimeError when API key is missing"
        except RuntimeError as e:
            assert "OPENROUTER_API_KEY" in str(e)
    finally:
        content_provider.OPENROUTER_API_KEY = old_key


def test_strips_markdown_fences():
    fake_pages = [{"page_number": 1, "text": "", "image_prompt": "a red balloon"}]
    fenced = "```json\n" + json.dumps(fake_pages) + "\n```"
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {"choices": [{"message": {"content": fenced}}]}

    with patch("content_provider.requests.post", return_value=mock_resp):
        pages = content_provider.generate_manuscript("test concept", page_count=1)

    assert pages == fake_pages


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
