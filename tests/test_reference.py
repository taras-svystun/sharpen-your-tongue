"""Step 4 check: every entry of a school reference cites a catalogued source, with enough terms."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHOOL = ROOT / "resources" / "schools" / "post-soviet"


def entries(text):
    """Split a reference into (id, body) pairs: a term bullet, or a concept/riddle section."""
    out = []
    for block in re.split(r"\n(?=### |- \*\*[^*]+\*\* `ps:t:)", text):
        m = re.search(r"`(ps:t:[a-z-]+)`|^### (ps:r:\d+)", block, re.M)
        if m:
            out.append((m.group(1) or m.group(2), block))
    return out


def test_every_entry_cites_a_source():
    found = entries((SCHOOL / "reference.md").read_text())
    missing = [i for i, body in found if "ps:src:" not in body]
    assert found and not missing


def test_at_least_60_terms():
    text = (SCHOOL / "reference.md").read_text()
    terms = set(re.findall(r"`(ps:t:[a-z-]+)`", text))
    assert len(terms) >= 60


def test_ids_are_unique():
    ids = [i for i, _ in entries((SCHOOL / "reference.md").read_text())]
    assert len(ids) == len(set(ids))


def test_cited_sources_are_catalogued():
    cited = set(re.findall(r"ps:src:\d+", (SCHOOL / "reference.md").read_text()))
    catalogued = set(re.findall(r"^### (ps:src:\d+)", (SCHOOL / "sources.md").read_text(), re.M))
    assert cited <= catalogued, cited - catalogued


def test_every_entry_has_a_label():
    found = entries((SCHOOL / "reference.md").read_text())
    unlabelled = [i for i, body in found if not re.search(r"\*(general|local|one source)", body, re.I)]
    assert not unlabelled, unlabelled
