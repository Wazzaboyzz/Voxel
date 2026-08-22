#!/usr/bin/env python3
"""
build_book.py - the actual publishing engine. Topic/concept in, a print-ready
PDF interior + a print-ready cover PDF out, sized correctly for Amazon KDP.

This is the publisher's core loop:
    concept -> page-by-page manuscript -> illustrated pages -> print-ready PDF

Pipeline:
  1. Nemotron 3 Ultra (free, via OpenRouter) writes the full page-by-page
     manuscript: for each page, the text (or none, for coloring books) and
     an image_prompt describing the illustration for that page.
     (via content_provider.generate_manuscript - shared across Voxel)
  2. Pollinations.ai (free, no key) generates one illustration per page.
  3. reportlab (free, pure Python) lays out a real print-ready interior PDF
     at the correct KDP trim size, with bleed margins and page numbers.
  4. A separate cover PDF is generated: front + spine + back, with spine
     width calculated automatically from page count and paper type.

Usage:
    python build_book.py "24-page coloring book of ocean animals for ages 4-7" --trim 8.5x8.5 --pages 24
    python build_book.py "20-page illustrated bedtime story about a lost kitten" --trim 8.5x8.5 --pages 20

Required environment variable:
    OPENROUTER_API_KEY   - free OpenRouter key (same as make_lesson.py)

Required local tools:
    pip install reportlab requests --break-system-packages

No key required for Pollinations basic image generation.
"""

import time
import argparse
import urllib.parse
from pathlib import Path

import requests
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from content_provider import generate_manuscript


POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/"

OUTPUT_DIR = Path("output_books")

# KDP requires a 0.125" bleed on each outer edge for full-bleed books.
BLEED_INCHES = 0.125

# Common KDP trim sizes, inches (width x height).
TRIM_SIZES = {
    "8.5x8.5": (8.5, 8.5),   # common for coloring/activity books
    "8.5x11": (8.5, 11.0),   # common for larger picture books / workbooks
    "6x9": (6.0, 9.0),       # common for text-heavy books
    "5x8": (5.0, 8.0),       # common for smaller story books
}

# KDP's approximate paper thickness in inches per page, for spine width
# calculation. White paper is thinner than cream. This is an approximation -
# ALWAYS double check against KDP's own spine width calculator before
# submitting a real cover, since paper stock affects this.
PAPER_THICKNESS_WHITE = 0.002252   # inches per page, white paper
PAPER_THICKNESS_CREAM = 0.0025     # inches per page, cream paper


# ---------------------------------------------------------------------------
# Step 1 - Nemotron writes the full page-by-page manuscript
# (shared implementation: content_provider.generate_manuscript)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Step 2 - Pollinations generates one illustration per page
# ---------------------------------------------------------------------------

def generate_image(prompt, out_path, width, height, seed=None, coloring_book=False):
    style_suffix = (
        ", clean black and white line art, simple bold outlines, no shading, "
        "coloring book style, no text, no watermark"
        if coloring_book else
        ", flat 2D illustration with dimensional shading, clean vector style, "
        "warm colors, children's book art, no text, no watermark"
    )
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


def generate_all_images(pages, image_dir, coloring_book=False, seed_base=100):
    image_dir.mkdir(parents=True, exist_ok=True)
    image_files = []

    # Generate at roughly double the final print resolution for print quality.
    gen_width, gen_height = 1600, 1600

    for page in pages:
        page_num = page["page_number"]
        prompt = page.get("image_prompt", "children's book illustration")
        out_path = image_dir / f"page_{page_num:03d}.png"

        try:
            print(f"  Generating illustration for page {page_num}: {prompt}")
            generate_image(
                prompt, out_path, gen_width, gen_height,
                seed=seed_base + page_num, coloring_book=coloring_book,
            )
            image_files.append(out_path)
        except requests.RequestException as e:
            print(f"  [warn] Image generation failed for page {page_num}: {e}")
            image_files.append(None)

        time.sleep(1)  # be polite to the free service

    return image_files


# ---------------------------------------------------------------------------
# Step 3 - Lay out the print-ready interior PDF
# ---------------------------------------------------------------------------

def build_interior_pdf(pages, image_files, trim_width_in, trim_height_in, out_path):
    """
    Builds a full-bleed interior PDF. Each page is trim size + bleed on all
    sides. Images are placed full-bleed; text (if any) sits in a safe margin
    well inside the trim edge so nothing gets cut during printing.
    """
    page_width = (trim_width_in + 2 * BLEED_INCHES) * inch
    page_height = (trim_height_in + 2 * BLEED_INCHES) * inch

    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path), pagesize=(page_width, page_height))

    safe_margin = 0.5 * inch  # text safe zone, well inside the trim edge

    for page, image_file in zip(pages, image_files):
        if image_file and Path(image_file).exists():
            img = ImageReader(str(image_file))
            # Fill the entire bleed-inclusive page with the image.
            c.drawImage(
                img, 0, 0, width=page_width, height=page_height,
                preserveAspectRatio=True, anchor="c",
            )

        text = page.get("text", "").strip()
        if text:
            # Simple text overlay in the safe zone. This is a first pass -
            # real books will want a nicer font, wrapping, and placement
            # logic tuned per book design, but this is functional and print-safe.
            c.setFillColorRGB(1, 1, 1)
            c.setFont("Helvetica-Bold", 18)
            text_x = safe_margin + BLEED_INCHES * inch
            text_y = safe_margin + BLEED_INCHES * inch
            c.drawString(text_x, text_y, text[:90])  # truncate for this first pass

        c.showPage()

    c.save()


# ---------------------------------------------------------------------------
# Step 4 - Build a print-ready cover (front + spine + back)
# ---------------------------------------------------------------------------

def calculate_spine_width(page_count, paper="white"):
    thickness = PAPER_THICKNESS_CREAM if paper == "cream" else PAPER_THICKNESS_WHITE
    return page_count * thickness


def build_cover_pdf(title, page_count, trim_width_in, trim_height_in, out_path,
                     paper="white", front_image=None):
    """
    Builds a single-page wraparound cover PDF: back cover | spine | front cover.
    Spine width is auto-calculated from page count per KDP's paper-thickness
    approximation. ALWAYS verify against KDP's own spine width tool before
    finalizing a real submission - paper stock and exact page count matter.
    """
    spine_width_in = calculate_spine_width(page_count, paper=paper)

    total_width_in = (2 * trim_width_in) + spine_width_in + (2 * BLEED_INCHES)
    total_height_in = trim_height_in + (2 * BLEED_INCHES)

    page_width = total_width_in * inch
    page_height = total_height_in * inch

    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path), pagesize=(page_width, page_height))

    # Front cover occupies the rightmost trim_width_in of the page.
    front_x_start = (trim_width_in + spine_width_in + BLEED_INCHES) * inch

    if front_image and Path(front_image).exists():
        img = ImageReader(str(front_image))
        c.drawImage(
            img, front_x_start, 0,
            width=trim_width_in * inch, height=page_height,
            preserveAspectRatio=True, anchor="c",
        )

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(
        front_x_start + (trim_width_in * inch) / 2,
        page_height * 0.85,
        title,
    )

    c.showPage()
    c.save()

    print(f"  Spine width calculated: {spine_width_in:.4f} in "
          f"(for {page_count} pages, {paper} paper)")
    print("  NOTE: verify this against KDP's own spine width calculator "
          "before submitting - this is an approximation.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Build a print-ready book from a concept.")
    parser.add_argument("concept", help="Book concept, e.g. '24-page coloring book of ocean animals for ages 4-7'")
    parser.add_argument("--pages", type=int, default=20, help="Number of interior pages (default 20)")
    parser.add_argument("--trim", default="8.5x8.5", choices=list(TRIM_SIZES.keys()),
                         help="KDP trim size (default 8.5x8.5)")
    parser.add_argument("--coloring-book", action="store_true",
                         help="Generate clean line-art suitable for a coloring book")
    parser.add_argument("--paper", default="white", choices=["white", "cream"],
                         help="Paper stock, affects spine width calculation")
    args = parser.parse_args()

    trim_width_in, trim_height_in = TRIM_SIZES[args.trim]

    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in args.concept).strip().replace(" ", "_")[:60]
    run_dir = OUTPUT_DIR / safe_name

    print(f"Generating manuscript for: {args.concept}")
    pages = generate_manuscript(args.concept, args.pages)
    print(f"  -> {len(pages)} pages planned")

    print("Generating illustrations (Pollinations.ai, free, no key required)...")
    image_files = generate_all_images(pages, run_dir / "images", coloring_book=args.coloring_book)

    print("Building print-ready interior PDF...")
    interior_path = run_dir / f"{safe_name}_interior.pdf"
    build_interior_pdf(pages, image_files, trim_width_in, trim_height_in, interior_path)
    print(f"  -> {interior_path}")

    print("Building print-ready cover PDF...")
    cover_path = run_dir / f"{safe_name}_cover.pdf"
    front_image = image_files[0] if image_files else None
    build_cover_pdf(
        args.concept[:40], len(pages), trim_width_in, trim_height_in,
        cover_path, paper=args.paper, front_image=front_image,
    )
    print(f"  -> {cover_path}")

    print()
    print("Done. Output folder:")
    print(f"  {run_dir.resolve()}")
    print()
    print("NOTE: this is a first working skeleton, not a polished final book.")
    print("Before uploading to KDP: review every page for text overflow/")
    print("truncation, verify the spine width against KDP's own calculator,")
    print("and manually proofread all generated text and images.")


if __name__ == "__main__":
    main()
