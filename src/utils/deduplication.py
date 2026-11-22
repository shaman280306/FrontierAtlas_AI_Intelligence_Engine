import hashlib
import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from typing import Optional

TRACKING_PARAMS = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'ref', 'ref_src', 'source', 'fbclid', 'gclid', 'mc_cid', 'mc_eid'
}

def normalize_url(url: Optional[str]) -> str:
    """
    Normalizes a URL by:
      - Lowercasing scheme and host
      - Stripping standard marketing/tracking query parameters (utm_*, ref, etc.)
      - Stripping trailing slash and whitespace
      - Sorting remaining query parameters deterministically
    """
    if not url:
        return ""
    
    clean_url = url.strip()
    try:
        parsed = urlparse(clean_url)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip('/')
        
        # Filter and sort query params
        query_pairs = parse_qsl(parsed.query, keep_blank_values=False)
        filtered_query = [(k, v) for k, v in query_pairs if k.lower() not in TRACKING_PARAMS]
        filtered_query.sort(key=lambda x: x[0])
        
        new_query = urlencode(filtered_query)
        # Discard fragments (#...) for canonical deduplication
        canonical = urlunparse((scheme, netloc, path, '', new_query, ''))
        return canonical
    except Exception:
        return clean_url

def compute_content_fingerprint(*args) -> str:
    """
    Computes a deterministic SHA-256 hash across entity fields to ensure idempotency.
    """
    combined = "|".join(str(a or '').strip().lower() for a in args)
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()
