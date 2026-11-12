"""
Article / Editorial Extractor
"""
import re
from typing import Optional, List
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from crawler.models import ArticleRecord
from crawler.discovery import DiscoveryEngine

class ArticleExtractor:
    @classmethod
    def extract(cls, html: str, url: str) -> Optional[ArticleRecord]:
        soup = BeautifulSoup(html, "html.parser")

        title = None
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            title = h1.get_text(strip=True)
        if not title:
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                title = og_title["content"].strip()

        if not title:
            return None

        slug = urlparse(url).path.rstrip("/").split("/")[-1]

        # Author
        author = None
        author_elem = soup.find(class_=re.compile(r"author|post-author|article-author", re.I))
        if author_elem:
            author = author_elem.get_text(strip=True)

        # Publish Date
        publish_date = None
        date_elem = soup.find(["time", "span"], class_=re.compile(r"date|published|post-date", re.I))
        if date_elem:
            publish_date = date_elem.get("datetime") or date_elem.get_text(strip=True)

        # Content HTML and summary
        content_html = None
        content_container = soup.find(class_=re.compile(r"article-content|post-content|entry-content|blog-content", re.I))
        if content_container:
            content_html = str(content_container)

        summary = None
        desc_meta = soup.find("meta", attrs={"name": "description"})
        if desc_meta and desc_meta.get("content"):
            summary = desc_meta["content"].strip()

        # Featured image
        featured_image_url = None
        og_img = soup.find("meta", property="og:image")
        if og_img and og_img.get("content"):
            featured_image_url = DiscoveryEngine.normalize_url(og_img["content"], url)

        # Tags
        tags: List[str] = []
        tag_elems = soup.find_all("a", class_=re.compile(r"tag|post-tag", re.I))
        for t in tag_elems:
            txt = t.get_text(strip=True)
            if txt and txt not in tags:
                tags.append(txt)

        return ArticleRecord(
            source_url=url,
            slug=slug,
            title=title,
            author=author,
            publish_date=publish_date,
            summary=summary,
            content_html=content_html,
            featured_image_url=featured_image_url,
            tags=tags
        )
