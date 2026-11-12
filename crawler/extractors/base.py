"""
Base Extractor for Page Metadata, OpenGraph, and JSON-LD
"""
import re
import json
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from crawler.models import PageMetadata

class BaseExtractor:
    @staticmethod
    def extract_metadata(html: str, url: str) -> PageMetadata:
        """Extract all standard SEO and semantic metadata from HTML document."""
        soup = BeautifulSoup(html, "html.parser")
        meta = PageMetadata()

        # 1. Document Title
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            meta.title = title_tag.string.strip()

        # 2. Meta Description
        desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if desc_tag and desc_tag.get("content"):
            meta.description = desc_tag.get("content").strip()

        # 3. Canonical Link
        canon_tag = soup.find("link", rel="canonical")
        if canon_tag and canon_tag.get("href"):
            meta.canonical = canon_tag.get("href").strip()

        # 4. OpenGraph Metadata
        for og_prop in ["og:title", "og:description", "og:image", "og:type"]:
            tag = soup.find("meta", property=og_prop)
            if tag and tag.get("content"):
                val = tag.get("content").strip()
                if og_prop == "og:title":
                    meta.og_title = val
                elif og_prop == "og:description":
                    meta.og_description = val
                elif og_prop == "og:image":
                    meta.og_image = val
                elif og_prop == "og:type":
                    meta.og_type = val

        # 5. Headings (H1, H2, H3)
        headings: Dict[str, List[str]] = {}
        for h_level in ["h1", "h2", "h3", "h4"]:
            tags = soup.find_all(h_level)
            text_list = [t.get_text(strip=True) for t in tags if t.get_text(strip=True)]
            if text_list:
                headings[h_level] = text_list
        meta.headings = headings

        # 6. Structured Data (JSON-LD)
        json_ld_list = []
        for script in soup.find_all("script", type="application/ld+json"):
            if script.string:
                try:
                    data = json.loads(script.string.strip())
                    if isinstance(data, list):
                        json_ld_list.extend(data)
                    elif isinstance(data, dict):
                        json_ld_list.append(data)
                except Exception:
                    pass
        meta.json_ld = json_ld_list

        # 7. Breadcrumbs
        breadcrumbs = []
        # Breadcrumb DOM containers common in e-commerce
        bc_container = soup.find(class_=re.compile(r"breadcrumb|breadcrumbs", re.I)) or soup.find("nav", attrs={"aria-label": "breadcrumb"})
        if bc_container:
            for item in bc_container.find_all(["li", "a", "span"]):
                text = item.get_text(strip=True)
                href = item.get("href") or (item.find("a").get("href") if item.find("a") else None)
                if text and text not in [b["label"] for b in breadcrumbs]:
                    breadcrumbs.append({"label": text, "url": href or ""})
        meta.breadcrumbs = breadcrumbs

        return meta
