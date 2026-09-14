#!/usr/bin/env python3
"""
generate_character_sheet.py - one-off tool to generate a multi-pose
character consistency sheet for a single character, using a real
reference image (not just a text description) via image_provider.py's
Gemini reference-image conditioning (same mechanism Phase 8h/8j added
for per-page consistency in build_book.py).

Why this exists: Canva Magic Media has no reference-image input, so
every prompt typed there is an independent generation with no memory of
the last one - even an identical text description drifts (hair curl
pattern, eye shape, exact blue shade) page to page. This script instead
feeds a real uploaded image into Gemini/Cloudflare as a design anchor,
the same design-locked / pose-from-prompt approach already fixed for
the robot book (Phase 8j: REFERENCE_MATCH_INSTRUCTION separates DESIGN,
which must match the reference, from POSE/ACTION, which must match each
prompt's own description).

Fix (2026-09-13): the first real run of this script hit 429 on every
single one of 15 poses, on BOTH Gemini and the Cloudflare fallback, with
no pause between iterations at all - unlike build_book.py's
generate_all_images(), which paces itself via polite_delay. Added the
same kind of delay here between poses so this script doesn't hammer both
providers back-to-back with zero spacing, which was very likely making
an already-tight quota (this ran the same day as a full book test) worse
instead of giving it any chance to recover between calls.

Usage (run via the character-sheet.yml workflow, not locally):
  python generate_character_sheet.py \
      --reference story_bibles/luna/reference.jpg \
      --output-dir character_sheets/luna \
      --character-name Luna

Requires the same secrets as the main pipeline: GEMINI_API_KEY (and
optionally CLOUDFLARE_ACCOUNT_ID/CLOUDFLARE_API_TOKEN as fallback) -
already configured as repo secrets.
"""

import argparse
import time
from pathlib import Path

import image_provider


# 15 poses/angles chosen to stress-test consistency across the range a
# real picture book would need: locomotion, stillness, different camera
# angles, and interaction with a prop/companion. Each ends with a
# distinct, unambiguous pose so the model has no room to default back to
# the reference image's own standing pose (Phase 8j's exact failure mode).
DEFAULT_POSES = [
    "standing still, facing forward, arms relaxed at her sides",
    "walking to the left, mid-stride, one arm swinging forward",
    "running to the right, both arms pumping, hair flying back",
    "sitting cross-legged on the ground, looking up and to the side",
    "climbing, one hand reaching up and gripping a branch above her head",
    "crouching low, peering forward with one hand shielding her eyes",
    "jumping in the air, both feet off the ground, arms flung wide",
    "seen from behind, walking away into the distance",
    "three-quarter back view, looking back over one shoulder",
    "side profile view, standing and pointing forward with one arm",
    "lying on her stomach, chin resting on both hands, feet kicked up behind her",
    "reaching up on tiptoes, both arms stretched high overhead",
    "sitting on a low stool, leaning forward with elbows on her knees",
    "spinning around with her arms out, pajama sleeves flaring",
    "kneeling down, both hands cupped together in front of her",
]


def main():
    parser = argparse.ArgumentParser(description="Generate a multi-pose character consistency sheet.")
    parser.add_argument("--reference", required=True, help="Path to the reference image (design anchor)")
    parser.add_argument("--output-dir", required=True, help="Directory to write the pose images into")
    parser.add_argument("--character-name", default="character", help="Used in filenames and prompts")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--polite-delay", type=int, default=15,
                         help="Seconds to wait between each pose to ease per-minute rate limits")
    args = parser.parse_args()

    reference_path = Path(args.reference)
    if not reference_path.exists():
        raise SystemExit(
            f"Reference image not found at {reference_path}. "
            f"Upload it to this exact path in the repo first, then re-run."
        )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(DEFAULT_POSES)} poses for {args.character_name}, "
          f"anchored to {reference_path}, with {args.polite_delay}s between poses\n")

    results = []
    for i, pose in enumerate(DEFAULT_POSES, start=1):
        prompt = f"{args.character_name}, {pose}"
        out_path = output_dir / f"{args.character_name.lower()}_pose_{i:02d}.png"
        print(f"[{i}/{len(DEFAULT_POSES)}] {pose}")
        try:
            used_fallback = image_provider.generate_image(
                prompt,
                out_path,
                width=args.width,
                height=args.height,
                style_suffix=image_provider.BOOK_STYLE_SUFFIX,
                reference_image_path=reference_path,
            )
            results.append((out_path.name, pose, "cloudflare" if used_fallback else "gemini"))
            print(f"    -> saved {out_path.name}" + (" (via Cloudflare fallback)" if used_fallback else ""))
        except RuntimeError as e:
            results.append((out_path.name, pose, f"FAILED: {e}"))
            print(f"    [warn] failed: {e}")

        if i < len(DEFAULT_POSES) and args.polite_delay:
            time.sleep(args.polite_delay)

    manifest_path = output_dir / "_manifest.md"
    lines = [f"# {args.character_name} character consistency sheet", "",
             f"Reference image: {reference_path}", ""]
    for filename, pose, provider in results:
        lines.append(f"- **{filename}** ({provider}): {pose}")
    manifest_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nDone. {len(results)} images written to {output_dir}/, manifest at {manifest_path}")
    print("Check every image by eye against the reference before trusting this character for a full book run.")


if __name__ == "__main__":
    main()
