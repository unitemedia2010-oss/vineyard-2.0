"""
Data Models and Enums for VINEYARD 2.0
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class PageType(str, Enum):
    HOMEPAGE = "homepage"
    CATEGORY = "category"
    PRODUCT = "product"
    BRAND = "brand"
    ARTICLE = "article"
    INFORMATIONAL = "informational"
    CONTACT = "contact"
    OTHER = "other"

class ExtractionStatus(str, Enum):
    PENDING = "pending"
    FETCHED = "fetched"
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"

class AssetCategory(str, Enum):
    PRODUCTS = "products"
    BANNERS = "banners"
    BRANDS = "brands"
    ARTICLES = "articles"
    ICONS = "icons"
    MISC = "misc"

class PageMetadata(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    canonical: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    og_type: Optional[str] = None
    headings: Dict[str, List[str]] = Field(default_factory=dict)
    json_ld: List[Dict[str, Any]] = Field(default_factory=list)
    breadcrumbs: List[Dict[str, str]] = Field(default_factory=list)

class PageRecord(BaseModel):
    url: str
    canonical_url: Optional[str] = None
    page_type: PageType = PageType.OTHER
    http_status: Optional[int] = None
    fetch_timestamp: Optional[datetime] = None
    response_time_ms: Optional[float] = None
    content_type: Optional[str] = None
    raw_html_path: Optional[str] = None
    extraction_status: ExtractionStatus = ExtractionStatus.PENDING
    error_message: Optional[str] = None
    metadata: PageMetadata = Field(default_factory=PageMetadata)
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductRecord(BaseModel):
    source_url: str
    canonical_url: Optional[str] = None
    name: str
    slug: str
    sku: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    origin_country: Optional[str] = None  # Xuất xứ (Pháp, Ý, Chile,...)
    region: Optional[str] = None          # Vùng (Bordeaux, Tuscany, Napa Valley,...)
    producer: Optional[str] = None        # Nhà sản xuất
    vintage: Optional[str] = None         # Niên vụ (năm sản xuất rượu)
    grape_variety: Optional[str] = None   # Giống nho (Cabernet Sauvignon, Merlot,...)
    volume: Optional[str] = None          # Dung tích (750ml, 1500ml,...)
    abv: Optional[str] = None             # Nồng độ cồn (% ABV)
    original_price: Optional[float] = None
    sale_price: Optional[float] = None
    currency: str = "VND"
    stock_status: Optional[str] = None    # Còn hàng / Hết hàng / Liên hệ
    description: Optional[str] = None     # Mô tả chi tiết
    tasting_notes: Optional[str] = None   # Hương vị, kết hợp món ăn
    specs: Dict[str, Any] = Field(default_factory=dict) # Các thuộc tính chi tiết dạng key-value
    main_image_url: Optional[str] = None
    gallery_image_urls: List[str] = Field(default_factory=list)
    crawl_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    extraction_source: str = "dom+jsonld"
    verification_level: str = "verified"   # verified, partial, unverified

class CategoryRecord(BaseModel):
    source_url: str
    slug: str
    name: str
    parent_category: Optional[str] = None
    description: Optional[str] = None
    product_count: Optional[int] = None
    crawl_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BrandRecord(BaseModel):
    source_url: str
    slug: str
    name: str
    country: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    crawl_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ArticleRecord(BaseModel):
    source_url: str
    slug: str
    title: str
    author: Optional[str] = None
    publish_date: Optional[str] = None
    summary: Optional[str] = None
    content_html: Optional[str] = None
    featured_image_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    crawl_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AssetRecord(BaseModel):
    original_url: str
    source_page_url: str
    asset_category: AssetCategory = AssetCategory.MISC
    local_path: Optional[str] = None
    mime_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    sha256: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    download_timestamp: Optional[datetime] = None
    status: str = "pending"  # pending, downloaded, error, duplicate
