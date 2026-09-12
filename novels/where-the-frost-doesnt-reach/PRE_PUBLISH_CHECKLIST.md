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

## TASK 4 — Full continuity read-through — PARTIALLY DONE, and a REAL PLOT CONTRADICTION FOUND this session, not yet fixed
- **FIXED (earlier):** ch.38 said "ten years" for a timespan every other chapter (ch.23, 32, 33, 39) establishes as "forty years." Corrected to match canon.
- Cross-checked "eight years"/"two years" figures for consistency — no contradictions found.
- **NEW FINDING, UNFIXED — the central mystery's own mechanics contradict themselves across ch.38, ch.39, and ch.43:**
  - Ch.38: Thomas calls Adelaide "Adelaide Whitlock... Ambrose's wife," directly identifying present-day Kell as the same person who was Adelaide's husband a century ago (an immortal who's worn other names, per the "wearing other names the way other men wear coats" line in the same chapter).
  - Ch.39: Kell speaks in the first person about Adelaide coming to *him* directly and *him* being the one who let her disappear — again, Kell IS the century-old husband.
  - Ch.43: Kell says the burden "was simply handed to me" after Ambrose Whitlock "finally disappeared" — now describing Whitlock in the third person as a *different, earlier person* Kell only later succeeded, not a name Kell himself once wore.
  - **These two versions of who Kell is cannot both be true as written.** This needs an editorial decision, not just a wording tweak: either (a) Kell IS Ambrose Whitlock, one immortal man across a century — in which case ch.43's "handed to me" language needs rewriting to stop describing Whitlock in the third person as someone else, or (b) Kell is a successor who inherited the role after the original Whitlock vanished — in which case ch.38 and ch.39 need rewriting to stop having Thomas and Kell both speak as if Kell was literally Adelaide's own husband. **Do not silently pick one and patch the wording without flagging the choice to Zia first** — this changes what kind of villain/mystery the book actually is (one immortal manipulator vs. a chain of successors), so it's a story decision, not a copyedit. As of this session Zia has NOT yet answered which one he wants — still genuinely open.
- **STILL OPEN, needs a dedicated session:** full line-by-line read of chapters 4-9 against final ch.3 canon, plus a full 45-chapter read purely for voice consistency and subtler plot contradictions (tone drift, a character knowing something too early, small prop/detail inconsistencies). The Whitlock/Kell contradiction above was found via a partial, targeted check (ch.29, 38, 39, 43 only) — a full sequential read of the other 41 chapters has NOT happened yet and could easily surface more of this same kind of thing. ~88,000+ words — needs unhurried sequential reading, not a grep-based pass. Do this AFTER Task 5's rewrite is complete, so newly-touched prose gets checked too, not before.

## TASK 5 — AI-authorship tell check — IN PROGRESS, chapters 1, 8, 10, 14-27 fixed/verified, 2-7, 9, 11-13, 28-45 remaining
Diagnostic (earlier session) found "the particular ___" / "the specific ___" as the dominant tell — ~189 combined occurrences across the manuscript, heaviest in ch.18 (8), ch.14 (7), ch.29/31/32 (6 each). Fix approach: read each chapter, replace or cut each instance individually so the sentence still reads naturally — this is a line-edit, NOT a find-and-replace.

**IMPORTANT CONTEXT, discovered this session — read before continuing:** ch.1 (Zia's own hand-written text, not AI-generated) turned out to ALSO use "this/that/a particular/specific X" repeatedly (4 instances found). This means the phrase is likely Zia's own authorial habit, not proof of AI authorship on its own — the AI-written expansion chapters may simply have picked up and continued an established voice from his own ch.1-3, which is actually good continuity, not a flaw. **Zia was told this explicitly and, after considering it, decided to proceed with removing the phrase anyway, including from his own ch.1-3.** Ch.1 has now been fixed on that basis (3 narration instances removed; the phrase was left alone in ch.1's one line of dialogue, and left alone where it was being used as an ordinary, non-repetitive adjective rather than the flagged pattern — e.g. "a specific sound" naming an actual sound stayed as-is). Apply this same judgment across the rest of the book: fix the narration pattern, leave dialogue and genuinely natural uses of "specific"/"particular" alone. Ch.2 and ch.3 have NOT yet been checked under this newly-expanded scope — check them like any other chapter, don't assume "Zia's own text" means skip them anymore.

**A regex/script fix was considered and explicitly rejected**: mechanically stripping "the particular "/"the specific " breaks sentence grammar in many cases (confirmed by testing on ch.15's drawer sentence, which needed restructuring, not deletion). Every fix so far was written and reviewed individually. Any future session should keep doing this by hand, chapter by chapter — do not attempt a scripted bulk replace across the remaining chapters. (A pure detection/audit script — no rewriting — was also tried to speed up scoping; it failed on a 403 from GitHub's API due to lacking authentication in the sandbox environment. Not worth re-attempting: the actual bottleneck is the line-edit judgment per instance, not finding the instances, which a manual grep-per-chapter already does reliably.) Note: not every chapter has instances — ch.10 and ch.24 were both found clean (0 instances) on inspection, which is expected and fine; log a chapter as DONE/0 rather than skipping it.

**Chapters 2-7, 9, and 11-13 have NOT yet been individually re-verified under any version of this task** — they were part of an original "prior session, not itemized" claim that already proved incomplete once (ch.8 had a missed instance). Treat that range as unverified, not confirmed, until someone actually checks each one — now including ch.2-3 specifically for the reason above.

**Progress log (update this table as you go — don't just say "done," log the count per chapter so nobody re-scans a clean chapter):**

| Chapter | Status | Instances fixed |
|---|---|---|
| 1 | DONE — re-checked this session under the expanded scope (Zia's own text included), 3 narration instances fixed | 3 |
| 2-7, 9, 11-13 | UNVERIFIED — not yet individually checked under the current (expanded) scope. Do not assume clean, and do not assume "Zia's own text" is exempt anymore. | unknown |
| 8 | DONE — re-verified, found and fixed 1 additional missed instance ("that specific hush") beyond the original prior-session pass | 1 (this session) + unknown prior |
| 10 | DONE — spot-checked, confirmed genuinely clean | 0 |
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

**Next session: three things need doing, not just one.** (1) Continue the primary pass forward at chapter 28 through 45, same method as ch.1/15-27 above (fetch chapter → grep for "the particular"/"the specific" → rewrite each narration instance for natural phrasing, leaving dialogue and genuinely natural uses alone → push with a commit message noting the count fixed → update this table). (2) Go back and check chapters 2-7, 9, and 11-13 the same way — including ch.2 and ch.3, which are Zia's own text but are now confirmed in-scope too. (3) Resolve the Whitlock/Kell contradiction in Task 4 above before doing further prose work in ch.38/39/43's vicinity.

Also worth checking once the "the particular/specific" pass is complete: the other tells found in the original diagnostic ("the kind of ___" 69 occurrences, "found herself/himself" 45, "in a way that" 41, "something in her/his [face/voice/eyes]" 32, "understood that" 12) were NOT in scope for this pass and remain fully unaddressed — flag as a possible Task 5b if Zia wants the manuscript further cleaned after the primary pass finishes.

## TASK 6 — KDP publishing-format requirements — STILL OPEN, not started
1. Front matter (title page, copyright page, dedication if any).
2. Table of contents.
3. Confirm chapter break formatting will render correctly in KDP's converter (the base64-encoding bug found in ch.4/ch.20 is a reminder to spot-check raw file content, not just assume plain text everywhere).
4. Trim size / manuscript formatting settings.
5. Metadata: title "Where the Frost Doesn't Reach", series "The Amity Falls Series, Book 1", author name/pen name Zia wants on the cover — NOT YET CONFIRMED, ask Zia.
6. Cover design — not yet started in this repo. Track in a new `cover_design.md` in this same folder if that work begins.

## Priority order recommended for next session
1. **Ask Zia the Whitlock/Kell identity question (Task 4 finding above) before writing anything** — this determines which chapters need rewriting and how, so it should be resolved before more prose work happens in ch.38/39/43's vicinity.
2. **Task 5 — continue the AI-tell rewrite pass starting at chapter 28, AND check chapters 2-7, 9, 11-13 (including Zia's own ch.2-3, per the updated scope above).**
3. Task 4's full continuity/voice read-through — after Task 5 is fully complete, and after the Whitlock/Kell decision above is made and applied.
4. HANDOFF.md's expansion/trim pass (word counts) — can run in parallel with Task 5/4 since it's independent chapter-level work.
5. Task 6 (KDP formatting) — last, once text is final. Cover design can proceed in parallel since it doesn't depend on final interior text.

## Update this file
Whoever picks up any task above should mark it DONE with a one-line result summary and update the Task 5 progress table above as they go — don't just delete the task, log the outcome so it isn't re-run from scratch next time.
