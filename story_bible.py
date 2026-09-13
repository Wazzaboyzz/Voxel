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

Phase 9 addendum (2026-09-13): beat maps. "Where the Frost Doesn't Reach"
(Amity Falls Book 1) was written chapter-by-chapter BY HAND, not through
this pipeline, and what actually made that novel work — a per-chapter
beat map, locked checkpoint chapters, per-character voice profiles, a
hard word-count band, and a zero-em-dash rule — was never ported into
voxel_cli.py's `novel` command. `generate_novel_chapter()` was calling
the LLM with nothing but a one-line brief. This addendum is that missing
piece: a BEAT MAP is a book-scoped (not series-scoped) JSON file under
story_bibles/beatmaps/<series_slug>__<book_slug>.json, applying ONLY to
novel-chapter generation (per PROJECT_ISOLATION_RULES.md rule 3 — never
picture-book pages). Schema:

{
  "series_slug": "amity-falls",
  "book_slug": "amity-falls-book-2",
  "word_count_floor": 1800,
  "word_count_ceiling": 2500,
  "zero_em_dash": true,
  "voice_profiles": {
    "Mara": "dry, controlled, engineering-metaphor",
    "Caleb": "steady, plainspoken, dry humor sideways"
  },
  "checkpoint_chapters": {
    "30": "first kiss - do not move",
    "34": "rupture - do not move"
  },
  "chapters": {
    "1": "one-line beat for this specific chapter, e.g. funeral reunion",
    "2": "..."
  }
}

Zia is browser-only, so this file is uploaded by hand via GitHub's web
"Add file > Upload files" (or Create new file) into story_bibles/beatmaps/
before running `voxel_cli.py novel --beat-map <that path>`. Nothing in
this pipeline invents a beat map on its own, same as it never invents a
concept/brief.
"""

import json
import os
import re

BIBLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "story_bibles")
BEATMAP_DIR = os.path.join(BIBLE_DIR, "beatmaps")


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


# --- Phase 9: beat maps (novel-chapter generation ONLY, see module ---------
# --- docstring and PROJECT_ISOLATION_RULES.md rule 3) ----------------------

def _beatmap_path(series_slug, book_slug):
    os.makedirs(BEATMAP_DIR, exist_ok=True)
    return os.path.join(BEATMAP_DIR, f"{series_slug}__{book_slug}.json")


def load_beat_map(series_slug, book_slug):
    """Returns the beat map dict, or None if it hasn't been uploaded yet.
    Never raises - a missing beat map is treated as 'not using one', which
    falls back to the old brief-only behavior so this stays backward
    compatible with a novel that genuinely doesn't have one prepared."""
    p = _beatmap_path(series_slug, book_slug)
    if not os.path.exists(p):
        return None
    with open(p, "r") as f:
        return json.load(f)


def save_beat_map(series_slug, book_slug, data):
    data.setdefault("series_slug", series_slug)
    data.setdefault("book_slug", book_slug)
    with open(_beatmap_path(series_slug, book_slug), "w") as f:
        json.dump(data, f, indent=2)
    return data


def beat_prompt_block(beat_map, chapter_number):
    """
    Renders the per-chapter beat, voice profiles, checkpoint warning, and
    style rules (word-count band, zero-em-dash) into one text block to
    prepend to generate_novel_chapter()'s prompt for THIS chapter. Returns
    "" if beat_map is None.
    """
    if not beat_map:
        return ""

    lines = ["NOVEL BEAT MAP — this chapter's specific requirements:"]

    beat = beat_map.get("chapters", {}).get(str(chapter_number))
    if beat:
        lines.append(f"This chapter's beat (must hit, do not invent a different plot event): {beat}")

    checkpoint = beat_map.get("checkpoint_chapters", {}).get(str(chapter_number))
    if checkpoint:
        lines.append(
            f"CHECKPOINT CHAPTER - this is a locked structural beat ({checkpoint}). "
            "Do not shift, delay, or soften this event."
        )

    voice_profiles = beat_map.get("voice_profiles") or {}
    if voice_profiles:
        lines.append("Match each character's established voice exactly:")
        for name, desc in voice_profiles.items():
            lines.append(f"  - {name}: {desc}")

    floor = beat_map.get("word_count_floor")
    ceiling = beat_map.get("word_count_ceiling")
    if floor and ceiling:
        lines.append(f"Target length: {floor}-{ceiling} words for this chapter.")

    if beat_map.get("zero_em_dash"):
        lines.append("HARD RULE: zero em dashes (—) anywhere in this chapter's prose.")

    return "\n".join(lines)


def check_chapter(text, beat_map):
    """
    Post-generation verification against the beat map's hard rules -
    mirrors the manual checks Zia's earlier chapter-by-chapter sessions
    ran by hand (word count + em-dash count) before calling a chapter
    done. Returns a dict of {word_count, em_dash_count, floor, ceiling,
    below_floor, above_ceiling, em_dash_violation} — does not modify the
    text; a violation is a flag for the caller to act on, never a silent
    rewrite (same integrity-first spirit as humanizer.py's fact gate).
    """
    word_count = len(text.split())
    em_dash_count = text.count("\u2014")  # —
    floor = (beat_map or {}).get("word_count_floor")
    ceiling = (beat_map or {}).get("word_count_ceiling")
    return {
        "word_count": word_count,
        "em_dash_count": em_dash_count,
        "floor": floor,
        "ceiling": ceiling,
        "below_floor": bool(floor) and word_count < floor,
        "above_ceiling": bool(ceiling) and word_count > ceiling,
        "em_dash_violation": bool((beat_map or {}).get("zero_em_dash")) and em_dash_count > 0,
    }
