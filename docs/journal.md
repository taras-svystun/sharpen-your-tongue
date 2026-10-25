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

## 2026-10-25: Step 3 review, what the first pass missed

- Bug: with `--subs-only`, a refusal from YouTube (HTTP 429) exited with code 3, so the batch queued the video for Whisper and went on, against the rule "on 429, stop the batch". Cause: the subtitle `except` treated "refused" like "absent". Fix: in that mode a refusal exits 1, which stops the loop; test added. The README loop checked by hand with exit codes 0, 3 and 1.
- Gap: the catalogue said nothing about whether we can read a source, and step 4 can quote only what it reads. Added an **Access** field. Free and read: Медиазона, Новая газета, Шаламов. Paid or library only: Лихачёв (the lihachev.ru PDF found earlier is just his bibliography), Росси, Олейник, Galeotti, all East Coast books. Videos: transcripts through the tool.
- Fixed: the Новая газета entry named a second article that was never found; it is one piece by А. Виноградов (written 2019-11-10). Its citations (Кузнецов, Амальрик) went to Candidates.
- Defined **independent** in `GLOSSARY.md`: a retelling does not count as a second source, and guests of a channel may count separately when cited by name.
- Structure: ok.

## 2026-10-25: Step 3, more voices and the "Ask Taras" list

- Catalogued 4 more: `ps:src:11` Олейник 2005 (five colonies of Kharkiv oblast, 2003), `ps:src:12` a Belarusian talk show on понятия (2019), `ps:src:13` hromadske's film on the Кременчуцька juvenile colony (2022), `ps:src:14` a Georgian policy brief on criminal subculture in prisons (2022). Ukraine now has three independent voices (Lebed & Shaman, Олейник, hromadske); Belarus and Georgia one each.
- Method: two videos taken with `--subs-only`, a minute apart (13 170 and 2 852 words, seconds each); PDFs that WebFetch could not decode were read with `pdftotext`.
- Agreement 18: sources I cannot open go to an "Ask Taras" list; copies, pirated ones included, live only in `data/sources/`. Why: a link to a pirated copy in a public repo invites a takedown of the whole repo.
- Research verdict: Belarus has a talk show and a series («Закон в натуре») but its key document, Вясна's ИК-17 report, was not found in full; Kazakhstan gave no testimony on понятия, only news on torture (web and YouTube search, 2026-10-25).
- Structure: added "source copies" to `data/` in the layout map; otherwise ok.

## 2026-10-25: Step 4, post-soviet reference

- `resources/schools/post-soviet/reference.md`: 6 concepts (понятия, the word as a deed, спрашивать / интересоваться, масти, red and black zones, play and debts), 3 trap riddles with accepted answers, 76 terms; 85 IDs (`ps:t:<word>`, `ps:r:<n>`) for the database of step 6. 33 labels say general, 51 local or one source.
- Check: `tests/test_reference.py` (every entry cites a `ps:src:` ID, at least 60 terms, IDs unique, every cited source is catalogued). 11 tests pass; a fake entry without a source is caught.
- Sources: Taras found 5 of the 7 on the "Ask Taras" list. Catalogue updated: Росси (`ps:src:07`, 1987 edition with text), Балдаев (`ps:src:08` is now the 1992 «Края Москвы» dictionary we hold, not the 1997 edition), Лихачёв (`ps:src:06`, the scan is the reprint inside Балдаев 1992). New: `ps:src:15` Кудин (Лукьяновское СИЗО, 1997-98), `ps:src:16` Вясна interview (Шклов, 2022), `ps:src:17` Лозовский (Russia and Ukraine, around 2000). Шаламов chapters and the Медиазона 2019 article saved as text.
- Research verdict: the file taken for Абрамкин's «Как выжить в советской тюрьме» is Андрей Кудин's «Как выжить в тюрьме», written in Лукьяновка; source: О. Крижанівська, ХПГ, 2001-12-12 (https://archive.khpg.org/1008168656).
- Research verdict: «смотрящий» is absent from Росси (material to 1961) and Балдаев (1992) but present in Kyiv 1997, Ukraine 2000s, Belarus 2010s and Kostroma 2019: a post-Soviet word. Its root, the ban on questions, is in Лихачёв (1933): «правила воровского „приличия" не позволяют вору задавать вопросы» (p. 62).
- Research verdict: «На тюрьме не спрашивают, а интересуются» is found in one first-hand source only (Лозовский, via a mybook.ru citation); classic прописка riddles only in low-reliability sources (vse42.ru, anonymous YouTube channels), kept as candidates.
- Method: Балдаев and Лихачёв are scans without text; OCR with macOS Vision (a Swift script, not kept: the copies are personal, and README names OCRmyPDF as the open way). Dictionaries are cited by headword and page. Two quotes from WebFetch's summariser proved inexact (it named the wrong author for Медиазона), so every quote was taken from a downloaded text with `grep`.
- Errors caught in review: three citations did not hold (Кудин has no «грев», only «подогревают»; Лозовский's «до хаты» means "home"; Балдаев says «Напускной вид»); fixed. Sentences that explain why a rule exists are marked *our reading*, so inference is not passed off as a source.
- YouTube: 3 videos by captions, 2 by Whisper, one search. One gap was shorter than a minute: the Whisper loop started while the captions loop was in its last pause. One Whisper transcript (oEFwzU8sk9U, «Как правильно заходить в камеру») is a prank vlog, not about prison; not cited. «в ответе» rests on captions only and is marked not usable until checked against the audio.
- Structure: the reference no longer restates the general/local rule (links to `GLOSSARY.md`); `data-examples/README.md` said files arrive in step 4, now step 6. Structure: fixed (2 items).

## 2026-10-25: Step 4, Абрамкин and the newcomer riddles

- Taras's answers: take riddles from anonymous channels, flagged low; «в ответе» checked against the audio (S5UJgZkT2vw @ 16:12) and now usable; drop the search for the rest of Абрамкин.
- Catalogued `ps:src:18` Абрамкин and Чижов, ch. 2 (interviews of 1988-91, the copy Taras found) and `ps:src:19`, four anonymous YouTube channels as one low-reliability source, since they likely copy each other.
- Reference now: 6 concepts, 18 trap riddles, 87 terms (93 `ps:t:` IDs). Абрамкин was the third source that made общак, грев, конь, малява, беспредел and наколка general, and gave 8 riddles with accepted answers, among them a false choice answered by a third way (`ps:r:10`) and an insult left unanswered (`ps:r:9`).
- Research verdict, correcting the step 4 entry above: «смотрящий» is late Soviet, not post-Soviet. It is absent from Росси (to 1961) and Балдаев (1992) but used in the interviews of 1988-91 (`ps:src:18`, §2.6).
- Research verdict: the classic прописка riddles (свадьба, гармошка) appear both in Абрамкин (late 1980s) and in anonymous videos of 2015-2019: the answers have stayed the same for 30 years.
- Method: a script checked all 231 «quotes» in the reference against the source texts. Fixed 4 that were not word for word (two words corrected from the captions, one dropped «это», one case ending). The 11 left unmatched are headings, term mentions, the mybook citation, and two OCR misreads checked by eye. Also dropped a riddle variant (the train) whose answer the captions do not give.
- YouTube: 4 videos by captions, one at a time, a minute apart; no refusals.
- Structure: ok.

## 2026-10-25: Keep every scrap; quote checker kept in the repo

- Agreement 19 (Taras): nothing found is thrown away; a one-source or low-reliability item goes in, flagged. Applied to what step 4 had skipped: 8 more riddles (`ps:r:19`-`ps:r:26`, among them the train riddle, «рога есть?», the swan, precision tests, pranks) and 33 more terms (скатка, дальняк, сечка, кобура, локалка, микрон, батя, обосновывать and others). Reference: 6 concepts, 26 riddles, 120 terms. Where a riddle's answer is not legible in the captions, the entry says so and asks for the audio.
- Catalogued `ps:src:20`, the vse42.ru article (low); it is a second source for «здесь не спрашивают, а интересуются».
- The quote checker moved from the session scratchpad to `tools/check_quotes.py`, since the scratchpad is lost with the session; README has its command; making it a test is in step 9 of `docs/PLAN.md`. Run: 292 quotes, 11 unmatched, all headings, term mentions, the mybook citation or OCR misreads.
- Taras's YouTube suggestions found and listed as candidates: «Всё о тюрьме», «ТЮРЕМНЫЙ ПОДКАСТ», Варламов's «Тюрьмы»; «Азбука тюрьмы» is ps:src:02. Three searches, a minute apart.
- Structure: added `check_quotes` to the layout map; otherwise ok.

## 2026-10-25: Audio checks by Taras

- Taras listened to the 12 passages marked "check the audio" (10 riddles, 2 words). All captions held; added from the audio: the domino answer «половину или середину» (`ps:r:21`), the full swan rhyme, «пацаном» where the captions garbled it, «бурбулятор», and «за бабу» as the wrong first answer to «за что сел». A viewer's comment gives another reading of the corners riddle (угол = уголовник), kept with the lowest reliability.
- Open: «яма» (S5UJgZkT2vw @ 16:12). Not clear from context; the 1992 dictionary gives «Оперчасть ИТУ» among its meanings (p. 301).
- Structure: ok.

## 2026-10-25: Clean-up before step 5

A review of every file gave 30 points; Taras approved all but Windows encodings; the `sys.path` hack in tests stays, as advised.

- Bug: without `--subs-only`, a subtitle refusal (HTTP 429) fell back to downloading the audio, one more request after a refusal, against the rule in `CLAUDE.md`. Cause: the fallback dated from the first 429, which came from asking for translations; `pick_track` fixed that, so the fallback only hid real refusals. Fix: any subtitle failure exits 1 in every mode; test added, and it fails on the old code.
- Bug: when yt-dlp wrote no subtitle file, `next(glob)` crashed with `StopIteration`; now a clear error. The whisper.cpp path wrote text without time stamps; it now reads SRT into the same `[m:ss]` paragraphs as the captions (unit test; whisper.cpp itself still not run).
- Quote check is now a test (`tests/test_quotes.py`, skips without copies in `data/`), moved up from step 9. The checker skips riddle names in headings, splits dictionary senses, and ignores a space before punctuation: 11 unmatched fragments became 1, the mybook citation, listed in the test with its reason. A new test checks that every reference entry has a label.
- Labels: the two dictionaries now count together as one source. A third source was found in Абрамкин, Лозовский or Lebed & Shaman for фраер, сука, параша, баланда, намордник, мойка, чифир, so they stay general; грев has none and is now local. This corrects the step 4 entry that called грев general.
- Reference: one ID for малолетка/взросляк; the первоход quote attributed; `ps:src:12` citations carry the video ID; a video quote is from captions unless marked *Whisper* (each transcript's header names its method, so the marker is not repeated per quote).
- One home per fact: the general/local rule lives in `GLOSSARY.md`, the harshness limits in `teaching-method.md` §8; PLAN and the school READMEs link to them. "riddle" added to the glossary and counted as an item; step 5 will tag each riddle with its trap type.
- Catalogues: stale lines on ps:src:01 updated, duplicate candidates removed; East Coast: Taras's copies of Anderson and Conover are Bookey summaries, a retelling, never quoted as the authors. README: Turbo timing, the refusal stop, an explicit second loop (the old "same loop" would have emptied its own queue), `pdftotext` for the quote check, the state of `data-examples/`.
- In `data/` (not tracked): a duplicate Кудин copy removed, three copies renamed to the naming scheme.
- Checked: `pytest` 16 passed; quote check 286 quotes, 1 known unmatched; a real `--subs-only` run on R6bgO2gqXaM gave the same text as before in 17 s; the README loops pass `bash -n`.
- Structure: CLAUDE.md layout map now lists README, GLOSSARY and `docs/`; fixed.
