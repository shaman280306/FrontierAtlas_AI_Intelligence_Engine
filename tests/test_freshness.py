import pytest
from datetime import datetime, timezone, timedelta
from src.utils.dates import (
    parse_iso_or_relative_date, is_within_hours, to_iso8601_utc, get_utc_now
)

def test_parse_iso8601():
    date_str = "2026-11-22T14:30:00Z"
    dt, conf = parse_iso_or_relative_date(date_str)
    assert dt is not None
    assert dt.year == 2026
    assert dt.month == 11
    assert dt.day == 22
    assert dt.hour == 14
    assert dt.minute == 30
    assert conf == 1.0

def test_parse_unix_timestamp():
    # 1700000000 is 2023-11-14T22:13:20Z
    dt, conf = parse_iso_or_relative_date(1700000000)
    assert dt is not None
    assert conf == 1.0
    assert dt.tzinfo == timezone.utc

def test_parse_relative_dates():
    now = datetime(2026, 11, 23, 12, 0, 0, tzinfo=timezone.utc)
    
    # "2 hours ago"
    dt, conf = parse_iso_or_relative_date("2 hours ago", ref_time=now)
    assert dt is not None
    assert dt == datetime(2026, 11, 23, 10, 0, 0, tzinfo=timezone.utc)
    assert conf == 0.85

    # "45 mins ago"
    dt, conf = parse_iso_or_relative_date("45 mins ago", ref_time=now)
    assert dt is not None
    assert dt == datetime(2026, 11, 23, 11, 15, 0, tzinfo=timezone.utc)
    assert conf == 0.85

    # "yesterday"
    dt, conf = parse_iso_or_relative_date("yesterday", ref_time=now)
    assert dt is not None
    assert dt == datetime(2026, 11, 22, 12, 0, 0, tzinfo=timezone.utc)
    assert conf == 0.80

def test_strict_24_hour_freshness():
    now = datetime(2026, 11, 23, 12, 0, 0, tzinfo=timezone.utc)

    # 10 hours ago -> FRESH
    fresh_time = now - timedelta(hours=10)
    assert is_within_hours(fresh_time, hours=24, ref_time=now) is True

    # Exactly 23 hours ago -> FRESH
    almost_stale = now - timedelta(hours=23)
    assert is_within_hours(almost_stale, hours=24, ref_time=now) is True

    # 25 hours ago -> STALE (REJECT)
    stale_time = now - timedelta(hours=25)
    assert is_within_hours(stale_time, hours=24, ref_time=now) is False

    # 5 days ago -> STALE (REJECT)
    old_time = now - timedelta(days=5)
    assert is_within_hours(old_time, hours=24, ref_time=now) is False

    # Future date beyond 15 min leeway -> INVALID (REJECT)
    future_time = now + timedelta(hours=2)
    assert is_within_hours(future_time, hours=24, ref_time=now) is False
