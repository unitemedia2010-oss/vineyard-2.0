import React, { useState, useMemo } from "react";
import productsData from "./data/products.json";
import categoriesData from "./data/categories.json";
import {
  Wine,
  ShoppingBag,
  Search,
  Filter,
  Sparkles,
  ShieldCheck,
  ThermometerSnowflake,
  Award,
  Plus,
  X,
  Phone,
  ExternalLink,
  ChevronRight,
  Eye,
  CheckCircle2,
  Send,
  Layers,
  Monitor,
  Tablet,
  Smartphone,
  FileText
} from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("catalog"); // 'catalog' | 'visual' | 'report'
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCountry, setSelectedCountry] = useState("All");
  const [selectedAbvRange, setSelectedAbvRange] = useState("All");
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [cartItems, setCartItems] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [consultSubmitted, setConsultSubmitted] = useState(false);
  const [selectedScreenshotDevice, setSelectedScreenshotDevice] = useState("desktop");

  // Filter countries list
  const countries = useMemo(() => {
    const set = new Set();
    productsData.forEach((p) => {
      if (p.origin_country) set.add(p.origin_country);
    });
    return ["All", ...Array.from(set)];
  }, []);

  // Filter products
  const filteredProducts = useMemo(() => {
    return productsData.filter((p) => {
      const matchSearch =
        searchQuery === "" ||
        p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (p.sku && p.sku.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (p.brand && p.brand.toLowerCase().includes(searchQuery.toLowerCase()));

      const matchCountry =
        selectedCountry === "All" ||
        (p.origin_country && p.origin_country.toLowerCase() === selectedCountry.toLowerCase());

      let matchAbv = true;
      if (selectedAbvRange !== "All" && p.abv) {
        const abvNum = parseFloat(p.abv.replace(/,/g, ".").replace(/[^\d.]/g, ""));
        if (!isNaN(abvNum)) {
          if (selectedAbvRange === "under14") matchAbv = abvNum < 14;
          else if (selectedAbvRange === "14to15") matchAbv = abvNum >= 14 && abvNum <= 15;
          else if (selectedAbvRange === "over15") matchAbv = abvNum > 15;
        }
      }

      return matchSearch && matchCountry && matchAbv;
    });
  }, [searchQuery, selectedCountry, selectedAbvRange]);

  // Cart operations
  const addToCart = (product) => {
    setCartItems((prev) => {
      const existing = prev.find((item) => item.product.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { product, quantity: 1 }];
    });
    setIsCartOpen(true);
  };

  const updateCartQuantity = (id, delta) => {
    setCartItems((prev) =>
      prev
        .map((item) => {
          if (item.product.id === id) {
            const newQ = item.quantity + delta;
            return newQ > 0 ? { ...item, quantity: newQ } : null;
          }
          return item;
        })
        .filter(Boolean)
    );
  };

  const removeFromCart = (id) => {
    setCartItems((prev) => prev.filter((item) => item.product.id !== id));
  };

  const totalBottles = cartItems.reduce((acc, item) => acc + item.quantity, 0);

  // Screenshots map
  const screenshots = [
    {
      name: "Trang Chủ (Homepage)",
      slug: "homepage",
      files: {
        desktop: "/screenshots/desktop/homepage.png",
        tablet: "/screenshots/tablet/homepage.png",
        mobile: "/screenshots/mobile/homepage.png"
      }
    },
    {
      name: "Danh Mục Rượu Vang (Category: Ruou-Vang)",
      slug: "danh-muc-ruou-vang",
      files: {
        desktop: "/screenshots/desktop/danh-muc-ruou-vang.png",
        tablet: "/screenshots/tablet/danh-muc-ruou-vang.png",
        mobile: "/screenshots/mobile/danh-muc-ruou-vang.png"
      }
    },
    {
      name: "Danh Mục Vang Tăng Độ (Port Wine)",
      slug: "danh-muc-vang-tang-do",
      files: {
        desktop: "/screenshots/desktop/danh-muc-vang-tang-do.png",
        tablet: "/screenshots/tablet/danh-muc-vang-tang-do.png",
        mobile: "/screenshots/mobile/danh-muc-vang-tang-do.png"
      }
    }
  ];

  return (
    <div className="min-h-screen bg-[#0A0708] text-[#FBF9F5] flex flex-col font-sans">
      {/* 18+ Top Bar */}
      <div className="bg-[#4A0E17] text-[#F3E5AB] text-xs py-1.5 px-4 text-center font-medium tracking-wide flex items-center justify-center gap-2 border-b border-[#661320]">
        <Sparkles className="w-3.5 h-3.5 text-[#D4AF37]" />
        <span>VINEYARD 2.0 • HỆ THỐNG KHẢO SÁT & HIỆN ĐẠI HÓA HẦM RƯỢU VANG THƯỢNG HẠNG</span>
        <span className="hidden md:inline font-mono opacity-80">• CHỈ DÀNH CHO NGƯỜI TRÊN 18 TUỔI</span>
      </div>

      {/* Main Header */}
      <header className="sticky top-0 z-40 bg-[#140D0F]/95 backdrop-blur-md border-b border-[#271B20] px-4 lg:px-8 h-20 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab("catalog")}>
            <div className="w-10 h-10 rounded-full border border-[#D4AF37]/40 bg-[#1C1417] flex items-center justify-center">
              <Wine className="w-5 h-5 text-[#D4AF37]" />
            </div>
            <div>
              <span className="font-serif text-2xl font-bold tracking-widest text-[#FBF9F5] block leading-none">
                VINEYARD
              </span>
              <span className="text-[10px] tracking-[0.25em] text-[#D4AF37] uppercase font-mono">
                Grand Cru Cellar 2.0
              </span>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex items-center gap-1 bg-[#1C1417] p-1 rounded-xl border border-[#271B20]">
            <button
              onClick={() => setActiveTab("catalog")}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition flex items-center gap-1.5 ${
                activeTab === "catalog"
                  ? "bg-[#4A0E17] text-[#F3E5AB] shadow"
                  : "text-[#A8A19F] hover:text-[#FBF9F5]"
              }`}
            >
              <Wine className="w-3.5 h-3.5" />
              <span>Hầm Rượu ({productsData.length})</span>
            </button>

            <button
              onClick={() => setActiveTab("visual")}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition flex items-center gap-1.5 ${
                activeTab === "visual"
                  ? "bg-[#4A0E17] text-[#F3E5AB] shadow"
                  : "text-[#A8A19F] hover:text-[#FBF9F5]"
              }`}
            >
              <Monitor className="w-3.5 h-3.5" />
              <span>Visual Audit Playwright</span>
            </button>

            <button
              onClick={() => setActiveTab("report")}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition flex items-center gap-1.5 ${
                activeTab === "report"
                  ? "bg-[#4A0E17] text-[#F3E5AB] shadow"
                  : "text-[#A8A19F] hover:text-[#FBF9F5]"
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Báo Cáo Kiểm Định</span>
            </button>
          </nav>
        </div>

        {/* Right Action: Hotline & Cart */}
        <div className="flex items-center gap-4">
          <a
            href="tel:0969843286"
            className="hidden sm:flex items-center gap-2 text-xs text-[#A8A19F] hover:text-[#D4AF37] transition border border-[#271B20] rounded-full px-3 py-1.5 bg-[#1C1417]"
          >
            <Phone className="w-3.5 h-3.5 text-[#D4AF37]" />
            <span>0969.843.286</span>
          </a>

          <button
            onClick={() => setIsCartOpen(true)}
            className="relative p-2.5 rounded-full bg-[#1C1417] border border-[#271B20] hover:border-[#D4AF37]/60 text-[#FBF9F5] transition"
          >
            <ShoppingBag className="w-5 h-5 text-[#D4AF37]" />
            {totalBottles > 0 && (
              <span className="absolute -top-1 -right-1 bg-[#821929] text-[#F3E5AB] text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center border border-[#0A0708]">
                {totalBottles}
              </span>
            )}
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1">
        {/* ================= TAB 1: CATALOG ================= */}
        {activeTab === "catalog" && (
          <div>
            {/* Hero Banner */}
            <section className="relative py-16 px-4 sm:px-6 bg-gradient-to-b from-[#140D0F] via-[#0A0708] to-[#0A0708] border-b border-[#271B20] overflow-hidden text-center">
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-[#4A0E17]/25 rounded-full blur-[130px] pointer-events-none" />

              <div className="max-w-4xl mx-auto relative z-10">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#D4AF37]/40 bg-[#1C1417]/80 text-[#D4AF37] text-xs font-mono uppercase tracking-widest mb-4">
                  <Sparkles className="w-3.5 h-3.5" /> Tuyển Chọn Vang Grand Cru & DOCG Nhập Khẩu
                </div>

                <h1 className="font-serif text-3xl sm:text-5xl font-bold tracking-tight text-[#FBF9F5] mb-4">
                  Tinh Hoa Thổ Nhưỡng Quốc Tế
                </h1>

                <p className="max-w-2xl mx-auto text-sm sm:text-base text-[#A8A19F] leading-relaxed mb-8">
                  Dữ liệu được trích xuất trực tiếp và kiểm định toàn vẹn từ{" "}
                  <a href="https://vineyard.vn" target="_blank" rel="noreferrer" className="text-[#D4AF37] underline">
                    vineyard.vn
                  </a>
                  . Lưu trữ đầy đủ thuộc tính giống nho, nồng độ, niên vụ và provenance.
                </p>

                {/* Trust Badges */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl mx-auto text-left">
                  <div className="p-3.5 rounded-xl bg-[#1C1417]/60 border border-[#271B20] flex items-center gap-3">
                    <ShieldCheck className="w-6 h-6 text-[#D4AF37] shrink-0" />
                    <div>
                      <div className="text-xs font-semibold text-[#FBF9F5]">100% Chính Ngạch</div>
                      <div className="text-[11px] text-[#A8A19F]">Tem mác & hồ sơ xuất xứ</div>
                    </div>
                  </div>

                  <div className="p-3.5 rounded-xl bg-[#1C1417]/60 border border-[#271B20] flex items-center gap-3">
                    <ThermometerSnowflake className="w-6 h-6 text-[#D4AF37] shrink-0" />
                    <div>
                      <div className="text-xs font-semibold text-[#FBF9F5]">Bảo Quản 16°C – 18°C</div>
                      <div className="text-[11px] text-[#A8A19F]">Hầm nhiệt độ & ẩm chuẩn</div>
                    </div>
                  </div>

                  <div className="p-3.5 rounded-xl bg-[#1C1417]/60 border border-[#271B20] flex items-center gap-3">
                    <Award className="w-6 h-6 text-[#D4AF37] shrink-0" />
                    <div>
                      <div className="text-xs font-semibold text-[#FBF9F5]">Sommelier Tư Vấn</div>
                      <div className="text-[11px] text-[#A8A19F]">Tư vấn chọn vị & kết hợp món</div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Filter & Search Bar */}
            <section className="sticky top-20 z-30 bg-[#140D0F]/90 backdrop-blur-md border-b border-[#271B20] py-4 px-4 sm:px-6 lg:px-8">
              <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
                {/* Search Input */}
                <div className="relative w-full md:w-80">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#A8A19F]" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Tìm tên vang, SKU, nhà sản xuất..."
                    className="w-full bg-[#1C1417] border border-[#271B20] rounded-xl pl-9 pr-4 py-2 text-xs text-[#FBF9F5] placeholder:text-[#6B6567] focus:outline-none focus:border-[#D4AF37]"
                  />
                  {searchQuery && (
                    <button
                      onClick={() => setSearchQuery("")}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[#6B6567] hover:text-[#FBF9F5]"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>

                {/* Country Filter Pills */}
                <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 scrollbar-none">
                  <span className="text-xs text-[#A8A19F] whitespace-nowrap flex items-center gap-1 font-medium">
                    <Filter className="w-3 h-3" /> Xuất xứ:
                  </span>
                  {countries.map((c) => (
                    <button
                      key={c}
                      onClick={() => setSelectedCountry(c)}
                      className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition ${
                        selectedCountry === c
                          ? "bg-[#D4AF37] text-[#0A0708] font-bold shadow"
                          : "bg-[#1C1417] border border-[#271B20] text-[#A8A19F] hover:text-[#FBF9F5]"
                      }`}
                    >
                      {c === "All" ? "Tất Cả" : c}
                    </button>
                  ))}
                </div>

                {/* ABV Filter */}
                <div className="flex items-center gap-2 self-start md:self-auto">
                  <span className="text-xs text-[#A8A19F] whitespace-nowrap">Nồng độ:</span>
                  <select
                    value={selectedAbvRange}
                    onChange={(e) => setSelectedAbvRange(e.target.value)}
                    className="bg-[#1C1417] border border-[#271B20] text-xs text-[#FBF9F5] rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-[#D4AF37]"
                  >
                    <option value="All">Tất cả nồng độ</option>
                    <option value="under14">&lt; 14% nhẹ nhàng</option>
                    <option value="14to15">14% - 15% đậm đà</option>
                    <option value="over15">&gt; 15% thượng hạng (R9 19°)</option>
                  </select>
                </div>
              </div>
            </section>

            {/* Wine Cards Grid */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
              <div className="flex items-center justify-between mb-6">
                <span className="text-xs text-[#A8A19F] font-mono">
                  Hiển thị <strong className="text-[#FBF9F5]">{filteredProducts.length}</strong> / {productsData.length} chai vang
                </span>
              </div>

              {filteredProducts.length === 0 ? (
                <div className="py-20 text-center">
                  <Wine className="w-16 h-16 text-[#271B20] mx-auto mb-3" />
                  <p className="font-serif text-lg text-[#FBF9F5]">Không tìm thấy sản phẩm phù hợp</p>
                  <button
                    onClick={() => {
                      setSearchQuery("");
                      setSelectedCountry("All");
                      setSelectedAbvRange("All");
                    }}
                    className="mt-3 text-xs text-[#D4AF37] underline"
                  >
                    Xóa toàn bộ bộ lọc
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {filteredProducts.map((p) => (
                    <div
                      key={p.id || p.slug}
                      className="group bg-[#140D0F] border border-[#271B20] rounded-xl overflow-hidden hover:border-[#D4AF37]/50 transition-all duration-300 flex flex-col justify-between shadow-lg hover:-translate-y-1"
                    >
                      {/* Top badges */}
                      <div className="p-3 flex items-center justify-between">
                        {p.origin_country ? (
                          <span className="bg-[#1C1417] border border-[#271B20] text-[#A8A19F] text-[11px] font-medium px-2 py-0.5 rounded-full">
                            {p.origin_country}
                          </span>
                        ) : <div />}

                        {p.abv && (
                          <span className="bg-[#4A0E17] border border-[#821929] text-[#F3E5AB] text-[11px] font-bold px-2 py-0.5 rounded-full font-mono">
                            {p.abv}
                          </span>
                        )}
                      </div>

                      {/* Image Stage */}
                      <div
                        onClick={() => setSelectedProduct(p)}
                        className="cursor-pointer relative aspect-[3/4] p-6 bg-gradient-to-b from-[#140D0F] to-[#0A0708] flex items-center justify-center overflow-hidden"
                      >
                        {p.main_image_url ? (
                          <img
                            src={p.main_image_url}
                            alt={p.name}
                            className="max-h-[85%] max-w-[85%] object-contain drop-shadow-[0_15px_15px_rgba(0,0,0,0.8)] group-hover:scale-105 transition-transform duration-500 ease-out"
                            loading="lazy"
                          />
                        ) : (
                          <Wine className="w-16 h-16 text-[#271B20]" />
                        )}
                      </div>

                      {/* Info Area */}
                      <div className="p-4 bg-[#140D0F] border-t border-[#271B20] flex-1 flex flex-col justify-between">
                        <div>
                          <div className="flex items-center justify-between text-[11px] text-[#D4AF37] font-mono mb-1 uppercase tracking-wider">
                            <span>{p.brand || "Vineyard"}</span>
                            {p.vintage && <span>{p.vintage}</span>}
                          </div>

                          <h3
                            onClick={() => setSelectedProduct(p)}
                            className="font-serif text-sm font-semibold text-[#FBF9F5] group-hover:text-[#D4AF37] transition-colors line-clamp-2 leading-snug cursor-pointer mb-2"
                          >
                            {p.name}
                          </h3>

                          {p.sku && (
                            <span className="text-[10px] font-mono text-[#6B6567] block mb-2">
                              SKU: {p.sku}
                            </span>
                          )}
                        </div>

                        {/* Price & Action */}
                        <div className="pt-3 border-t border-[#271B20] flex items-center justify-between mt-2">
                          <div>
                            <span className="text-[10px] text-[#6B6567] block">Giá tham khảo</span>
                            <span className="text-xs font-bold font-mono text-[#F3E5AB]">
                              {p.sale_price ? `${p.sale_price.toLocaleString("vi-VN")} ₫` : "Liên hệ tư vấn"}
                            </span>
                          </div>

                          <div className="flex items-center gap-1.5">
                            <button
                              onClick={() => setSelectedProduct(p)}
                              className="p-2 rounded-lg bg-[#1C1417] hover:bg-[#271B20] text-[#A8A19F] hover:text-[#FBF9F5] transition"
                              title="Xem chi tiết"
                            >
                              <Eye className="w-3.5 h-3.5" />
                            </button>
                            <button
                              onClick={() => addToCart(p)}
                              className="p-2 rounded-lg bg-[#4A0E17] hover:bg-[#661320] text-[#F3E5AB] transition shadow"
                              title="Thêm vào giỏ"
                            >
                              <Plus className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}

        {/* ================= TAB 2: VISUAL AUDIT & SCREENSHOTS ================= */}
        {activeTab === "visual" && (
          <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="mb-8">
              <div className="text-xs font-mono text-[#D4AF37] uppercase tracking-widest mb-1">
                Visual Inspection & Multi-Viewport Breakpoints
              </div>
              <h2 className="font-serif text-3xl font-bold text-[#FBF9F5]">
                Kiểm Toán Thị Giác Thực Tế Playwright
              </h2>
              <p className="text-xs text-[#A8A19F] mt-1 max-w-2xl">
                Hình ảnh chụp màn hình đầy đủ (Full-page Screenshots) được Playwright Chromium render trực tiếp tại 3 kích thước: Desktop (1440px), Tablet (768px), Mobile (390px).
              </p>
            </div>

            {/* Viewport Selector */}
            <div className="flex items-center gap-3 mb-8 bg-[#140D0F] p-2 rounded-xl border border-[#271B20] w-fit">
              <button
                onClick={() => setSelectedScreenshotDevice("desktop")}
                className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition ${
                  selectedScreenshotDevice === "desktop"
                    ? "bg-[#4A0E17] text-[#F3E5AB]"
                    : "text-[#A8A19F] hover:text-[#FBF9F5]"
                }`}
              >
                <Monitor className="w-4 h-4" />
                <span>Desktop (1440px)</span>
              </button>

              <button
                onClick={() => setSelectedScreenshotDevice("tablet")}
                className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition ${
                  selectedScreenshotDevice === "tablet"
                    ? "bg-[#4A0E17] text-[#F3E5AB]"
                    : "text-[#A8A19F] hover:text-[#FBF9F5]"
                }`}
              >
                <Tablet className="w-4 h-4" />
                <span>Tablet (768px)</span>
              </button>

              <button
                onClick={() => setSelectedScreenshotDevice("mobile")}
                className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition ${
                  selectedScreenshotDevice === "mobile"
                    ? "bg-[#4A0E17] text-[#F3E5AB]"
                    : "text-[#A8A19F] hover:text-[#FBF9F5]"
                }`}
              >
                <Smartphone className="w-4 h-4" />
                <span>Mobile (390px)</span>
              </button>
            </div>

            {/* Screenshot Gallery Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {screenshots.map((item) => (
                <div
                  key={item.slug}
                  className="bg-[#140D0F] border border-[#271B20] rounded-xl overflow-hidden shadow-xl flex flex-col justify-between"
                >
                  <div className="p-4 border-b border-[#271B20] bg-[#1C1417]">
                    <h4 className="font-serif text-sm font-semibold text-[#FBF9F5]">{item.name}</h4>
                    <span className="text-[10px] font-mono text-[#D4AF37] uppercase">{selectedScreenshotDevice} View</span>
                  </div>

                  <div className="p-4 bg-[#0A0708] flex items-center justify-center max-h-[500px] overflow-y-auto">
                    <img
                      src={item.files[selectedScreenshotDevice]}
                      alt={item.name}
                      className="w-full object-top rounded border border-[#271B20]"
                    />
                  </div>

                  <div className="p-3 bg-[#140D0F] border-t border-[#271B20] text-center">
                    <a
                      href={item.files[selectedScreenshotDevice]}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-[#D4AF37] hover:underline inline-flex items-center gap-1"
                    >
                      <span>Mở ảnh gốc độ phân giải cao</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* ================= TAB 3: DATA INTEGRITY REPORT ================= */}
        {activeTab === "report" && (
          <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="mb-8">
              <div className="text-xs font-mono text-[#D4AF37] uppercase tracking-widest mb-1">
                Data Validation & Pipeline Health
              </div>
              <h2 className="font-serif text-3xl font-bold text-[#FBF9F5]">
                Báo Cáo Kiểm Định Tính Toàn Vẹn Dữ Liệu
              </h2>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
              <div className="p-4 bg-[#140D0F] border border-[#271B20] rounded-xl text-center">
                <span className="text-2xl font-bold font-mono text-[#D4AF37]">346</span>
                <span className="text-xs text-[#A8A19F] block mt-1">Tổng URL Khảo Sát</span>
              </div>
              <div className="p-4 bg-[#140D0F] border border-[#271B20] rounded-xl text-center">
                <span className="text-2xl font-bold font-mono text-emerald-400">55</span>
                <span className="text-xs text-[#A8A19F] block mt-1">URL Tải Thành Công</span>
              </div>
              <div className="p-4 bg-[#140D0F] border border-[#271B20] rounded-xl text-center">
                <span className="text-2xl font-bold font-mono text-[#F3E5AB]">36</span>
                <span className="text-xs text-[#A8A19F] block mt-1">Sản Phẩm Đã Trích Xuất</span>
              </div>
              <div className="p-4 bg-[#140D0F] border border-[#271B20] rounded-xl text-center">
                <span className="text-2xl font-bold font-mono text-emerald-400">0</span>
                <span className="text-xs text-[#A8A19F] block mt-1">Lỗi Xử Lý (Errors)</span>
              </div>
            </div>

            <div className="bg-[#140D0F] border border-[#271B20] rounded-xl p-6 space-y-4 text-xs font-mono leading-relaxed text-[#A8A19F]">
              <div className="text-sm font-serif font-bold text-[#FBF9F5] mb-2">Thống Kê Kiểm Định Chi Tiết:</div>
              <p>✓ Cơ sở dữ liệu SQLite: <span className="text-[#FBF9F5]">data/database/vineyard.db</span> (FOREIGN KEY & INDEXES đầy đủ)</p>
              <p>✓ Khử trùng lặp ảnh: <span className="text-[#FBF9F5]">57 tài nguyên ảnh</span> được nhận diện qua băm SHA256.</p>
              <p>✓ Trạng thái giá: 36 sản phẩm giữ nguyên giá trị "Liên hệ" (null trong DB, không tự bịa giá giả).</p>
              <p>✓ Kiểm tra SKU trùng lặp: <span className="text-emerald-400 font-bold">0 SKU trùng</span>.</p>
              <p>✓ Tuân thủ Robots.txt: Đầy đủ 0 luật cấm, áp dụng tốc độ lịch sự 1.5s/request.</p>
            </div>
          </section>
        )}
      </main>

      {/* Product Detail Modal */}
      {selectedProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="relative w-full max-w-3xl bg-[#140D0F] border border-[#D4AF37]/40 rounded-2xl p-6 sm:p-8 shadow-2xl overflow-y-auto max-h-[90vh]">
            <button
              onClick={() => setSelectedProduct(null)}
              className="absolute top-4 right-4 p-2 rounded-full hover:bg-[#1C1417] text-[#A8A19F] hover:text-[#FBF9F5]"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              {/* Image */}
              <div className="aspect-[3/4] bg-[#0A0708] rounded-xl p-6 flex items-center justify-center border border-[#271B20]">
                {selectedProduct.main_image_url ? (
                  <img
                    src={selectedProduct.main_image_url}
                    alt={selectedProduct.name}
                    className="max-h-full max-w-full object-contain drop-shadow-[0_20px_20px_rgba(0,0,0,0.8)]"
                  />
                ) : (
                  <Wine className="w-16 h-16 text-[#271B20]" />
                )}
              </div>

              {/* Info */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-xs font-mono text-[#D4AF37]">
                  <span>{selectedProduct.brand || "Selection"}</span>
                  {selectedProduct.vintage && <span>• {selectedProduct.vintage}</span>}
                </div>

                <h3 className="font-serif text-xl sm:text-2xl font-bold text-[#FBF9F5] leading-tight">
                  {selectedProduct.name}
                </h3>

                {selectedProduct.sku && (
                  <div className="text-xs font-mono text-[#A8A19F]">
                    Mã sản phẩm: <span className="text-[#FBF9F5]">{selectedProduct.sku}</span>
                  </div>
                )}

                {/* Specs Grid */}
                <div className="grid grid-cols-2 gap-2 text-xs py-3 border-y border-[#271B20]">
                  {selectedProduct.origin_country && (
                    <div>
                      <span className="text-[#6B6567] block">Xuất xứ:</span>
                      <span className="font-semibold">{selectedProduct.origin_country}</span>
                    </div>
                  )}
                  {selectedProduct.region && (
                    <div>
                      <span className="text-[#6B6567] block">Vùng đất:</span>
                      <span className="font-semibold">{selectedProduct.region}</span>
                    </div>
                  )}
                  {selectedProduct.grape_variety && (
                    <div>
                      <span className="text-[#6B6567] block">Giống nho:</span>
                      <span className="font-semibold">{selectedProduct.grape_variety}</span>
                    </div>
                  )}
                  {selectedProduct.abv && (
                    <div>
                      <span className="text-[#6B6567] block">Nồng độ:</span>
                      <span className="font-semibold text-[#D4AF37] font-mono">{selectedProduct.abv}</span>
                    </div>
                  )}
                  {selectedProduct.volume && (
                    <div>
                      <span className="text-[#6B6567] block">Dung tích:</span>
                      <span className="font-semibold font-mono">{selectedProduct.volume}</span>
                    </div>
                  )}
                </div>

                {/* Tasting Notes */}
                {selectedProduct.tasting_notes && (
                  <div className="p-3 bg-[#1C1417] rounded-lg border border-[#271B20] text-xs text-[#A8A19F] leading-relaxed">
                    <span className="text-[#D4AF37] font-semibold block mb-1">Ghi chú thử nếm:</span>
                    {selectedProduct.tasting_notes}
                  </div>
                )}

                {/* Actions */}
                <div className="pt-2 flex items-center gap-3">
                  <button
                    onClick={() => {
                      addToCart(selectedProduct);
                      setSelectedProduct(null);
                    }}
                    className="flex-1 py-3 bg-[#4A0E17] hover:bg-[#661320] text-[#F3E5AB] font-serif font-bold text-xs tracking-wider rounded-xl transition shadow flex items-center justify-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    <span>THÊM VÀO DANH SÁCH TƯ VẤN</span>
                  </button>

                  <a
                    href={selectedProduct.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="p-3 bg-[#1C1417] hover:bg-[#271B20] text-[#A8A19F] hover:text-[#FBF9F5] rounded-xl border border-[#271B20] transition"
                    title="Xem trên vineyard.vn gốc"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Slide-over Cart Drawer */}
      {isCartOpen && (
        <div className="fixed inset-0 z-50 flex justify-end">
          <div className="fixed inset-0 bg-black/75 backdrop-blur-sm" onClick={() => setIsCartOpen(false)} />

          <div className="relative w-full max-w-md bg-[#140D0F] border-l border-[#271B20] text-[#FBF9F5] shadow-2xl flex flex-col justify-between z-10 h-full">
            <div className="p-5 border-b border-[#271B20] flex items-center justify-between bg-[#1C1417]">
              <div className="flex items-center gap-2">
                <Wine className="w-5 h-5 text-[#D4AF37]" />
                <h3 className="font-serif text-lg font-bold">Danh Sách Tư Vấn ({totalBottles})</h3>
              </div>
              <button onClick={() => setIsCartOpen(false)} className="p-1.5 rounded-full hover:bg-[#271B20]">
                <X className="w-5 h-5 text-[#A8A19F]" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-5 space-y-3">
              {cartItems.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center text-[#A8A19F] py-10">
                  <Wine className="w-12 h-12 text-[#271B20] mb-2" />
                  <p className="font-serif text-base text-[#FBF9F5]">Danh sách đang trống</p>
                  <p className="text-xs mt-1">Chọn chai vang bạn muốn thử để nhận tư vấn Sommelier.</p>
                </div>
              ) : consultSubmitted ? (
                <div className="h-full flex flex-col items-center justify-center text-center py-10">
                  <CheckCircle2 className="w-14 h-14 text-[#D4AF37] mb-3" />
                  <h4 className="font-serif text-xl font-bold">Đã Gửi Yêu Cầu</h4>
                  <p className="text-xs text-[#A8A19F] mt-1 max-w-xs">
                    Chuyên viên Sommelier của Vineyard sẽ gọi điện tư vấn và chuẩn bị giao rượu sớm nhất.
                  </p>
                </div>
              ) : (
                cartItems.map((item) => (
                  <div key={item.product.id} className="p-3 bg-[#1C1417] rounded-xl border border-[#271B20] flex items-center gap-3">
                    <div className="w-12 h-16 bg-[#0A0708] rounded flex items-center justify-center p-1">
                      {item.product.main_image_url ? (
                        <img src={item.product.main_image_url} alt="" className="max-h-full max-w-full object-contain" />
                      ) : <Wine className="w-5 h-5 text-[#271B20]" />}
                    </div>

                    <div className="flex-1 min-w-0">
                      <h5 className="font-serif text-xs font-semibold truncate text-[#FBF9F5]">{item.product.name}</h5>
                      <span className="text-[11px] text-[#D4AF37] font-mono block">
                        {item.product.sale_price ? `${item.product.sale_price.toLocaleString("vi-VN")} ₫` : "Liên hệ tư vấn"}
                      </span>
                      <div className="flex items-center gap-2 mt-2">
                        <button
                          onClick={() => updateCartQuantity(item.product.id, -1)}
                          className="w-5 h-5 rounded bg-[#271B20] text-xs flex items-center justify-center"
                        >-</button>
                        <span className="text-xs font-mono font-bold">{item.quantity}</span>
                        <button
                          onClick={() => updateCartQuantity(item.product.id, 1)}
                          className="w-5 h-5 rounded bg-[#271B20] text-xs flex items-center justify-center"
                        >+</button>
                      </div>
                    </div>

                    <button onClick={() => removeFromCart(item.product.id)} className="text-[#6B6567] hover:text-red-400 p-1">
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ))
              )}
            </div>

            {cartItems.length > 0 && !consultSubmitted && (
              <div className="p-5 border-t border-[#271B20] bg-[#1C1417] space-y-3">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    setConsultSubmitted(true);
                    setTimeout(() => {
                      setCartItems([]);
                      setConsultSubmitted(false);
                      setIsCartOpen(false);
                    }, 2500);
                  }}
                  className="space-y-2.5"
                >
                  <input
                    type="text"
                    placeholder="Họ và tên quý khách *"
                    required
                    className="w-full bg-[#140D0F] border border-[#271B20] rounded-lg px-3 py-2 text-xs text-[#FBF9F5] focus:outline-none focus:border-[#D4AF37]"
                  />
                  <input
                    type="tel"
                    placeholder="Số điện thoại / Zalo *"
                    required
                    className="w-full bg-[#140D0F] border border-[#271B20] rounded-lg px-3 py-2 text-xs text-[#FBF9F5] focus:outline-none focus:border-[#D4AF37]"
                  />
                  <button
                    type="submit"
                    className="w-full py-3 bg-[#4A0E17] hover:bg-[#661320] text-[#F3E5AB] font-serif font-bold text-xs tracking-wider rounded-lg transition shadow flex items-center justify-center gap-2"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>GỬI YÊU CẦU SOMMELIER TƯ VẤN</span>
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-[#271B20] bg-[#0A0708] py-8 px-4 text-center text-xs text-[#6B6567]">
        <p className="font-serif text-[#FBF9F5] text-sm font-bold tracking-widest mb-1">VINEYARD 2.0</p>
        <p className="max-w-xl mx-auto leading-relaxed">
          Cảnh báo: Rượu bia có hại cho sức khỏe. Uống có trách nhiệm. Không lái xe sau khi sử dụng đồ uống có cồn. Sản phẩm chỉ dành cho người đủ 18 tuổi trở lên.
        </p>
      </footer>
    </div>
  );
}
