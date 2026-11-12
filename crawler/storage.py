"""
SQLite Storage Engine for VINEYARD 2.0
"""
import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from crawler.config import config
from crawler.models import (
    PageRecord, ProductRecord, CategoryRecord, BrandRecord,
    ArticleRecord, AssetRecord, PageType, ExtractionStatus
)

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS crawl_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL,
    finished_at TIMESTAMP,
    total_discovered INTEGER DEFAULT 0,
    total_fetched INTEGER DEFAULT 0,
    total_extracted INTEGER DEFAULT 0,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    canonical_url TEXT,
    page_type TEXT NOT NULL,
    http_status INTEGER,
    response_time_ms REAL,
    content_type TEXT,
    raw_html_path TEXT,
    extraction_status TEXT NOT NULL DEFAULT 'pending',
    error_message TEXT,
    title TEXT,
    meta_description TEXT,
    metadata_json TEXT,
    discovered_at TIMESTAMP NOT NULL,
    fetched_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pages_url ON pages(url);
CREATE INDEX IF NOT EXISTS idx_pages_type ON pages(page_type);
CREATE INDEX IF NOT EXISTS idx_pages_status ON pages(extraction_status);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT UNIQUE NOT NULL,
    canonical_url TEXT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    sku TEXT,
    brand TEXT,
    category TEXT,
    origin_country TEXT,
    region TEXT,
    producer TEXT,
    vintage TEXT,
    grape_variety TEXT,
    volume TEXT,
    abv TEXT,
    original_price REAL,
    sale_price REAL,
    currency TEXT DEFAULT 'VND',
    stock_status TEXT,
    description TEXT,
    tasting_notes TEXT,
    specs_json TEXT,
    main_image_url TEXT,
    gallery_json TEXT,
    crawl_timestamp TIMESTAMP NOT NULL,
    extraction_source TEXT NOT NULL,
    verification_level TEXT NOT NULL DEFAULT 'verified'
);

CREATE INDEX IF NOT EXISTS idx_products_source_url ON products(source_url);
CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT UNIQUE NOT NULL,
    slug TEXT NOT NULL,
    name TEXT NOT NULL,
    parent_category TEXT,
    description TEXT,
    product_count INTEGER,
    crawl_timestamp TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);

CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT UNIQUE NOT NULL,
    slug TEXT NOT NULL,
    name TEXT NOT NULL,
    country TEXT,
    description TEXT,
    logo_url TEXT,
    crawl_timestamp TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_brands_slug ON brands(slug);

CREATE TABLE IF NOT EXISTS product_categories (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT UNIQUE NOT NULL,
    source_page_url TEXT NOT NULL,
    asset_category TEXT NOT NULL,
    local_path TEXT,
    mime_type TEXT,
    file_size_bytes INTEGER,
    sha256 TEXT UNIQUE,
    width INTEGER,
    height INTEGER,
    download_timestamp TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'pending'
);

CREATE INDEX IF NOT EXISTS idx_assets_url ON assets(original_url);
CREATE INDEX IF NOT EXISTS idx_assets_sha256 ON assets(sha256);
CREATE INDEX IF NOT EXISTS idx_assets_category ON assets(asset_category);

CREATE TABLE IF NOT EXISTS product_images (
    product_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    is_main INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    PRIMARY KEY (product_id, asset_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT UNIQUE NOT NULL,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    publish_date TEXT,
    summary TEXT,
    content_html TEXT,
    featured_image_url TEXT,
    tags_json TEXT,
    crawl_timestamp TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(source_url);

CREATE TABLE IF NOT EXISTS navigation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    url TEXT NOT NULL,
    parent_id INTEGER,
    sort_order INTEGER DEFAULT 0,
    menu_location TEXT DEFAULT 'main_nav',
    FOREIGN KEY (parent_id) REFERENCES navigation(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS redirects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT NOT NULL,
    target_url TEXT NOT NULL,
    http_status INTEGER NOT NULL,
    recorded_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS extraction_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    error_phase TEXT NOT NULL,
    error_type TEXT NOT NULL,
    error_message TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
"""

class Database:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or config.db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()

    def start_job(self, job_type: str, notes: str = "") -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO crawl_jobs (job_type, status, started_at, notes) VALUES (?, ?, ?, ?)",
                (job_type, "running", datetime.now(timezone.utc).isoformat(), notes)
            )
            conn.commit()
            return cursor.lastrowid

    def finish_job(self, job_id: int, total_discovered: int, total_fetched: int, total_extracted: int, status: str = "completed") -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE crawl_jobs
                SET status = ?, finished_at = ?, total_discovered = ?, total_fetched = ?, total_extracted = ?
                WHERE id = ?
                """,
                (status, datetime.now(timezone.utc).isoformat(), total_discovered, total_fetched, total_extracted, job_id)
            )
            conn.commit()

    def save_page_discovery(self, url: str, page_type: PageType, canonical_url: Optional[str] = None) -> bool:
        """Insert page if not exists. Return True if newly added, False if already exists."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO pages (url, canonical_url, page_type, extraction_status, discovered_at)
                VALUES (?, ?, ?, 'pending', ?)
                """,
                (url, canonical_url, page_type.value, datetime.now(timezone.utc).isoformat())
            )
            conn.commit()
            return cursor.rowcount > 0

    def update_page_fetched(
        self,
        url: str,
        http_status: int,
        response_time_ms: float,
        content_type: Optional[str],
        raw_html_path: Optional[str],
        title: Optional[str] = None,
        meta_description: Optional[str] = None,
        metadata_json: Optional[str] = None,
        error_message: Optional[str] = None,
        extraction_status: ExtractionStatus = ExtractionStatus.FETCHED
    ) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE pages
                SET http_status = ?, response_time_ms = ?, content_type = ?, raw_html_path = ?,
                    title = ?, meta_description = ?, metadata_json = ?, error_message = ?,
                    extraction_status = ?, fetched_at = ?
                WHERE url = ?
                """,
                (
                    http_status, response_time_ms, content_type, raw_html_path,
                    title, meta_description, metadata_json, error_message,
                    extraction_status.value, datetime.now(timezone.utc).isoformat(), url
                )
            )
            conn.commit()

    def get_pending_pages(self, limit: Optional[int] = None) -> List[sqlite3.Row]:
        query = """
            SELECT * FROM pages
            WHERE extraction_status = 'pending'
            ORDER BY 
                CASE page_type 
                    WHEN 'product' THEN 1 
                    WHEN 'category' THEN 2 
                    WHEN 'article' THEN 3
                    ELSE 4 
                END, id ASC
        """
        if limit:
            query += f" LIMIT {limit}"
        with self.get_connection() as conn:
            return conn.execute(query).fetchall()

    def get_page_by_url(self, url: str) -> Optional[sqlite3.Row]:
        with self.get_connection() as conn:
            return conn.execute("SELECT * FROM pages WHERE url = ?", (url,)).fetchone()

    def save_product(self, product: ProductRecord) -> int:
        ts = product.crawl_timestamp.isoformat() if hasattr(product.crawl_timestamp, "isoformat") else str(product.crawl_timestamp)
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO products (
                    source_url, canonical_url, name, slug, sku, brand, category,
                    origin_country, region, producer, vintage, grape_variety, volume, abv,
                    original_price, sale_price, currency, stock_status, description, tasting_notes,
                    specs_json, main_image_url, gallery_json, crawl_timestamp, extraction_source, verification_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_url) DO UPDATE SET
                    name=excluded.name,
                    slug=excluded.slug,
                    sku=excluded.sku,
                    brand=excluded.brand,
                    category=excluded.category,
                    origin_country=excluded.origin_country,
                    region=excluded.region,
                    producer=excluded.producer,
                    vintage=excluded.vintage,
                    grape_variety=excluded.grape_variety,
                    volume=excluded.volume,
                    abv=excluded.abv,
                    original_price=excluded.original_price,
                    sale_price=excluded.sale_price,
                    stock_status=excluded.stock_status,
                    description=excluded.description,
                    tasting_notes=excluded.tasting_notes,
                    specs_json=excluded.specs_json,
                    main_image_url=excluded.main_image_url,
                    gallery_json=excluded.gallery_json,
                    crawl_timestamp=excluded.crawl_timestamp,
                    extraction_source=excluded.extraction_source,
                    verification_level=excluded.verification_level
                """,
                (
                    product.source_url, product.canonical_url, product.name, product.slug, product.sku,
                    product.brand, product.category, product.origin_country, product.region,
                    product.producer, product.vintage, product.grape_variety, product.volume, product.abv,
                    product.original_price, product.sale_price, product.currency, product.stock_status,
                    product.description, product.tasting_notes, json.dumps(product.specs, ensure_ascii=False),
                    product.main_image_url, json.dumps(product.gallery_image_urls, ensure_ascii=False),
                    ts, product.extraction_source, product.verification_level
                )
            )
            conn.commit()
            return cursor.lastrowid

    def save_category(self, cat: CategoryRecord) -> int:
        ts = cat.crawl_timestamp.isoformat() if hasattr(cat.crawl_timestamp, "isoformat") else str(cat.crawl_timestamp)
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO categories (source_url, slug, name, parent_category, description, product_count, crawl_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_url) DO UPDATE SET
                    slug=excluded.slug,
                    name=excluded.name,
                    parent_category=excluded.parent_category,
                    description=excluded.description,
                    product_count=excluded.product_count,
                    crawl_timestamp=excluded.crawl_timestamp
                """,
                (cat.source_url, cat.slug, cat.name, cat.parent_category, cat.description, cat.product_count, ts)
            )
            conn.commit()
            return cursor.lastrowid

    def save_brand(self, brand: BrandRecord) -> int:
        ts = brand.crawl_timestamp.isoformat() if hasattr(brand.crawl_timestamp, "isoformat") else str(brand.crawl_timestamp)
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO brands (source_url, slug, name, country, description, logo_url, crawl_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_url) DO UPDATE SET
                    slug=excluded.slug,
                    name=excluded.name,
                    country=excluded.country,
                    description=excluded.description,
                    logo_url=excluded.logo_url,
                    crawl_timestamp=excluded.crawl_timestamp
                """,
                (brand.source_url, brand.slug, brand.name, brand.country, brand.description, brand.logo_url, ts)
            )
            conn.commit()
            return cursor.lastrowid

    def save_article(self, article: ArticleRecord) -> int:
        ts = article.crawl_timestamp.isoformat() if hasattr(article.crawl_timestamp, "isoformat") else str(article.crawl_timestamp)
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO articles (source_url, slug, title, author, publish_date, summary, content_html, featured_image_url, tags_json, crawl_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_url) DO UPDATE SET
                    slug=excluded.slug,
                    title=excluded.title,
                    author=excluded.author,
                    publish_date=excluded.publish_date,
                    summary=excluded.summary,
                    content_html=excluded.content_html,
                    featured_image_url=excluded.featured_image_url,
                    tags_json=excluded.tags_json,
                    crawl_timestamp=excluded.crawl_timestamp
                """,
                (
                    article.source_url, article.slug, article.title, article.author,
                    article.publish_date, article.summary, article.content_html,
                    article.featured_image_url, json.dumps(article.tags, ensure_ascii=False),
                    ts
                )
            )
            conn.commit()
            return cursor.lastrowid

    def save_asset(self, asset: AssetRecord) -> int:
        ts = asset.download_timestamp.isoformat() if hasattr(asset.download_timestamp, "isoformat") and asset.download_timestamp else (str(asset.download_timestamp) if asset.download_timestamp else None)
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO assets (original_url, source_page_url, asset_category, local_path, mime_type, file_size_bytes, sha256, width, height, download_timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(original_url) DO UPDATE SET
                    local_path=excluded.local_path,
                    mime_type=excluded.mime_type,
                    file_size_bytes=excluded.file_size_bytes,
                    sha256=excluded.sha256,
                    width=excluded.width,
                    height=excluded.height,
                    download_timestamp=excluded.download_timestamp,
                    status=excluded.status
                """,
                (
                    asset.original_url, asset.source_page_url, asset.asset_category.value,
                    asset.local_path, asset.mime_type, asset.file_size_bytes, asset.sha256,
                    asset.width, asset.height, ts, asset.status
                )
            )
            conn.commit()
            return cursor.lastrowid

    def record_error(self, url: str, error_phase: str, error_type: str, error_message: str) -> None:
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO extraction_errors (url, error_phase, error_type, error_message, timestamp) VALUES (?, ?, ?, ?, ?)",
                (url, error_phase, error_type, error_message, datetime.now(timezone.utc).isoformat())
            )
            conn.commit()

    def get_stats(self) -> Dict[str, int]:
        with self.get_connection() as conn:
            pages_total = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
            pages_pending = conn.execute("SELECT COUNT(*) FROM pages WHERE extraction_status = 'pending'").fetchone()[0]
            pages_success = conn.execute("SELECT COUNT(*) FROM pages WHERE extraction_status = 'success'").fetchone()[0]
            pages_failed = conn.execute("SELECT COUNT(*) FROM pages WHERE extraction_status = 'failed'").fetchone()[0]
            products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
            categories = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
            brands = conn.execute("SELECT COUNT(*) FROM brands").fetchone()[0]
            articles = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
            assets = conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
            errors = conn.execute("SELECT COUNT(*) FROM extraction_errors").fetchone()[0]

            return {
                "pages_total": pages_total,
                "pages_pending": pages_pending,
                "pages_success": pages_success,
                "pages_failed": pages_failed,
                "products": products,
                "categories": categories,
                "brands": brands,
                "articles": articles,
                "assets": assets,
                "errors": errors
            }
