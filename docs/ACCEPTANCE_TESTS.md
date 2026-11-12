# BẢNG TIÊU CHÍ NGHIỆM THU DỰ ÁN (ACCEPTANCE TESTS)

| STT | Hạng Mục Nghiệm Thu | Tiêu Chí Đánh Giá | Kết Quả Thực Tế | Trạng Thái |
|---|---|---|---|---|
| **1** | **Khởi Chạy Local-First** | Toàn bộ hệ thống chạy độc lập trên máy cục bộ, không gọi API tính phí ngoài | Chạy 100% trên Python 3.12, SQLite, Node 22, Playwright nội bộ | **ĐẠT (PASS)** |
| **2** | **Tuân Thủ Robots & Chính Sách** | Kiểm tra robots.txt, rate limiting, không bypass CAPTCHA/paywall | Đã phân tích robots.txt (0 rules cấm), áp dụng rate limit 1.5s/req | **ĐẠT (PASS)** |
| **3** | **Không Suy Đoán / Bịa Dữ Liệu** | Không tự gán giá, SKU, xuất xứ; giữ null nếu trang không cung cấp | Trường giá "Liên hệ" giữ `null`, SKU và thông số trích xuất chính xác từ DOM | **ĐẠT (PASS)** |
| **4** | **Bảo Toàn Provenance & Snapshot** | Mỗi bản ghi lưu source_url, timestamp, HTTP status, và raw HTML snapshot | Bảng `pages` và `products` lưu đầy đủ source_url, crawl_timestamp, file snapshot trong `data/raw/` | **ĐẠT (PASS)** |
| **5** | **Khử Trùng Lặp Ảnh Bằng SHA256** | Tài nguyên ảnh được băm SHA256, không tải lại file đã có hash trùng | Triển khai `AssetManager` với bảng `assets(sha256 UNIQUE)` | **ĐẠT (PASS)** |
| **6** | **Khả Năng Phục Hồi (Resume)** | Hỗ trợ tạm dừng và tiếp tục không mất dữ liệu đã crawl | Cơ chế checkpoint qua trạng thái `pending`/`success`/`failed` trong SQLite | **ĐẠT (PASS)** |
| **7** | **Visual Audit Đa Viewport** | Chụp screenshot chuẩn tại Desktop (1440), Tablet (768), Mobile (390) | Chụp thành công và xuất vào `data/screenshots/{desktop,tablet,mobile}/` | **ĐẠT (PASS)** |
| **8** | **Test Suite Tự Động** | Kiểm thử URL normalization, deduplication, extractor, SQLite và exporter | 5/5 bài kiểm thử tự động pytest đạt 100% | **ĐẠT (PASS)** |
| **9** | **Xuất Dữ Liệu Đa Định Dạng** | Có tệp SQLite .db, JSON chuẩn hóa, CSV và báo cáo Markdown | Đã tạo đầy đủ trong `data/normalized/`, `data/database/`, `data/reports/` | **ĐẠT (PASS)** |
| **10**| **Kế Hoạch Tái Thiết Next.js** | Kiến trúc frontend component-driven hiện đại chuẩn bị cho giai đoạn tiếp theo | Đã cấu hình và thiết lập thư viện mã nguồn Next.js + TS + Tailwind | **ĐẠT (PASS)** |
