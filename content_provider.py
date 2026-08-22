#!/usr/bin/env python3
"""
content_provider.py - single shared entry point for all Nemotron/OpenRouter
content generation across Voxel. Every script that needs an outline (slide
deck) or a manuscript (page-by-page book) calls into this module instead of
rolling its own HTTP call + JSON parsing.

This is Phase 1 of ARCHITECTURE.md: removing duplicated content-generation
code from make_lesson.py, build_book.py, and generate_images.py.
"""

import os
import json

import requests


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
NEMOTRON_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _call_nemotron(system_prompt, user_content, timeout=120):
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Export it before running:\n"
            "  export OPENROUTER_API_KEY=your_key_here"
        )

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": NEMOTRON_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    raw_text = data["choices"][0]["message"]["content"].strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Nemotron did not return valid JSON. Raw response was:\n{raw_text}"
        ) from e


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


def generate_manuscript(concept, page_count):
    """
    Page-by-page book manuscript for build_book.py.
    Returns a list of page dicts: page_number, text, image_prompt.
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
        "image_prompt should illustrate that page's specific moment."
    )
    return _call_nemotron(
        system_prompt, f"Book concept: {concept}", timeout=180
    )
