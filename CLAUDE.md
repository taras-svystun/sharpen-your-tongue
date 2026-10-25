# Sharpen Your Tongue

A daily trainer for quick wit under pressure, using Ukrainian and post-Soviet prison subculture as the training ground: read a situation, see its hidden rules, spot manipulation and word traps, and answer provocations briefly, precisely and calmly.

- `GLOSSARY.md`: the project's own words (school, scene, trap, move, item). Use them in code, docs and commits. School jargon is not here; it lives in each school's reference.
- `docs/PLAN.md`: the plan and **what we agreed** (standing decisions, numbered). Read it when starting a step. A new decision from a discussion goes there in one line, once.
- `docs/journal.md`: what each finished step did and why, and each research verdict.
- `resources/teaching-method.md`: how to ask, explain, give feedback and score. Read it before every session.
- `docs/adr/`: decisions that are hard to undo. Read before changing where personal data lives.

## Layout

One job per file, one home per fact. Other files link to a fact by its ID, never copy it.

```
resources/teaching-method.md          how to teach (all schools)
resources/curriculum/                 shared by all schools
  traps.md                            trap types, IDs like trap:false-choice
  moves.md                            answer moves, IDs like move:reject-premise
resources/schools/<school>/           one folder per school: post-soviet, east-coast
  README.md                           language, characters, scope of the school
  sources.md                          source catalogue, IDs like ps:src:03
  reference.md                        concepts and terms, each citing source IDs
tools/                                scripts (db, transcribe)
tests/                                pytest
data-examples/                        public template of data/
data/                                 git-ignored: profile, item states, sessions,
                                      transcripts, long lyrics
```

Folders are created when their first content arrives. When a file passes about 500 lines, split it by topic and update this map.

## Learning lab

Taras is learning social intelligence: how status, words and responsibility work in a closed group with strict unwritten rules. Prison subculture is the case study, not the goal; every debrief ends with how the same move works in ordinary life.

Who does what: the AI writes the scenarios, the feedback and the code; Taras owns the ideas and the answers, and must be able to explain every piece. Explain at the level of the mechanism: why a rule exists, what it protects, what happens to the one who breaks it.

Content stays educational: understanding, recognition and defence. No glorifying crime, and no guidance for real criminal activity.

## Rules of this project

- **Personal data stays in `data/`**, which git ignores (the repo is public). Never copy his answers or scores into a tracked file: not the journal, not an example, not a commit message.
- **No shared code with Fluent** (`~/Documents/Projects/Fluent`). Taras forbids it. Copy and adapt ideas only.

## Finishing a step

- `README.md` has a copy-paste command for every way to run the project.
- `git status --ignored data/` shows `data/` only as ignored, and nothing personal is staged.
