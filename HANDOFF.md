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

- **Phases 1–3 are done.** `content_provider.py` (shared text gen),
  `image_provider.py` (shared image gen), and `project_provider.py`
  (canonical `project.json` per run) are all built, all tested, and
  both `make_lesson.py` and `build_book.py` use them — no duplicated
  logic in either caller. Verified against the live repo on 2026-08-22.
- `test_content_provider.py`, `test_image_provider.py`, and
  `test_project_provider.py` mock every external call (OpenRouter,
  Pollinations) or use a real temp dir (file I/O only) — none need a
  real API key or network to run. 11/11 tests passing as of the last
  CI run.
- `.github/workflows/test.yml` runs the full suite on every push/PR to
  `main`, no filename hardcoded — any `test_*.py` file is picked up
  automatically.
- **Phase 4 (first real book, end to end) has NOT started.** This is
  the actual next step — see below. It is not a code task.

## Rules for anyone (or anything) working on this repo

- **Read `ARCHITECTURE.md`'s "Current state" section before writing
  code.** If it's stale (doesn't match what's actually in the repo),
  fix the doc as part of your change — don't leave the next
  person/session to rediscover the gap.
- **Work one phase at a time, in order.** Don't start Phase 5+ before
  Phase 4 has actually happened. Phase 4 generates the real usage data
  the later phases need to be designed against.
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
  scope violation — flag it, don't build it.
- **Don't claim a change works without running the tests.**
  `python -m pytest -v` locally, or check the Actions tab after pushing.
- This repo owner (Zia) is a non-coder working browser-only (GitHub web
  editor, no terminal). GitHub's write API returns 403 on this repo for
  automated tools — if you're an AI assistant hitting that, give Zia
  the exact web-editor URL (`.../edit/main/<path>` or
  `.../new/main?filename=<path>`) plus the full file content to paste,
  never a partial diff or "find this line" instruction.

## Next up: Phase 4 — first real book, end to end

This is a **run-it-and-watch** task, not a build-it task. The code is
ready; nobody has fed it a real concept and walked the output through
KDP yet, and that's the only way to find out what's actually weak.

Steps, in order:

1. **Pick one real book concept** — a real one you intend to publish,
   not a placeholder. Coloring book or illustrated book, your call.
2. **Run `build_book.py` locally** with that concept (needs
   `OPENROUTER_API_KEY` set, and `reportlab` + `requests` installed —
   see the docstring at the top of `build_book.py` for the exact
   command and flags).
3. **Open the output folder** it creates under `output_books/<name>/`.
   Check the interior PDF and cover PDF by eye. Check `project.json` —
   does it accurately describe what got made?
4. **Run the interior + cover PDFs through Amazon's own KDP Print
   Previewer** (not just eyeballing the PDF) — this is the tool that
   actually catches bleed/margin/spine problems before a real print run.
5. **Walk KDP's manual listing flow by hand**: category selection,
   keyword entry, pricing by region. Note every step that felt
   repetitive or error-prone — that list becomes Phase 5/6's scope,
   not a guess made in advance.
6. Once a real book has actually gone through this once, come back and
   we scope Phase 5 (KDP metadata + upload prep) based on what step 5
   actually surfaced — not before.

## Footer

Content generation pipeline — topic to finished deck/book. © 2026.
