import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_analytics_overview_endpoint():
    res = client.get("/api/v1/analytics/overview")
    assert res.status_code == 200
    data = res.json()
    assert data["counts"]["startups"] >= 1000
    assert data["counts"]["products"] >= 1000
    assert data["counts"]["research_papers"] >= 1000
    assert data["counts"]["jobs"] >= 300
    assert data["counts"]["news"] >= 70
    assert "distributions" in data
    assert "pricing" in data["distributions"]

def test_startups_pagination_and_search():
    res = client.get("/api/v1/startups?page=1&page_size=10&search=OpenAI")
    assert res.status_code == 200
    data = res.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) >= 1
    assert any("openai" in s["canonical_name"].lower() for s in data["items"])

def test_products_pricing_filter():
    res = client.get("/api/v1/products?page=1&page_size=10&pricing_model=FREEMIUM")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) > 0
    assert all(p["pricing_model"] == "FREEMIUM" for p in data["items"])

def test_products_compare():
    res = client.get("/api/v1/products/compare?ids=1,2,3")
    assert res.status_code == 200
    data = res.json()
    assert "products" in data
    assert len(data["products"]) == 3

def test_research_papers_github_filter():
    res = client.get("/api/v1/research-papers?has_github=true&page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) > 0
    assert all(p["github_url"] is not None for p in data["items"])

def test_jobs_remote_filter():
    res = client.get("/api/v1/jobs?is_remote=true&page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) > 0
    assert all(j["is_remote"] is True for j in data["items"])

def test_news_sources_and_list():
    res = client.get("/api/v1/news?page=1&page_size=5")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 5

def test_entity_graph():
    res = client.get("/api/v1/entities/OpenAI/graph")
    assert res.status_code == 200
    data = res.json()
    assert "nodes" in data
    assert "edges" in data
    assert data["node_count"] > 1

def test_frontier_trends():
    res = client.get("/api/v1/trends")
    assert res.status_code == 200
    data = res.json()
    assert "research_signals" in data
    assert len(data["research_signals"]) > 0
    assert "open_source_velocity" in data

def test_quality_metrics():
    res = client.get("/api/v1/quality/metrics")
    assert res.status_code == 200
    data = res.json()
    assert data["overall_quality_score"] >= 99.0
    assert len(data["datasets"]) == 6

def test_global_search():
    res = client.get("/api/v1/search?q=vision")
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] > 0
    assert "results" in data

def test_ai_query_assistant():
    res = client.post("/api/v1/ai/query", json={"prompt": "Which research papers have code?"})
    assert res.status_code == 200
    data = res.json()
    assert "response" in data
    assert "grounding" in data

def test_reports_list():
    res = client.get("/api/v1/reports/list")
    assert res.status_code == 200
    data = res.json()
    assert len(data["reports"]) >= 7
