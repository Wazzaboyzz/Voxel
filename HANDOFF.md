# Voxel — Handoff

Read this first if you're new to this repo (human or AI). It tells you
where things stand and how to not break what's already here.

## Read in this order

1. `README.md` — what Voxel does today, setup, known limitations.
2. `ARCHITECTURE.md` — the phased build plan.
3. This file — process rules and current status.

## START HERE — Phase 8c, 2026-09-13 session (first real end-to-end run)

**This is the most current section. Read this before anything else below.**

The one-command pipeline (`voxel_cli.py book`) was run for real for the
first time ever this session, via the `voxel-book.yml` GitHub Actions
workflow (browser-triggered — see the browser-only rule further down).
Two bugs were found and one is fixed; one needs Zia's decision before
anyone continues.

**FIXED, confirmed live in code (not yet re-verified by a real run):**
- `content_provider.py`: `NVIDIA_MODEL` default
  (`nvidia/llama-3.1-nemotron-70b-instruct`) was 404ing — retired from
  NVIDIA's catalog. Swapped default to `nvidia/nemotron-3-super-120b-a12b`
  (commit `29c2ec5`). **This got the manuscript generation stage working
  end-to-end for the first time** — a real 26-page manuscript was
  generated and passed through the humanizer, and print-ready PDFs +
  `project.json` were produced and uploaded as a workflow artifact.
  Not yet re-run since the fix to double-confirm the new model id holds.
- `.github/workflows/voxel-book.yml`: added `permissions: contents:
  write` at the workflow level (commit landed via Zia pasting into the
  GitHub web editor — **the GitHub App/OAuth connector used by AI
  assistants in this session could NOT write to anything under
  `.github/workflows/` directly, even though it had full write access
  everywhere else in the repo — that path needs GitHub's separate
  `workflow` OAuth scope, which this connector doesn't have. Any future
  change to a workflow YAML file will hit the same 403 and must go
  through Zia pasting it into the browser editor, not a direct API
  write.** This fixes the `git push` 403 seen in the "Commit updated
  story bible" step (was denied to `github-actions[bot]` before this).

**NOT FIXED — decision needed before continuing, DO NOT set up billing
without asking Zia first:**
- Every single image generation call (all 26/26) failed with `429 Too
  Many Requests` against `generativelanguage.googleapis.com`'s
  `gemini-2.5-flash-image` model, on the very first attempt, despite
  `image_provider.py` already having a 2s polite delay between calls.
  100%-immediate-failure across every call (not intermittent) points to
  a hard block, not real rate limiting. Checked live in Google AI
  Studio (aistudio.google.com/api-keys): the `GEMINI_API_KEY` in use
  (labelled "VOXEL ON WAZZABOYZZ") is on **Free tier with no billing
  set up**. `gemini-2.5-flash-image` most likely requires a linked
  billing account to serve any requests at all, even at near-zero
  actual cost.
- **Zia's explicit standing rule (confirmed this session, matches the
  cross-pipeline Atlas Frame rule): strictly free tier only, no billing,
  no paid elements, anywhere.** So linking billing is OFF THE TABLE —
  do not suggest it again, do not set it up even if asked casually.
- **The actual right fix**: switch `image_provider.py` back to a truly
  free image source. This also finally reconciles a stale-doc mismatch
  that's been flagged for a while (see below) — README.md,
  `build_book.py`, and `make_lesson.py` already (incorrectly) claim
  images come from "Pollinations.ai, free, no key required," but the
  real code calls Gemini. Making that true again (swap
  `image_provider.py`'s implementation to actually call Pollinations,
  or another genuinely-free-tier image API) is the next concrete task —
  not attempted yet this session, ran out of context budget.
- Once that's done, re-run `voxel-book.yml` (small page count, e.g. 4,
  for a fast test) and confirm images actually generate before trusting
  a full 26-page run.

## Where things actually stand (Phase 8, dating below may be inaccurate — see Phase 8c above for what's current)

**Note on this file's own dating:** the header above previously said
"updated 2026-09-13" for the whole Phase 8 write-up below, but Zia has
since said the original Phase 8 handoff was actually written roughly two
months before today (2026-09-13) — only the Phase 8b and 8c edits
(NVIDIA key section, and the section above) genuinely happened today.
Nobody has reconciled which internal dates in the Phase 8 section itself
are accurate. Don't trust "2026-09-13" elsewhere in this file as the
actual authorship date for anything except the Phase 8b/8c additions —
verify against git commit history if the exact date of a specific
change ever matters.

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
  To use it, set `NVIDIA_API_KEY` as a repo secret (for the
  `voxel-book.yml` / `voxel-novel.yml` Actions workflows, which already
  reference it) or as a local environment variable. If the model id
  `NVIDIA_MODEL` defaults to ever 404s again, check
  https://build.nvidia.com for the current catalog and override via the
  `NVIDIA_MODEL` env var (see Phase 8c above — this already happened
  once).
- **Phase 8c: see the section above — first real end-to-end run,
  NVIDIA/permissions fixes landed, image generation blocked pending a
  genuinely-free image source.**

### Files added in Phase 8

- **`voxel_cli.py`** — the single command Zia asked for.
  - `python voxel_cli.py book --concept "..." --pages 26 --series luna`
    generates a full illustrated picture book: manuscript → humanizer
    pass → images → print-ready interior/cover PDFs → project.json.
    Wraps `build_book.py`'s existing pipeline rather than duplicating it.
  - `python voxel_cli.py novel --series amity-falls --book "Book 2" --chapters 45 --brief "..."`
    generates a chapter-by-chapter prose novel/sequel, one `.md` file per
    chapter plus a compiled manuscript, under `novels/<series>/<book-slug>/`.
    `--commit` will `git add/commit/push` using whatever git login is
    already configured on the machine running it (no token handled by
    the script itself).
- **`humanizer.py`** — AI-tell scan + rewrite pass. Design (not code)
  borrowed from researched public repos: Aaron-Bushnell/humanizer
  (pattern-lint list + "content integrity gate" concept), Aboudjem/humanizer-skill
  (0-100 score), maximsmd/Humanizer (fact-preservation framing). The scan
  step is fully offline (regex-based, no API key, no network) so it costs
  nothing to run. Confirmed running for real this session as part of the
  first successful pipeline run. The rewrite step reuses the existing
  OpenRouter call — no new API/dependency introduced. Has an integrity
  gate: if a rewrite would drop a number, date, or proper name, the
  original text is kept and the page/chapter is flagged in
  `project.json` / console output instead of silently losing a fact.
- **`story_bible.py`** — one JSON file per series under `story_bibles/`
  (git-tracked). Tracks characters, visual style, established plot facts,
  and prior books in a series. `voxel_cli.py` reads it before generating
  a sequel (so Book 2 doesn't contradict Book 1) and writes to it after
  each run. Idea borrowed from `learfinance0705/bookframes`'s
  style-bible/character-reference step; no code copied.
- **`content_provider.py`** — added `generate_novel_chapter()` (plain
  prose, not JSON, for novel-length work) and `call_raw()` (exposed for
  `humanizer.py`'s rewrite step). Existing `generate_manuscript()` now
  takes an optional `continuity_block` param. (Also added the
  `NVIDIA_API_KEY` support under Phase 8b, and the model-id fix under
  Phase 8c.)

### What was deliberately NOT built (know these before extending)

- **No KDP upload automation.** `voxel_cli.py book` still ends at "here
  are your interior/cover PDFs" — the KDP Print Previewer check and the
  manual listing walk-through (category, keywords, pricing) from the
  original Phase 4 plan below still have to happen by hand. Automating
  that is real future scope, not done here.
- **No story-concept generation.** Both commands require Zia to supply
  the concept/brief. Nothing in this pipeline invents "what the next
  book should be about" — that's intentional; it's his call, not an
  auto-decision.
- **Novels have no cover-art generation wired in.** `voxel_cli.py novel`
  produces text only. If a novel needs a cover, that's still a separate
  manual step (or a follow-up addition to the CLI).
- **The `humanizer.py` pattern list is a starting set (~20 words/phrases),
  not exhaustive.** The researched repos claim 43-55 patterns; this
  session shipped a smaller, testable set rather than porting a huge
  list unverified. Expanding it is low-risk, additive work for a future
  session — just extend `BANNED_WORDS`/`BANNED_PHRASES` in `humanizer.py`.
- **No automated tests added for `humanizer.py`, `story_bible.py`, or
  `voxel_cli.py`.** Per the standing rule below ("add or update a test
  when you change shared logic"), this is a gap — `humanizer.py`'s
  `scan()` function especially is pure and easy to unit test (no mocking
  needed), and should get one before it's trusted on Book 2 of Amity
  Falls or a new Luna sequel.

## Known doc/repo mismatches not yet fixed (flagged, not resolved)

- **`ARCHITECTURE.md`'s "Current state" section is stale.** It still
  says Phase 4 is "NOT STARTED," contradicting this file's own account
  above that Phase 4 shipped (as Luna, off-pipeline). Needs reconciling.
- **README.md, `build_book.py`, and `make_lesson.py` still describe
  images as coming from "Pollinations.ai, free, no key required."**
  `image_provider.py`'s actual code calls Google Gemini
  (`GEMINI_API_KEY` required), not Pollinations — **and per Phase 8c
  above, Gemini's image model needs billing Zia has explicitly ruled
  out, so the fix here is now to make the code match the docs (switch
  to real Pollinations/another free source), not just fix the comment.**
- **`generate_images.py` is a second, disconnected image pipeline.**
  It's a GitHub-Actions-only script (Gemini → Cloudflare/FLUX → hosted
  FLUX fallback chain) that isn't called by `image_provider.py` or
  `voxel_cli.py` at all — only by `.github/workflows/test-image-secret.yml`.
  Worth checking whether its FLUX fallback chain is itself a genuinely
  free path that `image_provider.py` could reuse instead of building a
  third image pipeline from scratch.
- **`video_output.py` (Chatterbox-TTS narrated marketing video) is built
  but never wired into `voxel_cli.py`** and isn't mentioned elsewhere in
  this file. It's a standalone module waiting to be called from
  somewhere.
- **`build-book.yml` is redundant with `voxel-book.yml`.** The former
  calls `build_book.py` directly (bypassing humanizer/story-bible); the
  latter calls `voxel_cli.py book`. Worth deciding whether to keep both
  or retire the older one.
- **`_workflows_scope_test.md` and `_write_access_test.md`** in the repo
  root are leftover connectivity-check files, safe to delete whenever
  someone's in there anyway.

## Rules for anyone (or anything) working on this repo

- **Read `ARCHITECTURE.md`'s "Current state" section before writing
  code.** If it's stale, fix the doc as part of your change.
- **Add or update a test when you change shared logic**
  (`content_provider.py`, `image_provider.py`, `project_provider.py`,
  and now `humanizer.py`, `story_bible.py`). Mock external calls.
- **Don't claim a change works without running the tests.**
  `python -m pytest -v` locally, or check the Actions tab after pushing.
- **Strictly free tier only. No billing, no paid elements, anywhere in
  this pipeline** — confirmed explicitly by Zia 2026-09-13, matches the
  same standing rule across all of Zia's other AI pipelines. Never set
  up or suggest setting up billing on any API key used by this repo,
  even if it would unblock something and stay near-zero cost. If a
  provider requires billing to work at all, treat that provider as not
  usable here and find a genuinely free alternative instead.
- **This repo owner (Zia) works browser-only, including from his phone.
  He does NOT run a terminal/shell/CLI** — he will copy-paste any command
  or file content into a browser interface, but a local-clone terminal
  invocation of `voxel_cli.py` is a last resort only, to be used when no
  browser-based path (e.g. triggering the `voxel-book.yml`/
  `voxel-novel.yml` GitHub Actions workflows via the browser Actions tab)
  exists at all. Design any new workflow/step assuming browser-only
  access first.
- **Files under `.github/workflows/` cannot be written directly by the
  GitHub App/OAuth connector AI assistants use in this session — even
  with full write access to the rest of the repo.** That specific path
  needs GitHub's separate `workflow` OAuth scope. Confirmed via a real
  403 this session (`Resource not accessible by integration`) when
  attempting to edit `voxel-book.yml` directly, despite the same
  connector successfully writing to `content_provider.py` and
  `HANDOFF.md` moments earlier. Any workflow YAML change must be handed
  to Zia as a full file to paste into the GitHub web editor
  (`github.com/Wazzaboyzz/Voxel/edit/main/<path>`), the same as the
  historical repo-wide-403 workaround, but this one is scoped
  specifically to `.github/workflows/*` regardless of the connector's
  general repo permissions.
- **Before attempting any write to this or any other repo, an AI
  assistant must call whatever "get authenticated user" tool it has and
  confirm out loud which GitHub account is currently connected**, then
  actually attempt a real write and check the result rather than
  assuming a past session's account/permission problem still applies.
  `aliwaziri10` is a direct collaborator on this repo with `write` role
  (confirmed via the collaborators API) — logging into GitHub as
  `aliwaziri10` is sufficient to see and trigger this repo's Actions
  workflows too; no account switch to `Wazzaboyzz` is needed for that.

## Original Phase 4 walk-through (superseded by voxel_cli.py above, kept for reference)

1. Pick one real book concept.
2. Run `build_book.py` locally with that concept.
3. Open the output folder, check the PDFs and `project.json` by eye.
4. Run the interior + cover PDFs through Amazon's KDP Print Previewer.
5. Walk KDP's manual listing flow by hand; note repetitive/error-prone
   steps — that becomes future scope.
6. Come back and scope further automation based on what step 5 surfaced.

`voxel_cli.py book` now automates steps 1-3 into one command. Steps 4-5
are still manual and still the right place to learn what to automate next.

## Footer

Content generation pipeline — topic to finished deck/book. © 2026.
