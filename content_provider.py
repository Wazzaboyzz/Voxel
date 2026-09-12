#!/usr/bin/env python3
"""
content_provider.py - single shared entry point for all LLM-based content
generation across Voxel. Every script that needs an outline (slide deck),
a manuscript (page-by-page book), or a novel chapter calls into this
module instead of rolling its own HTTP call + JSON parsing.

This is Phase 1 of ARCHITECTURE.md: removing duplicated content-generation
code from make_lesson.py, build_book.py, and generate_images.py.

Phase 8 addendum (one-command publishing pipeline, see HANDOFF.md):
added generate_novel_chapter() and call_raw() for prose-chapter generation
(novels aren't a fixed-field JSON list like picture-book pages), used by
voxel_cli.py and humanizer.py.

Phase 8b addendum: added direct NVIDIA API support as an alternative to
OpenRouter. If NVIDIA_API_KEY is set, it's used (direct NVIDIA NIM
endpoint, no OpenRouter middleman/rate limits). Otherwise falls back to
OPENROUTER_API_KEY exactly as before - existing workflows/notebooks that
only set OPENROUTER_API_KEY keep working unchanged.
"""

import os
import json

import requests


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

# Direct NVIDIA NIM endpoint (build.nvidia.com), OpenAI-compatible.
# NVIDIA_MODEL can be overridden via env var if this default is renamed/
# retired - check https://build.nvidia.com for the current model catalog
# and matching model id if generation starts failing with a 404.
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct")


def _active_provider():
    """NVIDIA direct takes priority when its key is present, since it's a
    paid/direct key with no OpenRouter free-tier rate limits."""
    if NVIDIA_API_KEY:
        return NVIDIA_URL, NVIDIA_MODEL, NVIDIA_API_KEY
    if OPENROUTER_API_KEY:
        return OPENROUTER_URL, OPENROUTER_MODEL, OPENROUTER_API_KEY
    return None, None, None


def _require_key():
    if not NVIDIA_API_KEY and not OPENROUTER_API_KEY:
        raise RuntimeError(
            "No LLM API key is set. Export ONE of these before running:\n"
            "  export NVIDIA_API_KEY=your_key_here      (direct, no rate limit)\n"
            "  export OPENROUTER_API_KEY=your_key_here  (free tier, rate limited)"
        )


def _post(system_prompt, user_content, timeout):
    _require_key()
    url, model, key = _active_provider()
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _call_nemotron(system_prompt, user_content, timeout=120):
    raw_text = _post(system_prompt, user_content, timeout)

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Model did not return valid JSON. Raw response was:\n{raw_text}"
        ) from e


def call_raw(system_prompt, user_content, timeout=120):
    """
    Plain-text (non-JSON) LLM call. Exposed for humanizer.rewrite_pass and
    generate_novel_chapter, which need free-form prose back, not a JSON
    object.
    """
    return _post(system_prompt, user_content, timeout)


def generate_outline(topic):
    """
    Slide-deck outline for make_lesson.py / generate_images.py.
    Returns a list of slide dicts: title, body, narration, mood, image_prompt.
    """
    system_prompt = (
        "You are a lesson-deck writer. Given a topic, produce a JSON array "
        "of 6-10 slide objects for a classroom teaching deck. Return ONLY "
        "valid JSON, no markdown fences, no preamble. Each object must have "
        "exactly these keys:\n"
        '  "title": short slide title (few words)\n'
        '  "body": array of 2-5 short bullet point strings for the slide\n'
        '  "narration": 1-3 sentences the teacher/narrator would say aloud '
        "for this slide, plain spoken language\n"
        '  "mood": one or two words describing the background music mood '
        '(e.g. "calm focused", "upbeat playful", "serious neutral")\n'
        '  "image_prompt": a short visual description (5-15 words) of what '
        "should be illustrated for this slide, concrete and specific, "
        "no abstract concepts - describe an actual scene or object\n"
        "The first slide should be a title/intro slide. The last slide should "
        "be a short recap/summary slide."
    )
    return _call_nemotron(system_prompt, f"Topic: {topic}")


def generate_manuscript(concept, page_count, continuity_block=""):
    """
    Page-by-page book manuscript for build_book.py.
    Returns a list of page dicts: page_number, text, image_prompt.

    continuity_block: optional text from story_bible.continuity_prompt_block()
    to keep a sequel's characters/style/plot consistent with prior books.
    """
    system_prompt = (
        f"You are a children's book author and illustrator's art director. "
        f"Given a book concept, produce a JSON array of exactly {page_count} "
        f"page objects. Return ONLY valid JSON, no markdown fences, no "
        f"preamble. Each object must have exactly these keys:\n"
        '  "page_number": integer, 1-indexed\n'
        '  "text": the text for this page (can be an empty string for '
        "pages meant to be pure illustration, e.g. coloring book pages)\n"
        '  "image_prompt": a concrete, specific visual description '
        "(10-25 words) of the illustration for this page - describe an "
        "actual scene, character pose, or object, not an abstract idea\n"
        "If the concept describes a coloring book, text should be empty "
        "or a very short caption, and image_prompt should describe a "
        "clean line-art scene suitable for coloring. If it's a story, "
        "text should carry the narrative forward page by page and "
        "image_prompt should illustrate that page's specific moment. "
        "Avoid AI-writing tells: no rule-of-three lists, no stock phrases, "
        "vary sentence length naturally, write like a human author."
    )
    user_content = f"Book concept: {concept}"
    if continuity_block:
        user_content = f"{continuity_block}\n\n{user_content}"
    return _call_nemotron(system_prompt, user_content, timeout=180)


def generate_novel_chapter(chapter_number, chapter_brief, continuity_block=""):
    """
    One prose chapter for a novel-length work (e.g. Amity Falls series).
    Unlike generate_manuscript, this returns plain prose text, not JSON,
    since a novel chapter isn't a fixed-field list.
    """
    system_prompt = (
        "You are a novelist continuing an existing series. Write chapter "
        f"{chapter_number} in full prose, matching the tone and voice of "
        "the existing chapters. Write the actual chapter text, several "
        "pages long - do not summarize. Do not include a chapter title "
        "header unless the brief asks for one. Avoid AI-writing tells: no "
        "rule-of-three lists, no stock phrases like 'a testament to' or "
        "'in the tapestry of', vary sentence length naturally, no em-dash "
        "overuse."
    )
    user_content = f"Chapter {chapter_number} brief:\n{chapter_brief}"
    if continuity_block:
        user_content = f"{continuity_block}\n\n{user_content}"
    return call_raw(system_prompt, user_content, timeout=240)
