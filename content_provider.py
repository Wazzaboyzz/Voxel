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

Phase 8c fix (2026-09-13): the original NVIDIA_MODEL default,
"nvidia/llama-3.1-nemotron-70b-instruct", was returning 404 Not Found on
the live NVIDIA NIM endpoint (confirmed via a real Actions run) - the
model id was retired from the catalog. Swapped default to
"nvidia/nemotron-3-super-120b-a12b", which current NVIDIA-catalog
documentation lists as a live free-tier model as of this fix.

Phase 8g (2026-09-13): generate_manuscript()'s prompt was producing
generic, forgettable text - technically valid pages with no reason for a
reader to keep turning them. Rewritten from real published picture-book
craft research (page-turn hooks, show-don't-tell, sensory specificity,
refrain/repetition, punctuation-driven pacing, a want-driven character
arc, a satisfying-AND-surprising ending) rather than a generic "write a
children's book" instruction.

Phase 8i fix (2026-09-13): switched JSON parsing to
json.JSONDecoder().raw_decode() so a valid array with trailing model
commentary after it doesn't crash the whole run.

Phase 8j (2026-09-13): after a real retest, images had good character
consistency but the robot's POSE never changed page to page, and one
page dropped the robot from frame. Root cause traced to image_prompt
text itself often being scene/object-focused without explicitly stating
where the main character is and what it's doing. Added an explicit
requirement that every image_prompt name the main character and its
specific action/pose for that page - this pairs with the matching fix in
image_provider.py's REFERENCE_MATCH_INSTRUCTION (which now locks only
the character's DESIGN, not its pose, letting each page's stated action
actually take effect).
"""

import os
import json

import requests


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", "nvidia/nemotron-3-super-120b-a12b")


def _active_provider():
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


def _extract_first_json_value(raw_text):
    """
    Parses only the FIRST complete JSON value in raw_text and discards
    anything after it, instead of json.loads()'s all-or-nothing behavior.
    Free-tier models sometimes append a trailing note/sentence after a
    perfectly valid JSON array or object - that trailing text should not
    blow up an otherwise-good response (see Phase 8i in module docstring).
    Still raises json.JSONDecodeError (caught by callers) if there is no
    valid JSON value at all, e.g. the model returned pure prose.
    """
    decoder = json.JSONDecoder()
    stripped = raw_text.strip()
    value, end_index = decoder.raw_decode(stripped)
    trailing = stripped[end_index:].strip()
    if trailing:
        print(f"[content_provider] Note: ignored {len(trailing)} char(s) of "
              f"trailing text after valid JSON (model added extra commentary).")
    return value


def _call_nemotron(system_prompt, user_content, timeout=120):
    raw_text = _post(system_prompt, user_content, timeout)

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        return _extract_first_json_value(raw_text)
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

    Phase 8g: this prompt is built from real published-picture-book craft
    principles. Phase 8j: image_prompt now must explicitly name the
    character and its current pose/action on every page.
    """
    system_prompt = (
        "You are a bestselling children's picture book author - the kind "
        "whose books get \"read it again!\" every night. Given a book "
        f"concept, write exactly {page_count} pages that are a genuine "
        "page-turner, not a generic story that happens to be split into "
        "pages. Follow these craft rules, all drawn from how real "
        "published picture books actually work:\n\n"
        "1. WANT-DRIVEN PLOT: establish what the main character wants or "
        "is missing in page 1-2. Every page after that should move them "
        "toward or away from getting it - no filler pages that don't "
        "change anything.\n\n"
        "2. PAGE-TURN HOOKS: end the text on EVERY page (except the very "
        "last) with a reason to turn the page - an unanswered question, "
        "a sound, a half-finished action, something half-seen, or a "
        "sudden shift.\n\n"
        "3. SHOW, DON'T TELL: never state a character's emotion directly - "
        "show it through action, a small physical detail, or dialogue "
        "instead.\n\n"
        "4. READ-ALOUD RHYTHM: vary sentence length deliberately.\n\n"
        "5. A REFRAIN, IF IT FITS: use one consistently if it suits the "
        "story.\n\n"
        "6. A REAL ENDING: satisfying AND slightly surprising.\n\n"
        "7. HUMOR AND WARMTH WHERE IT FITS.\n\n"
        "Return ONLY valid JSON, no markdown fences, no preamble: a JSON "
        "array of page objects, each with exactly these keys:\n"
        '  "page_number": integer, 1-indexed\n'
        '  "text": the page-turn-crafted text for this page per the rules '
        "above (can be an empty string only for pure-illustration/coloring "
        "pages)\n"
        '  "image_prompt": a concrete, specific visual description '
        "(10-25 words) of the illustration for this page. This MUST "
        "explicitly name the main character and state exactly what "
        "physical pose or action they are performing RIGHT NOW on this "
        "page (e.g. 'the robot crouches, reaching under the fridge with "
        "one arm outstretched' - not just 'a fridge in a kitchen'). The "
        "main character must be visibly present and doing something "
        "distinct from every other page's action - never describe a "
        "scene, object, or setting alone without the character actively "
        "in it, unless the page's text explicitly says the character has "
        "left the scene.\n"
        "If the concept describes a coloring book, text should be empty "
        "or a very short caption, and image_prompt should describe a "
        "clean line-art scene suitable for coloring, still following the "
        "character-presence-and-action rule above.\n"
        "Avoid AI-writing tells: no rule-of-three lists, no stock phrases, "
        "vary sentence length naturally, write like a real human author "
        "who has actually read their pages aloud to a child.\n\n"
        "Return ONLY the JSON array itself - no trailing notes, comments, "
        "or explanation after the closing bracket."
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
