# 0001: Public repo, personal data only on the Mac

Date: 2026-10-25. Status: accepted.

## Context

Taras wants the repo public: the method, prompts and curriculum may help others. The database will hold his answers under pressure, which is a portrait of how he reacts to manipulation. That must not be public.

## Decision

`data/` is in `.gitignore` and never committed. `data-examples/` holds an empty, public template with the same shape. Scripts read `data/` and create it from the template if it is missing.

## Consequences

- His progress has no backup on GitHub. If the Mac dies, the history is gone. Accepted; a private backup can be added later without changing this.
- Before every commit, `git status` must show nothing under `data/`. Session logs, examples quoted from his answers, and journal lines must not copy his personal answers into public files.
