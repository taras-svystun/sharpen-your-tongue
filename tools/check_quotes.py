"""Check that every «quote» in a school reference appears word for word in the source texts.

Usage: .venv/bin/python tools/check_quotes.py [school]   (default: post-soviet)

Reads the copies in git-ignored data/ (data/sources/*.txt, data/sources/text/*.txt, data/transcripts/),
so it only works with your own copies. Prints each fragment it cannot find; a fragment is the
text between ellipses, or one numbered sense of a dictionary entry. Quotes in headings are
riddle names, not quotes, and are skipped. tests/test_quotes.py runs the same check.
"""
import re
import sys
from pathlib import Path

from items import reference_text

ROOT = Path(__file__).resolve().parent.parent


def norm(s):
    s = s.replace("ё", "е").replace("Ё", "Е").lower()
    s = re.sub(r"[«»\"“”„]", '"', s)
    s = re.sub(r"[–—−]", "-", s)
    s = re.sub(r"[^\w\"\-\.,:;!?()…/ ]", " ", s)
    s = re.sub(r"\s+([.,:;!?])", r"\1", s)  # OCR and some copies put a space before punctuation
    return re.sub(r"\s+", " ", s).strip()


def corpus():
    files = [*ROOT.glob("data/sources/*.txt"), *ROOT.glob("data/sources/text/*.txt"), *ROOT.glob("data/transcripts/*.md")]
    out = []
    for f in files:
        x = f.read_text(errors="ignore")
        x = re.sub(r"=== page \d+ ===\n(\d+\n)?(СЛОВАРЬ\n)?([А-Я]\n)?", "", x)  # OCR page headers
        x = re.sub(r"\(см\.\)", "", x)  # dictionary cross-references, left out when quoting
        x = re.sub(r"-\n", "", x) + "\n" + re.sub(r"-\n", "-", x)  # a line-end hyphen: split word or real hyphen
        x = re.sub(r"\[\d+:\d+(:\d+)?\]|\n\d\d:\d\d\n", " ", x)  # transcript time stamps
        out.append(norm(x))
    return "\n".join(out)


def quotes(text):
    text = re.sub(r"(?m)^#.*$", "", text)  # headings name riddles; they are not quotes
    out, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch == "«":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == "»" and depth:
            depth -= 1
            if depth == 0:
                out.append(text[start:i])
    return out


def unmatched(school, text):
    """Fragments of the school's reference quotes that are not in `text`, a corpus()."""
    ref = reference_text(ROOT / "resources" / "schools" / school)
    qs, bad = quotes(ref), []
    for q in qs:
        # ellipses join fragments; "2." or "З." (an OCR "3") joins the senses of a dictionary entry
        for frag in re.split(r"…|\.\.\.(?=\s)|\s[\dЗ]\.\s", q):
            f = norm(frag).strip(" .,;")
            if len(f) >= 12 and f not in text:
                bad.append(frag.strip())
    return qs, bad


def main():
    school = sys.argv[1] if len(sys.argv) > 1 else "post-soviet"
    text = corpus()
    if not text:
        sys.exit("No source texts in data/: nothing to check against.")
    qs, bad = unmatched(school, text)
    for frag in bad:
        print("NOT FOUND:", frag[:140])
    print(f"{len(qs)} quotes, {len(bad)} fragments not found")


if __name__ == "__main__":
    main()
