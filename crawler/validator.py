"""
Data Integrity, Validation, and Completeness Engine
"""
import sqlite3
import logging
from typing import Dict, Any, List
from crawler.storage import Database

logger = logging.getLogger("crawler.validator")

class DataValidator:
    def __init__(self, db: Database):
        self.db = db

    def run_full_validation(self) -> Dict[str, Any]:
        """Run all data cross-referencing and verification checks."""
        conn = self.db.get_connection()

        # 1. Page Counts & Pipeline Funnel
        pages_total = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
        pages_fetched = conn.execute("SELECT COUNT(*) FROM pages WHERE http_status IS NOT NULL").fetchone()[0]
        pages_success = conn.execute("SELECT COUNT(*) FROM pages WHERE extraction_status = 'success'").fetchone()[0]
        pages_failed = conn.execute("SELECT COUNT(*) FROM pages WHERE extraction_status = 'failed'").fetchone()[0]
        pages_pending = conn.execute("SELECT COUNT(*) FROM pages WHERE extraction_status = 'pending'").fetchone()[0]

        # 2. Entity Counts
        products_total = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        categories_total = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
        brands_total = conn.execute("SELECT COUNT(*) FROM brands").fetchone()[0]
        articles_total = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        assets_total = conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0]

        # 3. Product Integrity Checks
        missing_price = conn.execute("SELECT COUNT(*) FROM products WHERE sale_price IS NULL AND original_price IS NULL").fetchone()[0]
        missing_sku = conn.execute("SELECT COUNT(*) FROM products WHERE sku IS NULL OR sku = ''").fetchone()[0]
        missing_image = conn.execute("SELECT COUNT(*) FROM products WHERE main_image_url IS NULL OR main_image_url = ''").fetchone()[0]
        duplicate_skus = conn.execute(
            """
            SELECT sku, COUNT(*) as cnt FROM products
            WHERE sku IS NOT NULL AND sku != ''
            GROUP BY sku HAVING cnt > 1
            """
        ).fetchall()

        duplicate_names = conn.execute(
            """
            SELECT name, COUNT(*) as cnt FROM products
            GROUP BY name HAVING cnt > 1
            """
        ).fetchall()

        # 4. Asset Deduplication & Integrity
        duplicate_assets_sha256 = conn.execute(
            """
            SELECT sha256, COUNT(*) as cnt FROM assets
            WHERE sha256 IS NOT NULL
            GROUP BY sha256 HAVING cnt > 1
            """
        ).fetchall()

        missing_local_assets = conn.execute(
            "SELECT COUNT(*) FROM assets WHERE local_path IS NULL OR status = 'error'"
        ).fetchone()[0]

        # 5. Extraction Errors Breakdown
        errors = conn.execute(
            "SELECT error_phase, error_type, COUNT(*) as cnt FROM extraction_errors GROUP BY error_phase, error_type"
        ).fetchall()

        completeness_rate = round((pages_success / pages_total * 100), 2) if pages_total > 0 else 0.0

        return {
            "funnel": {
                "discovered": pages_total,
                "fetched": pages_fetched,
                "success": pages_success,
                "failed": pages_failed,
                "pending": pages_pending,
                "completeness_rate_percent": completeness_rate
            },
            "entities": {
                "products": products_total,
                "categories": categories_total,
                "brands": brands_total,
                "articles": articles_total,
                "assets": assets_total
            },
            "anomalies": {
                "products_missing_price": missing_price,
                "products_missing_sku": missing_sku,
                "products_missing_image": missing_image,
                "duplicate_skus_count": len(duplicate_skus),
                "duplicate_names_count": len(duplicate_names),
                "duplicate_assets_sha256_count": len(duplicate_assets_sha256),
                "unresolved_missing_assets": missing_local_assets
            },
            "errors_summary": [dict(e) for e in errors]
        }
