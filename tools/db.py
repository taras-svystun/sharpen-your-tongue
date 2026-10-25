"""The lesson database: a log of sessions in data/, and each item's state replayed from it with SM-2.

The log is the only record. Item states are computed from it on every run, so they are never stored
twice, and a change to the schedule rules applies to the whole history at once.

Usage:
  db.py record ID=Q [ID=Q ...] [--date YYYY-MM-DD]   append one session, then read it back; Q is 0-5
  db.py next [-n 3] [--school S]                      the next targets: due, then weak, then new
  db.py status [--school S]                           counts, due items, the reserve rule

Quality: the 0-5 scale in resources/teaching-method.md §5.
"""
import argparse
import datetime as dt
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import items

LOG = items.ROOT / "data" / "sessions.jsonl"
TEMPLATE = items.ROOT / "data-examples" / "sessions.jsonl"


@dataclass
class State:
    reps: int = 0         # correct answers in a row
    ef: float = 2.5       # SM-2 easiness factor: how fast the interval grows
    interval: int = 0     # days until the next review
    due: dt.date = None
    last_q: int = None
    seen: int = 0


def review(s, q, day):
    """SM-2 (Wozniak, 1990), with one change from teaching-method §6: a first answer at 5 skips a step."""
    if q < 3:
        s.reps, s.interval = 0, 1  # start over; SM-2 leaves the easiness factor as it was
    else:
        s.reps = 2 if s.seen == 0 and q == 5 else s.reps + 1
        s.interval = 1 if s.reps == 1 else 6 if s.reps == 2 else round(s.interval * s.ef)
        s.ef = max(1.3, s.ef + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    s.due, s.last_q, s.seen = day + dt.timedelta(days=s.interval), q, s.seen + 1
    return s


def read_log(path=None):
    path = path or LOG
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def states(log):
    """{item id: State} for every item in the log, replayed in date order."""
    out = {}
    for session in sorted(log, key=lambda x: x["date"]):
        day = dt.date.fromisoformat(session["date"])
        for item_id, q in session["scores"].items():
            out[item_id] = review(out.get(item_id, State()), q, day)
    return out


def record(scores, day, path=None, known=None):
    """Append one session. Refuses unknown IDs and qualities outside 0-5, so the log stays clean."""
    path = path or LOG
    known = items.load() if known is None else known
    bad = [f"{i}={q}" for i, q in scores.items() if i not in known or not 0 <= q <= 5]
    if bad:
        raise ValueError("unknown item or quality outside 0-5: " + ", ".join(bad))
    if not path.exists():  # ADR 0001: data/ is created from the public template
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(TEMPLATE, path)
    entry = {"date": day.isoformat(), "scores": scores}
    with path.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return check_recorded(entry, path)


def check_recorded(entry, path=None):
    """Read the log back: its last line must be this entry. Returns {item id: State} after the replay.

    A lesson missing from the log did not happen for SM-2, so the lesson trusts this, not the write.
    """
    log = read_log(path or LOG)
    if not log or log[-1] != entry:
        raise RuntimeError(f"log does not end with {entry}; last line: {log[-1] if log else 'none'}")
    return states(log)


def pick(known, st, today, n=3, school=None):
    """[(id, reason)]: overdue first, then weak (last quality under 4), then one new item in file order.

    A mastered item that is not due is never picked: time goes to what fails (teaching-method §6).
    At most one new item, since a brand-new item gets a scene of its own (teaching-method §2).
    """
    pool = [i for i, sch in known.items() if school is None or sch in (school, items.SHARED)]
    due = sorted((i for i in pool if i in st and st[i].due <= today), key=lambda i: (st[i].due, st[i].last_q))
    weak = sorted((i for i in pool if i in st and st[i].due > today and st[i].last_q < 4), key=lambda i: st[i].last_q)
    new = [i for i in pool if i not in st]
    ranked = [(i, f"due {st[i].due}") for i in due] + [(i, f"weak, last {st[i].last_q}") for i in weak]
    return (ranked + [(i, "new") for i in new[:1]])[:n]


def reserve(known, st):
    """{school: (studied terms, reserve)}. Agreement 12: the reserve must be at least the studied."""
    out = {}
    for i, sch in known.items():
        if items.kind(i) == "term":
            studied, left = out.get(sch, (0, 0))
            out[sch] = (studied + 1, left) if i in st else (studied, left + 1)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("scores", nargs="+", metavar="ID=Q")
    rec.add_argument("--date", type=dt.date.fromisoformat, default=dt.date.today())
    nxt = sub.add_parser("next")
    nxt.add_argument("-n", type=int, default=3)
    for p in (nxt, sub.add_parser("status")):
        p.add_argument("--school")
    a = ap.parse_args(argv)

    known, today = items.load(), dt.date.today()
    if a.cmd == "record":
        try:
            scores = {i: int(q) for i, q in (s.rsplit("=", 1) for s in a.scores)}
            st = record(scores, a.date, known=known)
        except (ValueError, RuntimeError) as e:
            sys.exit(f"not recorded: {e}")
        print(f"recorded and read back {len(scores)} items on {a.date}")
        for i, q in scores.items():
            print(f"{i}={q}\tnext due {st[i].due}")
        return
    st = states(read_log())
    if a.cmd == "next":
        for i, why in pick(known, st, today, a.n, a.school):
            print(f"{i}\t{items.kind(i)}\t{why}")
        return
    pool = {i: s for i, s in known.items() if a.school is None or s in (a.school, items.SHARED)}
    for k in ("trap", "move", "term", "riddle"):
        ids = [i for i in pool if items.kind(i) == k]
        seen = [i for i in ids if i in st]
        print(f"{k}s: {len(ids)}, studied {len(seen)}, due {sum(st[i].due <= today for i in seen)}")
    for sch, (studied, left) in reserve(pool, st).items():
        print(f"reserve {sch}: {left} unstudied terms vs {studied} studied: {'ok' if left >= studied else 'RESEARCH MORE TERMS'}")
    orphans = sorted(set(st) - set(known))
    if orphans:
        print("in the log but no longer defined (renamed or removed?): " + ", ".join(orphans))


if __name__ == "__main__":
    main()
