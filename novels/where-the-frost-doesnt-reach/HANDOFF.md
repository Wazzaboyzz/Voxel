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
5. Watch for **tense mismatches introduced by your own fix** — if the replacement lands inside past-tense narration, make sure the new phrasing is past tense too.
6. Verify zero em dashes remain after your edit (should already be zero, this is a can't-hurt check).
7. Push the whole corrected chapter file via the API directly (Zia has explicitly said to push directly for this task rather than round-trip through chat), verify by reading the file back, move to the next chapter.
8. Update this table with a one-line result.

**Status (as of this session, chapters checked in order):**

| Chapter | Task 5 (AI-tell) | Task 4 (continuity vs. ch.3) | Notes |
|---|---|---|---|
| 1 | DONE | N/A (is canon) | Fixed prior session — 5 instances, varied constructions. |
| 2 | DONE | N/A (is canon) | Fixed prior session — 1 instance. |
| 3 | DONE | N/A (is canon) | Fixed prior session — 1 instance. Zero em dashes confirmed. |
| 4 | DONE | Checked, no issues | Fixed prior session — 4 instances. |
| 5 | DONE | Checked, no issues | Fixed prior session — 6 instances, pushed live. |
| 6 | DONE | Checked, no issues | Fixed prior session — 5 instances, pushed live, tense-fix verified. |
| 7 | DONE | Checked, no issues | Fixed this session — 7 instances of "the particular/specific X" cut or rephrased. Pushed and verified on GitHub (sha 85582efc...). Zero em dashes, zero remaining tics. |
| 8 | DONE | Checked, no issues | Fixed this session — 4 instances of "the particular X" cut or rephrased. Pushed and verified on GitHub (sha b080b2a0...). Word count unchanged at 1,659 (below floor, not addressed this pass — that's Task in section 4 below, expansion, separate from Task 5). |
| 9 | DONE | Checked, no issues | Fixed this session — 8 instances of "the particular/specific X" cut or rephrased. Pushed and verified on GitHub (sha c2d4f139...). |
| 10–45 | NOT STARTED | NOT STARTED | Full remaining scope. Work sequentially, same method as above. Chapter 38 and 44 are also flagged in the main table above as over the 2,500-word ceiling — a trim pass on those two can happen in the same sitting as their AI-tell/continuity check, no need for a separate pass. |

**Session budget note:** this session completed chapters 7, 8, 9. Start the next session at chapter 10, same method, no re-derivation needed.

## What this project is
Expanding an original 24-chapter draft (~26,900 words) into a 45-chapter, ~112,500-word novel, per `beat_map_45ch.md` in this same folder (authoritative for chapter-by-chapter mapping).

## Prior open decisions (all resolved)
1. **Ch.3 em dashes** — RESOLVED. Zero em dashes confirmed across all 45 chapters.
2. **Ch.44 vs. beat map (closed-door vs. on-page intimacy)** — RESOLVED, no further action needed.
3. **Chapters 1-3 version conflict** — RESOLVED. Zia confirmed whatever is currently on GitHub for chapters 1-3 is final/canon.

## Repo location
All novel files live at `novels/where-the-frost-doesnt-reach/` in `Wazzaboyzz/Voxel`.
- `chapters/` — chapter_NN.md, all lowercase. All 45 files exist.
- `beat_map_45ch.md` — authoritative chapter mapping, old ch → new ch. Its "Written by" column is stale (still says "not yet written" for chapters now written) — trust the status table below instead.
- `architecture.md` — worldbuilding/continuity reference, check before writing any chapter.
- `PRE_PUBLISH_CHECKLIST.md` — pending pre-publish quality tasks, read before the next session does anything else.
- `HANDOFF.md` — this file.

## Revision pass (in progress)
Proposed order:
1. Fix ch.20 formatting bug — DONE.
2. Pick one word-count target and update both files to agree — DONE. Locked at 2,000-2,500, with 1,800 as an acceptable floor per Zia.
3. Read chapters 4-9 against final ch.3 for continuity, fix any mismatches — DONE for 4-9, all clean. Continue this check as part of Task 5 for 10 onward.
4. Expand every under-target chapter to the agreed range — NOT STARTED. Chapters currently BELOW the 1,800 floor (real gaps, need expansion): 10 (1,434), 11 (1,376), 23 (1,444), 24 (1,655), 25 (1,740), 26 (1,451), 27 (1,293), 8 (1,659), 37 (1,472). Chapters currently ABOVE the 2,500 ceiling (need a trim pass instead): 38 (2,544), 44 (2,556).
5. Full read-through for voice consistency and plot contradictions once everything is length-correct — NOT STARTED. (Also tracked as Task 4 in PRE_PUBLISH_CHECKLIST.md.)

## Status: chapters completed in the new 45-chapter structure

| New Ch | Status | Actual words | Notes |
|---|---|---|---|
| 1 | DONE | 2,534 | Zia's own text (funeral reunion). CANON. |
| 2 | DONE | 1,817 | Zia's own text (ring found). CANON. Below target. |
| 3 | DONE | 2,718 | CANON. Zero em dashes. |
| 4 | DONE | 2,106 | NEW — Odette/store/orchard settling-in scene. In target. |
| 5 | DONE | 2,023 | NEW — first Rosewood/Thomas visit. In target. |
| 6 | DONE | 2,068 | Thomas's first tolling reveal. In target. |
| 7 | DONE | 1,958 | Continues reveal; Warren Reyes (Thomas's son) name established. Task 5 applied this session. Below target. |
| 8 | DONE | ~1,653 | Records office, survey file found. Name-collision bug fixed (grandfather is Silas Reyes). Task 5 applied this session. Below floor, flagged for expansion. |
| 9 | DONE | 1,793 | Task 5 applied this session. Just below floor. |
| 10 | DONE | 1,434 | Well below floor — flag for expansion pass. Odette confession begins. |
| 11 | DONE | 1,376 | Well below floor — flag for expansion pass. Porch hand-touch. |
| 12 | DONE | 1,880 | Toll (the dog) arrives; ends on Wren's late-night arrival at the door, unsettled. Below target. |
| 13 | DONE | 2,030 | Wren's barn-door touch, fragmented flash of Caleb's toll, Dev's name surfaces. In target. |
| 14 | DONE | 1,993 | Priya's fear, Dev missing. Below target. |
| 15 | DONE | 1,885 | Yusuf/Priya backstory scene. Below target. |
| 16 | DONE | 1,944 | Dev found in the silo, initial confession. Below target. |
| 17 | DONE | 1,811 | Dev's fuller confession, Priya vigil. Below target. |
| 18 | DONE | 2,242 | Deducing Wren may be targeted next, store scene with Odette. In target. |
| 19 | DONE | 1,947 | Odette thickened as red herring. Below target. |
| 20 | DONE | 1,971 | Kell homestead confrontation pt.1. Below target. |
| 21 | DONE | 1,819 | Confrontation pt.2, porch vulnerability. Below target. |
| 22 | DONE | 1,807 | Odette red-herring peak then clears. Below target. |
| 23 | DONE | 1,444 | Below floor. Weather station discovery begins. |
| 24 | DONE | 1,655 | Below floor. Amplifier found, near-miss with Kell's car. |
| 25 | DONE | 1,740 | Below floor. Yusuf agrees to file. |
| 26 | DONE | 1,451 | Below floor. Threat text arrives. |
| 27 | DONE | 1,293 | Well below floor. Wren's agency arc begins. |
| 28 | DONE | 2,207 | Wren volunteers to read inert object; crooked-tree "falling twice" confession. In target. |
| 29 | DONE | 2,063 | Corinne/Whitlock reveal. In target. |
| 30 | DONE | 2,067 | **CHECKPOINT — first kiss.** Barn scene, interrupted by clerk break-in. In target. |
| 31 | DONE | 1,954 | Case-building, nine days, formal inquiry opens. Below target. |
| 32 | DONE | 1,983 | Door-to-door canvassing, found-family texture. Below target. |
| 33 | DONE | 2,417 | Town backlash, Caleb's early doubt, Yusuf's tires slashed. In target. |
| 34 | DONE | 2,333 | **CHECKPOINT — RUPTURE.** Kell's press attack; Caleb asks for space. In target. |
| 35 | DONE | 1,867 | Days of distance. Below target. |
| 36 | DONE | 1,890 | The hearing, partial win. Below target. |
| 37 | DONE | 1,472 | Reconciliation at the fence line. Below floor. |
| 38 | DONE | 2,544 | Hospital scene, Adelaide Whitlock named. Over ceiling — trim candidate. |
| 39 | DONE | 2,386 | Wren kidnapped, Kell's confession re: Adelaide. In target. |
| 40 | DONE | 2,065 | Descent into mill cellar, storm builds, Dev revealed as Priya's brother. In target. |
| 41 | DONE | 2,104 | **CHECKPOINT — mill climax.** Dev's full confession, Wren's toll redirect, structural collapse. In target. |
| 42 | DONE | 1,929 | Release sequence/aftermath, Kell and Dev taken into custody. Below target. |
| 43 | DONE | 2,001 | **CHECKPOINT — resolution.** Harvest festival, Adelaide confirmed publicly, Kell's collapse/unnatural aging reveal, Caleb's ring memory surfaces. In target. |
| 44 | DONE | 2,556 | Weeks after, memory returns in pieces, Mara stays for good. On-page per beat map. Over ceiling — trim candidate. |
| 45 | DONE | 1,977 | Wedding, Adelaide's letter, Whitlock/Book 2 hook. Below target. |

**All 45 chapters are written, present in the repo, and confirmed zero em dashes throughout. Chapters 1-3 are locked as final/canon.**

## Standing rules for this project (apply to every future chapter)
- Target 2,000–2,500 words per chapter, 1,800 acceptable floor per Zia.
- **No em dashes anywhere in chapter prose.**
- Match established voice exactly (Mara: dry, controlled, engineering-metaphor; Caleb: steady, plainspoken, dry humor sideways).
- No signs of AI/Claude authorship in the prose itself — see Task 5 tracker above for the active fix pass.
- EXISTING chapters: adapt from source, preserve established dialogue/plot beats, add texture to reach word count, don't alter established facts.
- NEW chapters: must not contradict any already-written chapter before or after it. Check architecture.md and adjacent chapters first.
- Checkpoint chapters (do not shift position): Ch.30 (first kiss), Ch.34 (rupture), Ch.41 (mill climax), Ch.43 (resolution).
- All filenames lowercase (`chapter_NN.md`).
- Zia is a non-technical, voice-dictation user (expect transcription garbles — "Waza boys"=Wazzaboyzz, "Vaza"/"Voxel"/"Watson"=Voxel). For NEW creative content Zia hasn't seen yet, give exact file paths and full GitHub URLs in copy blocks using the `?filename=` new-file link style, and let Zia push it himself. For the Task 5 AI-tell/continuity maintenance pass specifically, push directly via the API. Verify each push by reading the file back before moving to the next chapter.
- Verify word count and em-dash count in the same turn before calling any chapter done.

## Update this file
Whoever (whichever session) completes new chapters, edits an existing one, or makes progress on any PRE_PUBLISH_CHECKLIST.md task, should update the relevant table above before ending their session.
