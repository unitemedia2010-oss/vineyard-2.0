"""
Discovery Engine: Robots.txt, Sitemap Parser, URL Normalizer, CMS Detector & Frontier
"""
import re
import logging
from typing import List, Set, Dict, Any, Optional, Tuple
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from crawler.config import config
from crawler.client import HttpClient
from crawler.models import PageType, PageRecord

logger = logging.getLogger("crawler.discovery")

# Query parameters to strip for canonical normalization
STRIP_QUERY_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "ref", "source", "v", "_ga", "_gl", "token"
}

class DiscoveryEngine:
    def __init__(self, client: Optional[HttpClient] = None):
        self.client = client or HttpClient()
        self.robots_disallowed: List[str] = []
        self.sitemap_urls: List[str] = []
        self.discovered_urls: Set[str] = set()

    @staticmethod
    def normalize_url(raw_url: str, base_url: str = "https://vineyard.vn") -> Optional[str]:
        """
        Normalize URL:
        - Resolve relative URLs
        - Standardize scheme to https
        - Normalize host (vineyard.vn)
        - Clean trailing slashes consistently (except root)
        - Remove tracking & filter loop query parameters
        - Strip anchors / fragments
        """
        if not raw_url or raw_url.startswith(("javascript:", "mailto:", "tel:", "#", "data:")):
            return None

        # Resolve relative
        full_url = urljoin(base_url, raw_url.strip())
        parsed = urlparse(full_url)

        # Domain check
        netloc = parsed.netloc.lower()
        if not any(netloc == d or netloc.endswith("." + d) for d in config.allowed_domains):
            return None

        # Clean scheme
        scheme = "https"

        # Clean path
        path = parsed.path
        if not path:
            path = "/"
        elif path != "/" and path.endswith("/"):
            path = path.rstrip("/")

        # Clean query parameters
        query = ""
        if parsed.query:
            q_dict = parse_qs(parsed.query, keep_blank_values=False)
            filtered_q = {k: v for k, v in q_dict.items() if k.lower() not in STRIP_QUERY_PARAMS}
            if filtered_q:
                # Sort query keys for canonical stability
                sorted_pairs = []
                for k in sorted(filtered_q.keys()):
                    for val in sorted(filtered_q[k]):
                        sorted_pairs.append((k, val))
                query = urlencode(sorted_pairs)

        clean_url = urlunparse((scheme, netloc, path, "", query, ""))
        return clean_url

    def classify_url(self, url: str) -> PageType:
        """
        Classify URL type based on exact URL path structure of vineyard.vn.
        """
        parsed = urlparse(url)
        path = parsed.path.lower()

        if path in ("", "/"):
            return PageType.HOMEPAGE

        # Specific path prefixes
        if "/san-pham/" in path:
            return PageType.PRODUCT

        if "/danh-muc/" in path:
            return PageType.CATEGORY

        if any(p in path for p in ["/thuong-hieu/", "/brand/", "/nha-san-xuat/"]):
            return PageType.BRAND

        if any(p in path for p in ["/post/", "/tin-tuc/", "/bai-viet/", "/kien-thuc/", "/event/"]):
            return PageType.ARTICLE

        if any(p in path for p in ["/lien-he", "/contact"]):
            return PageType.CONTACT

        if any(p in path for p in ["/page/", "/gioi-thieu", "/about", "/chinh-sach", "/dieu-khoan", "/dia-chi"]):
            return PageType.INFORMATIONAL

        return PageType.OTHER

    def fetch_robots_txt(self) -> Dict[str, Any]:
        """Fetch and parse robots.txt for disallowed paths and sitemaps."""
        robots_url = f"{config.base_url}/robots.txt"
        logger.info(f"Checking robots.txt at {robots_url}")
        resp, _, err = self.client.fetch(robots_url)

        result = {
            "url": robots_url,
            "status_code": resp.status_code if resp else None,
            "disallowed": [],
            "sitemaps": [],
            "raw_text": resp.text if resp else ""
        }

        if resp and resp.status_code == 200:
            lines = resp.text.splitlines()
            current_applies = False
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.lower().startswith("user-agent:"):
                    agent = line.split(":", 1)[1].strip()
                    current_applies = agent in ("*", "VineyardAuditBot", "Mozilla/5.0")

                elif line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if current_applies and path:
                        result["disallowed"].append(path)
                        self.robots_disallowed.append(path)

                elif line.lower().startswith("sitemap:"):
                    sitemap_url = line.split(":", 1)[1].strip()
                    if sitemap_url:
                        result["sitemaps"].append(sitemap_url)
                        self.sitemap_urls.append(sitemap_url)

        # Fallback sitemaps if not declared in robots.txt
        if not self.sitemap_urls:
            self.sitemap_urls = [
                f"{config.base_url}/sitemap.xml",
                f"{config.base_url}/sitemap_index.xml",
                f"{config.base_url}/product-sitemap.xml"
            ]

        logger.info(f"Robots.txt parsed: {len(result['disallowed'])} rules, {len(self.sitemap_urls)} candidate sitemaps")
        return result

    def is_url_allowed_by_robots(self, url: str) -> bool:
        """Check if URL is prohibited by robots.txt disallow rules."""
        parsed = urlparse(url)
        path = parsed.path
        for dis in self.robots_disallowed:
            if dis and path.startswith(dis):
                return False
        return True

    def parse_sitemaps(self) -> List[str]:
        """
        Recursively discover and parse sitemaps, handling sitemap index files.
        Returns list of all discovered URLs.
        """
        discovered: Set[str] = set()
        queue = list(self.sitemap_urls)
        visited_sitemaps = set()

        while queue:
            sitemap_url = queue.pop(0)
            if sitemap_url in visited_sitemaps:
                continue
            visited_sitemaps.add(sitemap_url)

            logger.info(f"Inspecting sitemap: {sitemap_url}")
            resp, _, err = self.client.fetch(sitemap_url)
            if not resp or resp.status_code != 200:
                logger.debug(f"Sitemap {sitemap_url} returned {resp.status_code if resp else err}")
                continue

            try:
                # Handle XML namespace
                root = ET.fromstring(resp.content)
                # Check for sitemap index
                sub_sitemaps = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap")
                if sub_sitemaps:
                    for sm in sub_sitemaps:
                        loc = sm.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                        if loc is not None and loc.text:
                            clean_sm = loc.text.strip()
                            if clean_sm not in visited_sitemaps:
                                queue.append(clean_sm)
                                logger.info(f"Discovered nested sitemap: {clean_sm}")
                    continue

                # Parse URL locs
                urls = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
                for u in urls:
                    loc = u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    if loc is not None and loc.text:
                        clean_url = self.normalize_url(loc.text)
                        if clean_url and self.is_url_allowed_by_robots(clean_url):
                            discovered.add(clean_url)

            except ET.ParseError as e:
                logger.warning(f"XML parse error for sitemap {sitemap_url}: {e}")

        logger.info(f"Sitemap discovery found {len(discovered)} valid URLs.")
        return sorted(list(discovered))

    def detect_cms_and_platform(self, html: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Identify CMS, frontend framework, and backend platform based on concrete DOM/Header evidence.
        No speculation allowed.
        """
        evidence = []
        platform = "Custom / Unknown"

        soup = BeautifulSoup(html, "html.parser")

        # 1. Inspect HTTP Headers
        server = headers.get("server", "").lower()
        powered_by = headers.get("x-powered-by", "").lower()
        if server:
            evidence.append(f"Header 'Server': {server}")
        if powered_by:
            evidence.append(f"Header 'X-Powered-By': {powered_by}")

        # 2. Inspect Meta Generator
        meta_gen = soup.find("meta", attrs={"name": "generator"})
        if meta_gen and meta_gen.get("content"):
            gen_content = meta_gen.get("content")
            evidence.append(f"Meta Generator: {gen_content}")
            if "wordpress" in gen_content.lower():
                platform = "WordPress"
            elif "haravan" in gen_content.lower():
                platform = "Haravan"
            elif "shopify" in gen_content.lower():
                platform = "Shopify"
            elif "sapo" in gen_content.lower():
                platform = "Sapo"

        # 3. Inspect Scripts, Stylesheets, Asset paths
        scripts = [s.get("src", "") for s in soup.find_all("script") if s.get("src")]
        links = [l.get("href", "") for l in soup.find_all("link") if l.get("href")]

        all_assets = " ".join(scripts + links)

        if "wp-content" in all_assets or "wp-includes" in all_assets:
            platform = "WordPress / WooCommerce" if platform == "Custom / Unknown" else platform
            evidence.append("Asset path contains 'wp-content' or 'wp-includes'")
            if "woocommerce" in all_assets:
                evidence.append("WooCommerce asset detected")

        if "cdn.shopify.com" in all_assets or "shopify" in all_assets:
            platform = "Shopify"
            evidence.append("Shopify CDN detected in assets")

        if "haravan.com" in all_assets or "hstatic.net" in all_assets:
            platform = "Haravan"
            evidence.append("Haravan hstatic CDN detected")

        if "sapo.vn" in all_assets or "bizweb" in all_assets:
            platform = "Sapo / Bizweb"
            evidence.append("Sapo/Bizweb asset detected")

        # Frontend libraries
        if "next" in all_assets or soup.find(id="__next"):
            evidence.append("Next.js runtime detected")
        if "tailwind" in all_assets:
            evidence.append("Tailwind CSS utility classes/build detected")

        return {
            "platform": platform,
            "evidence": evidence
        }

    def extract_internal_links(self, html: str, current_url: str) -> List[Tuple[str, PageType]]:
        """Extract and normalize all internal links from HTML page."""
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for a in soup.find_all("a", href=True):
            clean = self.normalize_url(a["href"], current_url)
            if clean and self.is_url_allowed_by_robots(clean):
                ptype = self.classify_url(clean)
                results.append((clean, ptype))
        return results
