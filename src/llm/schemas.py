from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class ExtractedStartup(BaseModel):
    name: str = Field(description="Canonical or official name of the startup")
    website: Optional[str] = Field(default=None, description="Primary domain or website")
    employee_count: Optional[int] = Field(default=None, description="Verified number of employees if explicitly stated, else null")
    industry_tags: List[str] = Field(default_factory=list, description="Industry categories or tags")
    summary: Optional[str] = Field(default=None, description="One-sentence description of the company")

class ExtractedProduct(BaseModel):
    product_name: str = Field(description="Name of the product or software tool")
    startup_name: str = Field(description="Parent company or creator organization")
    pricing_model: Optional[Literal["FREE", "FREEMIUM", "PAID", "ENTERPRISE"]] = Field(
        default=None, description="Pricing tier: FREE, FREEMIUM, PAID, ENTERPRISE or null"
    )
    url: Optional[str] = Field(default=None, description="Product webpage or repo URL")
    description: Optional[str] = Field(default=None, description="Brief summary of product capabilities")

class ExtractedNewsArticle(BaseModel):
    title: str = Field(description="Headline or title of the news article")
    published_date_str: Optional[str] = Field(default=None, description="Raw date string as mentioned in text")
    primary_entity: Optional[str] = Field(default=None, description="Primary AI company or product mentioned")
    key_signals: List[str] = Field(default_factory=list, description="Key facts, funding, product launches")
    summary: str = Field(description="Concise summary of the news development")

class ExtractedJob(BaseModel):
    company: str = Field(description="Hiring company name")
    role_title: str = Field(description="Job title")
    role_family: str = Field(default="Engineering", description="Engineering, Research, Product, etc.")
    is_remote: bool = Field(default=False, description="Whether position is remote eligible")
    posted_date_str: Optional[str] = Field(default=None, description="Raw publication or relative date")

class ExtractionBundle(BaseModel):
    startups: List[ExtractedStartup] = Field(default_factory=list)
    products: List[ExtractedProduct] = Field(default_factory=list)
    news_items: List[ExtractedNewsArticle] = Field(default_factory=list)
    jobs: List[ExtractedJob] = Field(default_factory=list)
