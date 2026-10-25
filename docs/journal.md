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

## 2026-10-25: Transcript tool, polite requests and YouTube's labels

- How the 429 was found (for next time): YouTube's track list (youtube-transcript-api's error message) showed only one generated track, "uk", for Russian speech; the "ru" URL in yt-dlp's metadata carried `tlang=ru`; downloading `uk-orig` worked at once while `ru` kept failing. Method: list what the server offers, compare a call that works with one that fails, change one thing at a time.
- Polite requests: yt-dlp's `-t sleep` preset (0.75 s between requests, 5 s before subtitles, 10-20 s before a download). One video: 6 s → 17 s. Batches: one video at a time, a minute apart (rule in `CLAUDE.md`).
- The tool now prints YouTube's labels (video, audio and original caption languages) and warns when they differ from `--lang`; they also go into the transcript header. The audio track was labelled "uk" too, so checking audio tracks does not reveal a wrong label; only the text does.
- MacWhisper fallback passes `--model whisper-cpp:ggml-model-whisper-turbo` when downloaded, without changing the app's selected model. Same video: 7 min 16 s; on the test passage it matches YouTube's captions («тюрях маячит», «в инсте мы публикуем») where `small` garbled them.
- Structure: ok.

## 2026-10-25: Step 3, source catalogue

- `resources/schools/post-soviet/sources.md`: 10 catalogued sources (`ps:src:01`-`10`): Lebed & Shaman, «Азбука тюрьмы», Медиазона, Новая газета, Шаламов, Лихачёв, Росси, Балдаев, Олейник, Galeotti; plus candidates, including Ukrainian journalism (Радіо Свобода, hromadske, ХПГ) and the Ombudsman's prison reports. `resources/schools/east-coast/sources.md`: 5 (Anderson, Bourgois, Canada, Conover, Big L "Ebonics") plus candidates. Each catalogue entry has genre, scope, reliability, link and a "Checked" line.
- Decision: one entry per channel, book or outlet, not per video; a video is cited as `ps:src:01 / <video-id> @ m:ss`. Why: 169 prison videos from one channel are one narrator pair, and the general/local rule counts independent sources, not videos.
- Decision: candidates sit in the same file under "Candidates", so finding a source and checking it are separate moves. The reliability scale is defined once, in `GLOSSARY.md`.
- Cheap first (Taras's addition, agreement 17): `tools/transcribe.py --subs-only` never runs Whisper and exits with code 3, so a batch takes every captioned video in seconds and leaves the rest for a Whisper pass. `--list` lists a channel or a `ytsearch` query (metadata only), so YouTube still gets every request through the one polite tool.
- Research verdict: Lebed & Shaman has 732 videos, about 169 on prison by title; places named: Бучанская колония, Бердянская 77, Лукьяновское СИЗО, Чернигов, a juvenile colony (`--list`, 2026-10-25).
- Research verdict: «Азбука тюрьмы», 12 episodes from 50 interviews, Настоящее Время, summer 2021 (https://www.currenttime.tv/a/azbuka-tyurmy-podkast/31682968.html).
- Research verdict: «Мопс дядя Пес» rejected: a humiliation stream for money, not testimony (Медуза, 2017-06-08).
- Weak spots: Ukraine has only one catalogued voice (Lebed & Shaman); its Ukrainian candidates must be checked before step 4 calls any Ukrainian rule general. Олейник's publisher and year, and every "from memory" candidate, are unconfirmed. Russian web search returned thin results; YouTube search through the tool worked better.
- Structure: added "video lists" to `data/` in the layout map; otherwise ok.
