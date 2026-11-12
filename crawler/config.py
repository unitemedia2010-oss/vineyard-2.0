"""
Centralized Configuration for VINEYARD 2.0 Crawler
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

# Base workspace directory
ROOT_DIR = Path(__file__).resolve().parent.parent

@dataclass
class CrawlerConfig:
    base_url: str = os.getenv("VINEYARD_BASE_URL", "https://vineyard.vn")
    user_agent: str = os.getenv(
        "VINEYARD_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 VineyardAudit/2.0"
    )
    concurrency: int = int(os.getenv("CRAWLER_CONCURRENCY", "2"))
    rate_limit_delay: float = float(os.getenv("CRAWLER_RATE_LIMIT_DELAY", "1.5"))
    timeout: float = float(os.getenv("CRAWLER_TIMEOUT", "30.0"))
    max_retries: int = int(os.getenv("CRAWLER_MAX_RETRIES", "3"))
    retry_backoff: float = float(os.getenv("CRAWLER_RETRY_BACKOFF", "2.0"))
    resume: bool = os.getenv("CRAWLER_RESUME", "true").lower() in ("true", "1", "yes")
    dry_run: bool = os.getenv("CRAWLER_DRY_RUN", "false").lower() in ("true", "1", "yes")
    cache_enabled: bool = os.getenv("CRAWLER_CACHE_ENABLED", "true").lower() in ("true", "1", "yes")

    # Directory Paths
    db_path: Path = field(default_factory=lambda: ROOT_DIR / "data" / "database" / "vineyard.db")
    raw_path: Path = field(default_factory=lambda: ROOT_DIR / "data" / "raw")
    normalized_path: Path = field(default_factory=lambda: ROOT_DIR / "data" / "normalized")
    assets_path: Path = field(default_factory=lambda: ROOT_DIR / "data" / "assets")
    screenshots_path: Path = field(default_factory=lambda: ROOT_DIR / "data" / "screenshots")
    reports_path: Path = field(default_factory=lambda: ROOT_DIR / "data" / "reports")
    research_path: Path = field(default_factory=lambda: ROOT_DIR / "research")
    docs_path: Path = field(default_factory=lambda: ROOT_DIR / "docs")

    # Viewport specifications for visual audits
    viewport_desktop: dict = field(default_factory=lambda: {"width": 1440, "height": 900})
    viewport_tablet: dict = field(default_factory=lambda: {"width": 768, "height": 1024})
    viewport_mobile: dict = field(default_factory=lambda: {"width": 390, "height": 844})

    # Allowed domains to restrict crawling strictly
    allowed_domains: List[str] = field(default_factory=lambda: ["vineyard.vn", "www.vineyard.vn"])

    def ensure_directories(self) -> None:
        """Create all required data and report directories."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.normalized_path.mkdir(parents=True, exist_ok=True)
        self.screenshots_path.mkdir(parents=True, exist_ok=True)
        self.reports_path.mkdir(parents=True, exist_ok=True)
        self.research_path.mkdir(parents=True, exist_ok=True)
        self.docs_path.mkdir(parents=True, exist_ok=True)

        for subdir in ["products", "banners", "brands", "articles", "icons", "misc"]:
            (self.assets_path / subdir).mkdir(parents=True, exist_ok=True)

        for vp in ["desktop", "tablet", "mobile"]:
            (self.screenshots_path / vp).mkdir(parents=True, exist_ok=True)

config = CrawlerConfig()
