"""
Asset Downloader, Deduplicator, and Metadata Engine
"""
import hashlib
import mimetypes
import logging
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse
from PIL import Image
import httpx
from crawler.config import config
from crawler.models import AssetRecord, AssetCategory
from crawler.storage import Database
from crawler.discovery import DiscoveryEngine

logger = logging.getLogger("crawler.assets")

class AssetManager:
    def __init__(self, db: Database, client: Optional[httpx.Client] = None):
        self.db = db
        self.client = client or httpx.Client(
            headers={"User-Agent": config.user_agent},
            timeout=config.timeout,
            follow_redirects=True,
            verify=False
        )
        self.known_hashes = set()
        self._load_known_hashes()

    def _load_known_hashes(self):
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT sha256 FROM assets WHERE sha256 IS NOT NULL").fetchall()
            for r in rows:
                self.known_hashes.add(r[0])

    def categorize_asset(self, url: str, source_category: Optional[AssetCategory] = None) -> AssetCategory:
        if source_category:
            return source_category

        u_lower = url.lower()
        if any(w in u_lower for w in ["product", "ruou-vang", "san-pham", "chai"]):
            return AssetCategory.PRODUCTS
        elif any(w in u_lower for w in ["banner", "slider", "slide", "hero"]):
            return AssetCategory.BANNERS
        elif any(w in u_lower for w in ["brand", "logo", "producer", "nha-san-xuat"]):
            return AssetCategory.BRANDS
        elif any(w in u_lower for w in ["article", "blog", "tin-tuc", "post", "news"]):
            return AssetCategory.ARTICLES
        elif any(w in u_lower for w in ["icon", "svg", "favicon", "badge"]):
            return AssetCategory.ICONS
        return AssetCategory.MISC

    def download_and_process(
        self,
        original_url: str,
        source_page_url: str,
        category: Optional[AssetCategory] = None
    ) -> Optional[AssetRecord]:
        """
        Download asset, compute SHA256, extract image dimensions, avoid duplicates, and save locally.
        """
        clean_url = DiscoveryEngine.normalize_url(original_url, source_page_url)
        if not clean_url:
            return None

        # Check if URL already saved in DB
        with self.db.get_connection() as conn:
            existing = conn.execute("SELECT * FROM assets WHERE original_url = ?", (clean_url,)).fetchone()
            if existing and existing["local_path"] and Path(existing["local_path"]).exists():
                return AssetRecord(
                    original_url=existing["original_url"],
                    source_page_url=existing["source_page_url"],
                    asset_category=AssetCategory(existing["asset_category"]),
                    local_path=existing["local_path"],
                    mime_type=existing["mime_type"],
                    file_size_bytes=existing["file_size_bytes"],
                    sha256=existing["sha256"],
                    width=existing["width"],
                    height=existing["height"],
                    status="cached"
                )

        # Enforce domain restriction
        parsed = urlparse(clean_url)
        netloc = parsed.netloc.lower()
        if not any(netloc == d or netloc.endswith("." + d) for d in config.allowed_domains + ["hstatic.net", "shopify.com"]):
            # Ignore 3rd party tracker pixels or social widgets
            return None

        cat = self.categorize_asset(clean_url, category)

        try:
            resp = self.client.get(clean_url)
            if resp.status_code != 200:
                logger.debug(f"Failed to download asset {clean_url}: HTTP {resp.status_code}")
                return None

            content = resp.content
            file_size = len(content)
            if file_size == 0:
                return None

            # SHA256 computation
            sha256_hash = hashlib.sha256(content).hexdigest()

            # Determine extension and mime type
            content_type = resp.headers.get("content-type", "").split(";")[0].strip()
            ext = mimetypes.guess_extension(content_type) or Path(parsed.path).suffix or ".jpg"
            if ext in (".jpe", ".jpeg"):
                ext = ".jpg"

            # Check if file with exact same content hash already exists
            sub_folder = config.assets_path / cat.value
            sub_folder.mkdir(parents=True, exist_ok=True)
            filename = f"{sha256_hash[:16]}{ext}"
            local_file = sub_folder / filename

            # Write file if not duplicate
            if not local_file.exists():
                local_file.write_bytes(content)

            # Extract image dimensions if image
            width, height = None, None
            try:
                with Image.open(local_file) as img:
                    width, height = img.size
                    if not content_type or content_type == "application/octet-stream":
                        content_type = img.get_format_mimetype() or content_type
            except Exception:
                pass

            record = AssetRecord(
                original_url=clean_url,
                source_page_url=source_page_url,
                asset_category=cat,
                local_path=str(local_file),
                mime_type=content_type,
                file_size_bytes=file_size,
                sha256=sha256_hash,
                width=width,
                height=height,
                status="downloaded" if sha256_hash not in self.known_hashes else "duplicate_hash"
            )

            self.known_hashes.add(sha256_hash)
            self.db.save_asset(record)
            return record

        except Exception as e:
            logger.warning(f"Error processing asset {clean_url}: {e}")
            self.db.record_error(clean_url, "asset_download", type(e).__name__, str(e))
            return None
