import os
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from config.settings import settings
from src.storage.database import get_db_session
from src.storage.repositories import (
    StartupRepository, ProductRepository, PaperRepository, JobRepository, NewsRepository, EntityMappingRepository
)
from src.utils.logging import app_logger

class LocalExporter:
    """
    Exports ingested datasets into local CSVs and a styled multi-tab Excel workbook.
    Conforms strictly to the 6 required tabs:
      1. Startups
      2. Products
      3. Research Papers
      4. Jobs
      5. News
      6. Entity Mapping Log
    """
    def __init__(self, export_dir: Optional[Path] = None):
        self.export_dir = export_dir or settings.EXPORTS_DIR
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_all(self) -> Dict[str, Any]:
        app_logger.info(f"Exporting all datasets to {self.export_dir}...")
        with get_db_session() as session:
            startups = StartupRepository(session).get_all()
            products = ProductRepository(session).get_all()
            papers = PaperRepository(session).get_all()
            jobs = JobRepository(session).get_all()
            news = NewsRepository(session).get_all()
            entity_logs = EntityMappingRepository(session).get_all()

            stats = {
                "startups": len(startups),
                "products": len(products),
                "research_papers": len(papers),
                "jobs": len(jobs),
                "news": len(news),
                "entity_logs": len(entity_logs)
            }

            # 1. Export CSVs
            self._export_csv("startups.csv", [
                ["schemaVersion", "recordType", "source.name", "source.url", "content.entityName", "content.data.employeeCount", "collectedAt"]
            ] + [
                [s.schema_version, s.record_type, s.source_name, s.source_url, s.canonical_name, s.employee_count if s.employee_count is not None else "", s.collected_at]
                for s in startups
            ])

            self._export_csv("products.csv", [
                ["schemaVersion", "recordType", "source.name", "source.url", "content.startupName", "content.productName", "content.pricingModel", "collectedAt"]
            ] + [
                [p.schema_version, p.record_type, p.source_name, p.source_url, p.startup_name, p.product_name, p.pricing_model or "", p.collected_at]
                for p in products
            ])

            self._export_csv("research_papers.csv", [
                ["schemaVersion", "recordType", "content.title", "content.authors", "content.paper_url", "content.github_url", "content.github_stars", "github_stars_retrieved_at", "content.published_date"]
            ] + [
                [r.schema_version, r.record_type, r.title, "; ".join(r.authors), r.paper_url, r.github_url or "", r.github_stars if r.github_stars is not None else "", r.github_stars_retrieved_at or "", r.published_date]
                for r in papers
            ])

            self._export_csv("jobs.csv", [
                ["schemaVersion", "recordType", "source.name", "source.url", "content.company", "content.title", "content.date", "content.is_remote", "content.role_family", "first_discovered_at", "collected_at"]
            ] + [
                [j.schema_version, j.record_type, j.source_name, j.source_url, j.company, j.title or "", j.date, "TRUE" if j.is_remote else "FALSE", j.role_family, j.first_discovered_at, j.collected_at]
                for j in jobs
            ])

            self._export_csv("news.csv", [
                ["schemaVersion", "recordType", "source.name", "source.url", "content.title", "content.published_at", "content.summary", "content.author", "collectedAt", "firstDiscoveredAt"]
            ] + [
                [n.schema_version, n.record_type, n.source_name, n.source_url, n.title, n.published_at, n.summary or "", n.author or "", n.collected_at, n.first_discovered_at]
                for n in news
            ])

            self._export_csv("entity_mapping_log.csv", [
                ["raw_name", "canonical_name", "matching_method", "confidence_score", "source_url", "resolution_timestamp"]
            ] + [
                [e.raw_name, e.canonical_name, e.matching_method, f"{e.confidence_score:.4f}", e.source_url, e.resolution_timestamp]
                for e in entity_logs
            ])

            # 2. Export Master Excel Workbook with all 6 tabs and executive formatting
            xlsx_path = self.export_dir / "frontier_atlas_intelligence.xlsx"
            self._export_master_xlsx(xlsx_path, startups, products, papers, jobs, news, entity_logs)

        stats["excel_path"] = str(xlsx_path)
        app_logger.info(f"Local export completed successfully: {stats}")
        return stats

    def _export_csv(self, filename: str, rows: List[List[Any]]) -> None:
        filepath = self.export_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def _export_master_xlsx(
        self,
        filepath: Path,
        startups: list,
        products: list,
        papers: list,
        jobs: list,
        news: list,
        entity_logs: list
    ) -> None:
        wb = Workbook()
        # Remove default sheet
        wb.remove(wb.active)

        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid") # Navy
        header_align = Alignment(horizontal="left", vertical="center", wrap_text=False)
        regular_font = Font(name="Calibri", size=10)

        tabs_data = [
            ("Startups", [
                "schemaVersion", "recordType", "source.name", "source.url", "content.entityName", "content.data.employeeCount", "collectedAt"
            ], [
                [s.schema_version, s.record_type, s.source_name, s.source_url, s.canonical_name, s.employee_count, s.collected_at]
                for s in startups
            ]),
            ("Products", [
                "schemaVersion", "recordType", "source.name", "source.url", "content.startupName", "content.productName", "content.pricingModel", "collectedAt"
            ], [
                [p.schema_version, p.record_type, p.source_name, p.source_url, p.startup_name, p.product_name, p.pricing_model, p.collected_at]
                for p in products
            ]),
            ("Research Papers", [
                "schemaVersion", "recordType", "content.title", "content.authors", "content.paper_url", "content.github_url", "content.github_stars", "github_stars_retrieved_at", "content.published_date"
            ], [
                [r.schema_version, r.record_type, r.title, "; ".join(r.authors), r.paper_url, r.github_url, r.github_stars, r.github_stars_retrieved_at, r.published_date]
                for r in papers
            ]),
            ("Jobs", [
                "schemaVersion", "recordType", "source.name", "source.url", "content.company", "content.title", "content.date", "content.is_remote", "content.role_family", "first_discovered_at", "collected_at"
            ], [
                [j.schema_version, j.record_type, j.source_name, j.source_url, j.company, j.title, j.date, j.is_remote, j.role_family, j.first_discovered_at, j.collected_at]
                for j in jobs
            ]),
            ("News", [
                "schemaVersion", "recordType", "source.name", "source.url", "content.title", "content.published_at", "content.summary", "content.author", "collectedAt", "firstDiscoveredAt"
            ], [
                [n.schema_version, n.record_type, n.source_name, n.source_url, n.title, n.published_at, n.summary, n.author, n.collected_at, n.first_discovered_at]
                for n in news
            ]),
            ("Entity Mapping Log", [
                "raw_name", "canonical_name", "matching_method", "confidence_score", "source_url", "resolution_timestamp"
            ], [
                [e.raw_name, e.canonical_name, e.matching_method, e.confidence_score, e.source_url, e.resolution_timestamp]
                for e in entity_logs
            ])
        ]

        for title, headers, rows in tabs_data:
            ws = wb.create_sheet(title=title)
            ws.append(headers)

            # Style header row
            for col_num in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col_num)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_align

            ws.row_dimensions[1].height = 24

            # Append data rows
            for row in rows:
                ws.append(row)

            # Freeze top row
            ws.freeze_panes = "A2"

            # Enable auto-filter
            last_col_letter = get_column_letter(len(headers))
            ws.auto_filter.ref = f"A1:{last_col_letter}{len(rows) + 1}"

            # Auto-fit column widths with padding
            for col in ws.columns:
                max_len = 0
                col_letter = get_column_letter(col[0].column)
                for cell in col[:100]:  # sample first 100 cells
                    val = str(cell.value or "")
                    if len(val) > max_len:
                        max_len = len(val)
                ws.column_dimensions[col_letter].width = min(50, max(max_len + 4, 12))

        wb.save(filepath)
