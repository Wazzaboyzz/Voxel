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

- **Phase 1 (`ARCHITECTURE.md`) is done.** `content_provider.py` is the
  one shared place that calls Nemotron/OpenRouter. Both `make_lesson.py`
  and `build_book.py` import from it.
- **Phase 2 is done.** `project_provider.py` writes a canonical
  `project.json` manifest at the end of every `build_book.py` run.
  Tested by `test_project_provider.py`.
- **Phase 3 is done.** `image_provider.py` wraps Pollinations.ai and is
  shared by both `make_lesson.py` and `build_book.py`.
- All shared modules (`content_provider.py`, `image_provider.py`,
  `project_provider.py`) are tested with mocked/temp-dir tests — no
  API key or network needed to run any of them.
- `.github/workflows/test.yml` runs `python -m pytest -v` on every
  push/PR to `main` — generic, picks up any `test_*.py` automatically.
- `ARCHITECTURE.md` was missing from the repo until 2026-08-22 (existed
  only in HANDOFF references) — it now exists and documents the full
  phase plan. Read it before doing anything beyond Phase 3.
- **Phase 4 (first real book, end to end) has NOT been started.** No
  book has been produced end-to-end yet. This is the actual next step —
  not more infrastructure. See `ARCHITECTURE.md` for why.

## Rules for anyone (or anything) working on this repo

- **Read `ARCHITECTURE.md`'s phase list before writing code.** If it's
  stale (doesn't match what's actually in the repo), fix the doc as
  part of your change — don't leave the next person/session to
  rediscover the gap.
- **Work one phase at a time, in order.** Do not design or build ahead
  into later phases "while you're in there," even if a plan or prompt
  from another session asks for it.
- **A phase is done when the duplication/gap it targets is actually
  gone from the repo**, not when a new file merely exists alongside
  the old one.
- **Add or update a test when you change shared logic**
  (`content_provider.py`, `image_provider.py`, `project_provider.py`,
  and any future shared module). Mock external calls — no test should
  need a real API key or network to run.
- **No dashboard, no Canva, no video, no multi-product plugin system**
  until Phase 7 is reached and re-scoped for real, with actual usage
  behind it. If a plan or prompt asks for these earlier, that's a
  scope violation — flag it, don't build it. (This was tested on
  2026-08-22 when a full orchestrator/provider-registry/dashboard
  vision doc was proposed from another session and correctly rejected —
  see `ARCHITECTURE.md`.)
- **Don't claim a change works without running the tests.**
  `python -m pytest -v` locally, or check the Actions tab after pushing.
- This repo owner (Zia) is a non-coder working browser-only (GitHub web
  editor, no terminal). GitHub's write API returns 403 on this repo for
  automated tools — if you're an AI assistant hitting that, give Zia
  the exact web-editor URL (`.../edit/main/<path>` or
  `.../new/main?filename=<path>`) plus the full file content to paste,
  never a partial diff or "find this line" instruction.

## Next up (in order)

1. **Phase 4: pick one real book concept and run it fully through
   `build_book.py`.** Walk the manual steps (proofing, Amazon Print
   Previewer, KDP category/keyword selection, upload) by hand. This is
   the actual bottleneck right now, not more code.
2. Phase 5: KDP metadata + upload prep, informed by what Phase 4 finds.

## Footer

Content generation pipeline — topic to finished deck/book. © 2026.
