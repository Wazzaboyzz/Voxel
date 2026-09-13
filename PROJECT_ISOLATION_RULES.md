# Voxel — Project Isolation Rules (do not mix projects)

Added 2026-09-13 after a real mistake: after improving the picture-book
manuscript prompt (Phase 8g), Claude wrongly suggested applying the same
picture-book craft rules (page-turn hooks, refrains, read-aloud-for-a-
child rhythm) to Amity Falls Book 2's novel chapter generation. Those are
different content types with different, sometimes opposite, craft needs.
Zia caught it and asked for a fixed, explicit rule set so this kind of
cross-contamination stops happening. This file is that rule set. Read it
before touching any generation prompt or shared module.

## The 20 rules

1. Before reusing any prompt, rule, or technique from one project on
   another, explicitly name both projects and confirm they are the same
   content type (e.g. "picture book" vs "adult novel" are NOT the same
   type) before proceeding.
2. Picture-book craft rules (page-turn hooks every page, refrains,
   read-aloud-for-a-child rhythm, short simple vocabulary) apply ONLY to
   picture-book manuscript generation (`generate_manuscript`) — never to
   novel chapters.
3. Novel-chapter rules (beat-map checkpoint enforcement, voice-profile
   matching, word-count bands of 2,000-2,500, AI-telltale scrubbing)
   apply ONLY to `generate_chapter`/`generate_novel_chapter` — never to
   picture-book pages.
4. A change made to one content-type's generation prompt is never
   auto-applied to another content-type's prompt "for consistency" —
   consistency across unrelated formats is not a goal.
5. Amity Falls (novel series) and Luna/any picture-book series are
   permanently separate projects with separate prompts, separate QC (beat
   map vs page-turn hooks), and separate voice/style rules — never merged
   into one shared "story generation" prompt.
6. Before editing any shared module (`content_provider.py`,
   `image_provider.py`, etc.) that serves multiple content types, check
   which functions serve which content type and touch ONLY the function
   relevant to the current task.
7. When Claude has just improved something for Project A, Claude does
   not proactively suggest applying the same improvement to Project B
   without first checking whether the underlying content type/craft
   actually matches — pattern-matching "I improved X, should I improve
   the similar-looking Y" is not sufficient justification on its own.
8. Each project's standing rules (word count bands, style bans, voice
   profiles, checkpoint positions) live in that project's own section of
   memory/HANDOFF — never copied wholesale into another project's
   section.
9. If a technique genuinely could apply to multiple project types (e.g.
   "no em dashes," "avoid AI-telltale phrases"), it must be evaluated and
   confirmed per-project, not assumed to transfer just because it worked
   once.
10. Never blend two projects' outputs into one file, one prompt, or one
    generation call unless Zia explicitly asks for a crossover.
11. Before writing code that touches a pipeline file, confirm which
    project's pipeline path (picture-book vs novel vs any future type) is
    actually in scope for the current task.
12. A research finding gathered for one project (e.g. picture-book craft
    research) is cited and used only for that project's deliverable — it
    does not get silently folded into another project's spec document.
13. When in doubt about whether a rule crosses project boundaries, ask
    Zia directly rather than assuming and applying it.
14. Never suggest a "shared" or "unified" system across project types
    (e.g. one universal story-quality prompt) unless Zia explicitly
    requests unification — the default assumption is separation.
15. Each project keeps its own QC/checklist criteria (beat-map audit for
    novels, page-turn-hook check for picture books) — one project's QC
    checklist is never used to grade another project's output.
16. Voice profiles, character bibles, and story bibles are scoped
    per-series/per-project and never referenced or reused across
    unrelated series without explicit confirmation.
17. When multiple Voxel sub-projects exist in the repo (novels/, picture
    books, any future format), file/folder changes for one must not
    incidentally alter shared config in a way that changes another
    project's behavior without that being called out explicitly.
18. If Claude catches itself about to say "since I just did X for
    project A, let's also do X for project B" — that sentence itself is
    the signal to stop and check project-type compatibility first, per
    rule 7.
19. This file is not to be diluted, merged, or "simplified for
    consistency" into other docs — it stands as its own separate,
    explicit reference.
20. When corrected on a project-mixing mistake, state plainly what the
    mistake was and why, without minimizing it or reframing it as
    reasonable in hindsight.
