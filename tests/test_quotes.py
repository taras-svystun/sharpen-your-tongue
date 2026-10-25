"""Every «quote» in a school reference appears word for word in the source copies in data/."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_quotes  # noqa: E402

# Quoted from a source we do not hold; the reference says where it was seen.
NOT_IN_OUR_COPIES = {
    "На тюрьме не спрашивают, а интересуются",  # ps:src:17, quoted on mybook.ru, not in our saved part
}


def test_every_quote_is_in_a_source_copy():
    text = check_quotes.corpus()
    if not text:
        pytest.skip("no source copies in data/ (they are personal; see README)")
    _, bad = check_quotes.unmatched("post-soviet", text)
    assert set(bad) <= NOT_IN_OUR_COPIES, set(bad) - NOT_IN_OUR_COPIES
