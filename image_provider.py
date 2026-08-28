#!/usr/bin/env python3
"""
image_provider.py - single shared entry point for image generation across
Voxel, wrapping the Google Gemini image generation API (free tier, daily
quota, no cost). Both make_lesson.py and build_book.py call this instead of
each having their own copy.

Requires a free Gemini API key from https://aistudio.google.com/apikey,
passed via the GEMINI_API_KEY environment variable.
"""

import base64
import os
import time
from pathlib import Path

import requests


GEMINI_IMAGE_MODEL = "gemini-2.5-flash-image"
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_IMAGE_MODEL}:generateContent"
)

LESSON_STYLE_SUFFIX = (
    ", rich three-dimensional painterly illustration with strong depth, "
    "layered foreground midground background, volumetric lighting, "
    "clean dimensional shading, educational and friendly, "
    "no text, no watermark, no lettering, no captions"
)

BOOK_STYLE_SUFFIX = (
    ", rich three-dimensional painterly children's book illustration with "
    "strong depth, layered foreground midground background, volumetric "
    "lighting, warm gentle colors, dimensional soft-shaded characters, "
    "no text, no watermark, no lettering, no captions"
)

COLORING_BOOK_STYLE_SUFFIX = (
    ", clean black and white line art, simple bold outlines, no shading, "
    "coloring book style, no text, no watermark"
)


def _get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. Get a free key "
            "at https://aistudio.google.com/apikey and set it before calling "
            "generate_image()."
        )
    return key


def generate_image(prompt, out_path, width=1024, height=576, seed=None,
                    style_suffix=LESSON_STYLE_SUFFIX):
    """
    Calls Google's Gemini image generation API (free tier, daily quota).
    Requires GEMINI_API_KEY to be set in the environment.
    style_suffix controls the visual style appended to every prompt - pick
    LESSON_STYLE_SUFFIX, BOOK_STYLE_SUFFIX, or COLORING_BOOK_STYLE_SUFFIX,
    or pass a custom one.
    """
    api_key = _get_api_key()
    full_prompt = prompt + style_suffix

    body = {
        "contents": [
            {"parts": [{"text": full_prompt}]}
        ]
    }

    resp = requests.post(
        GEMINI_URL,
        params={"key": api_key},
        json=body,
        timeout=90,
    )
    resp.raise_for_status()
    data = resp.json()

    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Gemini response shape: {data}") from e

    image_b64 = None
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            image_b64 = inline["data"]
            break

    if image_b64 is None:
        raise RuntimeError(f"No image data returned by Gemini: {data}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(image_b64))


def generate_all_images(items, image_dir, filename_prefix="item", seed_base=42,
                         width=1024, height=576, style_suffix=LESSON_STYLE_SUFFIX,
                         prompt_key="image_prompt", number_key=None, polite_delay=2):
    """
    Generates one image per item in `items` (a list of dicts, e.g. slides or
    pages). `prompt_key` is the dict key holding the image prompt.
    `number_key` (optional, e.g. "page_number") controls the output filename
    number; otherwise items are numbered by their position in the list.
    Returns a list of Path (or None on failure) matching `items` order.
    `polite_delay` defaults to 2s to stay comfortably under Gemini's free
    daily rate limit.
    """
    image_dir.mkdir(parents=True, exist_ok=True)
    image_files = []

    for i, item in enumerate(items):
        number = item[number_key] if number_key else i + 1
        prompt = item.get(prompt_key, f"{filename_prefix} illustration")
        out_path = image_dir / f"{filename_prefix}_{number:03d}.png"

        try:
            print(f"  Generating image for {filename_prefix} {number}: {prompt}")
            generate_image(
                prompt, out_path, width=width, height=height,
                seed=seed_base + number, style_suffix=style_suffix,
            )
            image_files.append(out_path)
        except (requests.RequestException, RuntimeError) as e:
            print(f"  [warn] Image generation failed for {filename_prefix} {number}: {e}")
            image_files.append(None)

        if polite_delay:
            time.sleep(polite_delay)

    return image_files
