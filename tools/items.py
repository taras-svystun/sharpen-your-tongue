"""Every item the database tracks, read from where it is defined: one parser for tools and tests.

An item is defined, not just mentioned, at one of these places:
- a trap or move heading in resources/curriculum/: `## trap:false-choice`
- a concept heading in a school reference:        `### Понятия ... `ps:t:ponyatiya``
- a term bullet in a school reference:            `- **мужик** `ps:t:muzhik`: ...`
- a riddle heading in a school reference:         `### ps:r:5 «Свадьба»`

A school's reference is split by topic into REFERENCE_FILES; reference_text() joins them.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "resources" / "curriculum"
SCHOOLS = ROOT / "resources" / "schools"

KINDS = {"trap": "trap", "move": "move", "t": "term", "r": "riddle"}
SHARED = "shared"  # the school of a trap or a move
REFERENCE_FILES = ("reference.md", "terms.md")  # concepts and riddles; terms

DEFINITION = re.compile(
    r"^## ((?:trap|move):[a-z-]+)$"             # curriculum heading
    r"|^### [^\n`]*`([a-z]+:t:[a-z-]+)`"        # concept heading
    r"|^- \*\*[^*]+\*\* `([a-z]+:t:[a-z-]+)`"   # term bullet
    r"|^### ([a-z]+:r:\d+)\b",                  # riddle heading
    re.M,
)


HEADING = re.compile(r"^#{1,3} ", re.M)


def entries(text):
    """[(id, body)] in order of appearance, duplicates kept. A body runs to the next definition or heading."""
    found = list(DEFINITION.finditer(text))
    out = []
    for i, m in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(text)
        heading = HEADING.search(text, m.end(), end)
        out.append((next(g for g in m.groups() if g), text[m.start():heading.start() if heading else end]))
    return out


def defined_ids(text):
    """IDs defined in a markdown text, in order of appearance, duplicates kept."""
    return [i for i, _ in entries(text)]


def kind(item_id):
    """'trap:x' -> trap, 'move:x' -> move, 'ps:t:x' -> term, 'ps:r:5' -> riddle."""
    parts = item_id.split(":")
    return KINDS[parts[0] if len(parts) == 2 else parts[1]]


def reference_text(school_dir):
    """The whole reference of one school, its files joined in order."""
    return "\n".join((school_dir / n).read_text() for n in REFERENCE_FILES if (school_dir / n).exists())


def load():
    """{item id: school} for every item. Traps and moves belong to SHARED."""
    out = {}
    for name in ("traps", "moves"):
        out.update(dict.fromkeys(defined_ids((CURRICULUM / f"{name}.md").read_text()), SHARED))
    for ref in sorted(SCHOOLS.glob("*/reference.md")):
        out.update(dict.fromkeys(defined_ids(reference_text(ref.parent)), ref.parent.name))
    return out
