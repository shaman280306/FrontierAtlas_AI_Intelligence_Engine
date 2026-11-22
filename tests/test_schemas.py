import pytest
from pydantic import ValidationError
from src.llm.schemas import (
    ExtractedStartup, ExtractedProduct, ExtractedNewsArticle, ExtractedJob, ExtractionBundle
)

def test_valid_extracted_startup():
    startup = ExtractedStartup(
        name="Mistral AI",
        website="https://mistral.ai",
        employee_count=150,
        industry_tags=["Foundation Models", "Open Source"]
    )
    assert startup.name == "Mistral AI"
    assert startup.employee_count == 150

def test_startup_allows_null_employee_count():
    startup = ExtractedStartup(
        name="Stealth AI Lab",
        website=None,
        employee_count=None
    )
    assert startup.employee_count is None

def test_pricing_model_allowed_values():
    for pricing in ["FREE", "FREEMIUM", "PAID", "ENTERPRISE", None]:
        prod = ExtractedProduct(
            product_name="Test Tool",
            startup_name="Test Org",
            pricing_model=pricing
        )
        assert prod.pricing_model == pricing

def test_invalid_pricing_model_rejected():
    with pytest.raises(ValidationError):
        ExtractedProduct(
            product_name="Test Tool",
            startup_name="Test Org",
            pricing_model="DISCOUNTED"  # Invalid enum value
        )

def test_job_schema_validation():
    job = ExtractedJob(
        company="Anthropic",
        role_title="Research Engineer - Interpretability",
        role_family="Research",
        is_remote=True,
        posted_date_str="2026-11-22T12:00:00Z"
    )
    assert job.company == "Anthropic"
    assert job.is_remote is True
    assert job.role_family == "Research"
