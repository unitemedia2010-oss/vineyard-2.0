# VINEYARD 2.0 - E-Commerce Intelligence, Data Extraction & Modernization

## 🍷 Tổng Quan Dự Án
VINEYARD 2.0 là hệ sinh thái công cụ toàn diện nhằm khảo sát, phân tích kiến trúc, trích xuất dữ liệu có cấu trúc công khai từ `https://vineyard.vn/` và chuẩn bị nền tảng chuyển dịch lên kiến trúc Headless E-Commerce hiện đại (Next.js 15, TypeScript, Tailwind CSS, Framer Motion/GSAP).

Dự án tuân thủ nghiêm ngặt nguyên tắc:
- **Local-first**: Chạy hoàn toàn trên máy cục bộ, không phụ thuộc cloud trả phí.
- **Ethical & Compliant**: Tôn trọng `robots.txt`, rate limit, không bypass CAPTCHA hay truy cập dữ liệu riêng tư.
- **High Integrity**: Không suy đoán hoặc giả lập dữ liệu; lưu trữ provenance, HTTP status, timestamp, SHA256 assets.
- **Zero Loss / Deduplication**: Lưu cả raw HTML/JSON snapshot và normalized records vào SQLite; nhận diện ảnh trùng lặp qua hash SHA256.

---

## 📁 Cấu Trúc Dự Án
```
VINEYARD-2.0/
├── crawler/                # Core Python Crawler, Engine, Pipelines & Extractors
│   ├── __init__.py
│   ├── config.py           # Centralized configuration & environment loader
│   ├── client.py           # HTTP client with rate-limiting, backoff, retry
│   ├── discovery.py        # Sitemap, robots.txt, canonical & URL frontier discovery
│   ├── extractors/         # Domain-specific extractors (product, category, brand, article, visual)
│   ├── pipeline.py         # Pipeline orchestrator: Fetch -> Extract -> Validate -> Store
│   ├── assets.py           # Asset downloader, MIME detector, SHA256 hasher & dedup
│   ├── visual.py           # Playwright automation for multi-viewport screenshots & visual audit
│   ├── storage.py          # SQLite database schema, operations & checkpoints
│   ├── validator.py        # Data verification, cross-referencing & completeness checks
│   └── exporter.py         # JSON, CSV, and markdown export engine
├── data/
│   ├── raw/                # Unaltered raw HTTP response snapshots & JSON-LD
│   ├── normalized/         # Normalized clean JSON dumps
│   ├── database/           # SQLite database (vineyard.db)
│   ├── assets/             # Deduped media categorized by type
│   │   ├── products/
│   │   ├── banners/
│   │   ├── brands/
│   │   ├── articles/
│   │   ├── icons/
│   │   └── misc/
│   ├── screenshots/        # Multi-viewport screenshots (1440px, 768px, 390px)
│   └── reports/            # Crawl reports, gap analysis, coverage matrix
├── research/               # Deep architecture audit & design system specifications
│   ├── sitemap.md
│   ├── product_catalog.md
│   ├── content_inventory.md
│   ├── design_system.md
│   ├── ui_ux_audit.md
│   ├── animation_audit.md
│   └── redesign_strategy.md
├── docs/                   # Technical schemas, crawler guide & acceptance tests
│   ├── DATA_SCHEMA.md
│   ├── CRAWLER_GUIDE.md
│   └── ACCEPTANCE_TESTS.md
├── website/                # Modern Next.js 15 + TypeScript + Tailwind CSS Frontend Rebuild
└── tests/                  # Offline test suites & fixtures
```

---

## 🚀 Hướng Dẫn Cài Đặt & Vận Hành

### 1. Yêu cầu hệ thống
- **OS**: Windows 10/11, macOS hoặc Linux
- **Python**: 3.12+
- **Node.js**: v20+ & pnpm/npm
- **Playwright Chromium**: Hỗ trợ chụp màn hình và render dynamic page

### 2. Thiết lập môi trường ảo (Virtualenv)

#### Trên Windows (PowerShell):
```powershell
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1

# Cài đặt dependencies
pip install -r requirements.txt
playwright install chromium
```

#### Trên macOS / Linux (Bash/Zsh):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### 3. Cấu hình (.env)
Sao chép `.env.example` thành `.env` và điều chỉnh thông số nếu cần:
```bash
cp .env.example .env
```

### 4. Lệnh Vận Hành CLI Crawler (`crawler/cli.py`)
```powershell
# 1. Khảo sát sơ bộ (Discovery: robots.txt, sitemaps, URL classification)
python -m crawler.cli --discover-only

# 2. Thu thập thử nghiệm giới hạn (VD: 5 trang để verify extractor)
python -m crawler.cli --limit 5

# 3. Tiếp tục thu thập từ checkpoint trước đó
python -m crawler.cli --resume

# 4. Thu thập toàn bộ nội dung được phép
python -m crawler.cli --full

# 5. Chụp màn hình đa thiết bị (Desktop 1440px, Tablet 768px, Mobile 390px)
python -m crawler.cli --screenshot

# 6. Kiểm định tính toàn vẹn và đối chiếu dữ liệu
python -m crawler.cli --validate

# 7. Xuất dữ liệu ra JSON, CSV và Markdown reports
python -m crawler.cli --export
```

### 5. Chạy Test Suite Offline
```powershell
pytest tests/
```
