"""Step 6 check: SM-2 scheduling, the session log, target picking and the reserve rule."""
import datetime as dt
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import db  # noqa: E402
import items  # noqa: E402

D0 = dt.date(2026, 11, 1)


def day(n):
    return D0 + dt.timedelta(days=n)


def run(qs):
    s = db.State()
    for n, q in enumerate(qs):
        s = db.review(s, q, day(n))
    return s


def test_sm2_intervals_grow_on_success():
    assert [run([4] * k).interval for k in (1, 2, 3)] == [1, 6, 15]  # ef stays 2.5 at quality 4


def test_failure_starts_over_and_keeps_the_easiness():
    before = run([4, 3])
    after = db.review(run([4, 3]), 1, day(2))
    assert (after.reps, after.interval, after.ef) == (0, 1, before.ef)


def test_first_perfect_answer_skips_a_step():
    assert run([5]).interval == 6 and run([4]).interval == 1


def test_easiness_has_a_floor():
    assert run([3] * 20).ef == 1.3


def test_record_creates_the_log_and_replays_in_date_order(tmp_path):
    log, known = tmp_path / "data" / "sessions.jsonl", {"trap:a": "shared"}
    db.record({"trap:a": 4}, day(1), log, known)
    db.record({"trap:a": 1}, day(0), log, known)  # entered late, happened first
    s = db.states(db.read_log(log))["trap:a"]
    assert (s.last_q, s.due) == (4, day(2))


def test_record_refuses_unknown_items_and_bad_quality(tmp_path):
    log = tmp_path / "sessions.jsonl"
    for scores in ({"trap:nope": 3}, {"trap:a": 7}):
        with pytest.raises(ValueError):
            db.record(scores, D0, log, {"trap:a": "shared"})
    assert not log.exists()


def test_pick_due_then_weak_then_new_and_skips_mastered():
    known = dict.fromkeys(["trap:due", "trap:weak", "trap:done", "trap:new"], "shared")
    known["ec:t:x"] = "east-coast"
    st = {"trap:due": run([4]), "trap:weak": run([2]), "trap:done": run([5])}
    st["trap:weak"].due = day(5)  # not due yet, but failed last time
    picked = [i for i, _ in db.pick(known, st, day(3), n=10, school="post-soviet")]
    assert picked == ["trap:due", "trap:weak", "trap:new"]


def test_pick_offers_one_new_item_at_a_time():
    known = dict.fromkeys(["trap:a", "trap:b", "trap:c"], "shared")
    assert db.pick(known, {}, D0) == [("trap:a", "new")]


def test_reserve_counts_terms_only():
    known = {"ps:t:a": "post-soviet", "ps:t:b": "post-soviet", "ps:r:1": "post-soviet", "trap:x": "shared"}
    assert db.reserve(known, {"ps:t:a": run([4]), "ps:r:1": run([4])}) == {"post-soviet": (1, 1)}


def test_cli_record_then_next(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(db, "LOG", tmp_path / "sessions.jsonl")
    first = next(iter(items.load()))
    db.main(["record", f"{first}=1", "--date", "2026-01-01"])
    db.main(["next", "-n", "1"])
    assert capsys.readouterr().out.splitlines()[-1].startswith(first + "\t")
    assert json.loads((tmp_path / "sessions.jsonl").read_text()) == {"date": "2026-01-01", "scores": {first: 1}}
    with pytest.raises(SystemExit):
        db.main(["record", "nope=3"])


def test_items_are_defined_once_and_typed():
    ids = [i for ref in items.SCHOOLS.glob("*/reference.md") for i in items.defined_ids(ref.read_text())]
    assert len(ids) == len(set(ids))
    assert {items.kind(i) for i in items.load()} == {"trap", "move", "term", "riddle"}
