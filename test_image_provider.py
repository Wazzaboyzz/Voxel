#!/usr/bin/env python3
"""
test_image_provider.py - minimal smoke test for image_provider.py.

Mocks the Gemini HTTP call so this runs with no network, no cost, and no
real API key. Proves generate_image() builds the correct request and
generate_all_images() handles a failed item without crashing the whole
batch, so refactors here can't silently break make_lesson.py / build_book.py.

Run:
    pip install pytest requests --break-system-packages
    python -m pytest test_image_provider.py -v
"""

import base64
from pathlib import Path
from unittest.mock import patch, MagicMock

import requests

import image_provider


FAKE_IMAGE_BYTES = b"fake-png-bytes"
FAKE_IMAGE_B64 = base64.b64encode(FAKE_IMAGE_BYTES).decode("ascii")


def _mock_response(image_b64=FAKE_IMAGE_B64, status_ok=True, malformed=False):
    mock_resp = MagicMock()
    if status_ok:
        mock_resp.raise_for_status.return_value = None
    else:
        mock_resp.raise_for_status.side_effect = requests.RequestException("boom")

    if malformed:
        mock_resp.json.return_value = {"candidates": []}
    else:
        mock_resp.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"inlineData": {"mimeType": "image/png", "data": image_b64}}
                        ]
                    }
                }
            ]
        }
    return mock_resp


def test_generate_image_builds_correct_request(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    out_path = tmp_path / "slide_001.png"

    with patch("image_provider.requests.post", return_value=_mock_response()) as mock_post:
        image_provider.generate_image(
            "a red balloon", out_path, width=800, height=450, seed=42,
            style_suffix=image_provider.LESSON_STYLE_SUFFIX,
        )

    assert out_path.exists()
    assert out_path.read_bytes() == FAKE_IMAGE_BYTES

    called_url = mock_post.call_args[0][0]
    called_params = mock_post.call_args[1]["params"]
    called_json = mock_post.call_args[1]["json"]
    assert called_url == image_provider.GEMINI_URL
    assert called_params["key"] == "fake-key"
    expected_prompt = "a red balloon" + image_provider.LESSON_STYLE_SUFFIX
    assert called_json["contents"][0]["parts"][0]["text"] == expected_prompt


def test_generate_image_requires_api_key(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    out_path = tmp_path / "slide_001.png"

    try:
        image_provider.generate_image("a red balloon", out_path)
        assert False, "expected RuntimeError when GEMINI_API_KEY is unset"
    except RuntimeError as e:
        assert "GEMINI_API_KEY" in str(e)


def test_generate_all_images_uses_number_key(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    items = [
        {"page_number": 5, "image_prompt": "a dragon"},
        {"page_number": 6, "image_prompt": "a castle"},
    ]
    with patch("image_provider.requests.post", return_value=_mock_response()):
        with patch("image_provider.time.sleep"):
            files = image_provider.generate_all_images(
                items, tmp_path, filename_prefix="page",
                number_key="page_number", polite_delay=1,
            )

    assert files[0] == tmp_path / "page_005.png"
    assert files[1] == tmp_path / "page_006.png"
    assert files[0].exists() and files[1].exists()


def test_generate_all_images_survives_one_failure(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    good = _mock_response()
    bad = _mock_response(malformed=True)

    with patch("image_provider.requests.post", side_effect=[bad, good]):
        with patch("image_provider.time.sleep"):
            files = image_provider.generate_all_images(
                [{"image_prompt": "a"}, {"image_prompt": "b"}], tmp_path, filename_prefix="slide",
            )

    assert files[0] is None
    assert files[1] == tmp_path / "slide_002.png"
    assert files[1].exists()


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
