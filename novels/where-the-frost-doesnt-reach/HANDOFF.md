# WHERE THE FROST DOESN'T REACH — 45-CHAPTER EXPANSION — HANDOFF NOTES

**Series:** The Amity Falls Series, Book 1
**Confirmed title:** "Where the Frost Doesn't Reach" — NOT "The Weight of What We Forget" / "The Hollow Season."

## READ NEXT — pre-publish checklist
Before touching anything else, read `PRE_PUBLISH_CHECKLIST.md` in this same folder. It has 6 open tasks (style-originality check, character-name collision audit, real-person name check, continuity read-through, AI-authorship tell check, KDP formatting requirements) with a recommended priority order. This project is otherwise ~90% done per Zia — that checklist is the remaining 10%.

## TASK 5 (AI-tell rewrite pass) — PROGRESS TRACKER — READ THIS BEFORE STARTING TASK 5

**Method (proven, use this exact process for every remaining chapter):**
1. Fetch the chapter's current content + sha from GitHub.
2. Cross-check it against ch.3 (canon) for continuity issues while you're in there anyway — kills two tasks at once.
3. Find every instance of "the particular ___" and "the specific ___". Replace each with natural, varied phrasing that keeps the exact same meaning — cut the intensifier, use a different construction, or just state the plain fact. No plot, dialogue, or fact changes, ever.
4. Also worth a glance (not mandatory, same tic family): "the kind of ___", standalone "particular"/"specific" used as plain adjectives.
5. Watch for **tense mismatches introduced by your own fix** — if the replacement lands inside past-tense narration, make sure the new phrasing is past tense too. (Real example caught this session: "calculating exactly how much worse a known flaw becomes once you realize" should have been "became... realized" — present-tense verbs had slipped into a past-tense paragraph.)
6. Verify zero em dashes remain after your edit (should already be zero, this is a can't-hurt check).
7. Push the whole corrected chapter file via the API directly (Zia has explicitly said to stop doing the manual find/replace-in-chat workflow for this specific task — it was too slow at 38+ chapters remaining; push directly, verify by reading the file back, move to the next chapter without waiting for a check-in unless something looks genuinely wrong).
8. Update this table with a one-line result.

**Status (as of this session, chapters checked in order):**

| Chapter | Task 5 (AI-tell) | Task 4 (continuity vs. ch.3) | Notes |
|---|---|---|---|
| 1 | DONE | N/A (is canon) | Fixed prior session — 5 instances, varied constructions. |
| 2 | DONE | N/A (is canon) | Fixed prior session — 1 instance. |
| 3 | DONE | N/A (is canon) | Fixed prior session — 1 instance. Zero em dashes confirmed. |
| 4 | DONE | Checked, no issues | Fixed prior session — 4 instances. |
| 5 | DONE | Checked, no issues | Fixed this session — 6 instances: "the particular discomfort"→"that unsettled feeling"; "the specific thinness of a man"→cut, restated plain; "the particular glance of someone checking"→"checking, the way you would when"; "the particular density of paper"→"paper gone soft and dense"; "tired in the specific way of someone who spent"→"tired the way people get from spending"; "the specific reluctance of someone who has learned"→"reluctant the way you get when you've learned". Pushed live. |
| 6 | DONE | Checked, no issues | Fixed this session — 5 instances, all "the particular ___" cut or rephrased. Zia caught one awkward resulting sentence ("...engineered around once" — double "once") and it was corrected, then further polished to "calculating exactly how much worse a known flaw became once she realized someone had already learned to work around it" (past tense fix applied). Pushed live and verified by reading back — confirmed correct on GitHub. One remaining minor "specific" (not the "the specific X" pattern, just the bare word) was flagged as optional/low-priority and left as-is. |
| 7 | **NOT YET APPLIED — fixes identified, ready to push, do this first** | Checked, no issues | 7 instances found, none pushed yet: (1) "checking the monitor with the particular brisk efficiency of someone whose job required" → "checking the monitor with the brisk efficiency of someone whose job required"; (2) "cataloguing the particular way grief and fury sat together" → "cataloguing the way grief and fury sat together"; (3) "something in her had gone quietly alert, the particular instinct of noticing a beam" → "...the instinct of noticing a beam"; (4) "with the specific unease of a woman who had just watched a piece move" → "with the uneasy sense of a woman who had just watched a piece move"; (5) "starting to recognize as the particular vulnerability of a man deciding" → "starting to recognize as the vulnerability of a man deciding"; (6) "familiar and unfamiliar at once, the particular vertigo of a landscape" → "familiar and unfamiliar at once, that vertigo of a landscape"; (7) "old enough to have quietly held this particular secret since before" → "old enough to have quietly held this exact secret since before". Current sha as of this session: 2dfe4f2471b0d9ce9d3d465d02fd358b2585f55f — re-fetch to confirm it hasn't changed before pushing, in case Zia edited it manually in the meantime. |
| 8–45 | NOT STARTED | NOT STARTED | Full remaining scope. Work sequentially, same method as above. Chapter 38 and 44 are also flagged in the main table above as over the 2,500-word ceiling — a trim pass on those two can happen in the same sitting as their AI-tell/continuity check, no need for a separate pass. |

**Session budget note:** this session ended near its limit partway through chapter 7 — the fixes above are analyzed and ready, just not yet written back to GitHub. Start the next session by pushing chapter 7's fix directly (content given above), verify, then continue to chapter 8 without re-deriving any of this.

## What this project is
Expanding an original 24-chapter draft (~26,900 words) into a 45-chapter, ~112,500-word novel, per `beat_map_45ch.md` in this same folder (authoritative for chapter-by-chapter mapping).

## UPDATE (this session, Sept 2026 — full audit)
This session did a full read of every file in this folder plus all 45 chapter files against actual GitHub content, at Zia's request to fix chapter 8 and verify the whole novel. Three real problems found and fixed/corrected:

1. **Ch.8 name collision — ACTUALLY FIXED NOW.** `architecture.md` documented a fix (rename Caleb's grandfather from "Warren Reyes" to "Silas Reyes" to avoid colliding with Thomas's son Warren from ch.6/7) that had never been applied to the file. Chapter_08.md still said "Warren Reyes" as of this session. Fixed and pushed directly. Verified: single occurrence in the whole 45-chapter manuscript, now corrected, word count unchanged (1,659).
2. **Chapters 14-19 status was wrong — CORRECTED.** This file previously said 14-19 were "NOT WRITTEN, assigned to another session/profile." They are in fact written, in the repo, and their content matches the beat map exactly (Dev found in silo ch.16, Priya's vigil ch.17, Wren/Odette store scene ch.18-19). Status table below corrected. No duplication risk anymore — the gap this file used to warn about doesn't exist.
3. **Word-count table was stale across nearly every chapter** — corrected below against actual current file content (chapters have clearly been edited/expanded since the old counts were recorded, in most cases upward).
4. **New pre-publish checklist opened** — see `PRE_PUBLISH_CHECKLIST.md`. Zia raised a style-originality concern (possibly resembling a famous romantic-suspense author, name recalled as "Nora something" — not found anywhere in this repo's files or commit history when searched) plus a real-person-name check. Both logged as tasks there, not yet run.

No other continuity issues found: the only other name mentioned in `architecture.md`'s log (the ch.7 duplication fix) is confirmed correctly applied — ch.7 does not re-run ch.6's toll explanation.

Prior open decisions:
1. **Ch.3 em dashes** — RESOLVED (still holds). Zero em dashes confirmed across all 45 chapters, not just ch.3.
2. **Ch.44 vs. beat map (closed-door vs. on-page intimacy)** — RESOLVED, no further action needed.
3. **Chapters 1-3 version conflict — RESOLVED this session.** Zia confirmed: whatever is currently saved on GitHub for chapters 1, 2, and 3 is final and canon. The competing `Ch_1_to_10_expanded.zip` text is dead — do not use it, do not reconcile against it, do not raise this as an open question again. Ch.4-11 continuity can now be finalized against ch.1-3 as they stand in the repo.

## Repo location
All novel files live at `novels/where-the-frost-doesnt-reach/` in `Wazzaboyzz/Voxel`.
- `chapters/` — chapter_NN.md, all lowercase. All 45 files exist as of this session.
- `beat_map_45ch.md` — authoritative chapter mapping, old ch → new ch. NOTE: its "Written by" column also says "Not yet written" for chapters that are now written (35-45) — that column is stale in the same way this file's table was; trust the table below instead. It also references the ch.1-3 zip conflict as still open — that conflict is now resolved (see above), ignore that note in the beat map.
- `architecture.md` — worldbuilding/continuity reference, check before writing any chapter.
- `PRE_PUBLISH_CHECKLIST.md` — pending pre-publish quality tasks, read before the next session does anything else.
- `HANDOFF.md` — this file.

## Revision pass (in progress)
Proposed order:
1. Fix ch.20 formatting bug — DONE (earlier session).
2. Pick one word-count target and update both files to agree — DONE. Locked at 2,000-2,500.
3. Read chapters 4-9 against final ch.3 for continuity, fix any mismatches — IN PROGRESS, see Task 5 tracker above (continuity is being checked as part of the same pass as the AI-tell fix, chapters 4-7 confirmed clean so far).
4. Expand every under-target chapter to the agreed range — NOT STARTED. Per the corrected table below, chapters currently BELOW 2,000 words: 2, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 31, 32, 35, 36, 37, 42, 45. Chapters currently ABOVE the 2,500 ceiling (need a trim pass instead): 38 (2,544), 44 (2,556). Zia has said 1,800 words is an acceptable floor — chapters at or above 1,800 do NOT need expansion, only those genuinely below 1,800 are real gaps (re-check the table against this revised floor before doing any expansion work).
5. Full read-through for voice consistency and plot contradictions once everything is length-correct — NOT STARTED. (Also tracked as Task 4 in PRE_PUBLISH_CHECKLIST.md.)

## Status: chapters completed in the new 45-chapter structure (verified Sept 2026, word counts re-checked against actual file content this session)

| New Ch | Status | Actual words | Notes |
|---|---|---|---|
| 1 | DONE | 2,534 | Zia's own text (funeral reunion). CANON — confirmed final, no other version. |
| 2 | DONE | 1,817 | Zia's own text (ring found). CANON — confirmed final, no other version. Below target. |
| 3 | DONE | 2,718 | CANON — confirmed final, no other version. Zero em dashes. |
| 4 | DONE | 2,106 | NEW — Odette/store/orchard settling-in scene. In target. |
| 5 | DONE | 2,023 | NEW — first Rosewood/Thomas visit. In target. |
| 6 | DONE | 2,068 | Thomas's first tolling reveal. In target. |
| 7 | DONE | 1,963 | Continues reveal; Warren Reyes (Thomas's son) name established. Below target. |
| 8 | DONE | 1,659 | Records office, survey file found. Name-collision bug FIXED (grandfather now Silas Reyes). Below target. |
| 9 | DONE | 1,808 | Below target. |
| 10 | DONE | 1,434 | Well below target — flag for expansion pass. Odette confession begins. |
| 11 | DONE | 1,376 | Well below target — flag for expansion pass. Porch hand-touch. |
| 12 | DONE | 1,880 | Toll (the dog) arrives; ends on Wren's late-night arrival at the door, unsettled. Below target. |
| 13 | DONE | 2,030 | Wren's barn-door touch, fragmented flash of Caleb's toll, Dev's name surfaces. Picks up from ch.12's cliffhanger. In target. |
| 14 | DONE | 1,993 | Priya's fear, Dev missing. Below target. |
| 15 | DONE | 1,885 | Yusuf/Priya backstory scene. Below target. |
| 16 | DONE | 1,944 | Dev found in the silo, initial confession. Below target. |
| 17 | DONE | 1,811 | Dev's fuller confession, Priya vigil. Below target. |
| 18 | DONE | 2,242 | Deducing Wren may be targeted next, store scene with Odette. In target. |
| 19 | DONE | 1,947 | Odette thickened as red herring. Below target. |
| 20 | DONE | 1,971 | Kell homestead confrontation pt.1. Formatting bug previously fixed. Below target. |
| 21 | DONE | 1,819 | Confrontation pt.2, porch vulnerability. Below target. |
| 22 | DONE | 1,807 | Odette red-herring peak then clears. Below target. |
| 23 | DONE | 1,444 | Below target. Weather station discovery begins. |
| 24 | DONE | 1,655 | Below target. Amplifier found, near-miss with Kell's car. |
| 25 | DONE | 1,740 | Below target. Yusuf agrees to file. |
| 26 | DONE | 1,451 | Below target. Threat text arrives. |
| 27 | DONE | 1,293 | Well below target. Wren's agency arc begins. |
| 28 | DONE | 2,207 | Wren volunteers to read inert object; crooked-tree "falling twice" confession. In target. |
| 29 | DONE | 2,063 | Corinne/Whitlock reveal. In target. |
| 30 | DONE | 2,067 | **CHECKPOINT — first kiss.** Barn scene, interrupted by clerk break-in. In target. |
| 31 | DONE | 1,954 | Case-building, nine days, formal inquiry opens. Below target. |
| 32 | DONE | 1,983 | Door-to-door canvassing, found-family texture. Below target. |
| 33 | DONE | 2,417 | Town backlash, Caleb's early doubt, Yusuf's tires slashed. In target. |
| 34 | DONE | 2,333 | **CHECKPOINT — RUPTURE.** Kell's press attack; Caleb asks for space. In target. |
| 35 | DONE | 1,867 | Days of distance. Below target. |
| 36 | DONE | 1,890 | The hearing, partial win. Below target. |
| 37 | DONE | 1,472 | Reconciliation at the fence line. Below target. |
| 38 | DONE | 2,544 | Hospital scene, Adelaide Whitlock named. Over the 2,500 ceiling — trim candidate. |
| 39 | DONE | 2,386 | Wren kidnapped, Kell's confession re: Adelaide. In target. |
| 40 | DONE | 2,065 | Descent into mill cellar, storm builds, Dev revealed as Priya's brother. In target. |
| 41 | DONE | 2,104 | **CHECKPOINT — mill climax.** Dev's full confession, Wren's toll redirect, structural collapse. In target. |
| 42 | DONE | 1,929 | Release sequence/aftermath, Kell and Dev taken into custody. Below target. |
| 43 | DONE | 2,001 | **CHECKPOINT — resolution.** Harvest festival, Adelaide confirmed publicly, Kell's collapse/unnatural aging reveal, Caleb's ring memory surfaces. Thomas still alive at end of this chapter (dies per ch.44's opening, days later). In target. |
| 44 | DONE | 2,556 | Weeks after, memory returns in pieces, Mara stays for good. Closed-door vs. beat-map conflict resolved: kept as written, on-page per beat map. Over the 2,500 ceiling — trim candidate. |
| 45 | DONE | 1,977 | Wedding, Adelaide's letter, Whitlock/Book 2 hook. Below target. |

**All 45 chapters are written, present in the repo, and confirmed zero em dashes throughout. Chapters 1-3 are locked as final/canon (see above) — no version conflict remains anywhere in the project.**

## Standing rules for this project (apply to every future chapter)
- Target 2,000–2,500 words per chapter, though Zia has since confirmed 1,800 words is an acceptable floor — see revision pass note above.
- **No em dashes anywhere in chapter prose.** Confirmed holding across all 45 files as of this session.
- Match established voice exactly (Mara: dry, controlled, engineering-metaphor; Caleb: steady, plainspoken, dry humor sideways).
- No signs of AI/Claude authorship in the prose itself — see Task 5 tracker above for the specific, active fix pass on this.
- EXISTING chapters: adapt from source, preserve established dialogue/plot beats, add texture to reach word count, don't alter established facts.
- NEW chapters: must not contradict any already-written chapter before or after it. Check architecture.md and adjacent chapters first.
- Checkpoint chapters (do not shift position): Ch.30 (first kiss), Ch.34 (rupture), Ch.41 (mill climax), Ch.43 (resolution).
- All filenames lowercase (`chapter_NN.md`).
- Zia is a non-technical, voice-dictation user (expect transcription garbles — "Waza boys"=Wazzaboyzz, "Vaza"/"Voxel"/"Watson"=Voxel). For NEW creative content Zia hasn't seen yet, give exact file paths and full GitHub URLs in copy blocks using the `?filename=` new-file link style, and let Zia push it himself. For the Task 5 AI-tell/continuity maintenance pass specifically, Zia has explicitly said to push directly via the API instead — this is small mechanical fixes to already-approved text, not new content needing his review. Verify each push by reading the file back before moving to the next chapter.
- Verify word count and em-dash count in the same turn before calling any chapter done.
- **Before trusting this file's status table on any future session, spot-check at least 2-3 chapters' actual word counts against what's claimed here** — this table has gone stale before because completed work wasn't reflected back into this file at the end of the session that did it.

## Update this file
Whoever (whichever session) completes new chapters, edits an existing one, or makes progress on any PRE_PUBLISH_CHECKLIST.md task, should update the relevant table above before ending their session — this is the single biggest source of wasted effort/confusion found in this project so far.
