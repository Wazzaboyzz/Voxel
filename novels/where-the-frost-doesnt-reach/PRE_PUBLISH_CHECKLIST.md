# PRE-PUBLISH CHECKLIST — TASK HANDOFF FOR NEXT SESSION

**Read this file first if Zia says "check if the novel is ready to publish," "run the checks," or anything about pre-publish quality.** This is the punch list of everything still open after the Sept 2026 full-book audit. HANDOFF.md in this same folder has the chapter-by-chapter status table (word counts, done/not-done) — this file is specifically the QUALITY/SAFETY checklist that sits on top of that.

## Already done — do not redo
- All 45 chapter files confirmed to exist, correctly numbered, non-empty (chapter_01.md through chapter_45.md).
- Zero em dashes confirmed across all 45 chapters.
- Ch.8 name collision (Caleb's grandfather Warren Reyes → Silas Reyes) fixed and confirmed — only occurrence in the manuscript.
- Ch.1-3 canon decision resolved — GitHub's current versions are final, `Ch_1_to_10_expanded.zip` is dead, ignore it.
- Word counts re-verified against actual file content for all 45 chapters (see HANDOFF.md table).

## TASK 1 — Style-originality check — DONE, no concern found
Result: checked. The no-em-dash rule is Zia's own stated stylistic preference (confirmed directly by Zia), not something borrowed from any other author, and should not be flagged again as a possible imitation signal.

On the broader question of whether the manuscript reads as an imitation of a specific bestselling author (the earlier note suspected Nora Roberts): no real resemblance found. "Independent heroine, guarded-but-charming hero, small-town setting, family/romance/suspense interwoven" is a description of the entire romantic suspense genre, not a signature unique to one author — it applies to dozens of bestselling names in the category. If anything, the no-em-dash constraint pushes this manuscript's sentence rhythm further from Roberts' voice specifically, since her prose leans on em dashes and semicolons for rhythm breaks; this manuscript builds the same kind of pacing through longer comma-linked clauses instead, which is a structurally different technique. Conclusion: false flag, no voice pass needed. Closed.

## TASK 2 — Full character-name collision audit
Only one collision (Warren Reyes/Silas Reyes) has ever been checked, and it was found and fixed. No one has checked EVERY character name across all 45 chapters against every other character name for accidental duplicates or near-duplicates.

Steps:
1. Extract every proper name that appears across chapter_01.md through chapter_45.md (grep for capitalized words is a rough start; a full pass should distinguish character names from place names).
2. Cross-reference architecture.md's continuity log for any names it flags as reserved/resolved.
3. Flag any name reused for two different characters/entities, or any name close enough to cause reader confusion (e.g., two characters named similarly).

## TASK 3 — Real-person name check — DONE, no concern found
Checked main and named side-character full names (Mara Voss, Caleb Reyes, Thomas Voss, Odette, Wren Castellano, Dev, Priya Nair, Yusuf, Ambrose Kell, Adelaide Whitlock, Corinne, Silas Reyes, Warren) against real, identifiable public figures via web search. No exact or close matches to any real named person found. Closed.

## TASK 4 — Full continuity read-through (already flagged in HANDOFF.md, repeated here for visibility)
- Read chapters 4-9 against final ch.3 for continuity (now unblocked since ch.1-3 canon is settled) — fix any mismatches.
- Full read-through of all 45 chapters for voice consistency (Mara: dry, controlled, engineering-metaphor; Caleb: steady, plainspoken) and plot contradictions.
- This should happen AFTER the expansion/trim pass (see HANDOFF.md Revision pass item 4) so it's not done twice — under-target chapters will still be getting new material added.

## TASK 5 — AI-authorship tell check
Standing rule says "no signs of AI/Claude authorship in the prose itself" but this has never actually been audited — it's an intention stated in HANDOFF.md and beat_map_45ch.md, not a checked box. Read for common AI prose tells: repetitive sentence structures ("not just X, but Y"), over-explained emotional beats, excessive triadic lists, overuse of certain connective phrases. Flag any chapters that read as noticeably more "AI-smooth" than others.

## TASK 6 — KDP publishing-format requirements
Nothing in this repo yet addresses actual Amazon KDP submission requirements. Before publishing:
1. Front matter (title page, copyright page, dedication if any).
2. Table of contents.
3. Confirm chapter break formatting will render correctly in KDP's converter (check against the ch.20 paragraph-break bug pattern found earlier — that kind of formatting artifact should be checked for elsewhere too, not just assumed fixed everywhere because it was fixed in ch.20).
4. Trim size / manuscript formatting settings.
5. Metadata: title "Where the Frost Doesn't Reach", series "The Amity Falls Series, Book 1", author name/pen name Zia wants on the cover — NOT YET CONFIRMED, ask Zia.
6. Cover design — not yet discussed anywhere in this repo.

## Priority order recommended for next session
1. ~~Task 1 (style-originality)~~ — DONE, closed, no concern.
2. ~~Task 3 (real-person name check)~~ — DONE, closed, no concern.
3. Task 2 (name collision audit) — moderate effort, should happen before further continuity work.
4. HANDOFF.md's expansion/trim pass (word counts) — the bulk of remaining creative work.
5. Task 4 (continuity read-through) — after expansion pass, not before.
6. Task 5 (AI-tell check) — after continuity read-through, since new/expanded text should be checked too.
7. Task 6 (KDP formatting) — last, once text is final.

## Update this file
Whoever picks up any task above should mark it DONE with a one-line result summary, the same way HANDOFF.md's status table works — don't just delete the task, log the outcome so it isn't re-run from scratch next time.
