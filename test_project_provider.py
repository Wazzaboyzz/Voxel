#!/usr/bin/env python3
"""
test_project_provider.py - minimal smoke test for project_provider.py.

Uses a real temp directory (no mocking needed - this module only does
local file I/O, no network/API calls) to prove build_project_record() and
build_lesson_project_record() each produce the schema their respective
callers (build_book.py, make_lesson.py) depend on, and that
write_project_json() / read_project_json() round-trip correctly.

Run:
    pip install pytest --break-system-packages
    python -m pytest test_project_provider.py -v
"""

from pathlib import Path

import project_provider


def _sample_pages():
    return [
        {"page_number": 1, "text": "Once upon a time.", "image_prompt": "a small dragon"},
        {"page_number": 2, "text": "The end.", "image_prompt": "a sunset"},
    ]


def _sample_slides():
    return [
        {"title": "Intro", "narration": "Welcome.", "mood": "calm", "image_prompt": "a classroom"},
        {"title": "Recap", "narration": "Goodbye.", "mood": "upbeat", "image_prompt": "a sunset"},
    ]


def test_build_project_record_schema():
    pages = _sample_pages()
    image_files = [Path("images/page_001.png"), None]
    record = project_provider.build_project_record(
        concept="test concept",
        product_type="illustrated_book",
        trim_width_in=8.5,
        trim_height_in=8.5,
        paper="white",
        pages=pages,
        image_files=image_files,
        interior_path=Path("out_interior.pdf"),
        cover_path=Path("out_cover.pdf"),
        run_dir=Path("output_books/test_concept"),
    )

    assert record["schema_version"] == 1
    assert record["concept"] == "test concept"
    assert record["product_type"] == "illustrated_book"
    assert record["page_count"] == 2
    assert record["trim"] == {"width_in": 8.5, "height_in": 8.5}
    assert record["paper"] == "white"
    assert len(record["pages"]) == 2
    assert record["pages"][0]["image_file"] == "images/page_001.png"
    assert record["pages"][1]["image_file"] is None
    assert record["outputs"]["interior_pdf"] == "out_interior.pdf"
    assert record["outputs"]["cover_pdf"] == "out_cover.pdf"
    assert "generated_at" in record


def test_write_and_read_project_json(tmp_path):
    pages = _sample_pages()
    record = project_provider.build_project_record(
        concept="roundtrip test",
        product_type="illustrated_book",
        trim_width_in=6.0,
        trim_height_in=9.0,
        paper="cream",
        pages=pages,
        image_files=[None, None],
        interior_path=None,
        cover_path=None,
        run_dir=tmp_path,
    )
    written_path = project_provider.write_project_json(record, tmp_path)

    assert written_path == tmp_path / "project.json"
    assert written_path.exists()

    read_back = project_provider.read_project_json(tmp_path)
    assert read_back["concept"] == "roundtrip test"
    assert read_back["page_count"] == 2


def test_build_lesson_project_record_schema():
    slides = _sample_slides()
    record = project_provider.build_lesson_project_record(
        topic="test topic",
        slides=slides,
        image_files=[Path("images/slide_01.png"), None],
        deck_path=Path("test_topic.pptx"),
        narration_files=[Path("narration/slide_01.wav"), None],
        bg_files=[None, Path("background/slide_02.mp3")],
        mixed_files=[Path("mixed/slide_01.mp3"), None],
        run_dir=Path("output/test_topic"),
    )

    assert record["schema_version"] == 1
    assert record["concept"] == "test topic"
    assert record["product_type"] == "lesson_deck"
    assert record["slide_count"] == 2
    assert record["audio_embedded_in_pptx"] is False
    assert record["outputs"]["deck_pptx"] == "test_topic.pptx"

    slide0 = record["slides"][0]
    assert slide0["slide_number"] == 1
    assert slide0["title"] == "Intro"
    assert slide0["image_file"] == "images/slide_01.png"
    assert slide0["narration_file"] == "narration/slide_01.wav"
    assert slide0["background_file"] is None
    assert slide0["mixed_audio_file"] == "mixed/slide_01.mp3"

    slide1 = record["slides"][1]
    assert slide1["image_file"] is None
    assert slide1["background_file"] == "background/slide_02.mp3"


def test_lesson_record_write_and_read(tmp_path):
    slides = _sample_slides()
    record = project_provider.build_lesson_project_record(
        topic="roundtrip lesson",
        slides=slides,
        image_files=[None, None],
        deck_path=tmp_path / "deck.pptx",
        narration_files=[None, None],
        bg_files=[None, None],
        mixed_files=[None, None],
        run_dir=tmp_path,
    )
    written_path = project_provider.write_project_json(record, tmp_path)

    assert written_path.exists()
    read_back = project_provider.read_project_json(tmp_path)
    assert read_back["concept"] == "roundtrip lesson"
    assert read_back["product_type"] == "lesson_deck"
    assert read_back["slide_count"] == 2


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
