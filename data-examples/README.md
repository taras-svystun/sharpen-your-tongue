# Data template

The public shape of `data/`. `data/` itself is git-ignored because it holds personal answers (see `docs/adr/0001-public-repo-local-data.md`).

- `sessions.jsonl`: the lesson log, empty here. `tools/db.py record` copies it to `data/` on the first session and appends one line per session, for example `{"date": "2026-11-01", "scores": {"trap:false-choice": 3}}`: item IDs and qualities 0-5, nothing else. Item states are computed from this log, never stored.
- `session-notes.md` (not templated): `/interest` creates it and writes one entry per lesson: the sealed plan of the scene, then the slips and scores. Read by the next lesson and by tuning (step 8).
