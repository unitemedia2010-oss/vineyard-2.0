import sqlite3
import json

conn = sqlite3.connect('data/database/vineyard.db')
c = conn.cursor()

c.execute("SELECT id, original_url, source_page_url, local_path FROM assets WHERE asset_category='products'")
assets = c.fetchall()
print(f"Total product assets: {len(assets)}")
for a in assets[:8]:
    print(a[0], a[1][:60], a[2][:60], a[3])

c.execute("SELECT id, name, canonical_url, sku, abv, origin_country, brand FROM products")
products = c.fetchall()
print(f"Total products: {len(products)}")
for p in products[:8]:
    print(p[0], p[1], p[2])
