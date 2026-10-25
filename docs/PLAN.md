# Plan

## Purpose

A daily trainer for quick wit under pressure. Taras learns to notice manipulation and word traps (for example a false choice, where both offered options are bad), to answer provocations briefly, precisely and calmly, without swearing or insults, and to stand up for himself and his people. The training grounds are **schools**: closed worlds where words are binding, so every trap and every answer is sharp. First school: Ukrainian and post-Soviet prison subculture. Second: US East Coast street and prison culture, through documentary sources and old-school hip-hop. A smaller aim: know what that life and its words really are, from sources, without romanticising crime.

What it is not: French, or a script for speaking slang at work.

## What we agreed

Standing decisions. Each is written once, here; other files link to this list instead of repeating it.

2026-10-25:

1. Short daily sessions, about 10-15 minutes. French comes first.
2. It must be fun enough to want every morning: riddles, traps, games, logic.
3. A full tutor: exercises, analysis, feedback, adaptation. What he masters fast is left behind; time goes to his weakest spots.
4. Methods that work on Taras are copied from Fluent and adapted. **No shared code or library with Fluent, ever.**
5. Public repo; everything personal or copyrighted at length lives in git-ignored `data/` (ADR 0001).
6. No invention. Every fact about a school comes from a source in its catalogue, with its scope (place, years, institution, genre). A claim backed by one source, or only by lyrics, is flagged to Taras as such.
7. A claim is labelled **general** when at least three independent sources from different places agree, otherwise **local**. General claims may be stated plainly.
8. One shared curriculum of traps and answer moves for all schools. Schools differ in reference, language and characters, not in traps: learn the abstraction, not the setting.
9. Characters speak the school's language: Russian with феня for post-Soviet, English with slang for East Coast. The debrief is in Ukrainian. *Revisit later*: Taras may want the debrief in the school's language.
10. Lessons are realistic and harsh: threats, humiliation, pressure, real consequences. Limits: no how-to for real crimes; sexual violence never described graphically.
11. Lyrics: short quotes with a link, or a summary in our words, go public. Long quotes go to `data/`. Lyrics are a romanticised layer; documentary sources come first.
12. **Reserve rule**: the reference always holds at least as many researched terms he has not studied as terms he has studied (so at least twice what he knows in total).
13. The lesson skill is `/interest`: in the post-Soviet code you do not "спрашивать", you "интересоваться".
14. One fact lives in one file; others link to it by ID. The layout is in `CLAUDE.md`.
15. The repo is for other people too: anyone can clone it and rebuild everything from public instructions in `README.md`.
16. After every step, a structure review (rule in `CLAUDE.md`, "Finishing a step"), so the repo never turns into mush. Cheap now, expensive later.
17. Requests to YouTube are slow and polite, so we are never blocked as a bot (rule in `CLAUDE.md`). Cheap first: a batch makes one pass that takes YouTube's captions for every video (`--subs-only`), then a second pass runs MacWhisper only on the videos the first pass skipped.

## Steps

Each step has a check. A step is done when its check passes.

1. ✅ **Foundations.** Teaching method adapted from Fluent; `data/` git-ignored; repo layout set.
2. ✅ **Transcript tool.** `tools/transcribe.py <url>`: take YouTube's subtitles with `yt-dlp` (it needs a JavaScript runtime: Node 22+ or Deno); if there are none, download the audio only and transcribe it locally with MacWhisper's `mw` CLI, or with open `whisper.cpp` on other machines. Saves to `data/transcripts/`.
   Why: YouTube interviews are a large source, and the AI cannot watch video.
   Check: one prison video from Lebed & Shaman (https://www.youtube.com/@LebedShaman) gives a text file in `data/transcripts/`; then decide whether the `small` model is good enough for Russian or a larger one is needed.
3. ✅ **Source catalogue, both schools.** For each source: ID, genre (memoir, ethnography, dictionary, journalism, video, lyrics), scope (place, years, institution), reliability, link.
   Video: start from Lebed & Shaman (only the prison videos: series «НаКумаре», «Культяпка» (juvenile prison), «Зона строгого режима», феня, понятия; the channel has about 730 videos), then find other channels of former prisoners, so no claim rests on one narrator.
   Why: the reference may only cite what is catalogued; scope tells a local rule from a general one.
   Check: every entry has all fields; the verdict is in the journal.
   Machine transcripts (YouTube's captions or Whisper) garble jargon and names, so a term is quoted from a transcript only after checking it against a second source or the audio.
4. **Post-Soviet reference.** Concepts (понятия, the difference спрашивать / интересоваться, roles such as смотрящий, масти, debts, words and responsibility), classic trap riddles with their accepted answers, and at least 60 terms. Each claim: meaning, a quote in its source language, source IDs, scope, general or local.
   Why: scenes and debriefs stand on this; a thin start means invented detail.
   Check: no claim without a source ID; at least 60 terms.
5. **Shared curriculum.** About 12 trap types and about 8 answer moves. Each: mechanism, an example from each school, an everyday example, and the test that tells it from its look-alike.
   Why: this is what the database tracks and what lessons are built from.
   Check: every entry has the fields.
6. **Database and script.** `tools/db.py` (standard library): read the state, record a session, schedule items with SM-2 (spaced repetition: a well-answered item comes back later and later, a failed one tomorrow), pick the next targets (due first, then weakest), and report the reserve rule. Tested with pytest.
   Why: the next lesson comes from a record, not from the AI's memory.
   Check: `pytest` passes.
7. **`/interest`, post-Soviet school.** Load the state, pick 1-3 targets, build a scene with a hidden goal for the character, play 4-8 exchanges, let Taras guess what the character wanted, debrief errors only, record.
   Check: one real session end to end; `data/` changes; nothing from `data/` in `git status`.
8. **Three real sessions, then tune.**
   Check: a journal line per session with what changed.
9. **East Coast school.** Reference (Big L "Ebonics" as a slang anchor; Nas, Wu-Tang, Common, Mos Def, Biggie, 2Pac, KRS-One, Mobb Deep; documentary sources first) and its characters in `/interest`.
   Check: as in steps 4 and 7.

## Later: more lesson types

In this order unless sessions show otherwise:

1. **Riddle of the day**: one trap, 60 seconds.
2. **Parry in 10 words**: a series of provocations; scored for precision and brevity.
3. **Find the trap**: a finished dialogue; name the moment and the trap type.
4. **Transfer**: the same trap at a job interview or a negotiation.
5. **Term cards** with spaced repetition.
