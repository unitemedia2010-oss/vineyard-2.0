"""
Category & Collection Extractor
"""
import re
from typing import Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from crawler.models import CategoryRecord
from crawler.discovery import DiscoveryEngine

class CategoryExtractor:
    @classmethod
    def extract(cls, html: str, url: str) -> Optional[CategoryRecord]:
        soup = BeautifulSoup(html, "html.parser")

        # Category name
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

        # Category description
        description = None
        desc_elem = soup.find(class_=re.compile(r"category-description|cat-desc|collection-desc", re.I))
        if desc_elem:
            description = desc_elem.get_text(strip=True)

        # Count visible products in listing
        product_items = soup.find_all(class_=re.compile(r"product-item|product-card|pro-item|col-item", re.I))
        product_count = len(product_items) if product_items else None

        return CategoryRecord(
            source_url=url,
            slug=slug,
            name=name,
            description=description,
            product_count=product_count
        )
