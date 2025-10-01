"""Time utilities for aligning timestamps to quarter-hour boundaries.

These helpers centralize the market scheduling rules for start/end times:
- Align any input time to the next quarter: minutes 00, 15, 30, or 45
- Provide a milliseconds helper for consistent Unix epoch ms conversions

All operations assume UTC for determinism and cross-region consistency.
"""

from datetime import datetime, timedelta, timezone

QUARTER_MINUTES = (0, 15, 30, 45)


def align_to_next_quarter(dt: datetime) -> datetime:
    """Return ``dt`` aligned forward to the next quarter-hour boundary.

    - If ``dt`` lacks tzinfo, assume UTC.
    - If already on a boundary but with seconds/micros, normalize to the same minute.
    - Otherwise, move forward to the next 00/15/30/45 minute mark.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    minute = dt.minute
    next_quarter = next((m for m in QUARTER_MINUTES if m > minute), None)
    if next_quarter is None:
        next_dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        next_dt = dt.replace(minute=next_quarter, second=0, microsecond=0)
    if next_dt <= dt.replace(second=0, microsecond=0):
        next_dt += timedelta(minutes=15)
    return next_dt


def ms(dt: datetime) -> int:
    """Convert a datetime to Unix epoch milliseconds.

    Ensures timezone-aware UTC before conversion to avoid ambiguity.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)
