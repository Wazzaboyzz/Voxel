#!/usr/bin/env python3
"""
story_bible.py - character/continuity bible for Voxel series and picture
books, stored as one JSON file per series/book under story_bibles/.

Idea borrowed from bookframes' "style bible + character reference before
final export" step. No code copied — original implementation.

A bible answers four questions before any new content is generated:
  1. Who/what must look or sound the same as last time? (characters, style)
  2. What has already happened? (plot facts, so a sequel doesn't contradict)
  3. What's the visual reference (image path/description) to keep art
     consistent across pages/books?
  4. Is there an actual reference IMAGE FILE (not just text) that image
     generation should be conditioned on? (added Phase 8f, 2026-09-13 -
     see reference_image_path below. Text descriptions alone were not
     enough to stop the robot's design from changing page to page.)
"""

import json
import os

BIBLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "story_bibles")


def _path(series_slug):
    os.makedirs(BIBLE_DIR, exist_ok=True)
    return os.path.join(BIBLE_DIR, f"{series_slug}.json")


def load(series_slug):
    p = _path(series_slug)
    if not os.path.exists(p):
        return {
            "series_slug": series_slug,
            "characters": {},
            "visual_style": "",
            "plot_facts": [],
            "books": [],
            "reference_image_path": None,
        }
    with open(p, "r") as f:
        bible = json.load(f)
    bible.setdefault("reference_image_path", None)
    return bible


def save(series_slug, bible):
    with open(_path(series_slug), "w") as f:
        json.dump(bible, f, indent=2)


def register_book(series_slug, title, summary, new_plot_facts=None):
    bible = load(series_slug)
    bible["books"].append({"title": title, "summary": summary})
    if new_plot_facts:
        bible["plot_facts"].extend(new_plot_facts)
    save(series_slug, bible)
    return bible


def continuity_prompt_block(series_slug):
    """
    Renders the bible into a text block to prepend to any generation prompt
    (manuscript or image) so a sequel/new page/chapter stays consistent
    with what came before. Returns "" if no bible exists yet (first book
    in the series) so the prompt is unaffected.
    """
    bible = load(series_slug)
    if not bible["books"] and not bible["characters"]:
        return ""

    lines = ["CONTINUITY — must stay consistent with:"]
    if bible["visual_style"]:
        lines.append(f"Visual style: {bible['visual_style']}")
    for name, desc in bible["characters"].items():
        lines.append(f"Character '{name}': {desc}")
    if bible["plot_facts"]:
        lines.append("Established plot facts:")
        for fact in bible["plot_facts"]:
            lines.append(f"  - {fact}")
    if bible["books"]:
        lines.append("Prior books in this series:")
        for b in bible["books"]:
            lines.append(f"  - {b['title']}: {b['summary']}")
    return "\n".join(lines)


def set_characters(series_slug, characters_dict):
    bible = load(series_slug)
    bible["characters"].update(characters_dict)
    save(series_slug, bible)
    return bible


def set_visual_style(series_slug, style_text):
    bible = load(series_slug)
    bible["visual_style"] = style_text
    save(series_slug, bible)
    return bible


def set_reference_image(series_slug, image_path):
    """
    Records the path (relative to the repo root, e.g.
    output_books/<name>/images/page_001.png) of the actual generated image
    that should be used as a visual anchor for every future image call in
    this series/book - not just a text description. See image_provider.py's
    generate_all_images(): page 1 (or a dedicated character-sheet prompt)
    is generated first, then this path is fed back into every subsequent
    Gemini call as an actual image input so the model is editing/matching
    a real reference instead of re-imagining the character from text alone.
    """
    bible = load(series_slug)
    bible["reference_image_path"] = str(image_path)
    save(series_slug, bible)
    return bible


def get_reference_image(series_slug):
    return load(series_slug).get("reference_image_path")
