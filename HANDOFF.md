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

- Phase 1 of `ARCHITECTURE.md` is done: `content_provider.py` is the one
  shared place that calls Nemotron/OpenRouter. `make_lesson.py` imports
  `generate_outline` from it. `build_book.py` and `generate_images.py`
  still need to be switched over to import from it too (their local
  copies of the same logic have NOT been removed yet — that's next).
- `test_content_provider.py` mocks the OpenRouter call and checks the
  schema both callers depend on. No API key or network needed to run it.
- `.github/workflows/test.yml` runs that test on every push/PR to `main`.
  **If you break the schema in `content_provider.py`, this should fail
  before it reaches main.** If it doesn't, the test needs strengthening —
  don't just disable it.

## Rules for anyone (or anything) working on this repo

- **Read `ARCHITECTURE.md`'s "Current state" section before writing
  code.** If it's stale (doesn't match what's actually in the repo),
  fix the doc as part of your change — don't leave the next
  person/session to rediscover the gap.
- **Work one phase at a time, in order.** Don't build Phase 5 (audio
  embedding) while Phase 1 duplication still exists elsewhere. Check
  which scripts still have their own copy of outline/manuscript logic
  before assuming Phase 1 is fully done — currently it isn't (see above).
- **A phase is done when the duplication/gap it targets is actually
  gone from the repo**, not when a new file merely exists alongside
  the old one.
- **Add or update a test when you change shared logic**
  (`content_provider.py`, and future `image_provider.py` etc.). Mock
  external calls — no test should need a real API key or network to run.
- **No dashboard, no Canva, no video, no multi-product plugin system**
  until Phase 7 is reached and re-scoped for real, with actual usage
  behind it. If a plan or prompt asks for these earlier, that's a
  scope violation — flag it, don't build it.
- **Don't claim a change works without running the tests.** `python -m
  pytest -v` locally, or check the Actions tab after pushing.
- This repo owner (Zia) is a non-coder working browser-only (GitHub web
  editor, no terminal). GitHub's write API returns 403 on this repo for
  automated tools — if you're an AI assistant hitting that, give Zia
  the exact web-editor URL (`.../edit/main/<path>` or
  `.../new/main?filename=<path>`) plus the full file content to paste,
  never a partial diff or "find this line" instruction.

## Next up (in order)

1. Switch `build_book.py` to import `generate_manuscript` from
   `content_provider.py`, remove its local copy.
2. Switch `generate_images.py` to import `generate_outline` from
   `content_provider.py`, remove its local copy (this closes the
   dead-end duplication flagged in `ARCHITECTURE.md`).
3. Then Phase 2: canonical `project.json` per run.
