---
name: interest
description: Run one daily lesson of Sharpen Your Tongue in the post-soviet school - load the state, play a scene with a hidden goal, let Taras guess it, debrief errors only, record. Use when Taras types /interest or asks for today's lesson.
---

# /interest

One lesson, about 10-15 minutes (agreement 1 in `docs/PLAN.md`; the name is agreement 13).

How to teach, give feedback and score is in `resources/teaching-method.md`. Read it first, every time; this file only gives the order of the steps.

## 1. Load the state

```bash
.venv/bin/python tools/db.py status --school post-soviet
.venv/bin/python tools/db.py next --school post-soviet
```

If `status` says RESEARCH MORE TERMS, tell Taras in one line before the lesson (agreement 12).

The targets are what `next` prints, in its order. If they mix a **new** item with old ones, play two scenes: first the old ones together, then the new one alone (§2), shorter. If time runs out, drop the new one; it comes back next time.

Read each target where it is defined: traps in `resources/curriculum/traps.md` with the moves they name in `moves.md`, terms and riddles in `resources/schools/post-soviet/reference.md`. Read the last five entries of `data/session-notes.md` (if it exists), so a scene is not repeated.

## 2. Build the scene, and seal it

Before the first line, decide:

- **Place and people**: from the reference only (a хата in a СИЗО, a colony, a этап). Every fact the scene uses must be in the reference; mark its scope in the debrief.
- **The character's hidden goal**: what he wants from Taras (a debt, a rank, a confession, a laugh at his cost), and why.
- **The trap moment**: at which exchange the target trap or riddle comes, and the answer the reference accepts.

Write this plan as the start of today's entry in `data/session-notes.md` (create the file if missing) before the scene begins. The goal is then fixed and cannot drift toward Taras's guess.

## 3. Play 4-8 exchanges

- Open with one line in Ukrainian setting the place, then the character speaks Russian with феня, as in the sources. Taras may answer in any language.
- One character reply per turn; wait for Taras. No hints, no out-of-scene comments.
- The world reacts: a weak answer has a real cost in the scene (a debt, a nickname, lost status), harsh within §8.
- If Taras asks something out of scene (he marks it with `(?)`), answer in one line. If it was a target term, its quality is at most 3.
- End the scene when the trap has played out and at least 4 exchanges have passed, or at 8.

## 4. The guess

Ask: **«Чого він від тебе хотів?»** He names the goal, the moment and the trap. Wait. Then reveal the sealed plan in two lines.

## 5. Debrief

Ukrainian, errors only, shorter than the scene (§4). If one answer was weak, first ask for his own better answer (§3), wait, then give one stronger answer. Close with the same move in ordinary life, one line, and name any *local*, *one source* or *low reliability* fact the scene used.

Score each target 0-5 (§5). The guess counts: a good answer with the trap unnamed is at most 4; a trap not seen at all is 0.

## 6. Record

```bash
.venv/bin/python tools/db.py record ID=Q [ID=Q ...]
```

Finish today's entry in `data/session-notes.md`: the scene in one line, his slips (short), the scores, and anything that suggests changing this method (for step 8 of `docs/PLAN.md`). Tell Taras in one line what comes back tomorrow (quality under 3) and what is pushed ahead.
