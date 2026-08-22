#!/usr/bin/env python3
"""
project_provider.py - single shared entry point for writing the canonical
project.json manifest for a Voxel run. Phase 2 of ARCHITECTURE.md.

Every build script (build_book.py today, make_lesson.py later if it adopts
the same pattern) calls build_project_record() then write_project_json()
at the end of a run, so every output folder is self-describing: what was
asked for, what was produced, and where every file landed. This is NOT a
database and NOT an orchestrator - it's a flat, human-readable record of
one finished run, written once, after the run succeeds.
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
    Assembles the canonical record for one finished run. Takes plain
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


def write_project_json(record, run_dir):
    """
    Writes the record to <run_dir>/project.json. Returns the Path written.
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
