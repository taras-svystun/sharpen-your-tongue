"""Step 4 check: every entry of a school reference cites a catalogued source, with enough terms."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from items import SCHOOLS, entries, kind, reference_text  # noqa: E402

SCHOOL = SCHOOLS / "post-soviet"


def test_every_entry_cites_a_source():
    found = entries(reference_text(SCHOOL))
    missing = [i for i, body in found if "ps:src:" not in body]
    assert found and not missing


def test_at_least_60_terms():
    terms = {i for i, _ in entries(reference_text(SCHOOL)) if kind(i) == "term"}
    assert len(terms) >= 60


def test_ids_are_unique():
    ids = [i for i, _ in entries(reference_text(SCHOOL))]
    assert len(ids) == len(set(ids))


def test_cited_sources_are_catalogued():
    cited = set(re.findall(r"ps:src:\d+", reference_text(SCHOOL)))
    catalogued = set(re.findall(r"^### (ps:src:\d+)", (SCHOOL / "sources.md").read_text(), re.M))
    assert cited <= catalogued, cited - catalogued


def test_every_entry_has_a_label():
    found = entries(reference_text(SCHOOL))
    unlabelled = [i for i, body in found if not re.search(r"\*(general|local|one source)", body, re.I)]
    assert not unlabelled, unlabelled
