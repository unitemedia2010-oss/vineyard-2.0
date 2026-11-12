import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Google Fonts in <head>
old_fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600&family=Noto+Serif+Display:ital,wght@0,300;0,400;0,500;1,300&display=swap">'
new_fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pinyon+Script&family=Playfair+Display:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+Display:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap">'

if old_fonts in html:
    html = html.replace(old_fonts, new_fonts)
    print("Updated Google Fonts link with Pinyon Script & Playfair Display")
else:
    print("Old fonts string not matched, updating via regex")
    html = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]+">', new_fonts, html)

# 2. Update CSS variables for Light Mode and Dark Mode
old_css_root = """:root{
  --cellar:#140C0B; --cellar-2:#1D1211; --lees:#2A1216; --wine:#5E1224; --seal:#8E1F2F;
  --brass:#B58A4C; --brass-hi:#D9B57A; --label:#EADFCB; --muted:#A8957C; --ink:#2B1A17;
  --line:rgba(181,138,76,.28); --line-soft:rgba(234,223,203,.1);
  --serif:'Noto Serif Display','Noto Serif',Georgia,'Times New Roman',serif;
  --sans:'Be Vietnam Pro','Segoe UI',system-ui,-apple-system,sans-serif;
  --wrap:1240px; --gut:clamp(18px,4vw,40px); --ease:cubic-bezier(.22,.61,.36,1);
}"""

new_css_root = """:root{
  --cellar:#12080a; --cellar-2:#1c0d10; --lees:#2a1016; --wine:#5e1224; --seal:#8e1f2f;
  --brass:#b58a4c; --brass-hi:#d9b57a; --label:#eadfcb; --muted:#a8957c; --ink:#2b1a17;
  --line:rgba(181,138,76,.28); --line-soft:rgba(234,223,203,.1);
  --serif:'Noto Serif Display','Noto Serif',Georgia,'Times New Roman',serif;
  --sans:'Be Vietnam Pro','Segoe UI',system-ui,-apple-system,sans-serif;
  --script:'Pinyon Script',cursive;
  --wrap:1240px; --gut:clamp(18px,4vw,40px); --ease:cubic-bezier(.22,.61,.36,1);
  --shade-0:rgba(18,8,10,0); --shade-34:rgba(18,8,10,.28); --shade-70:rgba(18,8,10,.88); --shade-100:rgba(18,8,10,.975);
  --warm-glow:rgba(255,168,76,.7);
  --veil-1:rgba(18,8,10,.97); --veil-2:rgba(18,8,10,.86);
  --hdr-bg:rgba(18,8,10,.88);
  --niche-bg:radial-gradient(120% 85% at 50% 32%,#f3eadb 0%,#e3d3b7 55%,#c7b08d 100%);
  --niche-shadow:inset 0 14px 26px rgba(70,40,22,.38),inset 0 -8px 14px rgba(70,40,22,.22);
  --card-plinth:radial-gradient(circle at var(--mx,50%) var(--my,30%),#fdf7ec 0%,#ece0c9 42%,#d3bf9d 100%);
  --ftr-bg:#0d0607;
}

html.light{
  --cellar:#fbf8f3; --cellar-2:#f4ece0; --lees:#eae0d0; --wine:#6e1022; --seal:#942033;
  --brass:#8f662e; --brass-hi:#684616; --label:#1c1311; --muted:#746658; --ink:#ffffff;
  --line:rgba(143,102,46,.24); --line-soft:rgba(28,19,17,.08);
  --shade-0:rgba(251,248,243,0); --shade-34:rgba(251,248,243,.22); --shade-70:rgba(251,248,243,.82); --shade-100:rgba(251,248,243,.965);
  --warm-glow:rgba(217,181,122,.6);
  --veil-1:rgba(251,248,243,.97); --veil-2:rgba(251,248,243,.88);
  --hdr-bg:rgba(251,248,243,.92);
  --niche-bg:radial-gradient(120% 85% at 50% 32%,#ffffff 0%,#f5ece0 60%,#e4d4bf 100%);
  --niche-shadow:0 8px 24px rgba(60,35,20,.09),inset 0 4px 12px rgba(255,255,255,.9);
  --card-plinth:radial-gradient(circle at var(--mx,50%) var(--my,30%),#ffffff 0%,#f5eee4 46%,#e4d4bf 100%);
  --ftr-bg:#efe4d5;
}"""

if old_css_root in html:
    html = html.replace(old_css_root, new_css_root)
    print("Updated CSS root with Light and Dark variables")
else:
    # Replace via pattern
    html = re.sub(r':root\s*\{[^}]+\}', new_css_root, html)
    print("Replaced :root via regex")

# 3. Add styles for Theme Toggle, Typographic Pairing, Sparkles, and Wine Route
extra_styles = """
/* Theme Switcher Button */
.theme-btn{position:relative;overflow:hidden;display:grid;place-items:center}
.theme-btn .icon-sun,.theme-btn .icon-moon{position:absolute;width:19px;height:19px;transition:transform .4s var(--ease),opacity .3s}
:root .icon-sun{opacity:1;transform:rotate(0) scale(1);stroke:var(--brass-hi)}
:root .icon-moon{opacity:0;transform:rotate(-90deg) scale(.4)}
html.light .icon-sun{opacity:0;transform:rotate(90deg) scale(.4)}
html.light .icon-moon{opacity:1;transform:rotate(0) scale(1);stroke:var(--brass-hi)}

/* Typographic Pairing: Cursive Script + Bold Architectural Serif */
.typo-lockup{position:relative;display:inline-flex;flex-direction:column;align-items:flex-start}
.script-swash{font-family:var(--script);font-size:clamp(36px,5.2vw,64px);color:var(--brass-hi);line-height:.88;transform:rotate(-3deg) translateX(-6px);display:block;z-index:2;pointer-events:none;font-weight:400;text-shadow:0 3px 18px rgba(181,138,76,.3)}
.title-bold{font-family:var(--serif);font-size:clamp(30px,4.2vw,54px);font-weight:300;letter-spacing:.06em;text-transform:uppercase;color:var(--label);line-height:1.06;margin:0;z-index:1}
.sparkle{display:inline-block;font-size:.45em;vertical-align:.55em;color:var(--brass-hi);margin-left:6px;animation:sparkleTwinkle 2.8s infinite ease-in-out alternate}
@keyframes sparkleTwinkle{0%{transform:scale(.85) rotate(0deg);opacity:.65}50%{transform:scale(1.28) rotate(45deg);opacity:1;filter:drop-shadow(0 0 10px var(--brass-hi))}100%{transform:scale(.85) rotate(0deg);opacity:.65}}

.tag-editorial{display:inline-flex;align-items:center;gap:8px;font-size:10.5px;font-weight:600;letter-spacing:.26em;text-transform:uppercase;color:var(--brass);margin-bottom:8px}
.tag-editorial::before,.tag-editorial::after{content:'';width:20px;height:1px;background:var(--brass);opacity:.4}

/* Wine Route Strip (Inspired by Image 3) */
.wine-route-wrap{margin:clamp(36px,5vw,60px) 0 clamp(20px,3vw,36px);padding:24px 28px;background:var(--cellar-2);border:1px solid var(--line);border-radius:6px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px}
.route-item{display:flex;align-items:center;gap:12px}
.route-num{font-family:var(--script);font-size:32px;color:var(--brass-hi);line-height:1}
.route-info b{display:block;font-size:14.5px;letter-spacing:.05em;color:var(--label)}
.route-info span{font-size:12px;color:var(--muted)}
.route-sep{color:var(--brass);opacity:.4;font-size:14px}
@media (max-width:768px){.route-sep{display:none}.wine-route-wrap{display:grid;grid-template-columns:1fr 1fr;gap:16px}}

/* Baroque Accent Card (Inspired by Image 4) */
.bdx{background:linear-gradient(160deg,var(--wine) 0%,var(--lees) 70%);position:relative;overflow:hidden}
.bdx::before{content:'✦';position:absolute;top:20px;right:20px;font-size:24px;color:rgba(217,181,122,.2)}
html.light .bdx{background:linear-gradient(160deg,#f3ece0 0%,#e9decb 70%);color:var(--label)}
html.light .bdx-intro .lede{color:var(--muted)}
html.light .lg p{color:var(--muted)}
"""

# Inject extra styles right before </style>
html = html.replace('</style>', extra_styles + '\n</style>')
print("Injected extra styles for theme, typography, sparkles, and wine route")

# 4. Inject Theme Button into Header
theme_btn_html = """      <button class="icon-btn theme-btn" id="theme-btn" aria-label="Đổi chế độ Sáng / Tối" title="Đổi giao diện Sáng / Tối">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <a class="hotline" href="tel:0911002233">0911 00 22 33</a>"""

html = html.replace('<a class="hotline" href="tel:0911002233">0911 00 22 33</a>', theme_btn_html)
print("Injected theme switcher button in header")

# 5. Update Hero Section with Typographic Pairing (Cặp chữ bay bổng)
old_hero_markup = """    <h1 class="hero-h"><span class="ln"><span>Hầm Rượu</span></span><span class="ln"><span>Thượng Hạng.</span></span></h1>
    <p class="hero-sub">Tuyển chọn các nhãn vang Grand Cru, DOCG và rượu mạnh nhập khẩu chính ngạch từ các điền trang danh tiếng thế giới.</p>"""

new_hero_markup = """    <div class="typo-lockup" style="margin-bottom:12px">
      <span class="tag-editorial">BỘ SƯU TẬP HOÀNG GIA • EST. 2012</span>
      <span class="script-swash">Hầm Rượu</span>
      <h1 class="title-bold">THƯỢNG HẠNG <span class="sparkle">✦</span></h1>
    </div>
    <p class="hero-sub">Tuyển chọn các dòng vang Grand Cru, DOCG và rượu mạnh nhập khẩu chính ngạch từ các điền trang danh giá nhất thế giới.</p>"""

html = html.replace(old_hero_markup, new_hero_markup)
print("Updated Hero with Typographic Pairing")

# 6. Update Section Titles with Cặp Chữ Bay Bổng
# Danh mục
html = html.replace(
    '<div class="sec-head"><h2 class="h2">Danh mục hầm rượu</h2></div>',
    '<div class="sec-head"><div class="typo-lockup"><span class="script-swash">Bộ Sưu Tập</span><h2 class="title-bold">DANH MỤC HẦM RƯỢU <span class="sparkle">✦</span></h2></div></div>'
)

# Mở chai cho dịp nào
html = html.replace(
    '<div class="sec-head"><h2 class="h2">Mở chai cho dịp nào?</h2>${railNav(\'rail-occ\')}</div>',
    '<div class="sec-head"><div class="typo-lockup"><span class="script-swash">Thưởng Nếm</span><h2 class="title-bold">MỞ CHAI CHO DỊP NÀO?</h2></div>${railNav(\'rail-occ\')}</div>'
)

# Bán chạy và mới về
html = html.replace(
    '<div class="sec-head"><h2 class="h2">Bán chạy và mới về</h2>${railNav(\'rail-pick\')}</div>',
    '<div class="sec-head"><div class="typo-lockup"><span class="script-swash">Tuyển Chọn</span><h2 class="title-bold">BÁN CHẠY & MỚI VỀ <span class="sparkle">✦</span></h2></div>${railNav(\'rail-pick\')}</div>'
)

# Bordeaux Grand Cru
old_bdx = """<div class="bdx-intro"><h2 class="h2">Những lâu đài Bordeaux trong hầm</h2><p class="lede">Tuyển chọn niên vụ kinh điển từ các lâu đài Saint-Émilion, Margaux, Pauillac, Pomerol.</p><a class="btn" href="#/danh-muc/ruou-vang-cao-cap?country=${enc('Pháp')}">Xem ${nFR} nhãn vang Pháp cao cấp</a></div>"""
new_bdx = """<div class="bdx-intro"><div class="typo-lockup"><span class="script-swash">Lâu Đài Di Sản</span><h2 class="title-bold">BORDEAUX GRAND CRU <span class="sparkle">✦</span></h2></div><p class="lede">Tuyển chọn niên vụ kinh điển từ các lâu đài Saint-Émilion, Margaux, Pauillac, Pomerol.</p><a class="btn" href="#/danh-muc/ruou-vang-cao-cap?country=${enc('Pháp')}">Xem ${nFR} nhãn vang Pháp cao cấp</a></div>"""
html = html.replace(old_bdx, new_bdx)

# Quà tặng doanh nghiệp
old_gift = """<div><h2 class="h2">Quà Tết và quà doanh nghiệp</h2><p class="lede">Bộ quà tặng giới hạn kết hợp các dòng vang thượng hạng cùng ly pha lê RCR sang trọng.</p>"""
new_gift = """<div><div class="typo-lockup"><span class="script-swash">Đặc Quyền</span><h2 class="title-bold">QUÀ TẶNG DOANH NGHIỆP <span class="sparkle">✦</span></h2></div><p class="lede">Bộ quà tặng giới hạn kết hợp các dòng vang thượng hạng cùng ly pha lê RCR sang trọng.</p>"""
html = html.replace(old_gift, new_gift)

# Showroom
html = html.replace(
    '<div class="sec-head"><h2 class="h2">Hệ thống Showroom</h2></div>',
    '<div class="sec-head"><div class="typo-lockup"><span class="script-swash">Không Gian</span><h2 class="title-bold">HỆ THỐNG SHOWROOM <span class="sparkle">✦</span></h2></div></div>'
)

# 7. Add Wine Route graphic before Bordeaux section (Inspired by Image 3)
wine_route_markup = """
<div class="wrap">
  <div class="wine-route-wrap">
    <div class="route-item"><div class="route-num">01</div><div class="route-info"><b>BORDEAUX</b><span>Pháp • Premier Grand Cru</span></div></div>
    <div class="route-sep">✦ ────</div>
    <div class="route-item"><div class="route-num">02</div><div class="route-info"><b>PUGLIA</b><span>Ý • Passito & Primitivo</span></div></div>
    <div class="route-sep">✦ ────</div>
    <div class="route-item"><div class="route-num">03</div><div class="route-info"><b>BAROSSA</b><span>Úc • Old Vine Shiraz</span></div></div>
    <div class="route-sep">✦ ────</div>
    <div class="route-item"><div class="route-num">04</div><div class="route-info"><b>MAIPO</b><span>Chile • Andes Heritage</span></div></div>
  </div>
</div>
"""

html = html.replace('<section class="sec bdx" id="bordeaux">', wine_route_markup + '<section class="sec bdx" id="bordeaux">')
print("Added Wine Route Strip before Bordeaux")

# 8. Add JavaScript for Theme Management in boot()
theme_js = """
// ---------- Light / Dark Theme Controller ----------
function initTheme() {
  const saved = localStorage.getItem('vy_theme') || 'dark';
  applyTheme(saved);
  const btn = $('#theme-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const isLight = document.documentElement.classList.contains('light');
      const next = isLight ? 'dark' : 'light';
      applyTheme(next);
      localStorage.setItem('vy_theme', next);
    });
  }
}

function applyTheme(theme) {
  const isLight = theme === 'light';
  document.documentElement.classList.toggle('light', isLight);
  const btn = $('#theme-btn');
  if (btn) {
    btn.setAttribute('aria-label', isLight ? 'Chuyển sang chế độ tối (Hầm rượu)' : 'Chuyển sang chế độ sáng (Dinh thự)');
    btn.setAttribute('title', isLight ? 'Chế độ tối (Hầm rượu)' : 'Chế độ sáng (Dinh thự)');
  }
  const metaTheme = $('meta[name="theme-color"]');
  if (metaTheme) metaTheme.setAttribute('content', isLight ? '#FAF7F2' : '#12080A');
}
"""

html = html.replace('function boot() {', theme_js + '\nfunction boot() {\n  initTheme();')
print("Injected initTheme() into boot()")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated with Light/Dark mode and Typographic Pairing!")
