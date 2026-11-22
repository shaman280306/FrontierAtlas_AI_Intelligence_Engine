import pytest
from src.llm.chunking import SemanticChunker
from src.llm.schemas import (
    ExtractionBundle, ExtractedStartup, ExtractedProduct, ExtractedNewsArticle, ExtractedJob
)

def test_semantic_chunker_short_text():
    chunker = SemanticChunker(max_tokens_per_chunk=100)
    text = "Short text describing an AI startup called NovaAI."
    chunks = chunker.chunk_document(text, title="Doc 1")
    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].heading == "Doc 1"

def test_semantic_chunker_preserves_headings():
    chunker = SemanticChunker(max_tokens_per_chunk=30)
    long_doc = (
        "# Section 1: Overview\n\n"
        "This is paragraph one with enough text to approach the limit of the chunker token threshold.\n\n"
        "# Section 2: Products\n\n"
        "Here we discuss generative artificial intelligence models and products created by top labs."
    )
    chunks = chunker.chunk_document(long_doc)
    assert len(chunks) >= 2
    # Check that context heading is attached
    assert any("Overview" in c.text for c in chunks)
    assert any("Products" in c.text for c in chunks)

def test_reconcile_chunk_extractions():
    b1 = ExtractionBundle(
        startups=[
            ExtractedStartup(name="OpenAI", website=None, employee_count=None)
        ],
        products=[
            ExtractedProduct(product_name="ChatGPT", startup_name="OpenAI", pricing_model=None)
        ]
    )
    b2 = ExtractionBundle(
        startups=[
            # Chunk 2 finds more details for OpenAI
            ExtractedStartup(name="OpenAI", website="https://openai.com", employee_count=700)
        ],
        products=[
            # Chunk 2 finds pricing evidence
            ExtractedProduct(product_name="ChatGPT", startup_name="OpenAI", pricing_model="FREEMIUM")
        ]
    )
    merged = SemanticChunker.reconcile_chunk_extractions([b1, b2])
    assert len(merged.startups) == 1
    assert merged.startups[0].name == "OpenAI"
    assert merged.startups[0].website == "https://openai.com"
    assert merged.startups[0].employee_count == 700
    assert len(merged.products) == 1
    assert merged.products[0].pricing_model == "FREEMIUM"
