import difflib
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone
from src.entity_resolution.seed_entities import SEED_AI_STARTUPS
from src.entity_resolution.normalization import normalize_entity_name, unicode_normalize
from src.utils.dates import get_utc_now, to_iso8601_utc
from src.utils.logging import app_logger

class ResolutionResult:
    def __init__(
        self,
        raw_name: str,
        canonical_name: str,
        matching_method: str,
        confidence_score: float,
        source_url: str,
        resolution_timestamp: Optional[str] = None,
        is_ambiguous: bool = False
    ):
        self.raw_name = raw_name
        self.canonical_name = canonical_name
        self.matching_method = matching_method
        self.confidence_score = round(confidence_score, 4)
        self.source_url = source_url
        self.resolution_timestamp = resolution_timestamp or to_iso8601_utc(get_utc_now())
        self.is_ambiguous = is_ambiguous

    def to_log_dict(self) -> Dict[str, Any]:
        return {
            "raw_name": self.raw_name,
            "canonical_name": self.canonical_name,
            "matching_method": self.matching_method,
            "confidence_score": self.confidence_score,
            "source_url": self.source_url,
            "resolution_timestamp": self.resolution_timestamp
        }


class EntityResolver:
    """
    Deterministic and Fuzzy Entity Resolution Engine.
    Maps messy or variant entity strings to their canonical forms.
    Enforces deterministic resolution and avoids false mergers of unrelated entities.
    """
    def __init__(self, seed_data: Optional[Dict[str, Dict[str, Any]]] = None):
        self.seed = seed_data or SEED_AI_STARTUPS
        self._build_lookup_indices()

    def _build_lookup_indices(self) -> None:
        self.exact_canonical_map: Dict[str, str] = {}
        self.exact_alias_map: Dict[str, str] = {}
        self.normalized_map: Dict[str, str] = {}

        for canonical, info in self.seed.items():
            # Exact lower
            self.exact_canonical_map[canonical.lower()] = canonical
            norm_canonical = normalize_entity_name(canonical)
            if norm_canonical:
                self.normalized_map[norm_canonical] = canonical

            for alias in info.get("aliases", []):
                self.exact_alias_map[alias.lower()] = canonical
                norm_alias = normalize_entity_name(alias)
                if norm_alias:
                    self.normalized_map[norm_alias] = canonical

    @staticmethod
    def _token_sort_similarity(s1: str, s2: str) -> float:
        """Calculates token sort similarity ratio between two strings."""
        if not s1 or not s2:
            return 0.0
        t1 = " ".join(sorted(s1.split()))
        t2 = " ".join(sorted(s2.split()))
        return difflib.SequenceMatcher(None, t1, t2).ratio()

    def resolve(self, raw_name: Optional[str], source_url: str = "") -> ResolutionResult:
        """
        Resolves an input raw entity name to a canonical entity name.
        Guarantees that 'OpenAI', 'OpenAI, Inc.', and 'Open AI' resolve to 'OpenAI'.
        """
        if not raw_name or not str(raw_name).strip():
            return ResolutionResult(
                raw_name=raw_name or "Unknown",
                canonical_name="Unknown",
                matching_method="EMPTY_FALLBACK",
                confidence_score=0.0,
                source_url=source_url
            )

        cleaned_raw = str(raw_name).strip()
        lower_raw = cleaned_raw.lower()

        # 1. Exact match against canonical name
        if lower_raw in self.exact_canonical_map:
            return ResolutionResult(
                raw_name=cleaned_raw,
                canonical_name=self.exact_canonical_map[lower_raw],
                matching_method="EXACT_CANONICAL",
                confidence_score=1.0,
                source_url=source_url
            )

        # 2. Exact match against known aliases
        if lower_raw in self.exact_alias_map:
            return ResolutionResult(
                raw_name=cleaned_raw,
                canonical_name=self.exact_alias_map[lower_raw],
                matching_method="SEED_ALIAS",
                confidence_score=1.0,
                source_url=source_url
            )

        # 3. Normalized string match (legal suffixes and punctuation removed)
        norm_raw = normalize_entity_name(cleaned_raw)
        if norm_raw in self.normalized_map:
            return ResolutionResult(
                raw_name=cleaned_raw,
                canonical_name=self.normalized_map[norm_raw],
                matching_method="NORMALIZED_MATCH",
                confidence_score=0.95,
                source_url=source_url
            )

        # 4. Fuzzy token-sort similarity against normalized seed entities
        best_canonical: Optional[str] = None
        best_score = 0.0

        for norm_seed, canonical in self.normalized_map.items():
            score = self._token_sort_similarity(norm_raw, norm_seed)
            if score > best_score:
                best_score = score
                best_canonical = canonical

        # Strict thresholding
        if best_score >= 0.88 and best_canonical:
            return ResolutionResult(
                raw_name=cleaned_raw,
                canonical_name=best_canonical,
                matching_method="FUZZY_TOKEN_SORT",
                confidence_score=best_score,
                source_url=source_url
            )

        if best_score >= 0.70 and best_canonical:
            # Ambiguous match: Flag for manual review, preserve original name to prevent false merge
            app_logger.warning(
                f"Ambiguous entity match flagged: '{cleaned_raw}' -> potential '{best_canonical}' (score: {best_score:.2f})"
            )
            return ResolutionResult(
                raw_name=cleaned_raw,
                canonical_name=cleaned_raw,  # Retain original to prevent false merge
                matching_method="MANUAL_REVIEW_FLAGGED",
                confidence_score=best_score,
                source_url=source_url,
                is_ambiguous=True
            )

        # 5. Distinct standalone entity (not in seed database)
        # Clean up legal suffix if any and title-case
        formatted_name = cleaned_raw.strip()
        # If it has obvious legal suffixes, strip them for clean display
        stripped = normalize_entity_name(cleaned_raw, strip_ai_suffix=False).title()
        canonical_form = stripped if len(stripped) > 2 else formatted_name

        return ResolutionResult(
            raw_name=cleaned_raw,
            canonical_name=canonical_form,
            matching_method="STANDALONE_NORMALIZED",
            confidence_score=1.0,
            source_url=source_url
        )
