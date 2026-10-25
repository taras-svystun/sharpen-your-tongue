"""The lesson skill names files and tools by path; a renamed file must not break it silently."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from items import ROOT  # noqa: E402

SKILL = ROOT / ".claude" / "skills" / "interest" / "SKILL.md"


def test_every_path_in_the_skill_exists():
    paths = set(re.findall(r"(?:resources|docs|tools)/[\w./-]+\.(?:md|py)", SKILL.read_text()))
    assert paths, "the skill names no paths: did the pattern break?"
    assert [p for p in sorted(paths) if not (ROOT / p).exists()] == []
