#!/usr/bin/env python3
"""
generate_images.py - generates a 2D stylized illustration per slide using
Pollinations.ai (free, no API key required for basic text-to-image).

This is a standalone step that pairs with make_lesson.py. It reads the same
slide JSON structure (title, body, narration, mood) and produces one image
per slide, saved into the run's output folder.

Usage:
    python generate_images.py "Present perfect tense for intermediate ESL students"

This re-generates the outline via Nemotron (same as make_lesson.py) so it
can run independently, or be wired to reuse an already-saved outline later.

Required local tools:
    pip install requests --break-system-packages

Required environment variable:
    OPENROUTER_API_KEY   - for regenerating the outline (same key as make_lesson.py)

No key required for Pollinations basic image generation.
"""

import os
import sys
import json
import time
import urllib.parse
from pathlib import Path

import requests


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
NEMOTRON_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/"

OUTPUT_DIR = Path("output")

# Style suffix appended to every image prompt to keep a consistent
# "stylized 2D, dimensional-looking" look across all slides in a deck.
STYLE_SUFFIX = (
    ", flat 2D illustration with strong dimensional shading and depth, "
    "clean vector style, soft gradients, educational and friendly, "
    "no text, no watermark"
)


def generate_outline(topic):
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Export it before running:\n"
            "  export OPENROUTER_API_KEY=your_key_here"
        )

    system_prompt = (
        "You are a lesson-deck writer. Given a topic, produce a JSON array "
        "of 6-10 slide objects for a classroom teaching deck. Return ONLY "
        "valid JSON, no markdown fences, no preamble. Each object must have "
        "exactly these keys:\n"
        '  "title": short slide title (few words)\n'
        '  "body": array of 2-5 short bullet point strings for the slide\n'
        '  "narration": 1-3 sentences the teacher/narrator would say aloud '
        "for this slide, plain spoken language\n"
        '  "mood": one or two words describing the background music mood\n'
        '  "image_prompt": a short visual description (5-15 words) of what '
        "should be illustrated for this slide, concrete and specific, "
        "no abstract concepts - describe an actual scene or object"
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
                {"role": "user", "content": f"Topic: {topic}"},
            ],
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    raw_text = data["choices"][0]["message"]["content"].strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    slides = json.loads(raw_text)
    return slides


def generate_image(prompt, out_path, width=1024, height=576, seed=None):
    """
    Calls Pollinations.ai's free text-to-image endpoint. No API key needed
    for this basic path. Adds a fixed seed per call if given, so repeated
    runs with the same prompt can be reproduced if useful later.
    """
    full_prompt = prompt + STYLE_SUFFIX
    encoded_prompt = urllib.parse.quote(full_prompt)

    url = f"{POLLINATIONS_IMAGE_URL}{encoded_prompt}"
    params = {"width": width, "height": height, "nologo": "true"}
    if seed is not None:
        params["seed"] = seed

    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)


def generate_all_images(slides, image_dir, seed_base=42):
    image_dir.mkdir(parents=True, exist_ok=True)
    image_files = []

    for i, slide_data in enumerate(slides):
        prompt = slide_data.get("image_prompt", slide_data.get("title", "classroom illustration"))
        out_path = image_dir / f"slide_{i+1:02d}.png"

        try:
            print(f"  Generating image for slide {i+1}: {prompt}")
            generate_image(prompt, out_path, seed=seed_base + i)
            image_files.append(out_path)
        except requests.RequestException as e:
            print(f"  [warn] Image generation failed for slide {i+1}: {e}")
            image_files.append(None)

        # Be polite to the free service - small delay between requests
        time.sleep(1)

    return image_files


def main():
    if len(sys.argv) < 2:
        print('Usage: python generate_images.py "Your lesson topic here"')
        sys.exit(1)

    topic = " ".join(sys.argv[1:])
    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in topic).strip().replace(" ", "_")[:60]
    run_dir = OUTPUT_DIR / safe_name

    print(f"Generating lesson outline for: {topic}")
    slides = generate_outline(topic)
    print(f"  -> {len(slides)} slides planned")

    print("Generating images (Pollinations.ai, free, no key required)...")
    image_files = generate_all_images(slides, run_dir / "images")

    generated = sum(1 for f in image_files if f is not None)
    print()
    print(f"Done. {generated}/{len(slides)} images generated.")
    print(f"Output folder: {(run_dir / 'images').resolve()}")
    print()
    print("NOTE: this script runs independently of make_lesson.py right now")
    print("(it re-generates its own outline). Next step: merge this into")
    print("make_lesson.py so outline + deck + audio + images all come from")
    print("ONE outline generation call, and images get inserted directly")
    print("into the .pptx slides automatically instead of sitting in a")
    print("separate folder needing manual insertion.")


if __name__ == "__main__":
    main()
