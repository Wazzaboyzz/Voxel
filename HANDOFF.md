# Voxel — Handoff

Read this first if you're new to this repo (human or AI). It tells you
where things stand and how to not break what's already here.

## Read in this order

1. `README.md` — what Voxel does today, setup, known limitations.
2. `ARCHITECTURE.md` — the phased build plan. Says what phase we're on,
   what's NOT being built yet (dashboard, Canva, video — none of that
   is in scope until Phase 7, and Phase 7 isn't scheduled).
3. This file — process rules.

## Where things actually stand

- **Phase 1 of `ARCHITECTURE.md` is done.** `content_provider.py` is the
  one shared place that calls Nemotron/OpenRouter. Both `make_lesson.py`
  (`generate_outline`) and `build_book.py` (`generate_manuscript`) import
  from it — neither has a local copy of that logic anymore. Verified
  against the live repo on 2026-08-22.
- **Phase 3 (image provider abstraction) is also done.** `image_provider.py`
  wraps Pollinations.ai and is shared by both `make_lesson.py` and
  `build_book.py`.
- `test_content_provider.py` mocks the OpenRouter call and checks the
  schema both callers depend on. No API key or network needed to run it.
- `test_image_provider.py` mocks the Pollinations HTTP call, verifies
  `generate_image` builds the right URL/params, and verifies
  `generate_all_images` handles a failed request per-item without
  crashing the batch. No API key or network needed to run it. Added
  2026-08-22 — this closes the test-coverage gap that used to be listed
  here.
- `.github/workflows/test.yml` runs `python -m pytest -v` on every
  push/PR to `main` — generic, not hardcoded to any one test filename,
  so it automatically picks up any `test_*.py` file. Confirmed
  2026-08-22. **If you break the schema in `content_provider.py` or
  `image_provider.py`, this should fail before it reaches main.** If it
  doesn't, the test needs strengthening — don't just disable it.
- All 7 tests (4 from `test_content_provider.py` + 3 from
  `test_image_provider.py`) passing as of the last CI run (Run #9,
  2026-08-22).
- **No remaining test-coverage gaps** for the two shared modules.

## Rules for anyone (or anything) working on this repo

- **Read `ARCHITECTURE.md`'s "Current state" section before writing
  code.** If it's stale (doesn't match what's actually in the repo),
  fix the doc as part of your change — don't leave the next
  person/session to rediscover the gap.
- **Work one phase at a time, in order.**
- **A phase is done when the duplication/gap it targets is actually
  gone from the repo**, not when a new file merely exists alongside
  the old one.
- **Add or update a test when you change shared logic**
  (`content_provider.py`, `image_provider.py`, and any future shared
  module). Mock external calls — no test should need a real API key
  or network to run.
- **No dashboard, no Canva, no video, no multi-product plugin system**
  until Phase 7 is reached and re-scoped for real, with actual usage
  behind it. If a plan or prompt asks for these earlier, that's a
  scope violation — flag it, don't build it.
- **Don't claim a change works without running the tests.**
  `python -m pytest -v` locally, or check the Actions tab after pushing.
- This repo owner (Zia) is a non-coder working browser-only (GitHub web
  editor, no terminal). GitHub's write API returns 403 on this repo for
  automated tools — if you're an AI assistant hitting that, give Zia
  the exact web-editor URL (`.../edit/main/<path>` or
  `.../new/main?filename=<path>`) plus the full file content to paste,
  never a partial diff or "find this line" instruction.

## Next up (in order)

1. Phase 2: canonical `project.json` per run.

## Footer

Content generation pipeline — topic to finished deck/book. © 2026.
