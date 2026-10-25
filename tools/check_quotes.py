"""Check that every «quote» in a school reference appears word for word in the source texts.

Usage: .venv/bin/python tools/check_quotes.py [school]   (default: post-soviet)

Reads the copies in git-ignored data/ (data/sources/, data/sources/text/, data/transcripts/),
so it only works with your own copies. Prints each fragment it cannot find; a fragment is the
text between ellipses. Headings and term mentions in «» also show up: read the list by eye.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(s):
    s = s.replace('ё', 'е').replace('Ё', 'Е').lower()
    s = re.sub(r'[«»"“”„]', '"', s)
    s = re.sub(r'[–—−]', '-', s)
    s = re.sub(r'[^\w"\-\.,:;!?()…/ ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def corpus():
    files = [*ROOT.glob('data/sources/*.txt'), *ROOT.glob('data/sources/text/*.txt'), *ROOT.glob('data/transcripts/*.md')]
    out = []
    for f in files:
        x = f.read_text(errors='ignore')
        x = re.sub(r'=== page \d+ ===\n(\d+\n)?(СЛОВАРЬ\n)?([А-Я]\n)?', '', x)  # OCR page headers
        x = re.sub(r'\(см\.\)', '', x)  # dictionary cross-references, left out when quoting
        x = re.sub(r'-\n', '', x) + '\n' + re.sub(r'-\n', '-', x)  # a line-end hyphen: split word or real hyphen
        x = re.sub(r'\[\d+:\d+(:\d+)?\]|\n\d\d:\d\d\n', ' ', x)  # transcript time stamps
        out.append(norm(x))
    return '\n'.join(out)


def quotes(text):
    out, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch == '«':
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == '»' and depth:
            depth -= 1
            if depth == 0:
                out.append(text[start:i])
    return out


def main():
    school = sys.argv[1] if len(sys.argv) > 1 else 'post-soviet'
    ref = (ROOT / 'resources' / 'schools' / school / 'reference.md').read_text()
    text = corpus()
    if not text:
        sys.exit('No source texts in data/: nothing to check against.')
    qs, bad = quotes(ref), 0
    for q in qs:
        for frag in re.split(r'…|\.\.\.(?=\s)', q):
            f = norm(frag).strip(' .,;')
            if len(f) >= 12 and f not in text:
                bad += 1
                print('NOT FOUND:', frag.strip()[:140])
    print(f'{len(qs)} quotes, {bad} fragments not found')


if __name__ == '__main__':
    main()
