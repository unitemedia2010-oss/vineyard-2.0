"""
Unit and Integration Tests for VINEYARD 2.0 Engine
"""
import pytest
from pathlib import Path
from crawler.discovery import DiscoveryEngine
from crawler.models import PageType
from crawler.extractors.product import ProductExtractor
from crawler.extractors.category import CategoryExtractor
from crawler.storage import Database
from crawler.exporter import Exporter
from crawler.validator import DataValidator

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_url_normalization():
    # Test tracking params stripped
    raw = "https://vineyard.vn/san-pham/r9-primitivo?utm_source=facebook&fbclid=123"
    clean = DiscoveryEngine.normalize_url(raw)
    assert clean == "https://vineyard.vn/san-pham/r9-primitivo"

    # Test relative path resolution
    rel = "/san-pham/vang-y"
    clean_rel = DiscoveryEngine.normalize_url(rel, "https://vineyard.vn/danh-muc/vang-do")
    assert clean_rel == "https://vineyard.vn/san-pham/vang-y"

    # Test non-allowed domains rejected
    foreign = "https://evil-site.com/malicious"
    assert DiscoveryEngine.normalize_url(foreign) is None

    # Test pagination query kept
    page_url = "https://vineyard.vn/danh-muc/vang-do?page=2"
    assert DiscoveryEngine.normalize_url(page_url) == "https://vineyard.vn/danh-muc/vang-do?page=2"

def test_url_classification():
    engine = DiscoveryEngine()
    assert engine.classify_url("https://vineyard.vn") == PageType.HOMEPAGE
    assert engine.classify_url("https://vineyard.vn/san-pham/r9-primitivo") == PageType.PRODUCT
    assert engine.classify_url("https://vineyard.vn/danh-muc/vang-do") == PageType.CATEGORY
    assert engine.classify_url("https://vineyard.vn/post/khuyen-mai") == PageType.ARTICLE
    assert engine.classify_url("https://vineyard.vn/page/catalogue") == PageType.INFORMATIONAL

def test_product_extractor_with_fixture():
    fixture_path = FIXTURES_DIR / "sample_product.html"
    html = fixture_path.read_text(encoding="utf-8")
    product = ProductExtractor.extract(html, "https://vineyard.vn/san-pham/r9-primitivo-icono")

    assert product is not None
    assert product.name == "R9 Primitivo & Syrah Passito Salento IGP"
    assert product.sku == "B06.GRATI.06"
    assert product.brand == "Reputazione"
    assert product.origin_country == "Italy"
    assert product.region == "Puglia"
    assert product.grape_variety == "Primitivo"
    assert product.abv == "19,0%"
    assert product.volume == "0.75L"
    assert product.producer == "Reputazione"
    assert "Đỏ Ruby" in product.tasting_notes
    assert product.main_image_url is not None
    assert "R9-limited-edition.png" in product.main_image_url
    assert product.stock_status == "Còn trong kho"

def test_category_extractor_with_fixture():
    fixture_path = FIXTURES_DIR / "sample_category.html"
    html = fixture_path.read_text(encoding="utf-8")
    cat = CategoryExtractor.extract(html, "https://vineyard.vn/danh-muc/vang-do")

    assert cat is not None
    assert cat.name == "Vang Đỏ"
    assert cat.product_count == 2
    assert "tuyển chọn" in cat.description

def test_database_and_exporter(tmp_path):
    test_db_path = tmp_path / "test_vineyard.db"
    db = Database(db_path=test_db_path)

    # Test saving page discovery
    added = db.save_page_discovery("https://vineyard.vn/san-pham/test-wine", PageType.PRODUCT)
    assert added is True
    # Duplicate insert returns False
    assert db.save_page_discovery("https://vineyard.vn/san-pham/test-wine", PageType.PRODUCT) is False

    # Test saving product
    fixture_path = FIXTURES_DIR / "sample_product.html"
    product = ProductExtractor.extract(fixture_path.read_text(encoding="utf-8"), "https://vineyard.vn/san-pham/test-wine")
    prod_id = db.save_product(product)
    assert prod_id is not None

    stats = db.get_stats()
    assert stats["pages_total"] == 1
    assert stats["products"] == 1

    # Test validation
    validator = DataValidator(db)
    metrics = validator.run_full_validation()
    assert metrics["entities"]["products"] == 1
    assert metrics["anomalies"]["duplicate_skus_count"] == 0
