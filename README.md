# Sharpen Your Tongue

A daily trainer for quick wit under pressure: read a situation, spot manipulation and word traps, and answer provocations briefly, precisely and calmly. The training grounds are "schools", closed worlds where words are binding: post-Soviet prison subculture first, US East Coast street culture next. Lessons run in [Claude Code](https://claude.com/claude-code) from this folder.

Status: under construction, see `docs/PLAN.md`. The lesson itself (`/interest`) comes at step 7.

## Set up

Prerequisites:

- Python 3.11 (tested; 3.10+ should work)
- Node.js 22+ or Deno 2.3+: yt-dlp needs a JavaScript runtime to read YouTube ([yt-dlp wiki](https://github.com/yt-dlp/yt-dlp/wiki/EJS)). The tool passes `--js-runtimes node`; with Deno only, edit `yt_dlp()` in `tools/transcribe.py`.
- ffmpeg: `brew install ffmpeg`
- A local Whisper, for videos without usable subtitles. One of:
  - [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) (macOS app; ships the `mw` CLI). Download the Turbo model in the app (1.6 GB); the tool uses it when present, else the app's selected model.
  - [whisper.cpp](https://github.com/ggml-org/whisper.cpp), open source: `brew install whisper-cpp`, download a ggml model, and `export WHISPER_MODEL=/path/to/ggml-model.bin`. Not yet tested in this project.
- poppler, to turn PDFs with a text layer into text for the quote check: `brew install poppler` (gives `pdftotext`).

Install:

```bash
git clone https://github.com/taras-svystun/sharpen-your-tongue.git
cd sharpen-your-tongue
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Your own data lives in `data/`, which git ignores. The tools create the folders they need on first use. `data-examples/` holds the public template of `data/`: `tools/db.py` copies it on the first recorded session.

## Run

Transcribe a YouTube video into `data/transcripts/<video-id>.md` (Russian by default):

```bash
.venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
.venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang uk
.venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --force-audio
```

It takes YouTube's own subtitles first: manual ones in `--lang`, else YouTube's original automatic captions, whatever language YouTube labelled them (a 34-minute video takes seconds). It never asks for a machine-translated track: those are worse, and YouTube answers them with HTTP 429. With no usable track, the tool downloads the audio only and transcribes it locally (about 7 minutes for a 34-minute video with MacWhisper's Turbo model). If YouTube refuses the subtitles (HTTP 429 or a "not a bot" check), the tool stops with exit code 1 and asks for nothing more: find the cause before trying again.

It pauses between requests (yt-dlp's `-t sleep` preset), so one video takes about 20 seconds; for several videos, run them one after another, not in parallel. It also prints the languages YouTube claims for the video; they can be wrong, so it warns when they differ from `--lang`.

For many videos, go cheap first. List a channel (metadata only), then take captions for every video in one pass and run Whisper only on what that pass skipped (exit code 3 means "no usable subtitles"):

```bash
mkdir -p data/catalogue
.venv/bin/python tools/transcribe.py "https://www.youtube.com/@LebedShaman/videos" --list > data/catalogue/lebed-shaman.tsv
.venv/bin/python tools/transcribe.py "ytsearch30:бывший заключенный понятия интервью" --list   # search YouTube

# ids.txt: one video id per line, picked from the list
: > data/catalogue/whisper-queue.txt
while read -r id; do
  .venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=$id" --subs-only < /dev/null \
    || { [ $? -eq 3 ] && echo "$id" >> data/catalogue/whisper-queue.txt || break; }
  sleep 60
done < ids.txt

# second pass: Whisper on the queue only
while read -r id; do
  .venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=$id" < /dev/null || break
  sleep 60
done < data/catalogue/whisper-queue.txt
```

Any other failure stops the loop (`break`): find the cause before running it again.

Books and articles: each school's `sources.md` gives the bibliographic record of every source; find your own copy and put it in `data/sources/`. The reference cites dictionaries by headword and books by page or chapter, so any edition with the same pagination works. Two copies used here are scans without text (Балдаев 1992, Лихачёв); to search them, OCR them first, for example with the open [OCRmyPDF](https://ocrmypdf.readthedocs.io) (`ocrmypdf -l rus in.pdf out.pdf`) or macOS Live Text.

The quote check reads plain text only: `.txt` copies in `data/sources/` or `data/sources/text/`, and the transcripts. For a PDF with a text layer:

```bash
pdftotext data/sources/book.pdf data/sources/text/book.txt
```

Check that every quote in a school's reference appears word for word in your copies (it lists what it cannot find; `pytest` runs the same check and skips it when `data/` holds no copies):

```bash
.venv/bin/python tools/check_quotes.py post-soviet
```

The lesson database is one log, `data/sessions.jsonl`, one line per session; each item's schedule is computed from it with SM-2. Lessons call it; you can too:

```bash
.venv/bin/python tools/db.py status                          # items studied and due; the reserve rule
.venv/bin/python tools/db.py next --school post-soviet       # the next 1-3 targets
.venv/bin/python tools/db.py record trap:false-choice=3 ps:r:5=4   # one session; quality 0-5
```

Run the tests:

```bash
.venv/bin/pytest -q
```
