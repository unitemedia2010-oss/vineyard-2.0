import subprocess
import re

# Fetch raw git content directly
result = subprocess.run(['git', 'show', 'a9bedb9:index.html'], capture_output=True, check=True)
html = result.stdout.decode('utf-8')

# 1. Refine Hero Title & Subtitle to be minimal, spacious and elegant
html = re.sub(
    r'<h1 class="hero-h">.*?</h1>\s*<p class="hero-sub">.*?</p>',
    r'<h1 class="hero-h"><span class="ln"><span>Hầm Rượu</span></span><span class="ln"><span>Thượng Hạng.</span></span></h1>\n    <p class="hero-sub">Tuyển chọn các nhãn vang Grand Cru, DOCG và rượu mạnh nhập khẩu chính ngạch từ các điền trang danh tiếng thế giới.</p>',
    html,
    flags=re.DOTALL
)

# 2. Refine Hero CTA buttons
html = html.replace(
    '<div class="hero-cta row"><a class="btn btn-solid" href="#/tat-ca">Xem các nhãn rượu</a><a class="btn" href="${TEL}">Gọi ${HOT}</a></div>',
    '<div class="hero-cta row"><a class="btn btn-solid" href="#/tat-ca">Khám phá hầm rượu</a><a class="btn" href="${TEL}">Hotline ${HOT}</a></div>'
)

# 3. Clean up category section header - remove verbose description
html = html.replace(
    '<div class="sec-head"><div><h2 class="h2">Danh mục rượu</h2><p class="lede">Chọn nhóm rượu, sau đó lọc tiếp theo loại, vùng và thương hiệu.</p></div></div>',
    '<div class="sec-head"><h2 class="h2">Danh mục hầm rượu</h2></div>'
)

# 4. Clean up wine list item description - remove noisy paragraphs
html = html.replace(
    '<p class="wl-desc">${esc(c.desc)}</p>',
    ''
)

# 5. Clean up Bordeaux section
html = html.replace(
    '<p class="lede">Pauillac, Margaux, Saint-Julien, Saint-Émilion và Pomerol. Mỗi niên vụ là một chai riêng, bấm vào năm để xem chi tiết.</p>',
    '<p class="lede">Tuyển chọn niên vụ kinh điển từ các lâu đài Saint-Émilion, Margaux, Pauillac, Pomerol.</p>'
)

# 6. Clean up Gifting section
html = html.replace(
    '<p class="lede">Chọn set quà theo ngân sách và người nhận: vang Bordeaux, vang Ý bản giới hạn, whisky, ly pha lê RCR. Vineyard tư vấn chọn chai và giao tận nơi.</p>',
    '<p class="lede">Bộ quà tặng giới hạn kết hợp các dòng vang thượng hạng cùng ly pha lê RCR sang trọng.</p>'
)
html = html.replace(
    '<a class="btn" href="${gift.url}" target="_blank" rel="noopener">Đọc gợi ý set quà 2026</a>',
    '<a class="btn" href="#/danh-muc/ruou-vang-cao-cap">Xem vang cao cấp</a>'
)

# 7. Remove the text-heavy "Thương hiệu theo vùng" and "Đọc trước khi mở chai" blog clutter from the Home page!
pattern = r'<section class="sec" style="padding-top:0"><div class="wrap">\s*<div class="sec-head"><div><h2 class="h2">Thương hiệu theo vùng</h2>.*?(?=<section class="sec" id="showroom")'
html, count = re.subn(pattern, '', html, flags=re.DOTALL)
print(f"Removed text walls (brands by region & blog): {count} sections removed.")

# 8. Clean up Showroom section
html = html.replace(
    '<div class="sec-head"><div><h2 class="h2">Ghé showroom</h2><p class="lede">Xem rượu tận nơi ở TP.HCM, Hà Nội, Đà Nẵng, hoặc gọi để được giao.</p></div></div>',
    '<div class="sec-head"><h2 class="h2">Hệ thống Showroom</h2></div>'
)

# 9. Clean up Footer text
html = html.replace(
    '<p style="margin-top:18px">Website của Bình Minh Group (BMG), nhà nhập khẩu và phân phối rượu vang, rượu mạnh tại Việt Nam từ năm 2012.</p>',
    '<p style="margin-top:18px">Hệ thống phân phối rượu vang và rượu mạnh nhập khẩu chính ngạch uy tín tại Việt Nam.</p>'
)

# 10. Improve font styling slightly: typography letter spacing
html = html.replace(
    "h1,h2,h3{font-family:var(--serif);font-weight:400;line-height:1.12;margin:0;letter-spacing:-.005em}",
    "h1,h2,h3{font-family:var(--serif);font-weight:300;line-height:1.15;margin:0;letter-spacing:0.02em}"
)

# Enhance candle light size and warmth
html = html.replace(
    "R = Math.max(130, Math.min(270, Math.min(W, H) * 0.3));",
    "R = Math.max(160, Math.min(320, Math.min(W, H) * 0.35));"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html: Previous candle-lit version restored with minimal, ultra-luxurious text!")
