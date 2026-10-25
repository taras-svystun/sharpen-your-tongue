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

Install:

```bash
git clone https://github.com/taras-svystun/sharpen-your-tongue.git
cd sharpen-your-tongue
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Your own data lives in `data/`, which git ignores. It is created on first use.

## Run

Transcribe a YouTube video into `data/transcripts/<video-id>.md` (Russian by default):

```bash
.venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
.venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang uk
.venv/bin/python tools/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --force-audio
```

It takes YouTube's own subtitles first: manual ones in `--lang`, else YouTube's original automatic captions, whatever language YouTube labelled them (a 34-minute video takes seconds). It never asks for a machine-translated track: those are worse, and YouTube answers them with HTTP 429. With no usable track, the tool downloads the audio only and transcribes it locally (about 4 minutes for 34 minutes with MacWhisper's small model).

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
# then the same loop over data/catalogue/whisper-queue.txt, without --subs-only
```

Any other failure stops the loop (`break`): find the cause before running it again.

Books and articles: each school's `sources.md` gives the bibliographic record of every source; find your own copy and put it in `data/sources/`. The reference cites dictionaries by headword and books by page or chapter, so any edition with the same pagination works. Two copies used here are scans without text (Балдаев 1992, Лихачёв); to search them, OCR them first, for example with the open [OCRmyPDF](https://ocrmypdf.readthedocs.io) (`ocrmypdf -l rus in.pdf out.pdf`) or macOS Live Text.

Check that every quote in a school's reference appears word for word in your copies (it lists what it cannot find; headings and term mentions show up too):

```bash
.venv/bin/python tools/check_quotes.py post-soviet
```

Run the tests:

```bash
.venv/bin/pytest -q
```
