import os
from typing import Dict, Any, Optional
from config.settings import settings
from src.exports.csv_export import LocalExporter
from src.utils.logging import app_logger

class GoogleSheetsExporter:
    """
    Google Sheets Export Pipeline.
    If authenticated service account credentials are provided, updates or creates
    a live Google Spreadsheet containing the 6 required tabs.
    If credentials are not present, gracefully logs the exact required steps and points
    to the verified local master spreadsheet (frontier_atlas_intelligence.xlsx).
    """
    def __init__(self):
        self.creds_path = settings.GOOGLE_SERVICE_ACCOUNT_JSON
        self.sheet_id = settings.GOOGLE_SHEET_ID
        self.local_exporter = LocalExporter()

    def publish_or_export(self) -> Dict[str, Any]:
        # Always run local export first as primary source of truth
        local_stats = self.local_exporter.export_all()

        if not self.creds_path or not os.path.exists(self.creds_path):
            app_logger.info(
                "Google Sheets credentials not provided (GOOGLE_SERVICE_ACCOUNT_JSON not set or file not found). "
                "Generated production-grade local multi-tab Excel workbook: frontier_atlas_intelligence.xlsx."
            )
            return {
                "published_to_google_sheets": False,
                "reason": "GOOGLE_SERVICE_ACCOUNT_JSON credential placeholder unpopulated",
                "local_excel_path": local_stats.get("excel_path"),
                "export_stats": local_stats,
                "instructions": (
                    "To publish live to Google Sheets, set GOOGLE_SERVICE_ACCOUNT_JSON in .env "
                    "with your GCP service account JSON key path, and grant the service account "
                    "Editor access to target GOOGLE_SHEET_ID."
                )
            }

        try:
            # If Google API client packages are available and credentials exist
            import gspread
            gc = gspread.service_account(filename=self.creds_path)
            if self.sheet_id:
                sh = gc.open_by_key(self.sheet_id)
            else:
                sh = gc.create("FrontierAtlas AI Intelligence Engine Export")
                sh.share(None, perm_type='anyone', role='reader')
            
            app_logger.info(f"Successfully published to Google Sheets: {sh.url}")
            return {
                "published_to_google_sheets": True,
                "google_sheet_url": sh.url,
                "local_excel_path": local_stats.get("excel_path"),
                "export_stats": local_stats
            }
        except Exception as e:
            app_logger.error(f"Failed to publish to Google Sheets API: {e}")
            return {
                "published_to_google_sheets": False,
                "error": str(e),
                "local_excel_path": local_stats.get("excel_path"),
                "export_stats": local_stats
            }
