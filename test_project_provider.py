#!/usr/bin/env python3
"""
test_project_provider.py - minimal smoke test for project_provider.py.

Uses a real temp directory (no mocking needed - this module only does
local file I/O, no network/API calls) to prove build_project_record()
produces the schema build_book.py depends on, and that
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


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))
