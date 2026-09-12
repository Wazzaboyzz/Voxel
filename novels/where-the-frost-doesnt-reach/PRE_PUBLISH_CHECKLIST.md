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

## TASK 4 — Full continuity read-through — PARTIALLY DONE, and a REAL PLOT CONTRADICTION FOUND, not yet fixed
- **FIXED (earlier):** ch.38 said "ten years" for a timespan every other chapter (ch.23, 32, 33, 39) establishes as "forty years." Corrected to match canon.
- Cross-checked "eight years"/"two years" figures for consistency — no contradictions found.
- **UNFIXED, still awaiting Zia's decision — the central mystery's own mechanics contradict themselves across ch.38, ch.39, and ch.43:**
  - Ch.38: Thomas calls Adelaide "Adelaide Whitlock... Ambrose's wife," directly identifying present-day Kell as the same person who was Adelaide's husband a century ago (an immortal who's worn other names, per the "wearing other names the way other men wear coats" line in the same chapter).
  - Ch.39: Kell speaks in the first person about Adelaide coming to *him* directly and *him* being the one who let her disappear — again, Kell IS the century-old husband.
  - Ch.43: Kell says the burden "was simply handed to me" after Ambrose Whitlock "finally disappeared" — now describing Whitlock in the third person as a *different, earlier person* Kell only later succeeded, not a name Kell himself once wore.
  - **These two versions of who Kell is cannot both be true as written.** Needs an editorial decision, not just a wording tweak: (a) Kell IS Ambrose Whitlock, one immortal man across a century — rewrite ch.43's "handed to me" language; or (b) Kell is a successor — rewrite ch.38/ch.39 so Thomas and Kell stop speaking as if Kell was literally Adelaide's husband. **Ask Zia which one before touching any of these three chapters again** — still genuinely unanswered as of this session.
- **STILL OPEN, needs a dedicated session:** full line-by-line read of chapters 4-9 against final ch.3 canon, plus a full 45-chapter read purely for voice consistency and subtler plot contradictions. Do this AFTER Task 5's rewrite is complete.

## TASK 5 — AI-authorship tell check — IN PROGRESS, chapters 1-27 fully verified, 28-45 remaining
Diagnostic found "the particular ___" / "the specific ___" as the dominant tell. Fix approach: read each chapter, replace or cut each instance individually so the sentence still reads naturally — a line-edit, not a find-and-replace. **Regex/script fixes are explicitly rejected** — mechanical stripping breaks grammar in many cases. Every fix has been written and reviewed individually, chapter by chapter. Do not attempt a scripted bulk replace on the remaining chapters.

**Scope note (settled this session, no longer open for debate):** ch.1 (Zia's own hand-written text) also used this phrase repeatedly, meaning it's likely Zia's own authorial habit rather than proof of AI authorship. Zia was told this directly and decided to proceed with removing it anyway, everywhere, including his own ch.1-3. So: **the whole manuscript is in scope, "Zia wrote this chapter" is not an exemption.** Standing rule for every chapter: fix the repetitive narration pattern ("the/this/that/a particular/specific X" used as a scene-setting descriptor), leave dialogue lines alone, and leave genuinely natural, non-repetitive uses alone (e.g. "a specific sound" naming an actual sound, "trained specifically to notice" as a plain adverb) — these aren't the tell, they're just normal English.

**Chapters 1-13 are now FULLY verified** (a change from earlier in this session, when 2-7/9/11-13 were still an open question) — every one of them has been individually checked under the current scope:

**Progress log (update this table as you go — don't just say "done," log the count per chapter so nobody re-scans a clean chapter):**

| Chapter | Status | Instances fixed |
|---|---|---|
| 1 | DONE | 3 |
| 2 | DONE — checked, genuinely clean | 0 |
| 3 | DONE | 3 |
| 4 | DONE — checked, clean (1 dialogue instance left alone) | 0 |
| 5 | DONE — checked, genuinely clean | 0 |
| 6 | DONE — checked, genuinely clean | 0 |
| 7 | DONE — checked, genuinely clean | 0 |
| 8 | DONE | 1 (plus unknown prior) |
| 9 | DONE — checked, genuinely clean | 0 |
| 10 | DONE — checked, genuinely clean | 0 |
| 11 | DONE — checked, clean (2 dialogue instances left alone) | 0 |
| 12 | DONE — checked, clean (1 dialogue instance left alone) | 0 |
| 13 | DONE — checked, genuinely clean | 0 |
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
| 24 | DONE | 0 |
| 25 | DONE | 2 |
| 26 | DONE | 2 |
| 27 | DONE | 2 |
| 28-45 | NOT STARTED | — continue here, at chapter 28 |

**All of chapters 1-27 are now fully done. Next session (or continuing this one): pick up at chapter 28 and go straight through to 45**, same method as above (fetch chapter → check for "the particular"/"the specific" narration → rewrite each instance, leave dialogue/natural uses → push with a commit message noting the count → update this table).

Also worth checking once the "the particular/specific" pass is complete: the other tells found in the original diagnostic ("the kind of ___" 69 occurrences, "found herself/himself" 45, "in a way that" 41, "something in her/his [face/voice/eyes]" 32, "understood that" 12) were NOT in scope for this pass and remain fully unaddressed — flag as a possible Task 5b if Zia wants the manuscript further cleaned after the primary pass finishes.

## TASK 6 — KDP publishing-format requirements — STILL OPEN, not started
1. Front matter (title page, copyright page, dedication if any).
2. Table of contents.
3. Confirm chapter break formatting will render correctly in KDP's converter (the base64-encoding bug found in ch.4/ch.20 is a reminder to spot-check raw file content, not just assume plain text everywhere).
4. Trim size / manuscript formatting settings.
5. Metadata: title "Where the Frost Doesn't Reach", series "The Amity Falls Series, Book 1", author name/pen name Zia wants on the cover — NOT YET CONFIRMED, ask Zia.
6. Cover design — not yet started in this repo. Track in a new `cover_design.md` in this same folder if that work begins.

## Priority order recommended for next session
1. **Ask Zia the Whitlock/Kell identity question (Task 4 finding above) before writing anything** in ch.38/39/43's vicinity.
2. **Task 5 — continue the AI-tell rewrite pass starting at chapter 28** through 45. Chapters 1-27 are fully done, no need to revisit.
3. Task 4's full continuity/voice read-through — after Task 5 is fully complete, and after the Whitlock/Kell decision above is made and applied.
4. HANDOFF.md's expansion/trim pass (word counts) — can run in parallel with Task 5/4.
5. Task 6 (KDP formatting) — last, once text is final.

## Update this file
Whoever picks up any task above should mark it DONE with a one-line result summary and update the Task 5 progress table above as they go — don't just delete the task, log the outcome so it isn't re-run from scratch next time.
