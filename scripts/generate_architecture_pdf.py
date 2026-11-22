import os
import sys
from pathlib import Path

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group, Polygon
from reportlab.pdfgen import canvas
from src.utils.logging import app_logger

PDF_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "architecture.pdf"

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render exact total page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages 2 and 3)
        if self._pageNumber > 1:
            self.drawString(38, 762, "FrontierAtlas AI Intelligence Ingestion Engine — Production Architecture")
            self.drawRightString(574, 762, "GraphOne / FrontierAtlas")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(38, 756, 574, 756)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(38, 36, 574, 36)
        self.drawString(38, 24, "CONFIDENTIAL & PROPRIETARY — GRAPHONE / FRONTIERATLAS")
        self.drawRightString(574, 24, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


def create_architecture_diagram():
    """Generates an elegant vector diagram of the ingestion pipeline."""
    d = Drawing(536, 85)

    # Background canvas
    d.add(Rect(0, 0, 536, 85, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#E2E8F0"), strokeWidth=1, rx=4, ry=4))

    def draw_box(x, y, w, h, title, sub1, sub2, bg_color, border_color):
        g = Group()
        g.add(Rect(x, y, w, h, fillColor=colors.HexColor(bg_color), strokeColor=colors.HexColor(border_color), strokeWidth=1, rx=3, ry=3))
        g.add(String(x + w/2, y + h - 14, title, fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=colors.HexColor("#0F172A")))
        g.add(String(x + w/2, y + h - 28, sub1, fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=colors.HexColor("#334155")))
        g.add(String(x + w/2, y + h - 39, sub2, fontName="Helvetica", fontSize=6.5, textAnchor="middle", fillColor=colors.HexColor("#475569")))
        return g

    def draw_arrow(x1, y1, x2, y2):
        g = Group()
        g.add(Line(x1, y1, x2, y2, strokeColor=colors.HexColor("#2563EB"), strokeWidth=1.5))
        g.add(Polygon([x2, y2, x2 - 4, y2 + 3, x2 - 4, y2 - 3], fillColor=colors.HexColor("#2563EB"), strokeColor=colors.HexColor("#2563EB")))
        return g

    # 4 Architecture Columns
    d.add(draw_box(8, 14, 110, 58, "1. INGESTION SOURCES", "arXiv, Hugging Face, GitHub", "5x AI Job Boards, 5x News", "#EFF6FF", "#93C5FD"))
    d.add(draw_arrow(118, 43, 140, 43))

    d.add(draw_box(142, 14, 114, 58, "2. ASYNC CRAWLER CORE", "Rate Limiter, Anti-Bot Detect", "Canonical URLs, SHA-256 FP", "#F0FDF4", "#86EFAC"))
    d.add(draw_arrow(256, 43, 278, 43))

    d.add(draw_box(280, 14, 118, 58, "3. LLM & RESOLUTION", "Gemini -> Groq -> DeepSeek", "Deterministic Entity Resolver", "#FAF5FF", "#D8B4FE"))
    d.add(draw_arrow(398, 43, 420, 43))

    d.add(draw_box(422, 14, 106, 58, "4. STORAGE & EXPORT", "PostgreSQL Core, pgvector", "Neo4j Graph, 6-Tab Export", "#FFFBEB", "#FDE68A"))

    return d


def build_pdf():
    PDF_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(PDF_OUTPUT_PATH),
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=40,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569')
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=6,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.2,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=9,
        firstLineIndent=-5,
        spaceAfter=2
    )
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.white
    )
    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.2,
        leading=8.2,
        textColor=colors.HexColor('#0F172A')
    )
    td_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=td_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("FrontierAtlas AI Data Intelligence Engine", title_style))
    story.append(Paragraph("<b>Staff Architecture Specification & Production Scaling Blueprint</b> | GraphOne / FrontierAtlas Intelligence Graph", subtitle_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=5))

    # Architecture Diagram
    story.append(create_architecture_diagram())
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Executive Summary & Assessment Scope", h1_style))
    story.append(Paragraph(
        "GraphOne / FrontierAtlas is engineering the premier global Intelligence Graph for the artificial intelligence and venture ecosystem. "
        "Our infrastructure facilitates the continuous ingestion, normalization, and enrichment of multi-dimensional datasets encompassing startups, "
        "products, research papers, AI jobs, and real-time news signals from thousands of sources worldwide. "
        "Built on a production-grade Python 3.11 asynchronous architecture, this platform addresses the core technical frontiers: "
        "scaling bulk ingestion to lakhs of records without bottlenecks, bulletproof LLM fallback orchestration handling HTTP 429 and 413 exceptions, "
        "guaranteed 24-hour signal freshness, dynamic GitHub star metrics traceability, ethical anti-bot navigation, and deterministic entity resolution.",
        body_style
    ))

    story.append(Paragraph("2. Scale Strategy: Path to 500,000+ Records Without Code Changes", h1_style))
    story.append(Paragraph(
        "Scaling ingestion to lakhs (500,000+) of entities demands decoupled, event-driven infrastructure rather than monolithic crawlers:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Distributed Queue & Worker Topology:</b> Ingestion targets are partitioned into atomic work payloads published to Redis Streams or RabbitMQ queues. "
        "Stateless worker pods (Celery / Temporal.io) consume slices concurrently. Horizontal Pod Autoscalers (HPA) scale workers dynamically based on queue lag.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Bounded Concurrency & Per-Domain Semaphores:</b> Every target domain is throttled via token-bucket rate limiters and domain-specific <code>asyncio.Semaphore</code> "
        "guards to respect remote server capacities and prevent IP bans.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Pagination, Partitioning & Crawl Checkpointing:</b> Crawlers use cursor-based pagination and persistent state checkpoints in Redis/PostgreSQL. "
        "If a worker process restarts mid-crawl, ingestion resumes from the last committed cursor without duplicate re-fetching or data loss.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Database Partitioning & Bulk Writes:</b> Relational storage utilizes partitioned PostgreSQL tables (partitioned by <code>record_type</code> and <code>collected_at</code> monthly ranges). "
        "Writes are staged in memory and flushed via atomic <code>COPY</code> or bulk upserts (<code>ON CONFLICT (fingerprint) DO UPDATE</code>) in micro-batches of 500 records.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Dynamic Backpressure Management:</b> Storage buffer monitors emit backpressure signals to worker queues when DB write latencies spike above 100ms, "
        "automatically dampening crawler concurrency before memory thresholds are breached.",
        bullet_style
    ))

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("3. Resilient LLM Orchestration: Managing HTTP 413 & 429 Errors", h1_style))
    story.append(Paragraph(
        "LLM-based entity extraction operates under severe real-world constraints: vendor rate limits (HTTP 429) and context window overflows (HTTP 413). "
        "The FrontierAtlas extraction module employs a robust, multi-layered defense:",
        body_style
    ))

    def w_th(txt): return Paragraph(txt, th_style)
    def w_td(txt, bold=False): return Paragraph(txt, td_bold_style if bold else td_style)

    llm_table_data = [
        [w_th("Tier"), w_th("Provider"), w_th("Model Identifier"), w_th("Role in Ingestion Pipeline"), w_th("Fallback Trigger")],
        [w_td("Tier 1 (Primary)", True), w_td("Gemini Flash"), w_td("gemini-2.0-flash"), w_td("High-throughput extraction, 1M token context, structured JSON schema output"), w_td("HTTP 429 quota, auth error, outage")],
        [w_td("Tier 2 (Secondary)", True), w_td("Groq Llama 3"), w_td("llama-3.3-70b-versatile"), w_td("Ultra-low-latency LPU inference, strict schema adherence for high throughput"), w_td("HTTP 429, API rate-limit, 5xx error")],
        [w_td("Tier 3 (Tertiary)", True), w_td("DeepSeek"), w_td("deepseek-chat"), w_td("Complex entity reasoning, deep contextual extraction, and disambiguation"), w_td("Provider failure / exhaustion")],
        [w_td("Dead-Letter", True), w_td("Local Storage"), w_td("Raw JSON Dead-Letter"), w_td("Guarantees zero data loss: preserves raw text marked requires_reprocessing for offline retry"), w_td("All 3 tiers exhausted / unconfigured")]
    ]
    t_llm = Table(llm_table_data, colWidths=[65, 75, 105, 175, 116])
    t_llm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_llm)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "• <b>Semantic-Aware Chunking (413 Payload Too Large Mitigation):</b> When documents exceed context thresholds, the engine splits content along "
        "Markdown headings (<code>#</code>, <code>##</code>), section breaks, or double newlines rather than arbitrary destructive character slicing. "
        "Parent section headings are prepended as context to every chunk. Chunk extractions are independently parsed and reconciled using an entity-merging reducer.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Exponential Backoff with Full Jitter (429 Rate Limit Mitigation):</b> On encountering HTTP 429, workers extract the <code>Retry-After</code> header. "
        "If absent, delays scale exponentially: <i>t_wait = min(t_max, t_base * 2^(attempt-1)) + U(0, Jitter)</i>. This desynchronizes thundering herds.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Dead-Letter Preservation:</b> If all 3 tiers fail, raw documents are committed with <code>requires_reprocessing=True</code> and audit logs. "
        "Missing fields are preserved as explicit nulls; synthetic data is never hallucinated.",
        bullet_style
    ))

    story.append(Paragraph("4. Signal Freshness & Distributed Deduplication", h1_style))
    story.append(Paragraph(
        "Real-time venture intelligence demands strict freshness guarantees. News and jobs must satisfy our strict 24-hour freshness policy:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Four-Way Timestamp Distinction:</b> The system rigorously isolates: (1) <code>published_at</code> (original creator publication time), "
        "(2) <code>first_discovered_at</code> (initial crawler detection), (3) <code>last_updated_at</code> (source modification time), and (4) <code>collected_at</code> (ingestion pipeline run).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Strict 24-Hour Freshness Policy:</b> Timestamps are parsed from ISO-8601, RFC-2822, Unix epochs, and relative strings ('3 hours ago') into UTC. "
        "Records with parsed dates older than 24 hours relative to UTC now are strictly rejected. Low-confidence fallback heuristics are flagged in audit logs.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Distributed Deduplication & Fingerprinting:</b> URLs undergo canonical normalization (stripping tracking query parameters like <code>utm_*</code>, <code>ref</code>, <code>fbclid</code>). "
        "Content fingerprints are generated using SHA-256 over canonical names, URLs, and core fields. Redis distributed bloom filters and unique database indices guarantee zero duplicate ingestions.",
        bullet_style
    ))

    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("5. Storage Strategy & Polyglot Persistence Architecture", h1_style))
    story.append(Paragraph(
        "FrontierAtlas adopts a polyglot persistence architecture engineered for relational integrity, semantic vector search, and graph relationship exploration:",
        body_style
    ))

    storage_table_data = [
        [w_th("Layer"), w_th("Technology"), w_th("Primary Purpose"), w_th("Schema / Indexing Design"), w_th("Retention & Justification")],
        [w_td("Relational Core", True), w_td("PostgreSQL 16\n(SQLite Dev)"), w_td("System of record, ACID transactions, canonical entities, audits"), w_td("B-Tree on canonical names, SHA-256 unique constraints, composite indices on (record_type, collected_at)"), w_td("Permanent cold retention. High write throughput with MVCC.")],
        [w_td("Vector Layer", True), w_td("pgvector / Qdrant"), w_td("Semantic search, deduplication across messy text, similarity matching"), w_td("HNSW (Hierarchical Navigable Small World) index over 1536-dim embeddings with cosine distance"), w_td("Cached embedding indices. Enables semantic entity matching and topic clustering.")],
        [w_td("Graph Layer", True), w_td("Neo4j / GraphOne"), w_td("Ecosystem graph traversal (Startup -> Product -> Paper -> Founder)"), w_td("Labeled property graph with Cypher indexing on Entity UUIDs and relationship edges"), w_td("Dynamic graph representation of venture relationships and talent flows.")]
    ]
    t_storage = Table(storage_table_data, colWidths=[65, 75, 110, 165, 121])
    t_storage.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_storage)
    story.append(Spacer(1, 4))

    story.append(Paragraph("6. Deterministic Entity Resolution Architecture", h1_style))
    story.append(Paragraph(
        "Messy real-world strings (e.g., 'OpenAI', 'OpenAI, Inc.', 'Open AI') are canonicalized using a deterministic resolution cascade: "
        "(1) Exact matching against canonical seed database (50 curated AI entities), (2) Seed alias matching, (3) Normalization matching "
        "(Unicode NFKD transliteration, lowercase, legal corporate suffix stripping: <i>Inc, LLC, Ltd, Corp, Technologies, Labs</i>), and (4) Levenshtein / Token Sort fuzzy scoring. "
        "High confidence (>= 0.88) automatically maps; ambiguous matches (0.70 - 0.87) are flagged for manual review without false merging; scores < 0.70 form new standalone entities. "
        "Every resolution emits an auditable entry in <code>entity_mapping_logs</code>.",
        body_style
    ))

    story.append(Paragraph("7. Ethical Anti-Bot Navigation & High-Value Source Access", h1_style))
    story.append(Paragraph(
        "In strict adherence to engineering ethics and legal compliance, FrontierAtlas <b>never bypasses CAPTCHAs, defeats Cloudflare/Datadome gates, or circumvents access controls</b>. "
        "When protection gates are detected (HTTP 403/503 Cloudflare challenges), the crawler logs the restriction and seamlessly transitions to authorized alternative sources: "
        "official REST APIs (arXiv, GitHub, Hugging Face, Job APIs), syndication feeds (RSS/Atom), and permitted institutional data dumps. "
        "For enterprise production, high-value protected sources are ingested via authorized B2B API partnerships, licensed data firehoses, and sanctioned authenticated Webhooks.",
        body_style
    ))

    story.append(Paragraph("8. Deliverables & Production Quality Verification", h1_style))
    story.append(Paragraph(
        "• <b>Dataset Delivery:</b> Master Google Sheets workbook & local XLSX/CSV exports across all 6 tabs (Startups >=1,000, Products >=1,000, Research "
        "Papers >=1,000 with GitHub stars, 24-hr fresh Jobs, 24-hr fresh News, Entity Mapping Log).<br/>"
        "• <b>Engineering Codebase:</b> Modular Python 3.11 architecture, FastAPI endpoints, Pydantic validation, full Pytest test suite, Docker & Docker Compose deployment, and complete README documentation.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    app_logger.info(f"Generated architecture PDF: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
