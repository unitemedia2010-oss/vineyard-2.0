# VINEYARD 2.0 - DATA SCHEMA & ARCHITECTURE SPECIFICATION

## 1. Triết Lý Thiết Kế Dữ Liệu
Hệ thống lưu trữ của VINEYARD 2.0 tuân thủ mô hình **Dual-Layer Storage**:
1. **Raw Snapshot Layer (`data/raw/`)**: Giữ nguyên vẹn 100% HTML response từ máy chủ nguồn kèm timestamp và SHA256 để đảm bảo tính bất biến và truy xuất nguồn gốc (Provenance).
2. **Normalized Relational Layer (`data/database/vineyard.db`)**: Chuẩn hóa thành các bảng quan hệ trong SQLite, có ràng buộc khóa ngoại (`FOREIGN KEY`), khóa duy nhất (`UNIQUE`), chỉ mục (`INDEX`) và lưu trữ JSON specs linh hoạt.
3. **Asset Vault Layer (`data/assets/`)**: Lưu trữ hình ảnh và phương tiện truyền thông đã loại bỏ trùng lặp dựa trên băm mật mã SHA256.

---

## 2. Sơ Đồ Thực Thể Quan Hệ (Entity-Relationship Diagram)

```mermaid
erDiagram
    CRAWL_JOBS ||--o{ PAGES : tracks
    PAGES ||--o{ PRODUCTS : extracts
    PAGES ||--o{ CATEGORIES : extracts
    PAGES ||--o{ BRANDS : extracts
    PAGES ||--o{ ARTICLES : extracts
    PAGES ||--o{ EXTRACTION_ERRORS : logs
    PRODUCTS ||--o{ PRODUCT_CATEGORIES : classifies
    CATEGORIES ||--o{ PRODUCT_CATEGORIES : contains
    PRODUCTS ||--o{ PRODUCT_IMAGES : displays
    ASSETS ||--o{ PRODUCT_IMAGES : references

    CRAWL_JOBS {
        int id PK
        string job_type
        string status
        timestamp started_at
        timestamp finished_at
        int total_discovered
        int total_fetched
        int total_extracted
        string notes
    }

    PAGES {
        int id PK
        string url UK
        string canonical_url
        string page_type
        int http_status
        float response_time_ms
        string content_type
        string raw_html_path
        string extraction_status
        string error_message
        string title
        string meta_description
        json metadata_json
        timestamp discovered_at
        timestamp fetched_at
    }

    PRODUCTS {
        int id PK
        string source_url UK
        string canonical_url
        string name
        string slug
        string sku
        string brand
        string category
        string origin_country
        string region
        string producer
        string vintage
        string grape_variety
        string volume
        string abv
        float original_price
        float sale_price
        string currency
        string stock_status
        string description
        string tasting_notes
        json specs_json
        string main_image_url
        json gallery_json
        timestamp crawl_timestamp
        string extraction_source
        string verification_level
    }

    CATEGORIES {
        int id PK
        string source_url UK
        string slug
        string name
        string parent_category
        string description
        int product_count
        timestamp crawl_timestamp
    }

    BRANDS {
        int id PK
        string source_url UK
        string slug
        string name
        string country
        string description
        string logo_url
        timestamp crawl_timestamp
    }

    ASSETS {
        int id PK
        string original_url UK
        string source_page_url
        string asset_category
        string local_path
        string mime_type
        int file_size_bytes
        string sha256 UK
        int width
        int height
        timestamp download_timestamp
        string status
    }

    ARTICLES {
        int id PK
        string source_url UK
        string slug
        string title
        string author
        string publish_date
        string summary
        string content_html
        string featured_image_url
        json tags_json
        timestamp crawl_timestamp
    }
```

---

## 3. Đặc Tả Chi Tiết Các Trường (Fields Specification)

### Bảng `products` (Sản Phẩm Rượu Vang & Rượu Mạnh)
| Cột | Kiểu Dữ Liệu | Ràng Buộc | Ý Nghĩa / Nguồn Trích Xuất |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Khóa chính |
| `source_url` | `TEXT` | `UNIQUE NOT NULL` | URL trang sản phẩm gốc |
| `canonical_url` | `TEXT` | | Canonical URL chuẩn hóa |
| `name` | `TEXT` | `NOT NULL` | Tên đầy đủ của sản phẩm rượu |
| `slug` | `TEXT` | `NOT NULL` | URL slug thân thiện SEO |
| `sku` | `TEXT` | | Mã định danh quản lý kho hàng (`B06.GRATI.06`) |
| `brand` | `TEXT` | | Thương hiệu rượu (`Reputazione`, `Auswan Creek`...) |
| `category` | `TEXT` | | Phân cấp danh mục (VD: `Vang Đỏ > Vang Ý`) |
| `origin_country` | `TEXT` | | Quốc gia xuất xứ (`Ý`, `Pháp`, `Chile`, `Úc`...) |
| `region` | `TEXT` | | Vùng làm rượu vang (`Puglia`, `Bordeaux`, `Tuscany`...) |
| `producer` | `TEXT` | | Tên nhà làm rượu / Hãng sản xuất |
| `vintage` | `TEXT` | | Niên vụ thu hoạch nho (`2015`, `2018`, `2020`...) |
| `grape_variety` | `TEXT` | | Giống nho (`Primitivo`, `Cabernet Sauvignon`...) |
| `volume` | `TEXT` | | Dung tích đóng chai (`0.75L`, `3L`, `750ml`...) |
| `abv` | `TEXT` | | Nồng độ cồn (% ABV, VD: `19,0%`, `14.5%`) |
| `original_price`| `REAL` | | Giá niêm yết trước giảm giá (VND) |
| `sale_price` | `REAL` | | Giá bán thực tế (VND, `null` nếu "Liên hệ") |
| `currency` | `TEXT` | `DEFAULT 'VND'` | Đơn vị tiền tệ |
| `stock_status` | `TEXT` | | Tình trạng (`Còn trong kho`, `Hết hàng`, `Liên hệ`) |
| `description` | `TEXT` | | Mô tả tổng quan sản phẩm |
| `tasting_notes`| `TEXT` | | Ghi chú nếm thử (Màu sắc, hương thơm, vị vòm miệng) |
| `specs_json` | `TEXT` | | Thuộc tính mở rộng dạng JSON |
| `main_image_url`| `TEXT` | | URL ảnh đại diện chất lượng cao |
| `gallery_json` | `TEXT` | | Danh sách các ảnh chi tiết phụ |
| `crawl_timestamp`| `TIMESTAMP` | `NOT NULL` | Thời điểm thu thập theo chuẩn ISO 8601 UTC |
| `verification_level`| `TEXT` | `DEFAULT 'verified'` | Mức độ xác thực (`verified`, `partial`, `unverified`) |

---

## 4. Ánh Xạ Sang TypeScript Model Cho Next.js Frontend
```typescript
export interface WineProduct {
  id: number;
  sourceUrl: string;
  canonicalUrl?: string;
  name: string;
  slug: string;
  sku?: string;
  brand?: string;
  category?: string;
  originCountry?: string;
  region?: string;
  producer?: string;
  vintage?: string;
  grapeVariety?: string;
  volume?: string;
  abv?: string;
  originalPrice?: number;
  salePrice?: number;
  currency: string;
  stockStatus: "Còn trong kho" | "Hết hàng" | "Liên hệ";
  description?: string;
  tastingNotes?: string;
  specs: Record<string, string>;
  mainImageUrl?: string;
  galleryImageUrls: string[];
  crawlTimestamp: string;
  verificationLevel: "verified" | "partial" | "unverified";
}
```
