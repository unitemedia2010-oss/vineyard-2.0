"""
Wine & Spirit Product Extractor Tailored for VINEYARD.VN DOM
"""
import re
import logging
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from crawler.models import ProductRecord
from crawler.discovery import DiscoveryEngine

logger = logging.getLogger("crawler.extractors.product")

class ProductExtractor:
    @staticmethod
    def _clean_price(raw_text: Optional[str]) -> Optional[float]:
        if not raw_text or "liên hệ" in raw_text.lower():
            return None
        text = re.sub(r"[^\d]", "", raw_text)
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None

    @staticmethod
    def _extract_slug(url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        slug = path.split("/")[-1]
        slug = re.sub(r"\.(html|htm|php)$", "", slug)
        return slug or "unknown-product"

    @classmethod
    def extract(cls, html: str, url: str) -> Optional[ProductRecord]:
        soup = BeautifulSoup(html, "html.parser")
        infor_group = soup.find("div", class_="infor-group")

        # 1. Product Name
        name = None
        if infor_group:
            name_tag = infor_group.find(["h1", "h2"], class_="name")
            if name_tag and name_tag.get_text(strip=True):
                name = name_tag.get_text(strip=True)

        if not name:
            h1 = soup.find("h1")
            if h1 and h1.get_text(strip=True):
                name = h1.get_text(strip=True)

        if not name:
            title_tag = soup.find("title")
            if title_tag and title_tag.string:
                clean_t = title_tag.string.split("-")[0].split("|")[0].strip()
                if clean_t and "vineyard" not in clean_t.lower():
                    name = clean_t

        if not name:
            return None

        slug = cls._extract_slug(url)

        # 2. Brand
        brand = None
        if infor_group:
            brand_elem = infor_group.find("a", class_="brands-item")
            if brand_elem and brand_elem.get_text(strip=True) and brand_elem.get_text(strip=True) != "#":
                brand = brand_elem.get_text(strip=True)

        # 3. SKU
        sku = None
        if infor_group:
            model_p = infor_group.find("p", class_="model")
            if model_p:
                sku_txt = model_p.get_text(strip=True)
                sku_clean = re.sub(r"^(mã sản phẩm|mã sp|sku)\s*#?\s*[:：]?", "", sku_txt, flags=re.I).strip()
                if sku_clean:
                    sku = sku_clean

        # 4. Price & Stock
        sale_price = None
        original_price = None
        stock_status = "Còn trong kho"

        if infor_group:
            price_p = infor_group.find("p", class_="price")
            if price_p:
                price_txt = price_p.get_text(strip=True)
                sale_price = cls._clean_price(price_txt)

            stock_p = infor_group.find("p", class_="stock")
            if stock_p:
                stock_status = stock_p.get_text(strip=True)

        # 5. Extract Vine Specs from .product-ads-content
        specs: Dict[str, Any] = {}
        origin_country = None
        region = None
        grape_variety = None
        abv = None
        volume = None
        producer = None

        ads_content = soup.find("div", class_="product-ads-content")
        if ads_content:
            for col in ads_content.find_all(class_=re.compile(r"col-")):
                img = col.find("img")
                label = col.find(class_="label")
                if not label:
                    continue
                val = label.get_text(strip=True)
                attr_name = (img.get("alt") or img.get("title") or "").strip() if img else ""

                if not attr_name:
                    continue

                specs[attr_name] = val
                attr_lower = attr_name.lower()

                if "quốc gia" in attr_lower or "country" in attr_lower:
                    origin_country = val
                elif "vùng" in attr_lower or "region" in attr_lower:
                    region = val
                elif any(k in attr_lower for k in ["nho", "grape", "variety"]):
                    grape_variety = val
                elif any(k in attr_lower for k in ["nồng độ", "độ cồn", "abv"]):
                    abv = f"{val}%" if not val.endswith("%") else val
                elif any(k in attr_lower for k in ["dung tích", "thể tích", "volume"]):
                    volume = f"{val}L" if not val.lower().endswith(("l", "ml")) else val
                elif any(k in attr_lower for k in ["nhà sản xuất", "producer"]):
                    producer = val
                elif "thương hiệu" in attr_lower and not brand:
                    brand = val

        # 6. Vintage & Year detection
        vintage = None
        year_match = re.search(r"\b(19\d{2}|20[0-2]\d)\b", name)
        if year_match:
            vintage = year_match.group(1)

        # 7. Tasting notes & Description
        tasting_notes = None
        description = None

        content_divs = soup.find_all("div", class_="content")
        tasting_parts = []
        for c_div in content_divs:
            txt = c_div.get_text("\n", strip=True)
            if any(k in txt.lower() for k in ["màu:", "vị:", "hương:", "thưởng thức:", "kết hợp:"]):
                tasting_parts.append(txt)
            elif len(txt) > 50 and not any(k in txt.lower() for k in ["về chúng tôi", "điều khoản"]):
                description = txt

        if tasting_parts:
            tasting_notes = "\n\n".join(tasting_parts)

        # 8. Main image and Gallery
        main_image_url = None
        gallery_image_urls: List[str] = []

        # Find images inside SanPham directory
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if not src:
                continue
            if "sanpham" in src.lower() or "san-pham" in src.lower():
                clean_img = DiscoveryEngine.normalize_url(src, url)
                if clean_img and clean_img not in gallery_image_urls:
                    gallery_image_urls.append(clean_img)

        if gallery_image_urls:
            main_image_url = gallery_image_urls[0]

        # Category from breadcrumb or navigation
        category = None
        bc_nav = soup.find(class_=re.compile(r"breadcrumb|breadcrumbs", re.I))
        if bc_nav:
            crumbs = [a.get_text(strip=True) for a in bc_nav.find_all("a") if a.get_text(strip=True)]
            wine_cats = [c for c in crumbs if not re.search(r"trang chủ|home", c, re.I)]
            if wine_cats:
                category = " > ".join(wine_cats)

        return ProductRecord(
            source_url=url,
            canonical_url=DiscoveryEngine.normalize_url(url),
            name=name,
            slug=slug,
            sku=sku,
            brand=brand,
            category=category,
            origin_country=origin_country,
            region=region,
            producer=producer,
            vintage=vintage,
            grape_variety=grape_variety,
            volume=volume,
            abv=abv,
            original_price=original_price,
            sale_price=sale_price,
            currency="VND",
            stock_status=stock_status,
            description=description,
            tasting_notes=tasting_notes,
            specs=specs,
            main_image_url=main_image_url,
            gallery_image_urls=gallery_image_urls,
            extraction_source="vineyard_dom+meta",
            verification_level="verified"
        )
