"""Step 5 check: every trap and move has its fields, links resolve, and every riddle names a trap type."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import items  # noqa: E402

CURRICULUM = items.CURRICULUM
REFERENCE = items.SCHOOLS / "post-soviet" / "reference.md"

COMMON = ["**Mechanism.**", "- **Post-soviet**:", "- **East coast** (*illustration*):", "- **Everyday**:", "- **Look-alike**:"]
FIELDS = {"traps": COMMON + ["- **Answered by**:"], "moves": COMMON}


def entries(kind):
    """{id: body} of traps.md or moves.md."""
    return dict(items.entries((CURRICULUM / f"{kind}.md").read_text()))


def test_sizes():
    assert len(entries("traps")) >= 10 and len(entries("moves")) >= 6


def test_every_entry_has_the_fields():
    missing = [(i, f) for kind, fields in FIELDS.items() for i, body in entries(kind).items() for f in fields if f not in body]
    assert not missing, missing


def test_links_resolve():
    known = set(entries("traps")) | set(entries("moves"))
    text = "".join((CURRICULUM / f"{k}.md").read_text() for k in FIELDS) + REFERENCE.read_text()
    cited = set(re.findall(r"`((?:trap|move):[a-z-]+)`", text))
    assert cited <= known, cited - known
    ps_known = set(items.defined_ids(REFERENCE.read_text()))
    ps_cited = set(re.findall(r"`(ps:[tr]:[a-z0-9-]+)`", "".join((CURRICULUM / f"{k}.md").read_text() for k in FIELDS)))
    assert ps_cited <= ps_known, ps_cited - ps_known


def test_every_trap_is_answered_by_a_move():
    moves = set(entries("moves"))
    unanswered = [i for i, body in entries("traps").items()
                  if not set(re.findall(r"`(move:[a-z-]+)`", body.split("- **Answered by**:")[1])) & moves]
    assert not unanswered, unanswered


def test_every_riddle_names_one_trap_type():
    riddles = re.split(r"^(?=### ps:r:)", REFERENCE.read_text(), flags=re.M)[1:]
    bad = [r.split("\n")[0] for r in riddles if len(re.findall(r"^- \*\*Trap type\*\*: `trap:[a-z-]+`$", r, re.M)) != 1]
    assert riddles and not bad, bad


def test_trap_examples_match_riddle_tags():
    tags = dict(re.findall(r"^### (ps:r:\d+) .*\n+- \*\*Trap type\*\*: `(trap:[a-z-]+)`", REFERENCE.read_text(), re.M))
    wrong = [(trap, r) for trap, body in entries("traps").items()
             for r in re.findall(r"`(ps:r:\d+)`", body.split("- **Post-soviet**:")[1].split("\n")[0]) if tags.get(r) != trap]
    assert not wrong, wrong
