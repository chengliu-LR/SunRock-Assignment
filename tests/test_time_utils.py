from datetime import datetime, timezone
from app.utils.time import align_to_next_quarter


def test_align_to_next_quarter_basic():
    dt = datetime(2024, 1, 1, 13, 36, tzinfo=timezone.utc)
    aligned = align_to_next_quarter(dt)
    assert aligned.minute == 45
    assert aligned.hour == 13


def test_align_to_next_quarter_wrap_hour():
    dt = datetime(2024, 1, 1, 13, 59, tzinfo=timezone.utc)
    aligned = align_to_next_quarter(dt)
    assert aligned.minute == 0
    assert aligned.hour == 14
