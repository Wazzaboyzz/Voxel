#!/usr/bin/env python3
"""
voxel_cli.py - the one-command entry point for Voxel Publications.

This is what "one command, one book ready" means in practice:

  Picture book (like Luna):
    python voxel_cli.py book \
        --concept "A gentle bedtime story about a girl named Mira who..." \
        --pages 26 --trim 8.5x11 --series luna

  Novel chapter / sequel (like Where the Frost Doesn't Reach, Amity Falls):
    python voxel_cli.py novel \
        --series amity-falls --book "Amity Falls Book 2" \
        --chapters 45 \
        --brief "Book 2 picks up two years after the wedding in Book 1..."

What it does NOT do yet (see HANDOFF.md "Known gaps"):
  - It does not auto-decide the story concept for you. You give it a
    concept/brief; it does not invent the creative direction from nothing.
  - It does not upload to KDP. That's still the manual walk-through in
    build_book.py's original HANDOFF.md steps 4-5.
  - Image generation for novels (cover art) is not wired in here; novels
    are text-only output (.md chapter files + a compiled manuscript).

Required environment variables (same as before, nothing new):
    OPENROUTER_API_KEY
    GEMINI_API_KEY   (only needed for the 'book' command's illustrations)

Required local packages (same as before, nothing new):
    pip install reportlab requests --break-system-packages

This script assumes it's run from inside a local clone of this repo (so
relative imports of content_provider/image_provider/build_book work, and
so the git commands below can commit+push using your machine's own git
login - no GitHub token is handled by this script).
"""

import argparse
import subprocess
from pathlib import Path

import content_provider
import humanizer
import story_bible


NOVELS_DIR = Path("novels")


def cmd_book(args):
    """Generate a full picture book: manuscript -> humanize -> images ->
    print-ready PDFs -> project.json. Wraps the existing build_book.py
    pipeline instead of duplicating it, and adds the two things Phase 4
    was missing: continuity with prior books, and an AI-tell pass."""
    import build_book  # existing Phase 4 pipeline, imported not rewritten

    continuity = story_bible.continuity_prompt_block(args.series) if args.series else ""

    print(f"[voxel] Generating manuscript ({args.pages} pages)...")
    pages = content_provider.generate_manuscript(args.concept, args.pages, continuity_block=continuity)

    print("[voxel] Running humanizer pass (removing AI tells)...")
    pages = humanizer.humanize_manuscript(pages, content_provider.call_raw)
    flagged = [p for p in pages if p.get("_humanizer", {}).get("integrity_gate_failed")]
    if flagged:
        print(f"[voxel] WARNING: {len(flagged)} page(s) failed the integrity gate "
              "(a rewrite would have dropped a fact) - kept original text for those. "
              "Check project.json's '_humanizer' field per page.")

    trim_width_in, trim_height_in = build_book.TRIM_SIZES[args.trim]
    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in args.concept).strip().replace(" ", "_")[:60]
    run_dir = build_book.OUTPUT_DIR / safe_name

    print("[voxel] Generating illustrations...")
    style = build_book.COLORING_BOOK_STYLE_SUFFIX if args.coloring_book else build_book.BOOK_STYLE_SUFFIX
    image_files = build_book.generate_all_images(
        pages, run_dir / "images", filename_prefix="page",
        width=1600, height=1600, style_suffix=style,
        number_key="page_number", seed_base=100,
    )

    print("[voxel] Building print-ready interior PDF...")
    interior_path = run_dir / f"{safe_name}_interior.pdf"
    build_book.build_interior_pdf(pages, image_files, trim_width_in, trim_height_in, interior_path)

    print("[voxel] Building print-ready cover PDF...")
    cover_path = run_dir / f"{safe_name}_cover.pdf"
    front_image = image_files[0] if image_files else None
    build_book.build_cover_pdf(args.concept[:40], len(pages), trim_width_in, trim_height_in, cover_path, paper=args.paper, front_image=front_image)

    print("[voxel] Writing project.json...")
    product_type = "coloring_book" if args.coloring_book else "illustrated_book"
    record = build_book.build_project_record(
        concept=args.concept, product_type=product_type,
        trim_width_in=trim_width_in, trim_height_in=trim_height_in,
        paper=args.paper, pages=pages, image_files=image_files,
        interior_path=interior_path, cover_path=cover_path, run_dir=run_dir,
    )
    build_book.write_project_json(record, run_dir)

    if args.series:
        summary = args.summary or f"({args.pages}-page picture book: {args.concept[:120]})"
        story_bible.register_book(args.series, safe_name, summary)
        print(f"[voxel] Registered '{safe_name}' in the '{args.series}' story bible for future sequels.")

    print()
    print("[voxel] Done. Output folder:")
    print(f"  {run_dir.resolve()}")
    print("[voxel] Next manual step: run the interior + cover PDFs through KDP's Print Previewer, then the KDP listing flow (see HANDOFF.md).")


def cmd_novel(args):
    """Generate N chapters of a novel/sequel, one file per chapter under
    novels/<series>/<book-slug>/, plus a compiled single manuscript file.
    Runs the humanizer pass per chapter. Commits+pushes at the end if
    --commit is passed (uses your machine's own git credentials)."""
    continuity = story_bible.continuity_prompt_block(args.series)
    book_slug = "".join(c if c.isalnum() or c in " -_" else "" for c in args.book).strip().replace(" ", "-").lower()
    out_dir = NOVELS_DIR / args.series / book_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    compiled = []
    for n in range(1, args.chapters + 1):
        print(f"[voxel] Writing chapter {n}/{args.chapters}...")
        brief = args.brief if n == 1 else f"{args.brief}\n(Continue naturally from chapter {n-1}.)"
        chapter_text = content_provider.generate_novel_chapter(n, brief, continuity_block=continuity)

        print(f"[voxel]   humanizer pass for chapter {n}...")
        clean_text, meta = humanizer.humanize_text(chapter_text, content_provider.call_raw)
        if meta.get("integrity_gate_failed"):
            print(f"[voxel]   WARNING: chapter {n} rewrite dropped a fact - kept original text.")

        chapter_path = out_dir / f"chapter_{n:02d}.md"
        chapter_path.write_text(clean_text)
        compiled.append(clean_text)
        print(f"[voxel]   -> {chapter_path}")

    manuscript_path = out_dir / f"{book_slug}_full_manuscript.md"
    manuscript_path.write_text("\n\n---\n\n".join(compiled))

    summary = args.summary or f"({args.chapters}-chapter novel: {args.brief[:150]})"
    story_bible.register_book(args.series, args.book, summary)
    print(f"[voxel] Registered '{args.book}' in the '{args.series}' story bible for future sequels.")

    print()
    print("[voxel] Done. Output folder:")
    print(f"  {out_dir.resolve()}")

    if args.commit:
        print("[voxel] Committing and pushing (using your local git login)...")
        subprocess.run(["git", "add", str(out_dir), "story_bibles"], check=False)
        subprocess.run(["git", "commit", "-m", f"Add {args.book} ({args.chapters} chapters, auto-generated)"], check=False)
        subprocess.run(["git", "push"], check=False)
    else:
        print("[voxel] Not committed. Re-run with --commit to push, or paste the files via GitHub's web editor.")


def main():
    parser = argparse.ArgumentParser(description="Voxel Publications - one-command content pipeline.")
    sub = parser.add_subparsers(dest="command", required=True)

    book_p = sub.add_parser("book", help="Generate a full illustrated picture book, like Luna and the Lost Star.")
    book_p.add_argument("--concept", required=True)
    book_p.add_argument("--pages", type=int, default=26)
    book_p.add_argument("--trim", default="8.5x11", choices=["8.5x8.5", "8.5x11", "6x9", "5x8"])
    book_p.add_argument("--paper", default="white", choices=["white", "cream"])
    book_p.add_argument("--coloring-book", action="store_true")
    book_p.add_argument("--series", default=None, help="Story-bible slug, e.g. 'luna', so a sequel stays consistent.")
    book_p.add_argument("--summary", default=None, help="One-line summary to store in the series bible.")
    book_p.set_defaults(func=cmd_book)

    novel_p = sub.add_parser("novel", help="Generate a novel or novel sequel, chapter by chapter, like Amity Falls.")
    novel_p.add_argument("--series", required=True, help="Story-bible slug, e.g. 'amity-falls'.")
    novel_p.add_argument("--book", required=True, help="Book title, e.g. 'Amity Falls Book 2'.")
    novel_p.add_argument("--chapters", type=int, required=True)
    novel_p.add_argument("--brief", required=True, help="What this book/chapter arc is about.")
    novel_p.add_argument("--summary", default=None)
    novel_p.add_argument("--commit", action="store_true", help="git add/commit/push when done.")
    novel_p.set_defaults(func=cmd_novel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
