import re
import unicodedata

# Common legal and corporate suffixes
LEGAL_SUFFIX_PATTERN = re.compile(
    r'\b(?:inc(?:orporated)?|llc|l\s*l\s*c|ltd|limited|corp(?:oration)?|co(?:mpany)?|gmbh|pbc|p\s*b\s*c|sas|bv|b\s*v|pte\s+ltd|technologies|technology|labs?|systems?)\b',
    re.IGNORECASE
)

AI_SUFFIX_PATTERN = re.compile(
    r'(?:\s+ai|\.ai|\-ai)$',
    re.IGNORECASE
)

def unicode_normalize(text: str) -> str:
    """Normalizes string using Unicode NFKD and ascii transliteration."""
    if not text:
        return ""
    normalized = unicodedata.normalize('NFKD', text)
    # Strip combining marks (accents)
    return "".join(c for c in normalized if not unicodedata.combining(c))

def normalize_entity_name(text: str, strip_ai_suffix: bool = True) -> str:
    """
    Standardizes entity name for deterministic matching:
    1. Unicode NFKD transliteration
    2. Lowercasing
    3. Punctuation removal (except alphanumeric and spaces)
    4. Legal suffix stripping (Inc, LLC, Corp, etc.)
    5. Collapsing multiple spaces
    """
    if not text:
        return ""
    
    # Unicode NFKD
    cleaned = unicode_normalize(text).lower().strip()
    
    # Strip punctuation first to expose trailing tokens cleanly
    cleaned = re.sub(r'[^\w\s]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # Remove common corporate legal suffixes
    cleaned = LEGAL_SUFFIX_PATTERN.sub('', cleaned).strip()
    
    # Conditionally remove trailing ai suffix
    if strip_ai_suffix:
        cleaned = re.sub(r'\b(?:ai)\b\s*$', '', cleaned).strip()
        
    # Collapse multiple whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned
