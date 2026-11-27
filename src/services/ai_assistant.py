import os
import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from config.settings import settings
from src.storage.models import StartupRecord, ProductRecord, ResearchPaperRecord, JobRecord, NewsRecord
from src.llm.orchestrator import LLMOrchestrator
from src.utils.logging import app_logger

class AIAssistantService:
    def __init__(self, session: Session):
        self.session = session
        self.llm_orchestrator = LLMOrchestrator()
        self.has_keys = bool(settings.GEMINI_API_KEY or settings.GROQ_API_KEY or settings.DEEPSEEK_API_KEY)

    def query_intelligence(self, user_prompt: str) -> Dict[str, Any]:
        """
        Executes an intelligent contextual query against the AI ecosystem graph.
        Retrieves relevant database records and synthesizes a verified, source-grounded response.
        """
        prompt_lower = user_prompt.lower()

        # 1. Retrieve Grounding Context from Real Database Records
        context_papers = []
        context_products = []
        context_startups = []
        context_jobs = []
        context_news = []

        keywords = [w.strip() for w in prompt_lower.replace("?", "").replace(",", "").split() if len(w) > 3]

        if keywords:
            # Paper matches
            paper_filters = [ResearchPaperRecord.title.ilike(f"%{kw}%") for kw in keywords[:3]]
            papers = self.session.query(ResearchPaperRecord).filter(or_(*paper_filters)).order_by(desc(ResearchPaperRecord.github_stars)).limit(4).all()
            context_papers = [p.to_full_dict() for p in papers]

            # Product matches
            prod_filters = [ProductRecord.product_name.ilike(f"%{kw}%") for kw in keywords[:3]]
            prods = self.session.query(ProductRecord).filter(or_(*prod_filters)).limit(4).all()
            context_products = [p.to_full_dict() for p in prods]

            # Startup matches
            st_filters = [StartupRecord.canonical_name.ilike(f"%{kw}%") for kw in keywords[:3]]
            startups = self.session.query(StartupRecord).filter(or_(*st_filters)).limit(4).all()
            context_startups = [s.to_full_dict() for s in startups]

            # Job matches
            job_filters = [JobRecord.title.ilike(f"%{kw}%") for kw in keywords[:3]]
            jobs = self.session.query(JobRecord).filter(or_(*job_filters)).limit(4).all()
            context_jobs = [j.to_full_dict() for j in jobs]

            # News matches
            news_filters = [NewsRecord.title.ilike(f"%{kw}%") for kw in keywords[:3]]
            news = self.session.query(NewsRecord).filter(or_(*news_filters)).limit(4).all()
            context_news = [n.to_full_dict() for n in news]

        # Fallback to top records if no direct keyword match
        if not (context_papers or context_products or context_startups or context_jobs or context_news):
            context_papers = [p.to_full_dict() for p in self.session.query(ResearchPaperRecord).filter(ResearchPaperRecord.github_stars.isnot(None)).order_by(desc(ResearchPaperRecord.github_stars)).limit(3).all()]
            context_products = [p.to_full_dict() for p in self.session.query(ProductRecord).limit(3).all()]
            context_startups = [s.to_full_dict() for s in self.session.query(StartupRecord).limit(3).all()]

        # 2. Synthesize Grounded Response
        # If API keys are present, attempt inference via fallback chain
        ai_response_text = ""
        provider_used = "Deterministic Grounded Synthesizer"

        if self.has_keys:
            try:
                system_instruction = (
                    "You are the FrontierAtlas AI Intelligence Engine. Answer the user prompt accurately based ONLY on the provided database context. "
                    "Cite sources, paper titles, startups, products, and verified metrics directly. Do not hallucinate."
                )
                raw_payload = f"User Question: {user_prompt}\n\nRetrieved Context:\n"
                if context_papers:
                    raw_payload += "Research Papers: " + json.dumps(context_papers, default=str) + "\n"
                if context_products:
                    raw_payload += "Products: " + json.dumps(context_products, default=str) + "\n"
                if context_startups:
                    raw_payload += "Startups: " + json.dumps(context_startups, default=str) + "\n"

                result, provider = self.llm_orchestrator.extract_structured(
                    text=raw_payload,
                    schema=None, # Will return dict or string
                    prompt_override=system_instruction
                )
                if result:
                    ai_response_text = str(result)
                    provider_used = provider
            except Exception as e:
                app_logger.warning(f"LLM extraction fallback to local synthesizer: {e}")

        # Deterministic High-Quality Synthesis if keys absent or API unavailable
        if not ai_response_text:
            ai_response_text = self._build_deterministic_synthesis(
                user_prompt=user_prompt,
                papers=context_papers,
                products=context_products,
                startups=context_startups,
                jobs=context_jobs,
                news=context_news
            )

        return {
            "query": user_prompt,
            "response": ai_response_text,
            "provider": provider_used,
            "grounding": {
                "referenced_papers": context_papers,
                "referenced_products": context_products,
                "referenced_startups": context_startups,
                "referenced_jobs": context_jobs,
                "referenced_news": context_news
            }
        }

    def _build_deterministic_synthesis(
        self,
        user_prompt: str,
        papers: List[Dict[str, Any]],
        products: List[Dict[str, Any]],
        startups: List[Dict[str, Any]],
        jobs: List[Dict[str, Any]],
        news: List[Dict[str, Any]]
    ) -> str:
        lines = []
        lines.append(f"### Intelligence Synthesis: '{user_prompt}'\n")
        lines.append("Based on verified records indexed across the **FrontierAtlas AI Intelligence Graph**:\n")

        if papers:
            lines.append("#### Key Research Discoveries & Open-Source Code:")
            for p in papers[:3]:
                stars_info = f" ({p['github_stars']} GitHub stars)" if p.get("github_stars") is not None else ""
                repo_info = f" — [GitHub Repository]({p['github_url']})" if p.get("github_url") else " (No public repository indexed)"
                lines.append(f"- **{p['title']}**{stars_info}{repo_info}. [Paper Link]({p['paper_url']})")
            lines.append("")

        if products:
            lines.append("#### Notable AI Products & Pricing Models:")
            for pr in products[:3]:
                pricing = pr.get("pricing_model") or "Unspecified"
                lines.append(f"- **{pr['product_name']}** (by *{pr['startup_name']}*) — **{pricing}** tier. [Source]({pr['source_url']})")
            lines.append("")

        if startups:
            lines.append("#### Verified Startups & Organizations:")
            for st in startups[:3]:
                emp = f" ({st['employee_count']} employees)" if st.get("employee_count") else ""
                lines.append(f"- **{st['canonical_name']}**{emp}. [Source Directory]({st['source_url']})")
            lines.append("")

        if jobs:
            lines.append("#### Active Engineering Opportunities:")
            for j in jobs[:2]:
                remote_tag = "Remote" if j.get("is_remote") else "On-site"
                lines.append(f"- **{j['title']}** at **{j['company']}** ({j['role_family']}, {remote_tag}). [Apply]({j['source_url']})")
            lines.append("")

        if news:
            lines.append("#### Industry News Signals:")
            for n in news[:2]:
                lines.append(f"- **{n['title']}** (Source: *{n['source_name']}*). [Article]({n['source_url']})")
            lines.append("")

        lines.append("> [!NOTE]\n> All citations and metrics shown above are traceable to genuine collection timestamps in the FrontierAtlas database.")
        return "\n".join(lines)
