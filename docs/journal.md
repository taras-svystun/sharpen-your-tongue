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

## 2026-10-25: Step 2, transcript tool

- `tools/transcribe.py <url>`: YouTube subtitles via yt-dlp, else audio only through MacWhisper's `mw` (or whisper.cpp), saved to `data/transcripts/<id>.md` with title, channel, date and method.
- Cause of the first failure: YouTube answered HTTP 429 on its subtitle server for automatic Russian captions, even with curl-cffi impersonation. Evidence: yt-dlp's error line. Fix: subtitles are an optimisation, not a dependency; any subtitle error falls back to audio.
- Research verdict: the 429 is a known, intermittent block on YouTube's timedtext endpoint, not an IP-wide ban (https://github.com/yt-dlp/yt-dlp/issues/13831, checked 2026-10-25).
- Test video «Режим строгий, базар вольный!» (34:27): 5209 words in 4 min 11 s with the `small` model. Readable for gist; jargon and names are sometimes garbled. Verdict: fine for summaries; terms need a second check. A larger model is worth a try.
- Not tested: the whisper.cpp path.
- Structure: added `requirements.txt` to the layout map; otherwise ok.

## 2026-10-25: Transcript tool, the real cause of HTTP 429

- Cause: the 429 hit only machine-translated tracks. YouTube labelled this Russian video "uk", so the "ru" track yt-dlp asked for was a translation (`tlang=ru` in its URL). Evidence: the original track `uk-orig` downloaded at once, while `ru` failed 5 times out of 5 at 30 s intervals and from other player clients. This replaces the step 2 verdict above ("intermittent endpoint block"), which was wrong.
- Fix: `pick_track` takes manual subtitles in `--lang`, else the original automatic track (no `tlang=`) whatever its label, never a translation. Same video: 6 s instead of 4 min.
- Research verdict: yt-dlp labels the original automatic track `<lang>-orig` and gives translations a `tlang` parameter (yt-dlp 2026.10.21, `extractor/youtube/_video.py`).
- Tried and dropped: youtube-transcript-api (no gain once the right track is chosen, one more dependency); other player clients (tv, web_safari: errors; mweb: no captions).
- Quality: YouTube's captions are about as good as Whisper `small` on jargon, slightly better on names, but have no punctuation. Whisper is now the fallback for videos with no captions, so a larger model can wait until it is actually used.
- Structure: ok.
