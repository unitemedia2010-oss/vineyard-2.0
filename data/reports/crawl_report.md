# Báo Cáo Thu Thập Dữ Liệu VINEYARD 2.0 (Crawl Report)

## 1. Phễu Thu Thập (Pipeline Funnel)
- **Tổng URL Đã Khảo Sát (Discovered)**: 346
- **Tổng URL Đã Tải (Fetched)**: 55
- **Trích Xuất Thành Công (Success)**: 55
- **Trích Xuất Thất Bại (Failed)**: 0
- **Đang Chờ Xử Lý (Pending)**: 291
- **Tỷ Lệ Hoàn Thành (Completeness Rate)**: 15.9%

## 2. Thống Kê Thực Thể (Extracted Entities)
| Thực Thể | Số Lượng Thu Thập | Trạng Thái Lưu Trữ |
|---|---|---|
| **Sản phẩm (Products)** | 36 | SQLite + `products.json` + `products.csv` |
| **Danh mục (Categories)** | 6 | SQLite + `categories.json` + `categories.csv` |
| **Thương hiệu (Brands)** | 0 | SQLite + `brands.json` |
| **Bài viết / Blog (Articles)** | 3 | SQLite + `articles.json` |
| **Tài nguyên ảnh (Assets)** | 57 | SQLite + Phân loại `data/assets/` + Hash SHA256 |

## 3. Kiểm Định Dữ Liệu & Tính Toàn Vẹn (Data Integrity Audit)
- Sản phẩm thiếu giá: **36**
- Sản phẩm thiếu SKU: **1**
- Sản phẩm thiếu ảnh chính: **0**
- SKU trùng lặp (Duplicate SKUs): **0**
- Tên sản phẩm trùng lặp: **0**
- Ảnh trùng hash SHA256 được tái sử dụng: **0**
- Tài nguyên chưa tải được hoặc lỗi: **0**

## 4. Chi Tiết Lỗi Trích Xuất (Error Analysis)
```json
[]
```
