# Sharpen Your Tongue

A daily trainer for quick wit under pressure: read a situation, spot manipulation and word traps, and answer provocations briefly, precisely and calmly. The training grounds are "schools", closed worlds where words are binding: post-Soviet prison subculture first, US East Coast street culture next. Lessons run in [Claude Code](https://claude.com/claude-code) from this folder.

Status: under construction, see `docs/PLAN.md`. The lesson itself (`/interest`) comes at step 7.

## Set up

Prerequisites:

- Python 3.11 (tested; 3.10+ should work)
- Node.js 22+ or Deno 2.3+: yt-dlp needs a JavaScript runtime to read YouTube ([yt-dlp wiki](https://github.com/yt-dlp/yt-dlp/wiki/EJS)). The tool passes `--js-runtimes node`; with Deno only, edit `yt_dlp()` in `tools/transcribe.py`.
- ffmpeg: `brew install ffmpeg`
- A local Whisper, for videos without usable subtitles. One of:
  - [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) (macOS app; ships the `mw` CLI). Pick a model in the app.
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

It tries YouTube's subtitles first. YouTube often refuses them with HTTP 429; the tool then downloads the audio only and transcribes it locally (a 34-minute video took about 4 minutes with MacWhisper's small model).

Run the tests:

```bash
.venv/bin/pytest -q
```
