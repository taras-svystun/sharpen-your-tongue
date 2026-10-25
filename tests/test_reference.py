"""Step 4 check: every entry of a school reference cites a catalogued source, with enough terms."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from items import SCHOOLS, entries, kind  # noqa: E402

SCHOOL = SCHOOLS / "post-soviet"


def test_every_entry_cites_a_source():
    found = entries((SCHOOL / "reference.md").read_text())
    missing = [i for i, body in found if "ps:src:" not in body]
    assert found and not missing


def test_at_least_60_terms():
    terms = {i for i, _ in entries((SCHOOL / "reference.md").read_text()) if kind(i) == "term"}
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
