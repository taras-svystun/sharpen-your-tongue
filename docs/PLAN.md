# Plan

## Purpose

A daily trainer for quick wit under pressure. Taras learns to notice manipulation and word traps (for example a false choice, where both offered options are bad), to answer provocations briefly, precisely and calmly, without swearing or insults, and to stand up for himself and his people. Ukrainian and post-Soviet prison subculture is the training ground: a world where words are binding ("за базар отвечаешь"), so every trap and every answer is sharp. A second, smaller aim: know what prison life and its words really are (смотрящий, хата, масти, and so on), from sources, without romanticising crime.

What it is not: French, offices, or a script to speak in prison slang at work.

## What we agreed (2026-10-25)

- Short daily sessions, around 10-15 minutes. French comes first.
- It must be fun enough to want every morning: riddles, traps, games, logic.
- A full tutor, not a riddle prompt: exercises, analysis, feedback, adaptation. What he masters fast is left behind; time goes to his weakest spots.
- Methods that work on Taras are copied from Fluent and adapted. No shared code or library with Fluent, ever (Taras's rule).
- The repo is public. Everything personal (his answers, scores, profile) lives in `data/`, which git ignores. Method, prompts and curriculum are public. See `docs/adr/0001-public-repo-local-data.md`.
- Quotes keep the language of their source (Russian or Ukrainian). Explanations are in Ukrainian.
- First and only lesson type for now: a conversation simulation. The AI plays a character (смотрящий за хатой, a cellmate, a guard), tests or provokes Taras, and then debriefs: what he misread, where he took the bait, where he got cornered.

## Steps

Each step has a check. A step is done when its check passes.

1. **Foundations.** Adapt Fluent's teaching method to this project; keep `data/` out of git, with a public template in `data-examples/`.
   Why: without the method, sessions fall back to generic chatbot feedback; without the ignore rule, his answers leak to a public repo.
   Check: `git check-ignore data/x.json` prints the path; `resources/teaching-method.md` exists.
2. **Sourced reference.** Research the core concepts (понятия, масти, роли: смотрящий and others), around 30 terms, and the classic trap riddles with their accepted answers. Each entry: plain meaning, a quote in its source language, the source and date.
   Why: without sources, the AI invents "понятия" that sound right and are wrong.
   Check: every entry in `resources/reference.md` names a source; the verdict is in the journal.
3. **Curriculum of traps and moves.** About 12 trap types (false choice, gift as debt, question about your past, a dare to swear or promise, flattery, leading question, ...) and about 8 answer moves (reject the premise, answer with a question, take a third option, a short pause, ...). Each: the mechanism, a prison example, an everyday example, and the test that tells it apart from its look-alike.
   Why: this is what the database tracks and what the next lesson is built from; without it, adaptation has nothing to count.
   Check: every entry in `resources/curriculum.md` has the four fields.
4. **Database and script.** `tools/db.py` (standard library only): read the state, record a session, schedule items with SM-2 (spaced repetition: an item you answer well comes back later and later; a failed one comes back tomorrow), and pick the next targets (due items first, then the weakest). Tested with pytest.
   Why: so the next lesson comes from a record, not from the AI's memory.
   Check: `pytest` passes.
5. **The `/scene` lesson.** A skill in `.claude/skills/scene/`: load the state, pick 1-3 target items, build a scene with a hidden goal for the character, play 4-8 exchanges, then let Taras guess what the character wanted before the debrief, then debrief errors only, then record.
   Why: this is the product; steps 1-4 feed it.
   Check: one real session runs end to end; `data/` changes; `git status` shows nothing from `data/`.
6. **Three real sessions, then tune.** Fix what bores or misleads; choose the second lesson type.
   Why: the format is a guess until he has played it.
   Check: a journal line per session with what changed.
