# Voxel — Architecture

This is the phased build plan referenced by `HANDOFF.md`. It has been
missing from the repo until 2026-08-22, which caused ambiguity about
scope for Phase 2+ — this file exists to close that gap and prevent it
recurring.

## Ground rule

**Work one phase at a time, in order.** A phase is done when the
duplication/gap it targets is actually gone from the repo, not when a
new file merely exists alongside the old one. Do not start a phase
before the prior one is done. Do not build ahead into later phases
"while you're in there."

A large "AI creative production studio" vision (orchestrator, provider
registry across text/image/design/audio/video, Canva integration, live
multi-project dashboard, canonical multi-format rendering, multi-product
architecture) was proposed from a different working session on
2026-08-22 and explicitly rejected as premature. That vision is not
banned forever - it's just not in scope until Phase 7, and Phase 7 is
not scheduled until the phases below are actually done and there is
real usage (real books actually produced and sold) to design against.
Building orchestration/provider-abstraction machinery before a single
real product has shipped is designing blind.

## Phases

### Phase 1 — Shared content generation (DONE)
`content_provider.py` is the one shared place that calls
Nemotron/OpenRouter. `make_lesson.py` (`generate_outline`) and
`build_book.py` (`generate_manuscript`) both import from it. No local
copies of that logic remain in either caller.
Tested by `test_content_provider.py`.

### Phase 2 — Canonical `project.json` per run (DONE)
Every `build_book.py` run writes a `project.json` manifest into its
output folder: what was asked for (concept, trim, paper, page count),
what was produced (per-page text/image-prompt/image-file, interior PDF
path, cover PDF path), and when. This is a flat record of one finished
run - not a database, not a live project state, not something an
orchestrator reads to make decisions. It exists so a human (or a future
script) can inspect or resume a run without re-reading the whole
codebase.
Implemented in `project_provider.py`, wired into `build_book.py` after
both PDFs are built. Tested by `test_project_provider.py`.

### Phase 3 — Shared image generation (DONE)
`image_provider.py` wraps Pollinations.ai and is shared by both
`make_lesson.py` and `build_book.py`.
Tested by `test_image_provider.py`.

### Phase 4 — First real book, end to end (NOT STARTED)
Pick one real book concept and run it fully through `build_book.py`.
Walk the remaining manual steps (proofing, Amazon's Print Previewer,
KDP category/keyword selection, upload) by hand to find weak points
before automating further. This is the step that generates the real
usage data the later phases need. Nothing in Phase 5+ should be
designed before this has happened at least once.

### Phase 5 — KDP metadata + upload prep (NOT STARTED)
Title, subtitle, description, keywords, categories, regional pricing.
Depends on lessons from Phase 4.

### Phase 6 — Automation of the proven manual steps (NOT STARTED)
Only automate steps that Phase 4/5 proved are repetitive and
well-understood. Candidates already noted: kdp-scout (keyword research),
auto-kdp (bulk upload). Not scoped further than that until Phase 4/5
exist.

### Phase 7 — Re-scope, not before (NOT SCHEDULED)
This is where dashboard, Canva, video, and multi-product-type
architecture get re-evaluated - **with real usage behind them**, not
speculatively. Until this phase is reached and deliberately re-scoped,
none of that gets built.

## Current state (keep this in sync with reality)

- Shared modules: `content_provider.py`, `image_provider.py`,
  `project_provider.py` — all tested, no duplication in callers.
- Products: `make_lesson.py` (lesson decks), `build_book.py`
  (illustrated books / coloring books, KDP trim sizes, print-ready
  interior + cover PDFs, now with `project.json` manifest).
- CI: `.github/workflows/test.yml` runs `python -m pytest -v` on every
  push/PR to `main` — picks up any `test_*.py` automatically.
- No book has been produced end-to-end yet (Phase 4 not started). This
  is the actual next step, not further infrastructure.
