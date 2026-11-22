import pytest
from src.entity_resolution.resolver import EntityResolver
from src.entity_resolution.normalization import normalize_entity_name

@pytest.fixture
def resolver():
    return EntityResolver()

def test_canonical_openai_resolution(resolver):
    # Test strict assignment requirement:
    # "OpenAI", "OpenAI, Inc.", and "Open AI" must resolve to "OpenAI"
    test_cases = [
        "OpenAI",
        "OpenAI, Inc.",
        "Open AI",
        "openai",
        "OpenAI Inc",
        "OpenAI LLC"
    ]
    for variant in test_cases:
        res = resolver.resolve(variant)
        assert res.canonical_name == "OpenAI", f"Failed for variant: {variant} -> {res.canonical_name}"
        assert res.confidence_score >= 0.95

def test_canonical_anthropic_resolution(resolver):
    variants = ["Anthropic", "Anthropic, PBC", "Anthropic PBC", "Anthropic AI"]
    for variant in variants:
        res = resolver.resolve(variant)
        assert res.canonical_name == "Anthropic"

def test_canonical_mistral_resolution(resolver):
    variants = ["Mistral AI", "Mistral", "MistralAI", "Mistral AI SAS"]
    for variant in variants:
        res = resolver.resolve(variant)
        assert res.canonical_name == "Mistral AI"

def test_legal_suffix_stripping():
    assert normalize_entity_name("DeepSeek AI, Inc.") == "deepseek"
    assert normalize_entity_name("Pinecone Systems, LLC") == "pinecone"
    assert normalize_entity_name("Synthesia, Ltd.") == "synthesia"
    assert normalize_entity_name("Weaviate B.V.") == "weaviate"

def test_fuzzy_token_sort_matching(resolver):
    res = resolver.resolve("Weights & Biases, Inc.")
    assert res.canonical_name == "Weights & Biases"
    assert res.confidence_score >= 0.90

def test_unrelated_entities_not_falsely_merged(resolver):
    # Ensure unrelated entities with similar generic tokens do not get merged falsely
    res1 = resolver.resolve("Acme Robotics")
    res2 = resolver.resolve("Acme Diagnostics")
    assert res1.canonical_name != res2.canonical_name
