"""
Command Line Interface (CLI) for VINEYARD 2.0 Engine
"""
import argparse
import sys
import logging
import json
from rich.console import Console
from rich.table import Table
from crawler.config import config
from crawler.storage import Database
from crawler.client import HttpClient
from crawler.discovery import DiscoveryEngine
from crawler.pipeline import CrawlPipeline
from crawler.visual import VisualAuditor
from crawler.validator import DataValidator
from crawler.exporter import Exporter
from crawler.models import PageType

console = Console()
logger = logging.getLogger("crawler.cli")

def run_discovery(db: Database) -> None:
    console.print("\n[bold cyan]🔍 BẮT ĐẦU KHẢO SÁT HỆ THỐNG (DISCOVERY STAGE)...[/bold cyan]")
    client = HttpClient()
    discovery = DiscoveryEngine(client)

    # 1. Fetch robots.txt
    robots_data = discovery.fetch_robots_txt()
    console.print(f"[green]✓ Đã kiểm tra robots.txt:[/green] {len(robots_data['disallowed'])} luật disallow, {len(robots_data['sitemaps'])} sitemaps phát hiện.")

    # 2. Fetch homepage to inspect CMS and Headers
    console.print(f"[cyan]Đang kiểm tra trang chủ ({config.base_url})...[/cyan]")
    resp, elapsed, err = client.fetch(config.base_url)
    if resp and resp.status_code == 200:
        db.save_page_discovery(config.base_url, PageType.HOMEPAGE)
        cms_info = discovery.detect_cms_and_platform(resp.text, dict(resp.headers))
        console.print(f"[bold green]✓ Nền tảng phát hiện:[/bold green] {cms_info['platform']}")
        for ev in cms_info["evidence"]:
            console.print(f"  - Bằng chứng: {ev}")

        # Extract initial links from homepage
        links = discovery.extract_internal_links(resp.text, config.base_url)
        for url, ptype in links:
            db.save_page_discovery(url, ptype)
        console.print(f"[green]✓ Đã tìm thấy {len(links)} liên kết nội bộ từ trang chủ.[/green]")
    else:
        console.print(f"[bold red]✗ Không thể truy cập trang chủ: {err}[/bold red]")

    # 3. Parse XML Sitemaps
    console.print("[cyan]Đang phân tích các sitemap.xml...[/cyan]")
    sitemap_urls = discovery.parse_sitemaps()
    added_count = 0
    for u in sitemap_urls:
        ptype = discovery.classify_url(u)
        if db.save_page_discovery(u, ptype):
            added_count += 1
    console.print(f"[bold green]✓ Hoàn tất Discovery: Đã nạp {added_count} URL mới vào hàng đợi cơ sở dữ liệu.[/bold green]")

    stats = db.get_stats()
    table = Table(title="Tổng Hợp Kho URL Đã Khảo Sát")
    table.add_column("Mục", style="cyan")
    table.add_column("Số Lượng", style="magenta")
    table.add_row("Tổng số URL trong hệ thống", str(stats["pages_total"]))
    table.add_row("URL chờ xử lý", str(stats["pages_pending"]))
    console.print(table)

def run_crawl(db: Database, limit: int = None, resume: bool = False) -> None:
    console.print(f"\n[bold green]🚀 BẮT ĐẦU CRAWL & TRÍCH XUẤT DỮ LIỆU (Giới hạn: {limit or 'Không giới hạn'}, Tiếp tục: {resume})...[/bold green]")
    pipeline = CrawlPipeline(db)
    pipeline.run(limit=limit)
    console.print("[bold green]✓ Tiến trình crawl đã hoàn tất thành công.[/bold green]")

def run_visual_audit(db: Database, limit: int = 3) -> None:
    console.print("\n[bold magenta]📸 BẮT ĐẦU CHỤP MÀN HÌNH ĐA THIẾT BỊ & AUDIT THỊ GIÁC...[/bold magenta]")
    auditor = VisualAuditor()

    # Chụp trang chủ và một số trang đại diện
    urls_to_audit = [config.base_url]

    with db.get_connection() as conn:
        # Lấy 1 category
        cat = conn.execute("SELECT url FROM pages WHERE page_type = 'category' AND http_status = 200 LIMIT 1").fetchone()
        if cat:
            urls_to_audit.append(cat[0])
        # Lấy 1 product
        prod = conn.execute("SELECT source_url FROM products LIMIT 1").fetchone()
        if prod:
            urls_to_audit.append(prod[0])

    for target_url in urls_to_audit[:limit]:
        console.print(f"[cyan]Đang chụp & audit:[/cyan] {target_url}")
        res = auditor.audit_page(target_url, capture_screenshots=True)
        console.print(f"[green]✓ Đã chụp xong {target_url}[/green]")
        if res.get("typography", {}).get("body"):
            console.print(f"  - Font Body: {res['typography']['body'].get('fontFamily')}")
            console.print(f"  - Màu sắc đại diện: {res['colors'].get('palette', [])[:5]}")

def run_validation(db: Database) -> None:
    console.print("\n[bold yellow]⚖️ TIẾN HÀNH KIỂM ĐỊNH TÍNH TOÀN VẸN VÀ ĐỐI CHIẾU DỮ LIỆU...[/bold yellow]")
    validator = DataValidator(db)
    metrics = validator.run_full_validation()

    table = Table(title="Kết Quả Kiểm Định Tính Toàn Vẹn")
    table.add_column("Chỉ Số", style="cyan")
    table.add_column("Giá Trị", style="green")

    table.add_row("Tổng URL khảo sát", str(metrics["funnel"]["discovered"]))
    table.add_row("URL tải thành công", str(metrics["funnel"]["success"]))
    table.add_row("URL lỗi", str(metrics["funnel"]["failed"]))
    table.add_row("Tỷ lệ hoàn thành (Completeness)", f"{metrics['funnel']['completeness_rate_percent']}%")
    table.add_row("Sản phẩm đã trích xuất", str(metrics["entities"]["products"]))
    table.add_row("Danh mục", str(metrics["entities"]["categories"]))
    table.add_row("Thương hiệu", str(metrics["entities"]["brands"]))
    table.add_row("Bài viết", str(metrics["entities"]["articles"]))
    table.add_row("Tài nguyên ảnh (Assets)", str(metrics["entities"]["assets"]))
    table.add_row("Sản phẩm thiếu giá", str(metrics["anomalies"]["products_missing_price"]))
    table.add_row("Sản phẩm thiếu SKU", str(metrics["anomalies"]["products_missing_sku"]))
    table.add_row("SKU trùng lặp", str(metrics["anomalies"]["duplicate_skus_count"]))
    console.print(table)

def run_export(db: Database) -> None:
    console.print("\n[bold blue]📦 TIẾN HÀNH XUẤT DỮ LIỆU RA JSON, CSV VÀ BÁO CÁO...[/bold blue]")
    exporter = Exporter(db)
    files = exporter.export_all()
    for name, path in files.items():
        console.print(f"  [green]✓ {name}:[/green] {path}")
    console.print("[bold green]✓ Toàn bộ dữ liệu đã được xuất hoàn tất.[/bold green]")

def main():
    parser = argparse.ArgumentParser(description="VINEYARD 2.0 Web Crawler & Modernization Suite")
    parser.add_argument("--discover-only", action="store_true", help="Chỉ khảo sát robots.txt, sitemaps và cấu trúc trang")
    parser.add_argument("--limit", type=int, default=None, help="Giới hạn số lượng URL cần crawl")
    parser.add_argument("--resume", action="store_true", help="Tiếp tục crawl từ hàng đợi chưa hoàn thành")
    parser.add_argument("--full", action="store_true", help="Crawl toàn bộ danh sách URL được phép")
    parser.add_argument("--screenshot", action="store_true", help="Chụp màn hình đa thiết bị và audit thiết kế")
    parser.add_argument("--validate", action="store_true", help="Kiểm tra đối chiếu và tính toàn vẹn dữ liệu")
    parser.add_argument("--export", action="store_true", help="Xuất normalized data ra JSON/CSV/Markdown")
    parser.add_argument("--report", action="store_true", help="Tạo báo cáo tổng kết hoàn chỉnh")

    args = parser.parse_args()
    config.ensure_directories()
    db = Database()

    if args.discover_only:
        run_discovery(db)
    elif args.screenshot:
        run_visual_audit(db)
    elif args.validate:
        run_validation(db)
    elif args.export or args.report:
        run_export(db)
    elif args.full:
        run_discovery(db)
        run_crawl(db, limit=None)
        run_visual_audit(db)
        run_validation(db)
        run_export(db)
    elif args.limit or args.resume:
        run_crawl(db, limit=args.limit, resume=args.resume)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
