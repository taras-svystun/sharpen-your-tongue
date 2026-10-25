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


def test_srt_groups_into_timestamped_paragraphs():
    # whisper.cpp writes SRT; its transcripts must be citable @ m:ss like the captions.
    srt = ("1\n00:00:00,000 --> 00:00:04,000\nза базар\nотвечаешь\n\n"
           "2\n00:00:10,500 --> 00:00:12,000\nпонял\n\n"
           "3\n01:00:31,000 --> 01:00:33,000\nдальше\n")
    assert transcribe.srt_to_text(srt) == "[0:00] за базар отвечаешь понял\n\n[1:00:31] дальше"


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


def test_pick_track_prefers_the_original_in_lang_over_a_dub():
    # Real case (vdiQJ2x2teg): YouTube added an English dub, so both tracks
    # are originals; the English one came first and was taken for Russian.
    meta = {"subtitles": {}, "automatic_captions": {
        "en-US-orig": track("https://yt/timedtext?v=x"),
        "ru-orig": track("https://yt/timedtext?v=x"),
    }}
    assert transcribe.pick_track(meta, "ru") == ("automatic_captions", "ru-orig")


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


def test_a_refusal_never_falls_back_to_the_audio(monkeypatch):
    # Without --subs-only too: after a refusal, an audio download is one more request to YouTube.
    meta = '{"id": "x", "automatic_captions": {"ru": [{"url": "https://yt/timedtext?v=x"}]}}'
    monkeypatch.setattr(transcribe, "yt_dlp", lambda *args: meta)
    def refused(*args):
        raise RuntimeError("HTTP Error 429: Too Many Requests")
    monkeypatch.setattr(transcribe, "from_subtitles", refused)
    monkeypatch.setattr(transcribe, "from_audio", lambda *args: pytest.fail("audio downloaded after a refusal"))
    monkeypatch.setattr(sys, "argv", ["transcribe.py", "https://yt/x"])
    with pytest.raises(SystemExit) as exit_info:
        transcribe.main()
    assert exit_info.value.code not in (0, 3)


def test_missing_subtitle_file_is_a_clear_error(monkeypatch, tmp_path):
    monkeypatch.setattr(transcribe, "yt_dlp", lambda *args: "")
    with pytest.raises(RuntimeError, match="no subtitle file"):
        transcribe.from_subtitles("https://yt/x", "automatic_captions", "ru", tmp_path)
