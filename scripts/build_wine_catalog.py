import sqlite3
import json
import os

conn = sqlite3.connect('data/database/vineyard.db')
c = conn.cursor()

c.execute("""
    SELECT id, name, canonical_url, sku, abv, origin_country, brand, region, vintage, grape_variety, tasting_notes, description, main_image_url
    FROM products
""")
products = c.fetchall()

# Map product URL to asset
c.execute("""
    SELECT source_page_url, original_url, local_path, sha256
    FROM assets
    WHERE asset_category = 'products'
""")
assets = c.fetchall()

url_to_assets = {}
for source_url, orig_url, loc_path, sha in assets:
    filename = os.path.basename(loc_path) if loc_path else ''
    if source_url not in url_to_assets:
        url_to_assets[source_url] = []
    url_to_assets[source_url].append({
        'original_url': orig_url,
        'public_path': f"assets/products/{filename}" if filename else '',
        'filename': filename
    })

catalog = []
for p in products:
    p_id, name, url, sku, abv, country, brand, region, vintage, grape, tasting, desc, main_img = p
    
    # Filter out category pages or non-products
    if not url or 'danh-muc' in url or name == 'Vang Tăng Độ':
        continue

    images = url_to_assets.get(url, [])
    primary_img = ""
    fallback_img = main_img or ""
    
    if images:
        primary_img = images[0]['public_path']
        if not fallback_img:
            fallback_img = images[0]['original_url']
            
    clean_name = name.replace("Rượu vang ", "").strip()
    
    c_country = country or "Ý"
    if any(k in clean_name.lower() for k in ["úck", "úc", "auswan", "barossa"]):
        c_country = "Úc"
    elif any(k in clean_name.lower() for k in ["pháp", "château", "bordeaux", "saint-émilion"]):
        c_country = "Pháp"
    elif any(k in clean_name.lower() for k in ["chile", "montes", "aromo"]):
        c_country = "Chile"
    elif any(k in clean_name.lower() for k in ["tây ban nha", "spain", "rioja"]):
        c_country = "Tây Ban Nha"
    elif any(k in clean_name.lower() for k in ["đức", "germany", "eiswein", "silvaner"]):
        c_country = "Đức"
    elif any(k in clean_name.lower() for k in ["bồ đào nha", "portugal", "porto", "cruz"]):
        c_country = "Bồ Đào Nha"
    else:
        c_country = "Ý"

    # Sensory specs (radar)
    body_val = 8.5
    tannin_val = 8.0
    acidity_val = 6.5
    finish_text = "Dài Lâu"
    
    if "passito" in clean_name.lower() or "19" in str(abv or ""):
        body_val, tannin_val, acidity_val, finish_text = 9.8, 9.0, 6.2, "Bất Tận"
    elif "appassimento" in clean_name.lower():
        body_val, tannin_val, acidity_val, finish_text = 9.2, 8.4, 6.8, "Dài Sâu"
    elif "shiraz" in clean_name.lower():
        body_val, tannin_val, acidity_val, finish_text = 9.4, 8.8, 6.5, "Ấn Tượng"
    elif "grand cru" in clean_name.lower():
        body_val, tannin_val, acidity_val, finish_text = 9.7, 9.5, 7.8, "Huyền Thoại"
    elif "prosecco" in clean_name.lower() or "trắng" in clean_name.lower() or "bianco" in clean_name.lower():
        body_val, tannin_val, acidity_val, finish_text = 6.5, 3.2, 9.0, "Sảng Khoái"
    elif "ice wine" in clean_name.lower() or "ngọt" in clean_name.lower():
        body_val, tannin_val, acidity_val, finish_text = 8.6, 2.5, 9.4, "Ngọt Ngào"

    # Default image fallback if local not found
    final_img = primary_img if (primary_img and os.path.exists(os.path.join("public", primary_img))) else (fallback_img or "assets/products/28661ef5622345ad.png")

    catalog.append({
        'id': p_id,
        'name': clean_name,
        'watermark': (clean_name.split()[0] if clean_name else "VINTAGE").upper(),
        'brand': brand or "Vineyard Selection",
        'origin': f"{c_country} • {region or 'Thượng Hạng'}",
        'country': c_country,
        'region': region or "Thượng Hạng",
        'vintage': vintage or "Vintage",
        'grape': grape or "Tuyển chọn",
        'abv': str(abv or "14.5%").strip(),
        'sku': sku or f"VY.{p_id:03d}",
        'price': "Liên hệ Sommelier",
        'img': final_img,
        'fallback_img': fallback_img,
        'tasting': (tasting or desc or "Cấu trúc chắc chắn, hương thơm mộc qua, dâu rừng, gỗ sồi vani và sô-cô-la đen quý phái.")[:160],
        'source_url': url,
        'body': body_val,
        'tannin': tannin_val,
        'acidity': acidity_val,
        'finish': finish_text
    })

print(f"Catalog generated: {len(catalog)} products.")
with open("data/normalized/curated_catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

for item in catalog[:8]:
    print(f"[{item['id']}] {item['name']} | {item['origin']} | {item['abv']} | {item['img']}")
