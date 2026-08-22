#!/usr/bin/env python3
"""
project_provider.py - single shared entry point for writing the canonical
project.json manifest for a Voxel run. Phase 2 of ARCHITECTURE.md.

Every build script calls the record builder matching its product type,
then write_project_json(), at the end of a run, so every output folder
is self-describing: what was asked for, what was produced, and where
every file landed. This is NOT a database and NOT an orchestrator - it's
a flat, human-readable record of one finished run, written once, after
the run succeeds.

Two product types, two record builders, one shared writer:
  - build_project_record()        -> illustrated books / coloring books
                                      (build_book.py)
  - build_lesson_project_record() -> narrated lesson decks (make_lesson.py)
"""

import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_JSON_VERSION = 1


def build_project_record(
    concept,
    product_type,
    trim_width_in,
    trim_height_in,
    paper,
    pages,
    image_files,
    interior_path,
    cover_path,
    run_dir,
):
    """
    Assembles the canonical record for one finished book run. Takes plain
    values already available at the end of build_book.main() - no new
    generation, no side effects, just structuring what already happened.
    """
    return {
        "schema_version": PROJECT_JSON_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "concept": concept,
        "product_type": product_type,
        "trim": {"width_in": trim_width_in, "height_in": trim_height_in},
        "paper": paper,
        "page_count": len(pages),
        "pages": [
            {
                "page_number": page.get("page_number", i + 1),
                "text": page.get("text", ""),
                "image_prompt": page.get("image_prompt", ""),
                "image_file": str(image_files[i]) if i < len(image_files) and image_files[i] else None,
            }
            for i, page in enumerate(pages)
        ],
        "outputs": {
            "interior_pdf": str(interior_path) if interior_path else None,
            "cover_pdf": str(cover_path) if cover_path else None,
        },
        "run_dir": str(run_dir),
    }


def build_lesson_project_record(
    topic,
    slides,
    image_files,
    deck_path,
    narration_files,
    bg_files,
    mixed_files,
    run_dir,
):
    """
    Assembles the canonical record for one finished lesson-deck run. Takes
    plain values already available at the end of make_lesson.main() - no
    new generation, no side effects, just structuring what already happened.

    Audio isn't embedded in the .pptx yet (python-pptx limitation - see
    HANDOFF.md), so mixed_files are recorded here as the manual-insert
    list for whoever opens the deck next.
    """
    def _str_or_none(value):
        return str(value) if value else None

    return {
        "schema_version": PROJECT_JSON_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "concept": topic,
        "product_type": "lesson_deck",
        "slide_count": len(slides),
        "slides": [
            {
                "slide_number": i + 1,
                "title": slide.get("title", ""),
                "narration": slide.get("narration", ""),
                "mood": slide.get("mood", ""),
                "image_prompt": slide.get("image_prompt", ""),
                "image_file": _str_or_none(image_files[i]) if i < len(image_files) else None,
                "narration_file": _str_or_none(narration_files[i]) if i < len(narration_files) else None,
                "background_file": _str_or_none(bg_files[i]) if i < len(bg_files) else None,
                "mixed_audio_file": _str_or_none(mixed_files[i]) if i < len(mixed_files) else None,
            }
            for i, slide in enumerate(slides)
        ],
        "outputs": {
            "deck_pptx": _str_or_none(deck_path),
        },
        "audio_embedded_in_pptx": False,
        "run_dir": str(run_dir),
    }


def write_project_json(record, run_dir):
    """
    Writes the record to <run_dir>/project.json. Returns the Path written.
    Shared by both product types - the record shape differs, the write
    step doesn't.
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(run_dir) / "project.json"
    out_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return out_path


def read_project_json(run_dir):
    """
    Reads back <run_dir>/project.json. Raises FileNotFoundError if the run
    never completed (no project.json was written).
    """
    path = Path(run_dir) / "project.json"
    return json.loads(path.read_text(encoding="utf-8"))
