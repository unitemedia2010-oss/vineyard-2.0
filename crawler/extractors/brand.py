"""
Brand / Producer Extractor
"""
import re
from typing import Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from crawler.models import BrandRecord
from crawler.discovery import DiscoveryEngine

class BrandExtractor:
    @classmethod
    def extract(cls, html: str, url: str) -> Optional[BrandRecord]:
        soup = BeautifulSoup(html, "html.parser")

        name = None
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            name = h1.get_text(strip=True)
        if not name:
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                name = og_title["content"].strip()
        if not name:
            title_tag = soup.find("title")
            if title_tag and title_tag.string:
                name = title_tag.string.split("-")[0].split("|")[0].strip()

        if not name:
            return None

        slug = urlparse(url).path.rstrip("/").split("/")[-1]

        # Brand description
        description = None
        desc_elem = soup.find(class_=re.compile(r"brand-desc|brand-content|description", re.I))
        if desc_elem:
            description = desc_elem.get_text(strip=True)

        # Brand Logo
        logo_url = None
        logo_tag = soup.find("img", class_=re.compile(r"brand-logo|producer-logo", re.I))
        if logo_tag:
            src = logo_tag.get("src") or logo_tag.get("data-src")
            if src:
                logo_url = DiscoveryEngine.normalize_url(src, url)

        # Country
        country = None
        country_elem = soup.find(string=re.compile(r"quốc gia|xuất xứ|country", re.I))
        if country_elem and country_elem.parent:
            match = re.search(r"[:：]\s*([^\n\r<|]+)", country_elem.parent.get_text())
            if match:
                country = match.group(1).strip()

        return BrandRecord(
            source_url=url,
            slug=slug,
            name=name,
            country=country,
            description=description,
            logo_url=logo_url
        )
