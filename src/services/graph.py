import re
from typing import Dict, Any, List, Set, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.storage.models import StartupRecord, ProductRecord, ResearchPaperRecord, JobRecord, NewsRecord, EntityMappingLogRecord

class EntityGraphService:
    def __init__(self, session: Session):
        self.session = session

    def get_entity_graph(self, entity_name: str, max_depth: int = 1) -> Dict[str, Any]:
        """
        Constructs an interactive node-and-edge graph for an entity,
        linking Startups, Products, Research Papers, Jobs, and News signals.
        """
        clean_name = entity_name.strip()
        nodes: List[Dict[str, Any]] = []
        edges: List[Dict[str, Any]] = []
        seen_nodes: Set[str] = set()
        seen_edges: Set[str] = set()

        def add_node(node_id: str, label: str, node_type: str, metadata: Optional[Dict[str, Any]] = None):
            if node_id not in seen_nodes:
                seen_nodes.add(node_id)
                nodes.append({
                    "id": node_id,
                    "label": label,
                    "type": node_type,
                    "metadata": metadata or {}
                })

        def add_edge(source: str, target: str, relationship: str):
            edge_id = f"{source}->{target}:{relationship}"
            if edge_id not in seen_edges and source in seen_nodes and target in seen_nodes:
                seen_edges.add(edge_id)
                edges.append({
                    "id": edge_id,
                    "source": source,
                    "target": target,
                    "relationship": relationship
                })

        # 1. Root Entity Node
        root_id = f"entity:{clean_name.lower().replace(' ', '_')}"
        add_node(root_id, clean_name, "entity", {"is_root": True})

        # 2. Associated Startups
        startups = self.session.query(StartupRecord).filter(
            or_(
                StartupRecord.canonical_name.ilike(clean_name),
                StartupRecord.raw_name.ilike(f"%{clean_name}%")
            )
        ).limit(5).all()

        for s in startups:
            s_id = f"startup:{s.id}"
            add_node(s_id, s.canonical_name, "startup", {
                "source": s.source_name,
                "employees": s.employee_count,
                "url": s.source_url
            })
            add_edge(root_id, s_id, "RESOLVES_TO")

        # 3. Associated Products
        products = self.session.query(ProductRecord).filter(
            ProductRecord.startup_name.ilike(f"%{clean_name}%")
        ).limit(8).all()

        for p in products:
            p_id = f"product:{p.id}"
            add_node(p_id, p.product_name, "product", {
                "pricing": p.pricing_model,
                "url": p.source_url,
                "description": p.description[:100] if p.description else ""
            })
            add_edge(root_id, p_id, "OFFERS_PRODUCT")

        # 4. Associated Research Papers
        papers = self.session.query(ResearchPaperRecord).filter(
            or_(
                ResearchPaperRecord.title.ilike(f"%{clean_name}%"),
                ResearchPaperRecord.authors_json.ilike(f"%{clean_name}%")
            )
        ).limit(6).all()

        for r in papers:
            r_id = f"paper:{r.id}"
            add_node(r_id, r.title[:45] + "...", "paper", {
                "stars": r.github_stars,
                "has_repo": bool(r.github_url),
                "url": r.paper_url
            })
            add_edge(root_id, r_id, "AUTHORED_RESEARCH")

        # 5. Associated Jobs
        jobs = self.session.query(JobRecord).filter(
            JobRecord.company.ilike(f"%{clean_name}%")
        ).limit(6).all()

        for j in jobs:
            j_id = f"job:{j.id}"
            add_node(j_id, f"{j.title} ({j.role_family})", "job", {
                "is_remote": j.is_remote,
                "company": j.company,
                "url": j.source_url
            })
            add_edge(root_id, j_id, "HIRING_OPPORTUNITY")

        # 6. Associated News
        news = self.session.query(NewsRecord).filter(
            or_(
                NewsRecord.primary_entity.ilike(f"%{clean_name}%"),
                NewsRecord.title.ilike(f"%{clean_name}%")
            )
        ).limit(5).all()

        for n in news:
            n_id = f"news:{n.id}"
            add_node(n_id, n.title[:45] + "...", "news", {
                "source": n.source_name,
                "published_at": n.published_at,
                "url": n.source_url
            })
            add_edge(root_id, n_id, "MENTIONED_IN")

        return {
            "entity": clean_name,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges
        }

    def list_top_connected_entities(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns the most active canonical entities with connected signal counts."""
        seed_names = [
            "OpenAI", "Anthropic", "Mistral AI", "Google", "DeepMind", "Meta", "Microsoft",
            "Cohere", "Stability AI", "Midjourney", "Runway", "ElevenLabs", "Scale AI",
            "Hugging Face", "Perplexity AI", "Pinecone", "Weaviate", "LangChain", "Qdrant",
            "Groq", "Together AI", "Anyscale", "Databricks", "Snowflake", "Nvidia"
        ]

        results = []
        for name in seed_names[:limit]:
            prod_count = self.session.query(ProductRecord).filter(
                ProductRecord.startup_name.ilike(f"%{name}%")
            ).count()

            paper_count = self.session.query(ResearchPaperRecord).filter(
                or_(
                    ResearchPaperRecord.title.ilike(f"%{name}%"),
                    ResearchPaperRecord.authors_json.ilike(f"%{name}%")
                )
            ).count()

            job_count = self.session.query(JobRecord).filter(
                JobRecord.company.ilike(f"%{name}%")
            ).count()

            news_count = self.session.query(NewsRecord).filter(
                or_(
                    NewsRecord.primary_entity.ilike(f"%{name}%"),
                    NewsRecord.title.ilike(f"%{name}%")
                )
            ).count()

            total_connections = prod_count + paper_count + job_count + news_count
            results.append({
                "entity": name,
                "products": prod_count,
                "papers": paper_count,
                "jobs": job_count,
                "news": news_count,
                "total_connections": total_connections
            })

        results.sort(key=lambda x: x["total_connections"], reverse=True)
        return results
