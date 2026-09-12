# PRE-PUBLISH CHECKLIST — TASK HANDOFF FOR NEXT SESSION

**Read this file first if Zia says "check if the novel is ready to publish," "run the checks," or anything about pre-publish quality.** This is the punch list of everything still open after the Sept 2026 full-book audit. HANDOFF.md in this same folder has the chapter-by-chapter status table (word counts, done/not-done) — this file is specifically the QUALITY/SAFETY checklist that sits on top of that.

## Already done — do not redo
- All 45 chapter files confirmed to exist, correctly numbered, non-empty (chapter_01.md through chapter_45.md).
- Zero em dashes confirmed across all 45 chapters (re-verified this session with a fresh full-corpus scan).
- Ch.8 name collision (Caleb's grandfather Warren Reyes → Silas Reyes) fixed and confirmed — only occurrence in the manuscript.
- Ch.1-3 canon decision resolved — GitHub's current versions are final, `Ch_1_to_10_expanded.zip` is dead, ignore it.
- Word counts re-verified against actual file content for all 45 chapters (see HANDOFF.md table).
- **Critical formatting bug found and fixed (earlier session):** chapter_04.md and chapter_20.md were stored in the repo as raw Base64-encoded text instead of plain markdown (silent corruption, likely from an earlier upload/encoding mishap). Both decoded, verified against original prose, and re-pushed as plain text. **Recommend spot-checking any newly-uploaded chapter file for this same issue going forward** — a base64 file looks like garbled text (starts with "Iy..." for chapters, since that's "# " encoded) rather than throwing an error, so it's easy to miss without opening the raw file.

## TASK 1 — Style-originality check — DONE, no concern found
Result: checked. The no-em-dash rule is Zia's own stated stylistic preference (confirmed directly by Zia), not something borrowed from any other author, and should not be flagged again as a possible imitation signal. No real resemblance found to any single bestselling author's signature voice; "independent heroine, guarded-but-charming hero, small-town setting, family/romance/suspense interwoven" is genre-wide, not one author's fingerprint. Closed.

## TASK 2 — Full character-name collision audit — DONE, 2 real issues found and fixed
1. **FIXED:** "Constance Aldridge" (ch.32) vs. "Constance Oakes" (ch.36) — renamed board chair to **Marjorie Oakes** throughout ch.36.
2. **FIXED:** "Priti" (minor character, ch.4/ch.44) too phonetically close to "Priya" — renamed to **Renata** throughout both chapters.
No further collisions found. Closed.

## TASK 3 — Real-person name check — DONE, no concern found
Checked all named characters against real public figures. No matches. Closed.

## TASK 4 — Full continuity read-through — PARTIALLY DONE (targeted checks only, not a full line-by-line read)
- **FIXED:** ch.38 said "ten years" for a timespan every other chapter (ch.23, 32, 33, 39) establishes as "forty years." Corrected to match canon.
- Cross-checked "eight years"/"two years" figures for consistency — no contradictions found.
- **STILL OPEN, needs a dedicated session:** full line-by-line read of chapters 4-9 against final ch.3 canon, plus a full 45-chapter read purely for voice consistency and subtler plot contradictions (tone drift, a character knowing something too early, small prop/detail inconsistencies). ~88,000+ words — needs unhurried sequential reading, not a grep-based pass. Do this AFTER Task 5's rewrite is complete, so newly-touched prose gets checked too, not before.

## TASK 5 — AI-authorship tell check — IN PROGRESS, chapters 1-27 fixed/verified, 28-45 remaining
Diagnostic (earlier session) found "the particular ___" / "the specific ___" as the dominant tell — ~189 combined occurrences across the manuscript, heaviest in ch.18 (8), ch.14 (7), ch.29/31/32 (6 each). Fix approach: read each chapter, replace or cut each instance individually so the sentence still reads naturally — this is a line-edit, NOT a find-and-replace. **A regex/script fix was considered and explicitly rejected**: mechanically stripping "the particular "/"the specific " breaks sentence grammar in many cases (confirmed by testing on ch.15's drawer sentence, which needed restructuring, not deletion). Every fix in ch.1-27 was written and reviewed individually. Any future session should keep doing this by hand, chapter by chapter — do not attempt a scripted bulk replace across the remaining chapters. (A pure detection/audit script — no rewriting — was also tried to speed up scoping; it failed on a 403 from GitHub's API due to lacking authentication in the sandbox environment. Not worth re-attempting: the actual bottleneck is the line-edit judgment per instance, not finding the instances, which a manual grep-per-chapter already does reliably.) Note: not every chapter has instances — ch.10 and ch.24 were both found clean (0 instances) on inspection, which is expected and fine; log a chapter as DONE/0 rather than skipping it.

**IMPORTANT — the "1-13 not itemized, spot-check if in doubt" note from an earlier version of this file was a real risk, not just caution-language: ch.8 was individually spot-checked this session and DID have one missed instance ("that specific hush") that the original prior-session pass overlooked. It's fixed now, but this proves the un-itemized range cannot be assumed clean. Chapters 1-7, 9, and 11-13 have NOT yet been individually re-verified — they were part of the original "prior session" claim but have not been spot-checked the way 8 and 10 just were. Treat that range as unverified, not confirmed, until someone actually re-checks each one.**

**Progress log (update this table as you go — don't just say "done," log the count per chapter so nobody re-scans a clean chapter):**

| Chapter | Status | Instances fixed |
|---|---|---|
| 1-7, 9, 11-13 | UNVERIFIED — claimed done in an earlier, un-itemized session note, but not individually re-checked. Do not assume clean. | unknown |
| 8 | DONE — re-verified this session, found and fixed 1 additional missed instance ("that specific hush") beyond the original prior-session pass | 1 (this session) + unknown prior |
| 10 | DONE — spot-checked this session, confirmed genuinely clean | 0 |
| 14 | DONE (prior session) | 7 |
| 15 | DONE | 6 |
| 16 | DONE | 2 |
| 17 | DONE | 2 |
| 18 | DONE | 8 |
| 19 | DONE | 4 |
| 20 | DONE | 5 |
| 21 | DONE | 5 |
| 22 | DONE | 4 |
| 23 | DONE | 6 |
| 24 | DONE | 0 (already clean, no edit needed) |
| 25 | DONE | 2 |
| 26 | DONE | 2 |
| 27 | DONE | 2 |
| 28-45 | NOT STARTED | — continue here, at chapter 28 |

**Next session: two things need doing, not just one.** (1) Continue the primary pass forward at chapter 28 through 45, same method as ch.15-27 (fetch chapter → grep for "the particular"/"the specific" → rewrite each instance for natural phrasing → push with a commit message noting the count fixed → update this table). (2) Go back and individually spot-check chapters 1-7, 9, and 11-13 the same way ch.8 and ch.10 just were — don't trust the old "prior session" claim at face value, since ch.8 already proved it was incomplete once.

Also worth checking once the "the particular/specific" pass is complete: the other tells found in the original diagnostic ("the kind of ___" 69 occurrences, "found herself/himself" 45, "in a way that" 41, "something in her/his [face/voice/eyes]" 32, "understood that" 12) were NOT in scope for this pass and remain fully unaddressed — flag as a possible Task 5b if Zia wants the manuscript further cleaned after the primary pass finishes.

## TASK 6 — KDP publishing-format requirements — STILL OPEN, not started
1. Front matter (title page, copyright page, dedication if any).
2. Table of contents.
3. Confirm chapter break formatting will render correctly in KDP's converter (the base64-encoding bug found in ch.4/ch.20 is a reminder to spot-check raw file content, not just assume plain text everywhere).
4. Trim size / manuscript formatting settings.
5. Metadata: title "Where the Frost Doesn't Reach", series "The Amity Falls Series, Book 1", author name/pen name Zia wants on the cover — NOT YET CONFIRMED, ask Zia.
6. Cover design — not yet started in this repo. Track in a new `cover_design.md` in this same folder if that work begins.

## Priority order recommended for next session
1. **Task 5 — continue the AI-tell rewrite pass starting at chapter 28, AND go back to spot-check chapters 1-7, 9, 11-13** (this is the single actionable, well-defined, in-progress task — pick this up first, do the forward pass and the backward spot-check both).
2. Task 4's full continuity/voice read-through — after Task 5 is fully complete.
3. HANDOFF.md's expansion/trim pass (word counts) — can run in parallel with Task 5/4 since it's independent chapter-level work, but don't let it distract from finishing Task 5 once started.
4. Task 6 (KDP formatting) — last, once text is final. Cover design can proceed in parallel since it doesn't depend on final interior text.

## Update this file
Whoever picks up any task above should mark it DONE with a one-line result summary and update the Task 5 progress table above as they go — don't just delete the task, log the outcome so it isn't re-run from scratch next time.
