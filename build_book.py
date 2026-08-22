#!/usr/bin/env python3
"""
build_book.py - the actual publishing engine. Topic/concept in, a print-ready
PDF interior + a print-ready cover PDF out, sized correctly for Amazon KDP.

Pipeline:
  1. Nemotron 3 Ultra writes the manuscript (content_provider.generate_manuscript)
  2. Pollinations.ai generates one illustration per page (image_provider.generate_all_images)
  3. reportlab lays out a print-ready interior PDF at the correct KDP trim size
  4. A separate cover PDF is generated: front + spine + back
  5. A canonical project.json manifest is written for the run (project_provider)

Usage:
    python build_book.py "24-page coloring book of ocean animals for ages 4-7" --trim 8.5x8.5 --pages 24

Required environment variable:
    OPENROUTER_API_KEY   - free OpenRouter key (same as make_lesson.py)

Required local tools:
    pip install reportlab requests --break-system-packages
"""

import argparse
from pathlib import Path

from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from content_provider import generate_manuscript
from image_provider import generate_all_images, BOOK_STYLE_SUFFIX, COLORING_BOOK_STYLE_SUFFIX
from project_provider import build_project_record, write_project_json


OUTPUT_DIR = Path("output_books")
BLEED_INCHES = 0.125
TRIM_SIZES = {
    "8.5x8.5": (8.5, 8.5), "8.5x11": (8.5, 11.0), "6x9": (6.0, 9.0), "5x8": (5.0, 8.0),
}
PAPER_THICKNESS_WHITE = 0.002252
PAPER_THICKNESS_CREAM = 0.0025


def build_interior_pdf(pages, image_files, trim_width_in, trim_height_in, out_path):
    page_width = (trim_width_in + 2 * BLEED_INCHES) * inch
    page_height = (trim_height_in + 2 * BLEED_INCHES) * inch
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path), pagesize=(page_width, page_height))
    safe_margin = 0.5 * inch
    for page, image_file in zip(pages, image_files):
        if image_file and Path(image_file).exists():
            img = ImageReader(str(image_file))
            c.drawImage(img, 0, 0, width=page_width, height=page_height, preserveAspectRatio=True, anchor="c")
        text = page.get("text", "").strip()
        if text:
            c.setFillColorRGB(1, 1, 1)
            c.setFont("Helvetica-Bold", 18)
            text_x = safe_margin + BLEED_INCHES * inch
            text_y = safe_margin + BLEED_INCHES * inch
            c.drawString(text_x, text_y, text[:90])
        c.showPage()
    c.save()


def calculate_spine_width(page_count, paper="white"):
    thickness = PAPER_THICKNESS_CREAM if paper == "cream" else PAPER_THICKNESS_WHITE
    return page_count * thickness


def build_cover_pdf(title, page_count, trim_width_in, trim_height_in, out_path, paper="white", front_image=None):
    spine_width_in = calculate_spine_width(page_count, paper=paper)
    total_width_in = (2 * trim_width_in) + spine_width_in + (2 * BLEED_INCHES)
    total_height_in = trim_height_in + (2 * BLEED_INCHES)
    page_width = total_width_in * inch
    page_height = total_height_in * inch
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path), pagesize=(page_width, page_height))
    front_x_start = (trim_width_in + spine_width_in + BLEED_INCHES) * inch
    if front_image and Path(front_image).exists():
        img = ImageReader(str(front_image))
        c.drawImage(img, front_x_start, 0, width=trim_width_in * inch, height=page_height, preserveAspectRatio=True, anchor="c")
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(front_x_start + (trim_width_in * inch) / 2, page_height * 0.85, title)
    c.showPage()
    c.save()
    print(f"  Spine width calculated: {spine_width_in:.4f} in (for {page_count} pages, {paper} paper)")
    print("  NOTE: verify this against KDP's own spine width calculator before submitting.")


def main():
    parser = argparse.ArgumentParser(description="Build a print-ready book from a concept.")
    parser.add_argument("concept")
    parser.add_argument("--pages", type=int, default=20)
    parser.add_argument("--trim", default="8.5x8.5", choices=list(TRIM_SIZES.keys()))
    parser.add_argument("--coloring-book", action="store_true")
    parser.add_argument("--paper", default="white", choices=["white", "cream"])
    args = parser.parse_args()

    trim_width_in, trim_height_in = TRIM_SIZES[args.trim]
    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in args.concept).strip().replace(" ", "_")[:60]
    run_dir = OUTPUT_DIR / safe_name

    print(f"Generating manuscript for: {args.concept}")
    pages = generate_manuscript(args.concept, args.pages)
    print(f"  -> {len(pages)} pages planned")

    print("Generating illustrations (Pollinations.ai, free, no key required)...")
    style = COLORING_BOOK_STYLE_SUFFIX if args.coloring_book else BOOK_STYLE_SUFFIX
    image_files = generate_all_images(
        pages, run_dir / "images", filename_prefix="page",
        width=1600, height=1600, style_suffix=style,
        number_key="page_number", seed_base=100,
    )

    print("Building print-ready interior PDF...")
    interior_path = run_dir / f"{safe_name}_interior.pdf"
    build_interior_pdf(pages, image_files, trim_width_in, trim_height_in, interior_path)
    print(f"  -> {interior_path}")

    print("Building print-ready cover PDF...")
    cover_path = run_dir / f"{safe_name}_cover.pdf"
    front_image = image_files[0] if image_files else None
    build_cover_pdf(args.concept[:40], len(pages), trim_width_in, trim_height_in, cover_path, paper=args.paper, front_image=front_image)
    print(f"  -> {cover_path}")

    print("Writing project.json manifest...")
    product_type = "coloring_book" if args.coloring_book else "illustrated_book"
    record = build_project_record(
        concept=args.concept,
        product_type=product_type,
        trim_width_in=trim_width_in,
        trim_height_in=trim_height_in,
        paper=args.paper,
        pages=pages,
        image_files=image_files,
        interior_path=interior_path,
        cover_path=cover_path,
        run_dir=run_dir,
    )
    project_json_path = write_project_json(record, run_dir)
    print(f"  -> {project_json_path}")

    print()
    print("Done. Output folder:")
    print(f"  {run_dir.resolve()}")


if __name__ == "__main__":
    main()
