#!/usr/bin/env python3
"""
image_provider.py - single shared entry point for image generation across
Voxel. Tries Google Gemini first, then automatically falls back to
Cloudflare Workers AI (FLUX, free tier) if Gemini fails - both
make_lesson.py and build_book.py call this instead of each having their
own copy or their own fallback logic.

UPDATE (2026-09-13, Phase 8e): Gemini's gemini-2.5-flash-image model
returns 429 on every call for a key with no billing linked (confirmed by
a real run). Rather than requiring manual image generation (VEO3, Google
Flow) for every book, generate_image() now automatically falls back to
Cloudflare Workers AI's FLUX model when Gemini fails - CLOUDFLARE_ACCOUNT_ID
and CLOUDFLARE_API_TOKEN are already configured as repo secrets (added
for the disconnected generate_images.py GitHub Actions script, now reused
here) and Cloudflare Workers AI has a genuinely free tier, matching Zia's
standing "strictly free tier, no billing, anywhere" rule.

The manual-image workflow (write_image_prompts_file() / load_manual_images(),
Phase 8d) is kept as a fallback-of-the-fallback for the rare case where
both Gemini and Cloudflare fail - --manual-images / --images-dir on
voxel_cli.py book still work exactly as before.

Requires at least one of:
  GEMINI_API_KEY                          - free key, https://aistudio.google.com/apikey
  CLOUDFLARE_ACCOUNT_ID + CLOUDFLARE_API_TOKEN  - free tier, Workers AI
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

CLOUDFLARE_FLUX_MODEL = "@cf/black-forest-labs/flux-1-schnell"

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


def _try_gemini(full_prompt, out_path):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return False, "GEMINI_API_KEY not set"

    body = {"contents": [{"parts": [{"text": full_prompt}]}]}
    try:
        resp = requests.post(GEMINI_URL, params={"key": key}, json=body, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(base64.b64decode(inline["data"]))
                return True, None
        return False, f"No image data in Gemini response: {data}"
    except (requests.RequestException, KeyError, IndexError) as e:
        return False, str(e)


def _try_cloudflare(full_prompt, out_path):
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not account_id or not token:
        return False, "CLOUDFLARE_ACCOUNT_ID/CLOUDFLARE_API_TOKEN not set"

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{CLOUDFLARE_FLUX_MODEL}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.post(url, headers=headers, json={"prompt": full_prompt}, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        img_b64 = data["result"]["image"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(img_b64))
        return True, None
    except (requests.RequestException, KeyError) as e:
        return False, str(e)


def generate_image(prompt, out_path, width=1024, height=576, seed=None,
                    style_suffix=LESSON_STYLE_SUFFIX):
    """
    Tries Gemini first, then Cloudflare Workers AI (FLUX) if Gemini fails.
    Both are free-tier, no billing required. Raises RuntimeError only if
    every configured provider fails, so callers (generate_all_images) can
    still catch a single exception type the way they always have.
    """
    full_prompt = prompt + style_suffix

    ok, err = _try_gemini(full_prompt, out_path)
    if ok:
        return
    print(f"    [gemini failed, trying Cloudflare fallback] {err}")

    ok, err = _try_cloudflare(full_prompt, out_path)
    if ok:
        return

    raise RuntimeError(f"All image providers failed. Gemini/Cloudflare last error: {err}")


def generate_all_images(items, image_dir, filename_prefix="item", seed_base=42,
                         width=1024, height=576, style_suffix=LESSON_STYLE_SUFFIX,
                         prompt_key="image_prompt", number_key=None, polite_delay=2):
    """
    Generates one image per item in `items`, trying Gemini then Cloudflare
    per item (see generate_image()). Returns a list of Path (or None on
    total failure for that item) matching `items` order.
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
    Manual-image fallback (Phase 8d), kept for the rare case both Gemini
    and Cloudflare fail. Writes a markdown file listing one prompt per
    item, plus the EXACT filename each finished image must be saved as.
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
    Manual-image fallback (Phase 8d): looks for images already sitting in
    image_dir, named exactly as write_image_prompts_file() specified.
    Zero network calls. Returns a list of Path (or None) matching items'
    order, the same shape generate_all_images() returns.
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
