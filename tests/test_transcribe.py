import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import transcribe  # noqa: E402


def test_json3_groups_into_timestamped_paragraphs():
    data = {"events": [
        {"tStartMs": 0, "segs": [{"utf8": "за базар"}, {"utf8": " отвечаешь"}]},
        {"tStartMs": 5000, "segs": [{"utf8": "\n"}]},  # line-break event, no words
        {"tStartMs": 10000, "segs": [{"utf8": "понял"}]},
        {"tStartMs": 31000, "segs": [{"utf8": "дальше"}]},
    ]}
    assert transcribe.json3_to_text(data) == "[0:00] за базар отвечаешь понял\n\n[0:31] дальше"


def test_stamp_adds_hours_only_when_needed():
    assert transcribe.stamp(65_000) == "1:05"
    assert transcribe.stamp(3_725_000) == "1:02:05"


def track(url):
    return [{"ext": "json3", "url": url}]


def test_pick_track_takes_original_captions_never_a_translation():
    # Real case: Russian speech that YouTube labelled "uk"; "ru" is a machine
    # translation (tlang=), and YouTube answers translations with HTTP 429.
    meta = {"subtitles": {}, "automatic_captions": {
        "ru": track("https://yt/timedtext?v=x&tlang=ru"),
        "uk": track("https://yt/timedtext?v=x"),
        "uk-orig": track("https://yt/timedtext?v=x"),
    }}
    assert transcribe.pick_track(meta, "ru") == ("automatic_captions", "uk-orig")
    meta["subtitles"] = {"ru": track("https://yt/timedtext?v=x&lang=ru")}
    assert transcribe.pick_track(meta, "ru") == ("subtitles", "ru")


def test_pick_track_none_when_only_translations():
    meta = {"automatic_captions": {"ru": track("https://yt/timedtext?v=x&tlang=ru")}}
    assert transcribe.pick_track(meta, "ru") is None


def test_youtube_labels_show_the_mislabel():
    meta = {"language": "uk",
            "formats": [{"vcodec": "none", "acodec": "opus", "language": "uk"},
                        {"vcodec": "avc1", "acodec": "none"}],
            "automatic_captions": {"uk-orig": [], "ru": []}}
    assert transcribe.youtube_labels(meta) == "video uk, audio uk, original captions uk-orig"


def test_subs_only_skips_whisper_when_no_captions(monkeypatch):
    # Cheap first: a batch's first pass must not spend minutes on Whisper.
    monkeypatch.setattr(transcribe, "yt_dlp", lambda *args: '{"id": "x", "automatic_captions": {}}')
    monkeypatch.setattr(transcribe, "from_audio", lambda *args: pytest.fail("Whisper ran"))
    monkeypatch.setattr(sys, "argv", ["transcribe.py", "https://yt/x", "--subs-only"])
    with pytest.raises(SystemExit) as exit_info:
        transcribe.main()
    assert exit_info.value.code == 3


def test_subs_only_stops_on_a_refusal(monkeypatch):
    # HTTP 429 means "stop the batch" (CLAUDE.md), so it must not exit 3 like "no captions".
    meta = '{"id": "x", "automatic_captions": {"ru": [{"url": "https://yt/timedtext?v=x"}]}}'
    monkeypatch.setattr(transcribe, "yt_dlp", lambda *args: meta)
    def refused(*args):
        raise RuntimeError("HTTP Error 429: Too Many Requests")
    monkeypatch.setattr(transcribe, "from_subtitles", refused)
    monkeypatch.setattr(sys, "argv", ["transcribe.py", "https://yt/x", "--subs-only"])
    with pytest.raises(SystemExit) as exit_info:
        transcribe.main()
    assert exit_info.value.code != 3
