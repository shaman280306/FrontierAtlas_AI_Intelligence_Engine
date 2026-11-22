import re
from typing import List, Dict, Any, Optional
from src.llm.schemas import ExtractionBundle
from src.utils.logging import app_logger

class SemanticChunk:
    def __init__(self, text: str, index: int, heading: Optional[str] = None):
        self.text = text
        self.index = index
        self.heading = heading
        self.char_count = len(text)
        self.estimated_tokens = max(1, len(text) // 4)


class SemanticChunker:
    """
    Intelligent semantic-aware document chunker.
    Splits long documents at structural boundaries (headings, sections, paragraphs)
    rather than arbitrary character cuts, preventing payload 413 errors and context clipping.
    """
    def __init__(self, max_tokens_per_chunk: int = 2500, overlap_tokens: int = 150):
        self.max_chars = max_tokens_per_chunk * 4
        self.overlap_chars = overlap_tokens * 4

    def chunk_document(self, text: str, title: Optional[str] = None) -> List[SemanticChunk]:
        """
        Splits a text document into semantic chunks preserving heading context.
        """
        if not text or not text.strip():
            return []

        cleaned_text = text.strip()
        if len(cleaned_text) <= self.max_chars:
            return [SemanticChunk(text=cleaned_text, index=0, heading=title)]

        # Split on Markdown headings (#, ##, ###) or double newlines
        heading_split_pattern = r'(?m)(?=^(?:#{1,3}\s+|[A-Z0-9\s]{4,30}\n={3,}|[A-Z0-9\s]{4,30}\n-{3,}))'
        raw_sections = re.split(heading_split_pattern, cleaned_text)
        
        # If no heading splits, split by double newlines (paragraphs)
        if len(raw_sections) <= 1:
            raw_sections = cleaned_text.split("\n\n")

        chunks: List[SemanticChunk] = []
        current_chunk_text = ""
        current_heading = title
        chunk_idx = 0

        for sec in raw_sections:
            sec_clean = sec.strip()
            if not sec_clean:
                continue

            # Detect heading in section
            first_line = sec_clean.split("\n")[0].strip()
            if first_line.startswith("#"):
                current_heading = first_line.lstrip("#").strip()

            if len(current_chunk_text) + len(sec_clean) + 2 <= self.max_chars:
                current_chunk_text = f"{current_chunk_text}\n\n{sec_clean}".strip()
            else:
                if current_chunk_text:
                    prefix = f"Context: {current_heading}\n\n" if current_heading else ""
                    chunks.append(SemanticChunk(text=f"{prefix}{current_chunk_text}", index=chunk_idx, heading=current_heading))
                    chunk_idx += 1
                
                # If a single section exceeds max_chars, split by sentences
                if len(sec_clean) > self.max_chars:
                    sentences = re.split(r'(?<=[.!?])\s+', sec_clean)
                    current_chunk_text = ""
                    for s in sentences:
                        if len(current_chunk_text) + len(s) + 1 <= self.max_chars:
                            current_chunk_text = f"{current_chunk_text} {s}".strip()
                        else:
                            prefix = f"Context: {current_heading}\n\n" if current_heading else ""
                            chunks.append(SemanticChunk(text=f"{prefix}{current_chunk_text}", index=chunk_idx, heading=current_heading))
                            chunk_idx += 1
                            current_chunk_text = s
                else:
                    current_chunk_text = sec_clean

        if current_chunk_text:
            prefix = f"Context: {current_heading}\n\n" if current_heading else ""
            chunks.append(SemanticChunk(text=f"{prefix}{current_chunk_text}", index=chunk_idx, heading=current_heading))

        app_logger.info(f"Chunked document into {len(chunks)} semantic chunks (total chars: {len(cleaned_text)})")
        return chunks

    @staticmethod
    def reconcile_chunk_extractions(bundles: List[ExtractionBundle]) -> ExtractionBundle:
        """
        Merges extractions across all chunks of a document, deduplicating entities
        and reconciling conflicting information.
        """
        merged_startups = {}
        merged_products = {}
        merged_news = {}
        merged_jobs = {}

        for b in bundles:
            for s in b.startups:
                key = s.name.strip().lower()
                if key not in merged_startups:
                    merged_startups[key] = s
                else:
                    # Prefer non-null employee counts and websites
                    if s.employee_count is not None and merged_startups[key].employee_count is None:
                        merged_startups[key].employee_count = s.employee_count
                    if s.website and not merged_startups[key].website:
                        merged_startups[key].website = s.website

            for p in b.products:
                key = (p.startup_name.strip().lower(), p.product_name.strip().lower())
                if key not in merged_products:
                    merged_products[key] = p
                else:
                    if p.pricing_model and not merged_products[key].pricing_model:
                        merged_products[key].pricing_model = p.pricing_model

            for n in b.news_items:
                key = n.title.strip().lower()
                if key not in merged_news:
                    merged_news[key] = n

            for j in b.jobs:
                key = (j.company.strip().lower(), j.role_title.strip().lower())
                if key not in merged_jobs:
                    merged_jobs[key] = j

        return ExtractionBundle(
            startups=list(merged_startups.values()),
            products=list(merged_products.values()),
            news_items=list(merged_news.values()),
            jobs=list(merged_jobs.values())
        )
