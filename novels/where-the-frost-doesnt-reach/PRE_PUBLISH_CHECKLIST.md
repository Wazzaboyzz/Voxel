# PRE-PUBLISH CHECKLIST — TASK HANDOFF FOR NEXT SESSION

**Read this file first if Zia says "check if the novel is ready to publish," "run the checks," or anything about pre-publish quality.** This is the punch list of everything still open after the Sept 2026 full-book audit. HANDOFF.md in this same folder has the chapter-by-chapter status table (word counts, done/not-done) — this file is specifically the QUALITY/SAFETY checklist that sits on top of that.

## Already done — do not redo
- All 45 chapter files confirmed to exist, correctly numbered, non-empty (chapter_01.md through chapter_45.md).
- Zero em dashes confirmed across all 45 chapters (re-verified this session with a fresh full-corpus scan).
- Ch.8 name collision (Caleb's grandfather Warren Reyes → Silas Reyes) fixed and confirmed — only occurrence in the manuscript.
- Ch.1-3 canon decision resolved — GitHub's current versions are final, `Ch_1_to_10_expanded.zip` is dead, ignore it.
- Word counts re-verified against actual file content for all 45 chapters (see HANDOFF.md table).
- **NEW THIS SESSION — critical formatting bug found and fixed:** chapter_04.md and chapter_20.md were stored in the repo as raw Base64-encoded text instead of plain markdown (silent corruption, likely from an earlier upload/encoding mishap). Both decoded, verified against original prose, and re-pushed as plain text. This would have broken KDP conversion silently if not caught. **Recommend spot-checking any newly-uploaded chapter file for this same issue going forward** — a base64 file looks like garbled text (starts with "Iy..." for chapters, since that's "# " encoded) rather than throwing an error, so it's easy to miss without opening the raw file.

## TASK 1 — Style-originality check — DONE, no concern found
Result: checked. The no-em-dash rule is Zia's own stated stylistic preference (confirmed directly by Zia), not something borrowed from any other author, and should not be flagged again as a possible imitation signal.

On the broader question of whether the manuscript reads as an imitation of a specific bestselling author (the earlier note suspected Nora Roberts): no real resemblance found. "Independent heroine, guarded-but-charming hero, small-town setting, family/romance/suspense interwoven" is a description of the entire romantic suspense genre, not a signature unique to one author — it applies to dozens of bestselling names in the category. If anything, the no-em-dash constraint pushes this manuscript's sentence rhythm further from Roberts' voice specifically, since her prose leans on em dashes and semicolons for rhythm breaks; this manuscript builds the same kind of pacing through longer comma-linked clauses instead, which is a structurally different technique. Conclusion: false flag, no voice pass needed. Closed.

## TASK 2 — Full character-name collision audit — DONE, 2 real issues found and fixed
Ran a full-corpus proper-noun extraction across all 45 chapters (frequency + chapter-spread analysis). Findings:

1. **FIXED — real collision:** "Constance Aldridge" (retired schoolteacher, ch.32) and "Constance Oakes" (county board chair, ch.36) were two entirely unrelated characters sharing the first name "Constance." Renamed the board chair to **Marjorie Oakes** throughout ch.36 (3 occurrences fixed).
2. **FIXED — near-duplicate causing likely reader confusion:** "Priti" (Mara's minor Chicago colleague/project lead, ch.4 and ch.44 only) was phonetically very close to "Priya" (Priya Nair, a major recurring character). Renamed the minor character to **Renata** throughout both chapters (5 occurrences fixed total).
3. Checked and confirmed NOT a collision: "Del" (consistent nurse/caretaker character at Rosewood Care, ch.6/38/42), "Rosewood" (place name, consistent), "Ferris" (family name, consistent references), "Denise" (Mara's cousin, consistent), "Eleanor" (Mara's grandmother, single character, no clash).

No further collisions found in the remaining name list (Mara, Caleb, Kell/Ambrose, Priya, Odette, Dev, Wren, Thomas, Yusuf, Frey/Elias, Whitlock/Adelaide, Voss, Reyes, Nair, Castellano, Toll). Closed.

## TASK 3 — Real-person name check — DONE, no concern found
Checked main and named side-character full names (Mara Voss, Caleb Reyes, Thomas Voss, Odette, Wren Castellano, Dev, Priya Nair, Yusuf, Ambrose Kell, Adelaide Whitlock, Corinne, Silas Reyes, Warren, Marjorie Oakes, Renata, Constance Aldridge, Del) against real, identifiable public figures via web search. No exact or close matches to any real named person found. Closed.

## TASK 4 — Full continuity read-through — PARTIALLY DONE this session (targeted checks, not a full line-by-line read)
What was checked and fixed this session:
- **FIXED — real continuity error:** ch.38 stated "my grandfather spent ten years of his life chasing a hunch" about Kell/Whitlock. Every other chapter that references this (ch.23, ch.32, ch.33, ch.39) consistently establishes it as **forty years**. Corrected ch.38 to "forty years" to match established canon.
- Cross-checked "eight years" (Mara's time away) and "two years" (Caleb's memory gap) for count consistency across all chapters that reference them — no contradictions found in the specific figures used.
- NOT yet done (still open, genuinely needs a dedicated session): a full line-by-line read-through of chapters 4-9 against the final ch.3 canon (flagged as an open risk since these were originally written to follow a REJECTED ch.3 draft), and a full read of all 45 chapters purely for voice consistency and subtler plot contradictions that a targeted grep-based check can't catch (tone drift, a character knowing something they shouldn't yet, small prop/detail inconsistencies). This is a genuinely large task — 88,000+ words — and deserves unhurried, sequential reading rather than being rushed. Recommend scheduling as its own session.

## TASK 5 — AI-authorship tell check — DONE (diagnostic pass), fix NOT yet done
Ran a frequency analysis across the full manuscript for common AI-prose crutch phrases. Results (total occurrences across all 45 chapters):
- "the particular ___": **135 occurrences** (~3.0 per chapter)
- "the kind of ___": **69 occurrences** (~1.5 per chapter)
- "the specific ___": **54 occurrences** (~1.2 per chapter)
- "found herself/himself": **45 occurrences**
- "in a way that": **41 occurrences**
- "something in her/his [face/voice/eyes]": **32 occurrences**
- "understood that": **12 occurrences**

This is a real, measurable tell — "the particular X" / "the specific X" together account for nearly 200 instances, which is a noticeably repetitive intensifier pattern a human editor would flag. Highest-density chapters for "the particular": ch.18 (8), ch.14 (7), ch.29/31/32 (6 each) — worth starting there if doing a manual variety pass.

**This was NOT fixed this session** — rewriting ~200+ instances across 45 chapters to vary the phrasing is a substantial line-edit task in its own right, not something to rush through alongside everything else checked this session. Recommend a dedicated editing pass, chapter by chapter, replacing repeated constructions with varied phrasing (or simply cutting the intensifier and trusting the plain sentence).

## TASK 6 — KDP publishing-format requirements — STILL OPEN, not started
Nothing in this repo yet addresses actual Amazon KDP submission requirements. Before publishing:
1. Front matter (title page, copyright page, dedication if any).
2. Table of contents.
3. Confirm chapter break formatting will render correctly in KDP's converter. (The base64-encoding bug found and fixed this session in ch.4/ch.20 is a good reminder to spot-check raw file content generally before trusting any chapter is publish-ready, not just assume plain text everywhere.)
4. Trim size / manuscript formatting settings.
5. Metadata: title "Where the Frost Doesn't Reach", series "The Amity Falls Series, Book 1", author name/pen name Zia wants on the cover — NOT YET CONFIRMED, ask Zia.
6. Cover design — Zia is moving into front/back cover design work directly after this checklist session (as of this note). Track cover decisions in a new file if that work starts, e.g. `cover_design.md` in this same folder.

## Priority order recommended for next session
1. ~~Task 1 (style-originality)~~ — DONE, closed.
2. ~~Task 3 (real-person name check)~~ — DONE, closed.
3. ~~Task 2 (name collision audit)~~ — DONE, closed, 2 fixes made.
4. HANDOFF.md's expansion/trim pass (word counts) — the bulk of remaining creative work; 9 chapters still under the 1,800-word floor as of this session (see HANDOFF.md table).
5. Task 4 (full continuity read-through) — genuinely still open, needs a dedicated session, targeted checks this session are not a substitute.
6. Task 5 (AI-tell rewrite pass) — diagnosed this session, not fixed; do after continuity pass so newly-touched text gets checked too.
7. Task 6 (KDP formatting) — last, once text is final. Cover design can proceed in parallel since it doesn't depend on final interior text.

## Update this file
Whoever picks up any task above should mark it DONE with a one-line result summary, the same way HANDOFF.md's status table works — don't just delete the task, log the outcome so it isn't re-run from scratch next time.
