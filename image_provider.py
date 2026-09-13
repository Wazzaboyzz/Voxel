#!/usr/bin/env python3
"""
image_provider.py - single shared entry point for image generation across
Voxel, wrapping the Google Gemini image generation API (free tier, daily
quota). Both make_lesson.py and build_book.py call this instead of each
having their own copy.

NOTE (2026-09-13): Gemini's gemini-2.5-flash-image model returns 429 on
every call for a key with no billing linked - confirmed by a real run.
Zia's standing rule is strictly free tier, no billing, anywhere. So the
functions below are NOT the primary image path anymore for build_book.py /
voxel_cli.py - see write_image_prompts_file() and load_manual_images()
below, which support generating images by hand (VEO3, Google Flow, etc.)
instead. generate_image()/generate_all_images() are kept for make_lesson.py
(which hasn't hit this limit) and as a fallback if a genuinely-free Gemini
path or another free provider is wired in later.

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
    Calls Google's Gemini image generation API. Requires GEMINI_API_KEY.
    As of 2026-09-13 this 429s on free-tier keys with no billing linked -
    see the module docstring. Kept for make_lesson.py and as a fallback.
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
    Generates one image per item in `items` via Gemini. See module docstring -
    as of 2026-09-13 this fails with 429 on a no-billing free-tier key.
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
        except (requests.RequestException, RuntimeError) as e:
            print(f"  [warn] Image generation failed for {filename_prefix} {number}: {e}")
            image_files.append(None)

        if polite_delay:
            time.sleep(polite_delay)

    return image_files


def write_image_prompts_file(items, out_path, prompt_key="image_prompt",
                              number_key=None, filename_prefix="item"):
    """
    Writes a markdown file listing one prompt per item, plus the EXACT
    filename each finished image must be saved as. This is step 1 of the
    manual-image workflow: Zia generates each image by hand (VEO3, Google
    Flow, or any other tool) using these prompts, saves each one with the
    exact filename shown, uploads all of them into one folder in the repo,
    then re-runs the build with --images-dir pointed at that folder so
    load_manual_images() below can pick them up. Zero API calls, zero cost.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Image prompts - generate each one by hand (VEO3, Google Flow, etc.)",
        "",
        "For each prompt below: generate the image, save it using the EXACT",
        "filename shown as the heading, then upload every file into one folder",
        "in this repo (e.g. via the GitHub web \"Add file > Upload files\" button).",
        "Once they're all uploaded, re-run the build and pass",
        "--images-dir <that folder's path> so it uses these instead of calling",
        "any image API.",
        "",
    ]
    for i, item in enumerate(items):
        number = item[number_key] if number_key else i + 1
        prompt = item.get(prompt_key, f"{filename_prefix} illustration")
        filename = f"{filename_prefix}_{number:03d}.png"
        lines.append(f"## {filename}")
        lines.append(prompt)
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def load_manual_images(items, image_dir, filename_prefix="item", number_key=None):
    """
    Step 2 of the manual-image workflow: looks for images already sitting in
    image_dir, named exactly as write_image_prompts_file() specified above.
    Makes zero network calls - just checks the filesystem. Returns a list of
    Path (or None if that page's image isn't there yet) matching items'
    order, the same shape generate_all_images() returns, so build_book.py's
    PDF-assembly code works identically either way.
    """
    image_dir = Path(image_dir)
    image_files = []
    for i, item in enumerate(items):
        number = item[number_key] if number_key else i + 1
        candidate = image_dir / f"{filename_prefix}_{number:03d}.png"
        if candidate.exists():
            image_files.append(candidate)
        else:
            print(f"  [warn] No manual image found for {filename_prefix} {number} "
                  f"(expected {candidate})")
            image_files.append(None)
    return image_files
