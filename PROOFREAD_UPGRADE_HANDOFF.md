# Proofreading upgrade - handoff (updated 2026-10-20)

Owner: Zia. The work happens in `aliwaziri10/Voxel`, not here. Read `PROOFREAD_UPGRADE_HANDOFF.md` and `PROOFREAD_RULES.md` in that repo first; this file is only a pointer plus what is specific to this repo.

## This repo
- Role for this task: reference copy. Book 1 (`novels/where-the-frost-doesnt-reach/`) is read-only. Do not edit or scan it.
- Has an older `humanizer.py` only. No proofreader, no `scripts/` folder. Changed here: added this file and `PROOFREAD_RULES.md`.
- Existing `HANDOFF.md` is picture-book focused and partly stale. Left untouched on purpose.

## Decision
Zia adopted the 10 rules in `PROOFREAD_RULES.md` as his official proofreading parameters on 2026-10-20.

## Status (verified 2026-10-20)
- All manuscript proofreading code lives in `aliwaziri10/Voxel` (`scripts/proofread_novel.py`, `scripts/manuscript_qa.py`, `proofreader.py`, `humanizer.py`).
- New read-only engine there: `scripts/proofread_core.py` plus tests (28 passed locally). Every check is tagged to one of the 10 rules. It refuses frozen published books.
- Not checked: GitHub Actions result. Not done: any real book scanned.

## Next (in aliwaziri10/Voxel)
Dry run on one confirmed-unpublished book, then LanguageTool with caching, hyphen-compound checks, continuity ledger, and a replacement `proofread.yml` handed to Zia as a full file.

## Rules
Strictly free tier. Browser-only for Zia. Claude cannot edit `.github/workflows/`. Re-fetch files before trusting any note.
