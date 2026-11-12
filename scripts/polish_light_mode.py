with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add light mode refinements to CSS
light_mode_refinements = """
/* Light Mode Refinements */
html.light .nav>li>a{color:#4a3a30}
html.light .nav>li>a:hover,html.light .nav>li>a[aria-current]{color:var(--wine)}
html.light .dd{background:#ffffff;border-color:var(--line);box-shadow:0 18px 40px rgba(60,35,20,.12)}
html.light .dd a{color:var(--label)}
html.light .dd a:hover{background:rgba(143,102,46,.1)}
html.light .hero-sub{color:#5d4e43}
html.light .badge{background:rgba(255,255,255,.92);color:var(--label);border:1px solid var(--line);box-shadow:0 4px 12px rgba(60,35,20,.08)}
html.light .cap b{color:#1c1311;text-shadow:0 2px 10px rgba(255,255,255,.9)}
html.light .cap span{color:var(--brass-hi);text-shadow:0 1px 6px rgba(255,255,255,.9)}
html.light .hint{color:var(--muted)}
html.light .hint i{background:var(--brass);box-shadow:0 0 10px 2px rgba(143,102,46,.4)}
html.light .tab{color:#554438}
html.light .tab[aria-selected="true"]{background:var(--wine);color:#ffffff;border-color:var(--wine)}
html.light .srch{background:rgba(251,248,243,.96)}
html.light .srch input{color:var(--label);border-bottom-color:var(--brass)}
html.light .srch li a:hover,html.light .srch li a.act{background:rgba(143,102,46,.1)}
html.light .dock a:nth-child(3){background:#ffffff;color:var(--label)}
html.light .dock a span{background:#ffffff;color:var(--label)}
html.light .gift-img{background:#ffffff}
html.light .map{background:#ffffff;filter:grayscale(.2) sepia(.15) contrast(1.02)}
"""

# Insert before </style>
html = html.replace('</style>', light_mode_refinements + '\n</style>')

# Also add theme toggle inside mobile menu #mnav-list
old_mnav = '<a href="#/thuong-hieu">Thương hiệu<span>${D.brands.length}</span></a><a href="#/showroom">Showroom<span>3 thành phố</span></a><a href="${TEL}">Gọi tư vấn<span>${HOT}</span></a>'
new_mnav = '<a href="#" id="mnav-theme-btn">Chế độ giao diện<span id="mnav-theme-val">Sáng / Tối</span></a><a href="#/thuong-hieu">Thương hiệu<span>${D.brands.length}</span></a><a href="#/showroom">Showroom<span>3 thành phố</span></a><a href="${TEL}">Gọi tư vấn<span>${HOT}</span></a>'

if old_mnav in html:
    html = html.replace(old_mnav, new_mnav)
    print("Added theme button to mobile menu template")

# Add click event for mnav-theme-btn in initTheme()
old_init_theme = """  const btn = $('#theme-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const isLight = document.documentElement.classList.contains('light');
      const next = isLight ? 'dark' : 'light';
      applyTheme(next);
      localStorage.setItem('vy_theme', next);
    });
  }"""

new_init_theme = """  const toggleTheme = () => {
    const isLight = document.documentElement.classList.contains('light');
    const next = isLight ? 'dark' : 'light';
    applyTheme(next);
    localStorage.setItem('vy_theme', next);
  };
  const btn = $('#theme-btn');
  if (btn) btn.addEventListener('click', toggleTheme);
  document.addEventListener('click', e => {
    if (e.target.closest('#mnav-theme-btn')) {
      e.preventDefault();
      toggleTheme();
    }
  });"""

html = html.replace(old_init_theme, new_init_theme)

# Update applyTheme to update mobile text
old_apply = """  const metaTheme = $('meta[name="theme-color"]');
  if (metaTheme) metaTheme.setAttribute('content', isLight ? '#FAF7F2' : '#12080A');"""

new_apply = """  const metaTheme = $('meta[name="theme-color"]');
  if (metaTheme) metaTheme.setAttribute('content', isLight ? '#FAF7F2' : '#12080A');
  const mVal = $('#mnav-theme-val');
  if (mVal) mVal.textContent = isLight ? 'Đang bật Sáng (Dinh thự)' : 'Đang bật Tối (Hầm rượu)';"""

html = html.replace(old_apply, new_apply)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Light mode styles and mobile menu toggle fully wired up!")
