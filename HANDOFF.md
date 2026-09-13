# Voxel — Handoff

Read this first if you're new to this repo (human or AI). It tells you
where things stand and how to not break what's already here.

## Read in this order

1. `README.md` — what Voxel does today, setup, known limitations.
2. `ARCHITECTURE.md` — the phased build plan.
3. `PROJECT_ISOLATION_RULES.md` — 20 rules against mixing picture-book
   and novel craft/logic. Read before touching any generation prompt.
4. This file — process rules and current status.

## START HERE — Phase 9, 2026-09-13 (most current — image consistency fixed, novel beat-maps added)

**This section replaces everything previously under "Phase 8d." That
section sat here claiming to be current for hours after five more
phases shipped directly to `main` from the `Wazzaboyzz` account —
nobody had gone back and fixed it until now. If you're reading an
older cached copy of this file, or a summary from earlier in a
conversation, re-fetch this file from GitHub before trusting anything
it says about current status.**

**The real problem Zia reported after the first full run (26 pages):
image quality was good, three-dimensional, but zero character
consistency page to page.** That was accurate for the code at the
time. It is fixed as of the latest commit on `main`:

- **Phase 8e:** Cloudflare Workers AI (FLUX) added as an automatic
  fallback when Gemini 429s, removing the need for manual VEO3/Google
  Flow image generation — the Phase 8d manual-image workflow
  (`--manual-images`/`--images-dir`, still in `image_provider.py`/
  `build_book.py`/`voxel_cli.py`) is kept only as a fallback-of-the-
  fallback, not the primary path anymore.
- **Phase 8f:** Root-caused the consistency problem — every page was
  generated from a fresh text prompt with zero shared visual state, so
  the character was redesigned from scratch each time. Fix: the first
  successful image in a run becomes a real reference image, fed back
  into Gemini on every subsequent call in that run so it matches the
  reference instead of reinventing the character. `story_bible.py`
  gained `reference_image_path` so a sequel can anchor to a prior
  book's actual reference image, not just a text description.
- **Phase 8g:** `generate_manuscript`'s prompt rewritten around real
  picture-book craft (page-turn hooks, show-don't-tell, want-driven
  plot, read-aloud rhythm) instead of a generic instruction.
- **Mistake + fix:** Claude wrongly suggested applying Phase 8g's
  picture-book craft rules to Amity Falls' novel generation. Zia caught
  it. Result: `PROJECT_ISOLATION_RULES.md` (20 rules) — read it before
  touching any generation prompt or shared module.
- **Phase 8h:** Two more fixes after that first run: (1) Gemini's image
  model (`gemini-2.5-flash-image`) is deprecated by Google, shutting
  down October 2, 2026 — swapped to `gemini-3.1-flash-image`. (2) The
  Cloudflare fallback model (`flux-1-schnell`) had no image-input
  capability at all, so any page that fell back had zero consistency
  regardless of the Phase 8f fix — swapped to `flux-2-klein-4b`
  (Apache 2.0, commercial-safe — NOT `flux-2-dev`, which is non-
  commercial-licensed and would conflict with selling these books on
  KDP), which accepts a reference image just like Gemini does. The
  per-page delay was also raised from 2s to 12s to stay under Gemini's
  free-tier per-minute rate limit across a full book run.
- **Phase 9:** `voxel_cli.py novel` now supports `--beat-map`: a
  book-scoped JSON (via `story_bible.py`) giving each chapter its own
  beat, checkpoint-chapter locks, voice profiles, a 2,000-2,500 word-
  count band, and a zero-em-dash rule — ported from how "Where the
  Frost Doesn't Reach" was actually written by hand. Writes
  `novel_progress.json` after generation (word count + em-dash count
  per chapter), mirroring the tracking table that novel used to keep
  in its own HANDOFF.md by hand. Optional and backward-compatible — no
  beat map falls back to brief-only generation exactly as before.
  Scoped to novels only per isolation rule 3 above.
- **Latest commit (18:47 UTC today):** `content_provider.py`'s JSON
  parsing now extracts the first valid JSON value from a response
  instead of crashing on trailing text some free-tier models add after
  the JSON — a real crash this was hit by, not a theoretical one.

**What this means practically:** the pipeline has NOT been re-run
end-to-end since these fixes landed. The 26-page run Zia saw is now
stale evidence — it tested code that predates all of the above. The
next real run is the first one that reflects current `main`, and
should be checked by eye specifically for character consistency
across pages (including any page that used the Cloudflare fallback —
check `_fallback_report.json` next to the generated images) before
concluding anything about whether this is actually fixed.

**Still not done:**
- No automated tests for any of Phase 8e–9's new code
  (`_try_cloudflare` reference-image path, beat-map loading, the new
  JSON extraction function).
- `voxel-book.yml`'s `manual_images`/`images_dir` inputs (Phase 8d) are
  live and working but have never been exercised by a real run either.
- README.md / `make_lesson.py` still describe images as coming from
  "Pollinations.ai" — still stale, still lower priority (see mismatches
  section below).
- `ARCHITECTURE.md`'s "Current state" still says Phase 4 is
  "NOT STARTED" — still stale, still not reconciled.

## Where things actually stand (Phase 8 background — dating in this section is unreliable, see Phase 9 above for what's current)

**Note on this file's own dating:** the header above previously said
"updated 2026-09-13" for the whole Phase 8 write-up below, but Zia has
since said the original Phase 8 handoff was actually written roughly two
months before today (2026-09-13) — only the Phase 8b onward edits
genuinely happened today. Don't trust "2026-09-13" elsewhere in this
file as an authorship date for anything except those — verify against
git commit history if the exact date of a specific change ever matters.

- **Phases 1–3 are done.** `content_provider.py`, `image_provider.py`,
  `project_provider.py` are shared modules, tested, used by both
  `make_lesson.py` and `build_book.py`.
- **Phase 4 (first real book, end to end) is done and shipped.** Two real
  products exist, but neither went through this repo's own pipeline:
  - `novels/where-the-frost-doesnt-reach/` — 45-chapter novel, written
    chapter-by-chapter by hand/direct-API-push, not via `build_book.py`.
  - "Luna and the Lost Star" — built and published on KDP entirely
    manually in Canva, not via this repo at all.
- **Phase 8 (one-command pipeline): a one-command pipeline was added on
  top of the existing Phase 1-4 code**, explicitly at Zia's direction,
  ahead of the Phase 7 gate the previous HANDOFF.md set (multi-product
  pipeline was flagged as out of scope until Phase 7 — Zia overrode that
  explicitly and asked for it now; noting this so the override is
  visible, not silently absorbed).
- **Phase 8b: direct NVIDIA API support.** `content_provider.py` prefers
  `NVIDIA_API_KEY` over `OPENROUTER_API_KEY` when both are set — direct
  NVIDIA NIM endpoint, no OpenRouter middleman or free-tier rate limit.
- **Phase 8c: first real end-to-end run.** NVIDIA model-id 404 and a
  workflow-permissions 403 both fixed; manuscript generation + humanizer
  confirmed working for real. Image generation blocked by Gemini 429s on
  a no-billing free-tier key.
- **Phase 8d: manual-image workflow.** Fixed the Phase 8c image blocker
  by supporting hand-generated images (VEO3, Google Flow). Superseded as
  the *primary* path by Phase 8e-8h above, but kept as a fallback.
- **Phase 8e-9: see START HERE above** — this is the current state.

### Files added/changed across Phase 8-9

- **`voxel_cli.py`** — `book` and `novel` subcommands (see START HERE
  above for `novel`'s Phase 9 `--beat-map` addition).
- **`humanizer.py`** — AI-tell scan + rewrite pass, offline regex scan,
  integrity gate (won't drop a fact silently).
- **`story_bible.py`** — per-series JSON continuity file; gained
  `reference_image_path` (Phase 8f) and beat-map support (Phase 9).
- **`content_provider.py`** — `generate_novel_chapter()`, `call_raw()`,
  NVIDIA support, model-id fix, and the JSON-extraction fix (latest
  commit).
- **`image_provider.py`** — manual-image functions (8d), Cloudflare
  fallback (8e), reference-image conditioning on both providers (8f,
  8h), model swaps (8h).
- **`PROJECT_ISOLATION_RULES.md`** — new file, 20 rules, see top of
  this doc.

### What was deliberately NOT built (know these before extending)

- **No KDP upload automation.** Still fully manual per the original
  Phase 4 walk-through at the bottom of this file.
- **No story-concept generation.** Zia supplies the concept/brief for
  both `book` and `novel` — nothing here invents what to write about.
- **Novels have no cover-art generation wired in.**
- **`humanizer.py`'s pattern list (~20 phrases) is a starting set, not
  exhaustive.**
- **No automated tests** for `humanizer.py`, `story_bible.py`,
  `voxel_cli.py`, or any of Phase 8e-9's new logic.

## Known doc/repo mismatches not yet fixed (flagged, not resolved)

- **`ARCHITECTURE.md`'s "Current state" section is stale** — still says
  Phase 4 is "NOT STARTED."
- **README.md and `make_lesson.py` still describe images as coming from
  "Pollinations.ai, free, no key required."** Real code path (Gemini →
  Cloudflare fallback) differs; `make_lesson.py` doesn't use the
  manual-image workflow either.
- **`generate_images.py` is a second, disconnected image pipeline** —
  GitHub-Actions-only, not called by `image_provider.py` or
  `voxel_cli.py`, only by `.github/workflows/test-image-secret.yml`.
- **`video_output.py` is built but never wired into `voxel_cli.py`.**
- **`build-book.yml` is redundant with `voxel-book.yml`** and doesn't
  have the `--manual-images`/`--images-dir` inputs wired up.
- **`_workflows_scope_test.md` and `_write_access_test.md`** in the repo
  root are leftover connectivity-check files, safe to delete.

## Rules for anyone (or anything) working on this repo

- **Read `ARCHITECTURE.md`'s "Current state" section AND this file's
  "START HERE" section before writing code.** If either is stale, fix
  it as part of your change — don't leave the next reader trusting a
  section that's five phases behind reality, the way this file's own
  "Phase 8d" section sat here for hours after Phase 9 shipped.
- **Read `PROJECT_ISOLATION_RULES.md` before touching any generation
  prompt or shared module** — see the rules file for why.
- **Add or update a test when you change shared logic.** Still not
  happening consistently — see "not built" list above. Mock external
  calls.
- **Strictly free tier only. No billing, no paid elements, anywhere in
  this pipeline.** If a provider requires billing to work at all,
  treat it as unusable and find a genuinely free alternative, or a
  manual-generation path that needs no API at all.
- **Zia works browser-only, including from his phone. He does NOT run
  a terminal/shell/CLI** — copy-paste into a browser interface only,
  local-clone terminal use is a last resort. Design any new
  workflow/step assuming browser-only access first.
- **Files under `.github/workflows/` cannot be written directly by the
  GitHub App/OAuth connector AI assistants use in this session** —
  confirmed via repeated real 403s (`Resource not accessible by
  integration`) even with full write access elsewhere in the repo.
  Any workflow YAML change must be handed to Zia as a full file to
  paste into GitHub's web editor.
- **Before attempting any write to this or any other repo, an AI
  assistant must call whatever "get authenticated user" tool it has
  and confirm which account is connected**, then actually attempt a
  real write and check the result rather than assuming a past
  session's access note still applies. `aliwaziri10` has direct
  collaborator `write` access to this repo (confirmed) — no account
  switch to `Wazzaboyzz` is needed.
- **Don't trust a cached/remembered summary of this file's status —
  always re-fetch HANDOFF.md from GitHub before reporting on current
  state.** This exact file just spent hours being five phases stale in
  someone's memory/context before anyone re-checked it against `main`.

## Original Phase 4 walk-through (superseded by voxel_cli.py, kept for reference)

1. Pick one real book concept.
2. Run `build_book.py` locally with that concept.
3. Open the output folder, check the PDFs and `project.json` by eye.
4. Run the interior + cover PDFs through Amazon's KDP Print Previewer.
5. Walk KDP's manual listing flow by hand; note repetitive/error-prone
   steps — that becomes future scope.
6. Come back and scope further automation based on what step 5 surfaced.

## Footer

Content generation pipeline — topic to finished deck/book. © 2026.
