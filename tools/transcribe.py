"""Turn a YouTube video into a plain-text transcript in data/transcripts/.

Usage:
    .venv/bin/python tools/transcribe.py <url> [--lang ru] [--force-audio]

Order of attempts:
1. YouTube's own subtitles (manual first, then automatic), via yt-dlp.
2. If there are none, if YouTube refuses them (it often answers HTTP 429 on
   its subtitle server), or with --force-audio: download the audio only and
   transcribe it locally with MacWhisper's `mw` CLI, or with whisper.cpp's
   `whisper-cli` when `mw` is missing (set WHISPER_MODEL to a ggml model).

Transcripts are other people's words, so they stay in git-ignored data/.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "transcripts"
MW = "/Applications/MacWhisper.app/Contents/MacOS/mw"
CHUNK_SECONDS = 30  # one timestamped paragraph per ~30 s, so claims can cite a moment


def yt_dlp(*args):
    """Run yt-dlp from this venv. Node 22+ or Deno solves YouTube's JS challenge."""
    cmd = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "node", "--quiet", "--no-warnings", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError((result.stderr.strip().splitlines() or ["yt-dlp failed"])[-1])
    return result.stdout


def stamp(ms):
    s = int(ms // 1000)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def json3_to_text(data):
    """YouTube json3 captions -> lines '[m:ss] text', grouped into ~30 s paragraphs."""
    paragraphs, start, words = [], None, []
    for event in data.get("events", []):
        text = "".join(seg.get("utf8", "") for seg in event.get("segs", [])).replace("\n", " ").strip()
        if not text:
            continue
        t = event.get("tStartMs", 0)
        if start is None:
            start = t
        elif t - start >= CHUNK_SECONDS * 1000:
            paragraphs.append(f"[{stamp(start)}] {' '.join(words)}")
            start, words = t, []
        words.append(text)
    if words:
        paragraphs.append(f"[{stamp(start)}] {' '.join(words)}")
    return "\n\n".join(paragraphs)


def pick_track(meta, lang):
    """Return (kind, key) of the best caption track, or None."""
    for kind in ("subtitles", "automatic_captions"):
        tracks = meta.get(kind) or {}
        for key in (lang, f"{lang}-orig"):
            if key in tracks:
                return kind, key
    return None


def from_subtitles(url, kind, key, tmp):
    flag = "--write-subs" if kind == "subtitles" else "--write-auto-subs"
    yt_dlp(url, "--skip-download", flag, "--sub-langs", key, "--sub-format", "json3", "-o", f"{tmp}/sub.%(ext)s")
    path = next(Path(tmp).glob("sub*.json3"))
    return json3_to_text(json.loads(path.read_text(encoding="utf-8")))


def from_audio(url, lang, tmp):
    yt_dlp(url, "-f", "bestaudio", "-x", "--audio-format", "m4a", "-o", f"{tmp}/audio.%(ext)s")
    audio = f"{tmp}/audio.m4a"
    if Path(MW).exists():
        return subprocess.run([MW, "transcribe", audio, "--language", lang, "--format", "txt", "--timestamps"],
                              check=True, capture_output=True, text=True).stdout.strip(), "MacWhisper (mw)"
    if shutil.which("whisper-cli") and os.environ.get("WHISPER_MODEL"):
        wav = f"{tmp}/audio.wav"  # whisper.cpp wants 16 kHz mono WAV
        subprocess.run(["ffmpeg", "-loglevel", "error", "-i", audio, "-ar", "16000", "-ac", "1", wav], check=True)
        subprocess.run(["whisper-cli", "-m", os.environ["WHISPER_MODEL"], "-l", lang, "-otxt", "-of", f"{tmp}/out", wav],
                       check=True, capture_output=True)
        return Path(f"{tmp}/out.txt").read_text(encoding="utf-8").strip(), "whisper.cpp"
    sys.exit("No subtitles and no local Whisper: install MacWhisper, or whisper.cpp and set WHISPER_MODEL (see README).")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("url")
    parser.add_argument("--lang", default="ru", help="ISO 639-1 language of the speech (default: ru)")
    parser.add_argument("--force-audio", action="store_true", help="skip subtitles, transcribe the audio")
    args = parser.parse_args()

    meta = json.loads(yt_dlp(args.url, "-J", "--skip-download"))
    track = None if args.force_audio else pick_track(meta, args.lang)
    with tempfile.TemporaryDirectory() as tmp:
        text = None
        if track:
            try:
                text = from_subtitles(args.url, *track, tmp)
                method = "YouTube manual subtitles" if track[0] == "subtitles" else "YouTube automatic captions"
            except RuntimeError as err:
                print(f"Subtitles failed ({err}); transcribing the audio instead.", file=sys.stderr)
        if text is None:
            text, method = from_audio(args.url, args.lang, tmp)

    date = meta.get("upload_date") or ""
    header = "\n".join([
        f"# {meta.get('title')}",
        "",
        f"- Channel: {meta.get('channel')}",
        f"- URL: https://www.youtube.com/watch?v={meta['id']}",
        f"- Uploaded: {date[:4]}-{date[4:6]}-{date[6:]}" if date else "- Uploaded: unknown",
        f"- Duration: {stamp((meta.get('duration') or 0) * 1000)}",
        f"- Method: {method}, language {args.lang}",
        "",
    ])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{meta['id']}.md"
    out.write_text(header + "\n" + text + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
