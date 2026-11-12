"""
Orchestration Pipeline: Fetch -> Snapshot -> Extract -> Deduplicate Assets -> Save
"""
import hashlib
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timezone
from crawler.config import config
from crawler.client import HttpClient
from crawler.storage import Database
from crawler.discovery import DiscoveryEngine
from crawler.extractors.base import BaseExtractor
from crawler.extractors.product import ProductExtractor
from crawler.extractors.category import CategoryExtractor
from crawler.extractors.brand import BrandExtractor
from crawler.extractors.article import ArticleExtractor
from crawler.assets import AssetManager
from crawler.models import PageType, ExtractionStatus, AssetCategory

logger = logging.getLogger("crawler.pipeline")

class CrawlPipeline:
    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()
        self.client = HttpClient()
        self.discovery = DiscoveryEngine(self.client)
        self.asset_mgr = AssetManager(self.db)

    def _save_raw_snapshot(self, url: str, html: str) -> str:
        """Store exact unadulterated HTML snapshot with hash naming for provenance."""
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:12]
        slug = url.strip("/").split("/")[-1] or "home"
        clean_slug = "".join(c for c in slug if c.isalnum() or c in ("-", "_"))[:30]
        filename = f"{clean_slug}_{url_hash}.html"
        snapshot_path = config.raw_path / filename
        snapshot_path.write_text(html, encoding="utf-8", errors="replace")
        return str(snapshot_path)

    def process_url(self, url: str, ptype: PageType) -> bool:
        """
        Execute full pipeline for a single URL.
        Returns True if successful, False otherwise.
        """
        logger.info(f"Processing ({ptype.value}): {url}")
        resp, elapsed_ms, err = self.client.fetch(url)

        if not resp or resp.status_code != 200:
            error_msg = err or f"HTTP {resp.status_code if resp else 'No Response'}"
            self.db.update_page_fetched(
                url=url,
                http_status=resp.status_code if resp else 0,
                response_time_ms=elapsed_ms,
                content_type=resp.headers.get("content-type") if resp else None,
                raw_html_path=None,
                error_message=error_msg,
                extraction_status=ExtractionStatus.FAILED
            )
            self.db.record_error(url, "fetch", "HttpError", error_msg)
            return False

        html = resp.text
        raw_snapshot_path = self._save_raw_snapshot(url, html)

        # 1. Base Metadata Extraction
        meta = BaseExtractor.extract_metadata(html, url)

        # 2. Re-classify page type if more concrete evidence in DOM
        if ptype == PageType.OTHER:
            if meta.json_ld:
                for j in meta.json_ld:
                    if isinstance(j, dict) and j.get("@type") == "Product":
                        ptype = PageType.PRODUCT
                        break

        # 3. Domain Specific Extraction
        extraction_success = True
        try:
            if ptype == PageType.PRODUCT:
                product = ProductExtractor.extract(html, url)
                if product:
                    self.db.save_product(product)
                    logger.info(f"Successfully extracted product: '{product.name}' (SKU: {product.sku})")
                    # Download product images
                    if product.main_image_url:
                        self.asset_mgr.download_and_process(product.main_image_url, url, AssetCategory.PRODUCTS)
                    for g_img in product.gallery_image_urls[:5]:  # Polite download top gallery
                        self.asset_mgr.download_and_process(g_img, url, AssetCategory.PRODUCTS)
                else:
                    extraction_success = False

            elif ptype == PageType.CATEGORY:
                category = CategoryExtractor.extract(html, url)
                if category:
                    self.db.save_category(category)
                    logger.info(f"Successfully extracted category: '{category.name}'")

            elif ptype == PageType.BRAND:
                brand = BrandExtractor.extract(html, url)
                if brand:
                    self.db.save_brand(brand)
                    logger.info(f"Successfully extracted brand: '{brand.name}'")
                    if brand.logo_url:
                        self.asset_mgr.download_and_process(brand.logo_url, url, AssetCategory.BRANDS)

            elif ptype == PageType.ARTICLE:
                article = ArticleExtractor.extract(html, url)
                if article:
                    self.db.save_article(article)
                    logger.info(f"Successfully extracted article: '{article.title}'")
                    if article.featured_image_url:
                        self.asset_mgr.download_and_process(article.featured_image_url, url, AssetCategory.ARTICLES)

        except Exception as e:
            extraction_success = False
            self.db.record_error(url, "extraction", type(e).__name__, str(e))
            logger.error(f"Extraction error on {url}: {e}")

        # 4. Discover new internal links
        new_links = self.discovery.extract_internal_links(html, url)
        for link_url, link_type in new_links:
            self.db.save_page_discovery(link_url, link_type)

        # 5. Update Page Record
        self.db.update_page_fetched(
            url=url,
            http_status=resp.status_code,
            response_time_ms=elapsed_ms,
            content_type=resp.headers.get("content-type"),
            raw_html_path=raw_snapshot_path,
            title=meta.title,
            meta_description=meta.description,
            metadata_json=meta.model_dump_json(),
            extraction_status=ExtractionStatus.SUCCESS if extraction_success else ExtractionStatus.PARTIAL
        )

        return True

    def run(self, limit: Optional[int] = None) -> None:
        """Process pending queue up to limit."""
        job_id = self.db.start_job("crawl", f"Limit: {limit or 'Full'}")
        pending_rows = self.db.get_pending_pages(limit=limit)
        logger.info(f"Queue execution started. {len(pending_rows)} pending tasks to execute.")

        processed = 0
        succeeded = 0

        for row in pending_rows:
            url = row["url"]
            ptype = PageType(row["page_type"])
            ok = self.process_url(url, ptype)
            processed += 1
            if ok:
                succeeded += 1

        stats = self.db.get_stats()
        self.db.finish_job(
            job_id=job_id,
            total_discovered=stats["pages_total"],
            total_fetched=processed,
            total_extracted=succeeded
        )
        logger.info(f"Queue complete: {succeeded}/{processed} pages processed successfully.")
