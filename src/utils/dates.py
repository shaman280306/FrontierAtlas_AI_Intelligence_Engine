import re
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
from dateutil import parser as date_parser

def get_utc_now() -> datetime:
    """Return current UTC datetime with timezone awareness."""
    return datetime.now(timezone.utc)

def parse_iso_or_relative_date(date_str: Optional[str or int or float], ref_time: Optional[datetime] = None) -> Tuple[Optional[datetime], float]:
    """
    Parses a wide variety of date formats into a timezone-aware UTC datetime.
    Supports:
      - Unix timestamps (int or float)
      - Standard ISO-8601 strings
      - RFC-2822 / HTTP dates (from RSS feeds)
      - Relative text strings ('2 hours ago', '45 mins ago', 'yesterday', '3 days ago')
    
    Returns:
      (datetime_in_utc, confidence_score)
      confidence_score: 1.0 (strict exact timestamp), 0.8 (relative text), 0.0 (unparseable)
    """
    if date_str is None:
        return None, 0.0

    if ref_time is None:
        ref_time = get_utc_now()

    # 1. Handle numeric timestamps (Unix epoch)
    if isinstance(date_str, (int, float)):
        try:
            # Handle millisecond vs second timestamps
            ts = float(date_str)
            if ts > 1e11:  # milliseconds
                ts = ts / 1000.0
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return dt, 1.0
        except Exception:
            return None, 0.0

    raw_str = str(date_str).strip()
    if not raw_str:
        return None, 0.0

    # If it's a string of pure digits, parse as epoch
    if raw_str.isdigit():
        return parse_iso_or_relative_date(int(raw_str), ref_time)

    # 2. Handle relative strings (e.g. "2 hours ago", "yesterday", "5m ago")
    relative_match = re.match(
        r'(\d+)\s*(second|sec|s|minute|min|m|hour|hr|h|day|d|week|w|month|year)s?\s*ago',
        raw_str,
        re.IGNORECASE
    )
    if relative_match:
        val = int(relative_match.group(1))
        unit = relative_match.group(2).lower()
        if unit in ('second', 'sec', 's'):
            delta = timedelta(seconds=val)
        elif unit in ('minute', 'min', 'm'):
            delta = timedelta(minutes=val)
        elif unit in ('hour', 'hr', 'h'):
            delta = timedelta(hours=val)
        elif unit in ('day', 'd'):
            delta = timedelta(days=val)
        elif unit in ('week', 'w'):
            delta = timedelta(weeks=val)
        elif unit in ('month',):
            delta = timedelta(days=val * 30)
        elif unit in ('year',):
            delta = timedelta(days=val * 365)
        else:
            delta = timedelta(seconds=0)

        dt = ref_time - delta
        return dt, 0.85

    if raw_str.lower() == 'yesterday':
        dt = ref_time - timedelta(days=1)
        return dt, 0.80

    if raw_str.lower() in ('today', 'just now'):
        return ref_time, 0.80

    # 3. Standard string date parsing (ISO-8601, RFC-2822, feedparser formats)
    try:
        dt = date_parser.parse(raw_str)
        if dt.tzinfo is None:
            # Naive datetime: assume UTC with slightly lower confidence
            dt = dt.replace(tzinfo=timezone.utc)
            return dt, 0.90
        else:
            dt = dt.astimezone(timezone.utc)
            return dt, 1.0
    except Exception:
        pass

    return None, 0.0

def to_iso8601_utc(dt: Optional[datetime]) -> Optional[str]:
    """Converts a datetime to strict ISO-8601 UTC format (e.g. 2026-11-22T18:00:00Z)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def is_within_hours(dt: Optional[datetime], hours: int = 24, ref_time: Optional[datetime] = None) -> bool:
    """
    Evaluates whether a timestamp falls strictly within the past `hours` window relative to `ref_time`.
    Rejects future timestamps beyond 10 minutes (clock drift margin) and stale timestamps.
    """
    if dt is None:
        return False
    if ref_time is None:
        ref_time = get_utc_now()

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    diff = ref_time - dt
    # Reject dates older than specified window
    if diff > timedelta(hours=hours):
        return False
    # Reject future dates beyond 15 min leeway
    if diff < timedelta(minutes=-15):
        return False
    return True
