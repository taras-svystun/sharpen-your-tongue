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

## 2026-10-25: Step 5, shared curriculum

- `resources/curriculum/traps.md`: 14 trap types; `moves.md`: 11 answer moves. Each has a mechanism (what it takes, how, where it stops), a post-soviet example by riddle ID, an east-coast example, an everyday example, and a look-alike with the test that tells them apart. Which move answers which trap is written once, in `traps.md`.
- Each of the 26 riddles in the post-soviet reference now names one trap type. The types came from the riddles, not from a textbook list: false choice is the commonest (5 riddles), performance next (4).
- Decision: the east-coast examples are invented illustrations in plain English with no slang, labelled as such, because that school has no reference until step 9 and agreement 6 forbids unsourced facts. Step 9 replaces them with sourced ones.
- Decision: 14 traps and 11 moves instead of about 12 and 8. Merging would have hidden pairs with opposite answers (performance: don't do it; nerve test: do it calmly), which are the most useful look-alikes to train.
- Check: `tests/test_curriculum.py` (fields present, IDs resolve, every trap has a move, every riddle has exactly one trap type, a trap's example riddle carries that trap's tag). `pytest` 22 passed; a removed field and a misspelled tag each make it fail. Quote check unchanged: 286 quotes, 1 known unmatched.
- Structure: "look-alike" added to `GLOSSARY.md`; otherwise ok.

## 2026-10-25: One item parser; step 6, database and script

- `tools/items.py`: the one place that knows where an item is defined (trap and move headings, concept headings, term bullets, riddle headings). Both reference tests and `db.py` use it; before, each test had its own regex, and a blank line already broke one of them once. 176 items: 14 traps, 11 moves, 125 terms (concepts included), 26 riddles.
- `tools/db.py` (standard library): `record`, `next`, `status`. The only stored record is a log, `data/sessions.jsonl`, one line per session with item IDs and qualities. Item states are replayed from it with SM-2 on every run.
- Decision: a log, not a state file or SQLite. Why: one home per fact (a state file would repeat what the log says, and the two can disagree), a change to the schedule rules re-applies to the whole history, and the file stays readable by eye and by the lesson. Cost: a replay on each run, under a millisecond at this size.
- Decision: SM-2 as Wozniak wrote it (a failure starts over and keeps the easiness factor), with two changes from `teaching-method.md`: a first answer at 5 goes straight to 6 days (§6), and `next` offers at most one new item, since a new item gets its own scene (§2). Order: overdue, then weak (last quality under 4), then one new; a mastered item that is not due is never picked.
- `record` refuses unknown IDs and qualities outside 0-5, so a typo never enters the log; `status` names IDs in the log that are no longer defined, so a renamed item is not lost silently.
- The 0-5 quality scale moved into `teaching-method.md` §5, its one home; `db.py` links to it.
- Check: `pytest` 33 passed (11 new for the database). Loosening the "weak" rule makes a test fail. `status` and `next` ran on the real, still empty, `data/`; nothing was recorded, so the real log stays empty.
- Structure: layout map now lists `items` and says "session log" instead of "item states"; `data-examples/` holds the empty log template. Structure: fixed (2 items).

## 2026-10-25: Step 7, the /interest skill (built, not yet played)

- `.claude/skills/interest/SKILL.md`: the order of a lesson only (state, targets, sealed scene, 4-8 exchanges, the guess, debrief, record). How to teach and score stays in `teaching-method.md`; the skill links to it.
- Decision: the scene's plan (hidden goal, trap moment, accepted answer) is written to `data/session-notes.md` before the first line. Why: otherwise nothing stops the hidden goal from drifting toward Taras's guess, and the guess is scored. The same file keeps one short entry per lesson, so scenes do not repeat and step 8 has material; the log stays numbers only.
- Decision: when `next` mixes a new item with old ones, two scenes, old first, the new one alone and shorter (`teaching-method.md` §2); the new one is dropped if time runs out.
- Decision: only the targets are scored. A move Taras happens to use is not recorded unless it was a target, so the log measures what was tested, not what came up.
- Check: `tests/test_skill.py`, every file path the skill names exists (a misspelled path makes it fail). `pytest` 34 passed. `db.py next` on the empty log gives `trap:false-choice`, so the first lesson is one new trap, alone. The step's own check, one real session, waits for Taras.
- Structure: layout map now lists the skill and the session notes; the skill links to agreements 1 and 13 instead of restating them. Structure: ok.

## 2026-10-25: Are all instructions reachable?

- Taras's worry from Fluent: method files that nothing points to are never read. Checked every tracked `.md`: who links to it and when it is read. `CLAUDE.md` loads every session and says when to read the plan, the method and the ADR; `/interest` names every file a lesson needs.
- Found one gap: the school README (language and characters) was linked by nothing, and the skill restated its rule instead. The skill now reads it and links to it; `moves.md` is named by full path, so the path test covers it.
- Structure: fixed (1 item).

## 2026-10-25: First lesson played; /interest gets a check and a close

- First real `/interest` session played (scores stay in `data/`). Step 7 done; step 8 at 1 of 3.
- Taras could not tell when the lesson had ended. `/interest` §6 now checks that the log holds today's scores (`tail -1 data/sessions.jsonl`, `db.py next`), and a new §7 closes with one fixed line: done, what was recorded, what comes tomorrow.
- Check: today's log line holds the session; `pytest` 34 passed (the path test covers the skill).
- Structure: ok.

## 2026-10-25: record checks itself

- The close check from the last entry was an instruction the model could skip. Now `db.py record` reads the log back after the write: the last line must be the entry it sent, or it exits with "not recorded". It then prints each target with its next due date, and `/interest` §7 closes from that output, so a lesson cannot close with numbers the log does not hold.
- Not covered: a lesson where `record` is never run. The fixed close line names the recorded scores, which makes that slip visible to Taras; a hook would be the next step if it ever happens.
- Check: `pytest` 35 passed; the new test edits the log after the write and expects the read-back to fail.
- Structure: ok.

## 2026-10-25: Harvest from sources already on disk

- Read what the reference did not use yet: 4 uncited transcripts (BWE9JSvtrng, R6bgO2gqXaM, TXHEJcQTlV8, oEFwzU8sk9U), the tattoo video 6CAxbmw6m0A, Кудин ch. 2 (interrogation), Абрамкин §2.2-2.4 and §2.9, and the Балдаев dictionary for words on talk, deals and debts. No YouTube requests.
- Verdict on the transcripts: three of four are near empty (recovery talk, a clickbait sketch); the yield came from the books. Кудин ch. 2 is a catalogue of manipulation methods; Абрамкин §2.9 explains the prisoners' семья.
- Added: concept `ps:t:semya`; riddles `ps:r:27`-`ps:r:29` (cleaning by turn, «Где чалился?», «уболтать»); a new section, Interrogation traps, with `ps:r:30`-`ps:r:32`; 23 terms (people: порядочный, левый, штымп, терпила, подельник and others; words: маза, подписаться, замазать, гнилой заход, расколоться, сдать and others); additions to `ps:t:dolg` (no debt without a deal), `ps:t:fuflo` (an empty promise is a lie) and `ps:t:otvechat-za-slova`.
- Decision: no new trap types. Each new riddle fits one of the 14; a new type needs more than one riddle behind it.
- Check: quote check 382 quotes, 1 known unmatched; `pytest` 35 passed; `db.py status` 153 terms, 32 riddles, reserve ok.
- Structure: `reference.md` is at 494 lines; the next harvest must first split it by topic (concepts and riddles / terms) and teach `tools/items.py` the new file. Two repeated quotes replaced by links. Otherwise ok.

## 2026-10-25: Split the post-soviet reference

- `reference.md` (494 lines) is now `reference.md` (concepts, riddles, interrogation traps; 329 lines) and `terms.md` (words; 164 lines).
- `tools/items.py` names the files once (`REFERENCE_FILES`) and joins them (`reference_text()`); the item loader, the quote check and the tests read the reference only through it, so a later split is one line.
- Check: the same numbers before and after: 382 quotes (1 known unmatched), 153 terms, 32 riddles; `pytest` 35 passed.
- Structure: layout map, glossary, teaching method and `/interest` name the new file. Structure: ok.

## 2026-10-25: Абрамкин found whole; Лозовский part 2; the Center's dictionary

- Research verdict: the rest of Абрамкин's «Как выжить в советской тюрьме» is in the Wayback Machine, `prison.org/biblio/kakvizjit/` (2001-2002 copies); prison.org itself refused connections. New material is part 1 (the law of arrest and trial) and part 3 (prayers); part 2 is the chapter we had. The same archive holds the Center's «Краткий толковый словарь тюремного мира» (`biblio/glossary2.htm`, 2000), now `ps:src:22`. Source: Wayback CDX index, 2026-10-25.
- Research verdict: Лозовский part 2 exists only as a paid book; the free ЛитРес preview (avidreaders.ru) holds the chapter «Понятия воровские, людские, гадские». Added to `ps:src:17`.
- New source `ps:src:21`, Абрамкин's essay «Тюремная субкультура» (2008); with `ps:src:18` and `ps:src:22` it counts as one source.
- Added: concept `ps:t:lyudskoe-gadskoe` (how a charge is judged: by-the-brother or as-with-a-гад, a charge must be grounded); riddles `ps:r:33` (forbidden words: свидетель, козья шерсть) and `ps:r:34` (a charge from your past life); 17 terms (гад, чушок, сухарь, угловой, предъява, метла, очевидец, душняк and others); the broom as a second description of `ps:r:10`.
- Safety: pages fetched as HTML or a zipped `.txt` only, each file type checked before opening, archives read by Python without extracting paths; Wayback was asked one page at a time, 6 s apart, after one 429 answer.
- Check: quote check 428 quotes, 1 known unmatched; `pytest` 35 passed; `db.py status` 171 terms, 34 riddles, reserve ok.
- Structure: `reference.md` 356 lines, `terms.md` 181. Structure: ok.

## 2026-10-25: transcribe.py took an English dub for Russian

- Cause: on videos where YouTube added an English dub, there are two original speech tracks (`en-US-orig`, `ru-orig`); `pick_track` took the first `-orig` key and ignored `--lang`. Evidence: vdiQJ2x2teg and N1hiINQgAc8, labels «audio en-US, ru, original captions en-US-orig, ru-orig», header «track en-US-orig», English text.
- Fix: among original tracks, the one in `--lang` comes first; with none in `--lang` (a mislabelled video) the old order holds. Test: `test_pick_track_prefers_the_original_in_lang_over_a_dub` failed before, passes now; `pytest` 36 passed. The two transcripts are being fetched again.
- Also seen: age-restricted videos (x6JtNdVZ5ng, 5vS9J4oM1S4) need a signed-in account; skipped, not a bot block. Signing in with Taras's browser cookies is his decision.

## 2026-10-25: Conflict stories from the new transcripts

- Read 4 of the new Lebed & Shaman transcripts (2DKOko460eM, IGu_kzMoM0g, oGRj_2O3who, N1hiINQgAc8); the others are on disk, not yet read.
- Also added `ps:r:38` (a false confession offered to end a beating: refuse it, and keep records) and the term дорожник.
- Added riddles `ps:r:35` (a loan you cannot refuse: lend it as a game stake, with witnesses), `ps:r:36` (a rumour that you eat with a рогатый: ask why the accuser did not come to you), `ps:r:37` (a lie let off as a «непонятка»: make the judges name the same act done by you); a Ukrainian case for `ps:r:34` (a hidden past, «под вопросом», the search note), which is the first source for it independent of Абрамкин; a milder «protection for parcels» for `ps:r:29`; the loan/card-debt paradox in `ps:t:dolg`; 6 terms (рогатый, под вопросом, сбой по жизни, интрига, поисковая, уделить).
- Check: quote check 466 quotes, 1 known unmatched; `pytest` 36 passed.
- Structure: `reference.md` 386 lines, `terms.md` 188. Structure: ok.
