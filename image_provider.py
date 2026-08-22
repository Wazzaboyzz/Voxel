#!/usr/bin/env python3
"""
image_provider.py - single shared entry point for image generation across
Voxel, wrapping Pollinations.ai (free, no key). Both make_lesson.py and
build_book.py call this instead of each having their own copy.

Phase 3 of ARCHITECTURE.md: first real provider abstraction.
"""

import time
import urllib.parse
from pathlib import Path

import requests


POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/"

LESSON_STYLE_SUFFIX = (
    ", flat 2D illustration with strong dimensional shading and depth, "
    "clean vector style, soft gradients, educational and friendly, "
    "no text, no watermark"
)

BOOK_STYLE_SUFFIX = (
    ", flat 2D illustration with dimensional shading, clean vector style, "
    "warm colors, children's book art, no text, no watermark"
)

COLORING_BOOK_STYLE_SUFFIX = (
    ", clean black and white line art, simple bold outlines, no shading, "
    "coloring book style, no text, no watermark"
)


def generate_image(prompt, out_path, width=1024, height=576, seed=None,
                    style_suffix=LESSON_STYLE_SUFFIX):
    """
    Calls Pollinations.ai's free text-to-image endpoint. No API key needed.
    style_suffix controls the visual style appended to every prompt - pick
    LESSON_STYLE_SUFFIX, BOOK_STYLE_SUFFIX, or COLORING_BOOK_STYLE_SUFFIX,
    or pass a custom one.
    """
    full_prompt = prompt + style_suffix
    encoded_prompt = urllib.parse.quote(full_prompt)

    url = f"{POLLINATIONS_IMAGE_URL}{encoded_prompt}"
    params = {"width": width, "height": height, "nologo": "true"}
    if seed is not None:
        params["seed"] = seed

    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)


def generate_all_images(items, image_dir, filename_prefix="item", seed_base=42,
                         width=1024, height=576, style_suffix=LESSON_STYLE_SUFFIX,
                         prompt_key="image_prompt", number_key=None, polite_delay=1):
    """
    Generates one image per item in `items` (a list of dicts, e.g. slides or
    pages). `prompt_key` is the dict key holding the image prompt.
    `number_key` (optional, e.g. "page_number") controls the output filename
    number; otherwise items are numbered by their position in the list.
    Returns a list of Path (or None on failure) matching `items` order.
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
        except requests.RequestException as e:
            print(f"  [warn] Image generation failed for {filename_prefix} {number}: {e}")
            image_files.append(None)

        if polite_delay:
            time.sleep(polite_delay)

    return image_files
