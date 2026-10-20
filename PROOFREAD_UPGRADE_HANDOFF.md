# Proofreading upgrade - handoff (2026-10-20)

Owner: Zia. The work happens in `aliwaziri10/Voxel`, not here. Read `PROOFREAD_UPGRADE_HANDOFF.md` in that repo first; this file is only a pointer plus what is specific to this repo.

## This repo
- Role for this task: reference copy. Book 1 (`novels/where-the-frost-doesnt-reach/`) is read-only. Do not edit or scan it.
- Has an older `humanizer.py` only. No proofreader, no `scripts/` folder. Nothing was changed here except adding this file.
- Existing `HANDOFF.md` is picture-book focused and partly stale. Left untouched on purpose.

## Summary of findings (verified 2026-10-20)
- All manuscript proofreading code lives in `aliwaziri10/Voxel` (`scripts/proofread_novel.py`, `scripts/manuscript_qa.py`, `proofreader.py`, `humanizer.py`).
- New read-only engine added there: `scripts/proofread_core.py` plus tests. It refuses frozen published books.
- Open question for Zia: what are his "10 parameters"? Not found in any repo.

## Next (in aliwaziri10/Voxel)
Dry run on one new unpublished book, then add LanguageTool with caching, Chicago 18 checks, continuity ledger, and a replacement `proofread.yml` handed to Zia as a full file.

## Rules
Strictly free tier. Browser-only for Zia. Claude cannot edit `.github/workflows/`. Re-fetch files before trusting any note.
