import sys
from pathlib import Path

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


def test_pick_track_prefers_manual_then_automatic():
    meta = {"subtitles": {}, "automatic_captions": {"ru": [], "en": []}}
    assert transcribe.pick_track(meta, "ru") == ("automatic_captions", "ru")
    meta["subtitles"] = {"ru": []}
    assert transcribe.pick_track(meta, "ru") == ("subtitles", "ru")
    assert transcribe.pick_track(meta, "uk") is None
