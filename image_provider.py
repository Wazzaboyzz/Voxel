#!/usr/bin/env python3
"""
image_provider.py - single shared entry point for image generation across
Voxel. Tries Google Gemini first (with retry/backoff on rate limits), then
falls back to Cloudflare Workers AI (FLUX, free tier) only as a last
resort - both make_lesson.py and build_book.py call this instead of each
having their own copy or their own fallback logic.

Phase 8f (2026-09-13) - fixes two real problems found on the first
Cloudflare-fallback run (sock-collecting robot book):
  1. STYLE MISMATCH: pages that fell back to Cloudflare's FLUX-schnell
     came back flat/2D/uncolored, visually nothing like the Gemini pages
     around them. Fix: Gemini now retries with exponential backoff (3
     attempts) before ever falling back, since a 429 is a rate limit, not
     a hard quota-exceeded - most pages should now stay on Gemini and
     never need the fallback at all. Any page that still falls back is
     now loudly flagged (console + a _fallback_report.json manifest next
     to the images) instead of silently shipping a mismatched page.
  2. NO CHARACTER CONSISTENCY: every page was generated from a fresh text
     prompt with zero shared visual state, so the robot looked different
     every single page. Fix: the FIRST successful image in a run is now
     kept as a real reference image and fed back into Gemini (which
     accepts image input, not just text) on every later call in the same
     run, with an explicit instruction to match the reference exactly and
     only change the pose/scene. If story_bible.set_reference_image() was
     already called for this series (a prior book), that image is used
     as the starting reference instead, so a sequel's character matches
     the original too.

UPDATE (2026-09-13, Phase 8e): Gemini's gemini-2.5-flash-image model can
429 on a key with no billing linked. Cloudflare Workers AI's FLUX model is
used as a last-resort fallback - CLOUDFLARE_ACCOUNT_ID and
CLOUDFLARE_API_TOKEN are already configured as repo secrets. Both are
genuinely free tier, matching Zia's standing "strictly free tier, no
billing, anywhere" rule.

The manual-image workflow (write_image_prompts_file() / load_manual_images(),
Phase 8d) is kept as a fallback-of-the-fallback for the rare case where
both Gemini (after retries) and Cloudflare fail.

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

GEMINI_RETRY_DELAYS = [15, 30, 60]  # seconds, before giving up and trying Cloudflare

REFERENCE_MATCH_INSTRUCTION = (
    "IMPORTANT: The attached reference image shows this exact character. "
    "Keep the character's design, proportions, colors, and materials "
    "IDENTICAL to the reference image. Only change the pose, action, and "
    "surrounding scene as described below. Do not redesign the character."
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


def _image_to_inline_part(image_path):
    data = Path(image_path).read_bytes()
    mime = "image/png" if str(image_path).lower().endswith(".png") else "image/jpeg"
    return {"inlineData": {"mimeType": mime, "data": base64.b64encode(data).decode("ascii")}}


def _try_gemini_once(full_prompt, out_path, reference_image_path=None):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return False, "GEMINI_API_KEY not set", None

    parts = []
    if reference_image_path and Path(reference_image_path).exists():
        parts.append(_image_to_inline_part(reference_image_path))
        parts.append({"text": REFERENCE_MATCH_INSTRUCTION + "\n\n" + full_prompt})
    else:
        parts.append({"text": full_prompt})

    body = {"contents": [{"parts": parts}]}
    try:
        resp = requests.post(GEMINI_URL, params={"key": key}, json=body, timeout=90)
        if resp.status_code == 429:
            return False, "429 rate limited", 429
        resp.raise_for_status()
        data = resp.json()
        response_parts = data["candidates"][0]["content"]["parts"]
        for part in response_parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(base64.b64decode(inline["data"]))
                return True, None, None
        return False, f"No image data in Gemini response: {data}", None
    except (requests.RequestException, KeyError, IndexError) as e:
        return False, str(e), None


def _try_gemini_with_retries(full_prompt, out_path, reference_image_path=None):
    last_err = None
    for attempt, delay in enumerate([0] + GEMINI_RETRY_DELAYS):
        if delay:
            print(f"    [gemini rate limited, retrying in {delay}s (attempt {attempt + 1})]")
            time.sleep(delay)
        ok, err, code = _try_gemini_once(full_prompt, out_path, reference_image_path)
        if ok:
            return True, None
        last_err = err
        if code != 429:
            # a non-rate-limit failure won't be fixed by waiting - stop retrying Gemini
            break
    return False, last_err


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
                    style_suffix=LESSON_STYLE_SUFFIX, reference_image_path=None):
    """
    Tries Gemini first (with retry/backoff on 429s), then Cloudflare
    Workers AI (FLUX) only if Gemini still fails after retries. Returns
    (used_fallback: bool) on success via return value is not given here -
    see generate_all_images() for the fallback-tracking wrapper used by
    callers that need to know which pages need a manual look.

    reference_image_path, if given and Gemini is used, is attached as an
    actual image input so the model matches that character exactly rather
    than reinventing it from text alone. Has no effect on the Cloudflare
    path (FLUX-schnell via this simple endpoint has no image-conditioning
    input) - a page that falls back to Cloudflare should be treated as
    needing a manual consistency check, which is why it's flagged.
    """
    full_prompt = prompt + style_suffix

    ok, err = _try_gemini_with_retries(full_prompt, out_path, reference_image_path)
    if ok:
        return False  # used_fallback = False

    print(f"    [gemini failed after retries ({err}), trying Cloudflare fallback - "
          f"NOTE: this page will NOT match the character reference]")

    ok, err = _try_cloudflare(full_prompt, out_path)
    if ok:
        return True  # used_fallback = True

    raise RuntimeError(f"All image providers failed. Last error: {err}")


def generate_all_images(items, image_dir, filename_prefix="item", seed_base=42,
                         width=1024, height=576, style_suffix=LESSON_STYLE_SUFFIX,
                         prompt_key="image_prompt", number_key=None, polite_delay=2,
                         reference_image_path=None):
    """
    Generates one image per item in `items`. The first successful image in
    the run becomes the running reference for every image after it (unless
    reference_image_path is already supplied, e.g. from a prior book in
    the same series via story_bible.get_reference_image()), so the same
    character design carries through the whole book instead of being
    reinvented per page.

    Returns a list of Path (or None on total failure for that item),
    matching `items` order - same shape as before, so build_book.py's
    PDF assembly is unaffected. Also writes `_fallback_report.json` in
    image_dir listing any page numbers that had to use the Cloudflare
    fallback (and therefore may not match the reference character) -
    check this file after any run before treating the book as done.
    """
    image_dir.mkdir(parents=True, exist_ok=True)
    image_files = []
    fallback_pages = []
    running_reference = reference_image_path

    for i, item in enumerate(items):
        number = item[number_key] if number_key else i + 1
        prompt = item.get(prompt_key, f"{filename_prefix} illustration")
        out_path = image_dir / f"{filename_prefix}_{number:03d}.png"

        try:
            print(f"  Generating image for {filename_prefix} {number}: {prompt}")
            used_fallback = generate_image(
                prompt, out_path, width=width, height=height,
                seed=seed_base + number, style_suffix=style_suffix,
                reference_image_path=running_reference,
            )
            image_files.append(out_path)
            if used_fallback:
                fallback_pages.append(number)
            elif running_reference is None:
                # first successful Gemini image becomes the reference for
                # every page after it
                running_reference = out_path
                print(f"    -> set as character reference for remaining pages")
        except (requests.RequestException, RuntimeError) as e:
            print(f"  [warn] Image generation failed for {filename_prefix} {number}: {e}")
            image_files.append(None)

        if polite_delay:
            time.sleep(polite_delay)

    if fallback_pages:
        report_path = image_dir / "_fallback_report.json"
        import json
        report_path.write_text(json.dumps({
            "pages_using_cloudflare_fallback": fallback_pages,
            "note": ("These pages could not use the Gemini character reference and "
                     "may not match the rest of the book's character design. "
                     "Check them by eye; consider regenerating manually if they "
                     "don't match."),
        }, indent=2), encoding="utf-8")
        print(f"\n  [!] {len(fallback_pages)} page(s) used the Cloudflare fallback "
              f"and may not match the character reference: {fallback_pages}")
        print(f"      See {report_path} for details.")

    return image_files


def write_image_prompts_file(items, out_path, prompt_key="image_prompt",
                              number_key=None, filename_prefix="item"):
    """
    Manual-image fallback (Phase 8d), kept for the rare case both Gemini
    (after retries) and Cloudflare fail. Writes a markdown file listing
    one prompt per item, plus the EXACT filename each finished image must
    be saved as.
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
