# Journal

Newest at the bottom.

## 2026-10-25: Step 1, foundations

- Purpose sharpened after the first grill: quick wit and calm, precise answers under pressure; not French, not office-first.
- Plan written: six steps, first lesson type is a conversation simulation.
- `resources/teaching-method.md`: Fluent's explanation and exercise-density rules adapted (one trap per scene, guess first, errors-only feedback, honest scoring, dodging is not winning).
- `data/` is git-ignored; ADR 0001 records why and the cost (no remote backup).

## 2026-10-25: Plan revised after the second grill

- Added schools (post-soviet first, east-coast at step 9) sharing one curriculum of traps and moves, so he learns the abstraction, not the setting.
- Added a transcript tool step: YouTube interviews are a major source and the AI cannot watch video.
- Standing decisions numbered in `docs/PLAN.md` ("What we agreed"); repo layout and one-home-per-fact rule in `CLAUDE.md`; project words in `GLOSSARY.md`.
- Teaching method: source labels (general / local / one source / lyrics only) and the harshness rule with its limits.

## 2026-10-25: Rules for reproducibility and structure review

- Two standing rules added (agreements 15-16): README must let a stranger rebuild everything; every step ends with a structure review.
- Research verdict: yt-dlp needs a JavaScript runtime for YouTube (Deno, or Node 22+ with `--js-runtimes node`), source: https://github.com/yt-dlp/yt-dlp/wiki/EJS (wiki, last edited 2026-07-12).
- Research verdict: MacWhisper 14.7.1 ships a CLI, `mw transcribe <file> --language ru --format txt`; checked with `mw help transcribe`.
- Structure: ok.
