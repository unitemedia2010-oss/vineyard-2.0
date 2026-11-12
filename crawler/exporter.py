"""
Data Exporter for JSON, CSV, and Markdown Catalogs
"""
import csv
import json
import sqlite3
import logging
from pathlib import Path
from typing import Dict, Any, List
from crawler.config import config
from crawler.storage import Database
from crawler.validator import DataValidator

logger = logging.getLogger("crawler.exporter")

class Exporter:
    def __init__(self, db: Database):
        self.db = db
        self.norm_dir = config.normalized_path
        self.reports_dir = config.reports_path
        self.research_dir = config.research_path
        self.norm_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.research_dir.mkdir(parents=True, exist_ok=True)

    def export_all(self) -> Dict[str, str]:
        """Export normalized JSONs, CSVs, and markdown reports."""
        conn = self.db.get_connection()
        exported_files = {}

        # 1. Export Products
        p_rows = conn.execute("SELECT * FROM products ORDER BY id ASC").fetchall()
        products_list = []
        for r in p_rows:
            d = dict(r)
            d["specs"] = json.loads(d["specs_json"]) if d.get("specs_json") else {}
            d["gallery"] = json.loads(d["gallery_json"]) if d.get("gallery_json") else []
            d.pop("specs_json", None)
            d.pop("gallery_json", None)
            products_list.append(d)

        prod_json_path = self.norm_dir / "products.json"
        prod_json_path.write_text(json.dumps(products_list, ensure_ascii=False, indent=2), encoding="utf-8")
        exported_files["products_json"] = str(prod_json_path)

        # CSV products
        prod_csv_path = self.norm_dir / "products.csv"
        if products_list:
            fieldnames = [
                "id", "name", "slug", "sku", "brand", "category", "origin_country", "region",
                "producer", "vintage", "grape_variety", "volume", "abv", "original_price",
                "sale_price", "currency", "stock_status", "source_url"
            ]
            with open(prod_csv_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(products_list)
            exported_files["products_csv"] = str(prod_csv_path)

        # 2. Export Categories
        c_rows = conn.execute("SELECT * FROM categories ORDER BY id ASC").fetchall()
        categories_list = [dict(r) for r in c_rows]
        cat_json_path = self.norm_dir / "categories.json"
        cat_json_path.write_text(json.dumps(categories_list, ensure_ascii=False, indent=2), encoding="utf-8")
        exported_files["categories_json"] = str(cat_json_path)

        cat_csv_path = self.norm_dir / "categories.csv"
        if categories_list:
            with open(cat_csv_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=list(categories_list[0].keys()))
                writer.writeheader()
                writer.writerows(categories_list)
            exported_files["categories_csv"] = str(cat_csv_path)

        # 3. Export Brands
        b_rows = conn.execute("SELECT * FROM brands ORDER BY id ASC").fetchall()
        brands_list = [dict(r) for r in b_rows]
        brand_json_path = self.norm_dir / "brands.json"
        brand_json_path.write_text(json.dumps(brands_list, ensure_ascii=False, indent=2), encoding="utf-8")
        exported_files["brands_json"] = str(brand_json_path)

        # 4. Export Articles
        a_rows = conn.execute("SELECT * FROM articles ORDER BY id ASC").fetchall()
        articles_list = []
        for r in a_rows:
            d = dict(r)
            d["tags"] = json.loads(d["tags_json"]) if d.get("tags_json") else []
            d.pop("tags_json", None)
            articles_list.append(d)
        art_json_path = self.norm_dir / "articles.json"
        art_json_path.write_text(json.dumps(articles_list, ensure_ascii=False, indent=2), encoding="utf-8")
        exported_files["articles_json"] = str(art_json_path)

        # 5. Export Assets Metadata
        asset_rows = conn.execute("SELECT * FROM assets ORDER BY id ASC").fetchall()
        assets_list = [dict(r) for r in asset_rows]
        asset_json_path = self.norm_dir / "assets.json"
        asset_json_path.write_text(json.dumps(assets_list, ensure_ascii=False, indent=2), encoding="utf-8")
        exported_files["assets_json"] = str(asset_json_path)

        # 6. Generate Crawl Report Markdown
        validator = DataValidator(self.db)
        metrics = validator.run_full_validation()
        report_md_path = self.reports_dir / "crawl_report.md"
        report_content = f"""# Báo Cáo Thu Thập Dữ Liệu VINEYARD 2.0 (Crawl Report)

## 1. Phễu Thu Thập (Pipeline Funnel)
- **Tổng URL Đã Khảo Sát (Discovered)**: {metrics['funnel']['discovered']}
- **Tổng URL Đã Tải (Fetched)**: {metrics['funnel']['fetched']}
- **Trích Xuất Thành Công (Success)**: {metrics['funnel']['success']}
- **Trích Xuất Thất Bại (Failed)**: {metrics['funnel']['failed']}
- **Đang Chờ Xử Lý (Pending)**: {metrics['funnel']['pending']}
- **Tỷ Lệ Hoàn Thành (Completeness Rate)**: {metrics['funnel']['completeness_rate_percent']}%

## 2. Thống Kê Thực Thể (Extracted Entities)
| Thực Thể | Số Lượng Thu Thập | Trạng Thái Lưu Trữ |
|---|---|---|
| **Sản phẩm (Products)** | {metrics['entities']['products']} | SQLite + `products.json` + `products.csv` |
| **Danh mục (Categories)** | {metrics['entities']['categories']} | SQLite + `categories.json` + `categories.csv` |
| **Thương hiệu (Brands)** | {metrics['entities']['brands']} | SQLite + `brands.json` |
| **Bài viết / Blog (Articles)** | {metrics['entities']['articles']} | SQLite + `articles.json` |
| **Tài nguyên ảnh (Assets)** | {metrics['entities']['assets']} | SQLite + Phân loại `data/assets/` + Hash SHA256 |

## 3. Kiểm Định Dữ Liệu & Tính Toàn Vẹn (Data Integrity Audit)
- Sản phẩm thiếu giá: **{metrics['anomalies']['products_missing_price']}**
- Sản phẩm thiếu SKU: **{metrics['anomalies']['products_missing_sku']}**
- Sản phẩm thiếu ảnh chính: **{metrics['anomalies']['products_missing_image']}**
- SKU trùng lặp (Duplicate SKUs): **{metrics['anomalies']['duplicate_skus_count']}**
- Tên sản phẩm trùng lặp: **{metrics['anomalies']['duplicate_names_count']}**
- Ảnh trùng hash SHA256 được tái sử dụng: **{metrics['anomalies']['duplicate_assets_sha256_count']}**
- Tài nguyên chưa tải được hoặc lỗi: **{metrics['anomalies']['unresolved_missing_assets']}**

## 4. Chi Tiết Lỗi Trích Xuất (Error Analysis)
```json
{json.dumps(metrics['errors_summary'], ensure_ascii=False, indent=2)}
```
"""
        report_md_path.write_text(report_content, encoding="utf-8")
        exported_files["crawl_report_md"] = str(report_md_path)

        # 7. Generate research/product_catalog.md
        catalog_md_path = self.research_dir / "product_catalog.md"
        cat_lines = ["# Danh Mục Sản Phẩm Đã Khảo Sát (Product Catalog Research)\n\n"]
        cat_lines.append("| Tên Sản Phẩm | Giá Bán (VND) | SKU | Xuất Xứ | Nồng Độ | Niên Vụ | URL Nguồn |\n")
        cat_lines.append("|---|---|---|---|---|---|---|\n")
        for p in products_list[:100]:  # Up to top 100 in markdown table
            price_str = f"{p['sale_price']:,.0f}" if p.get("sale_price") else "Liên hệ"
            cat_lines.append(f"| {p['name']} | {price_str} | {p.get('sku') or '—'} | {p.get('origin_country') or '—'} | {p.get('abv') or '—'} | {p.get('vintage') or '—'} | [{p['slug']}]({p['source_url']}) |\n")
        catalog_md_path.write_text("".join(cat_lines), encoding="utf-8")
        exported_files["product_catalog_md"] = str(catalog_md_path)

        # 8. Generate research/content_inventory.md
        inv_md_path = self.research_dir / "content_inventory.md"
        inv_content = f"""# Bản Đồ Nội Dung Website (Content Inventory & Structure)

## Phân Bổ Nội Dung Đã Khảo Sát
- **Sản phẩm rượu vang**: {metrics['entities']['products']} mặt hàng.
- **Danh mục phân cấp**: {metrics['entities']['categories']} danh mục (Vang đỏ, Vang trắng, Vang nổ/Champagne, Vang ngọt, Phụ kiện...).
- **Thương hiệu & Nhà sản xuất**: {metrics['entities']['brands']} thương hiệu.
- **Bài viết chuyên môn & Kiến thức**: {metrics['entities']['articles']} bài viết.

## Cấu Trúc Điều Hướng (Navigation Architecture)
- **Header**: Logo, Tìm kiếm sản phẩm, Danh mục chính (Rượu vang theo quốc gia, theo giống nho, theo mức giá), Về chúng tôi, Liên hệ, Giỏ hàng.
- **Footer**: Thông tin công ty, Giấy phép kinh doanh rượu, Địa chỉ showroom, Hotline, Chính sách đổi trả & giao hàng, Cảnh báo độ tuổi (18+).
"""
        inv_md_path.write_text(inv_content, encoding="utf-8")
        exported_files["content_inventory_md"] = str(inv_md_path)

        return exported_files
