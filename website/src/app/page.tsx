"use client";

import React, { useState, useEffect } from "react";
import { Header } from "@/components/Header";
import { ProductCard } from "@/components/ProductCard";
import { CartDrawer } from "@/components/CartDrawer";
import { WineProduct, CartItem } from "@/types/wine";
import { Wine, ShieldCheck, ThermometerSnowflake, Award, ArrowRight, Sparkles } from "lucide-react";
import Link from "next/link";

export default function HomePage() {
  const [products, setProducts] = useState<WineProduct[]>([]);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [filterCountry, setFilterCountry] = useState<string>("All");

  useEffect(() => {
    // Dynamic import normalized data if in local browser
    fetch("/products.json")
      .then((res) => res.json())
      .then((data: WineProduct[]) => {
        if (Array.isArray(data) && data.length > 0) {
          setProducts(data);
        }
      })
      .catch(() => {
        // Fallback preview wines
        setProducts([
          {
            id: 1,
            source_url: "https://vineyard.vn/san-pham/r9-primitivo-icono",
            name: "R9 Primitivo & Syrah Passito Salento IGP",
            slug: "r9-primitivo-icono",
            sku: "B06.GRATI.06",
            brand: "Reputazione",
            category: "Vang Đỏ > Vang Ý",
            origin_country: "Italy",
            region: "Puglia",
            producer: "Reputazione",
            vintage: "2019",
            grape_variety: "Primitivo",
            volume: "0.75L",
            abv: "19,0%",
            currency: "VND",
            stock_status: "Còn trong kho",
            specs: { "Quốc gia": "Italy", "Vùng": "Puglia", "Nồng độ": "19,0%", "Dung tích": "0.75L" },
            main_image_url: "https://vineyard.vn/userfiles/images/SanPham/RuouVangCaoCap/VangY/R9-limited-edition.png",
            gallery_image_urls: []
          },
          {
            id: 2,
            source_url: "https://vineyard.vn/san-pham/40-appassimento-puglia-igp",
            name: "40 Appassimento Puglia IGP",
            slug: "40-appassimento-puglia-igp",
            sku: "B06.TAGARO.01",
            brand: "Quaranta",
            category: "Vang Đỏ > Vang Ý",
            origin_country: "Italy",
            region: "Puglia",
            producer: "Tagaro",
            vintage: "2020",
            grape_variety: "Blended",
            volume: "0.75L",
            abv: "15,0%",
            currency: "VND",
            stock_status: "Còn trong kho",
            specs: { "Quốc gia": "Italy", "Vùng": "Puglia", "Nồng độ": "15,0%" },
            main_image_url: "https://vineyard.vn/userfiles/images/SanPham/RuouVang/VangDo/40%20Appassimento%20Puglia%20IGP%20red%20%20(chai%20%C4%91%E1%BB%8F).png",
            gallery_image_urls: []
          },
          {
            id: 3,
            source_url: "https://vineyard.vn/san-pham/ruou-vang-auswan-creek-diplomat-70-shiraz",
            name: "Rượu vang Auswan Creek Diplomat 70 Shiraz",
            slug: "ruou-vang-auswan-creek-diplomat-70-shiraz",
            sku: "B08.SWAN.06",
            brand: "Auswan Creek",
            category: "Vang Đỏ > Vang Úc",
            origin_country: "Australia",
            region: "Barossa Valley",
            producer: "Auswan",
            vintage: "2018",
            grape_variety: "Shiraz",
            volume: "0.75L",
            abv: "15,0%",
            currency: "VND",
            stock_status: "Còn trong kho",
            specs: { "Quốc gia": "Australia", "Nồng độ": "15,0%" },
            main_image_url: "https://vineyard.vn/userfiles/images/SanPham/RuouVang/VangDo/PAVO%20No_1%20Shiraz.png",
            gallery_image_urls: []
          }
        ]);
      });
  }, []);

  const handleAddToCart = (product: WineProduct) => {
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

  const handleUpdateQuantity = (id: number, delta: number) => {
    setCartItems((prev) =>
      prev
        .map((item) => {
          if (item.product.id === id) {
            const newQ = item.quantity + delta;
            return newQ > 0 ? { ...item, quantity: newQ } : null;
          }
          return item;
        })
        .filter(Boolean) as CartItem[]
    );
  };

  const handleRemoveItem = (id: number) => {
    setCartItems((prev) => prev.filter((item) => item.product.id !== id));
  };

  const filteredProducts = filterCountry === "All"
    ? products
    : products.filter((p) => p.origin_country?.toLowerCase() === filterCountry.toLowerCase());

  return (
    <div className="flex-1 flex flex-col bg-cellar-950 text-alabaster">
      <Header
        cartCount={cartItems.reduce((sum, item) => sum + item.quantity, 0)}
        onOpenCart={() => setIsCartOpen(true)}
      />

      {/* Hero Showcase Section */}
      <section className="relative min-h-[580px] lg:min-h-[640px] flex items-center justify-center bg-gradient-to-b from-cellar-950 via-cellar-900 to-cellar-950 border-b border-cellar-800/80 px-4 sm:px-6 overflow-hidden">
        {/* Subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-bordeaux/20 rounded-full blur-[140px] pointer-events-none" />

        <div className="max-w-5xl mx-auto text-center relative z-10 py-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-champagne/40 bg-cellar-900/80 text-champagne text-xs font-mono uppercase tracking-widest mb-6 backdrop-blur-sm">
            <Sparkles className="w-3.5 h-3.5" /> Bộ Sưu Tập Rượu Vang Thượng Hạng 2026
          </div>

          <h1 className="font-serif text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-alabaster leading-[1.1] mb-6">
            Tuyệt Tác Thổ Nhưỡng <br />
            <span className="bg-gradient-to-r from-champagne via-champagne-light to-alabaster bg-clip-text text-transparent">
              Tinh Hoa Hầm Rượu Vang
            </span>
          </h1>

          <p className="max-w-2xl mx-auto text-base sm:text-lg text-alabaster-muted font-sans font-light leading-relaxed mb-10">
            Khám phá hơn 100+ dòng vang danh giá từ các điền trang lâu đời bậc nhất nước Ý, Pháp, Chile và Úc. Lưu trữ và bảo quản tiêu chuẩn hầm rượu quốc tế.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4">
            <a
              href="#catalog"
              className="px-8 py-4 rounded-xl bg-bordeaux hover:bg-bordeaux-hover text-champagne-light font-serif font-semibold tracking-wider text-sm transition-all shadow-xl hover:shadow-bordeaux/30 flex items-center gap-2"
            >
              <span>KHÁM PHÁ HẦM RƯỢU</span>
              <ArrowRight className="w-4 h-4" />
            </a>
            <a
              href="tel:0969843286"
              className="px-8 py-4 rounded-xl border border-cellar-700 bg-cellar-900/70 hover:border-champagne/60 text-alabaster font-sans font-medium text-sm transition-all"
            >
              TƯ VẤN VỚI SOMMELIER
            </a>
          </div>
        </div>
      </section>

      {/* Brand Pillars & Trust Assurance */}
      <section className="border-b border-cellar-800 bg-cellar-900/60 py-10 px-4 sm:px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="flex items-center gap-4 p-4 rounded-xl bg-cellar-950/40 border border-cellar-800/80">
            <div className="w-12 h-12 rounded-lg bg-bordeaux/30 border border-bordeaux-light/40 flex items-center justify-center text-champagne">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-serif text-base font-semibold text-alabaster">100% Nhập Khẩu Nguyên Chai</h4>
              <p className="text-xs text-alabaster-muted mt-0.5">Đầy đủ tem kiểm định & hồ sơ xuất xứ chính ngạch.</p>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 rounded-xl bg-cellar-950/40 border border-cellar-800/80">
            <div className="w-12 h-12 rounded-lg bg-bordeaux/30 border border-bordeaux-light/40 flex items-center justify-center text-champagne">
              <ThermometerSnowflake className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-serif text-base font-semibold text-alabaster">Hầm Chuẩn 16°C – 18°C</h4>
              <p className="text-xs text-alabaster-muted mt-0.5">Kiểm soát nhiệt độ & độ ẩm tối ưu 24/7 bảo vệ hương vị.</p>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 rounded-xl bg-cellar-950/40 border border-cellar-800/80">
            <div className="w-12 h-12 rounded-lg bg-bordeaux/30 border border-bordeaux-light/40 flex items-center justify-center text-champagne">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-serif text-base font-semibold text-alabaster">Chuyên Gia Sommelier WSET</h4>
              <p className="text-xs text-alabaster-muted mt-0.5">Tư vấn chọn rượu kết hợp món ăn và tiệc doanh nghiệp.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Catalog Showcase */}
      <section id="catalog" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 flex-1 w-full">
        {/* Section Heading & Filter Bar */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div>
            <div className="text-xs font-mono text-champagne uppercase tracking-widest mb-2 flex items-center gap-1.5">
              <Wine className="w-4 h-4" /> Danh Mục Thực Tế Đã Khảo Sát
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl font-bold text-alabaster">
              Bộ Sưu Tập Rượu Vang Tuyển Chọn
            </h2>
          </div>

          {/* Quick Filter Pills */}
          <div className="flex flex-wrap items-center gap-2">
            {["All", "Italy", "France", "Chile", "Australia"].map((country) => (
              <button
                key={country}
                onClick={() => setFilterCountry(country)}
                className={`px-4 py-2 rounded-full text-xs font-medium tracking-wide transition-all ${
                  filterCountry === country
                    ? "bg-champagne text-cellar-950 font-bold shadow-md"
                    : "bg-cellar-900 border border-cellar-800 text-alabaster-muted hover:border-champagne/40 hover:text-alabaster"
                }`}
              >
                {country === "All" ? "Tất Cả" : country}
              </button>
            ))}
          </div>
        </div>

        {/* Product Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredProducts.map((p) => (
            <ProductCard key={p.id || p.slug} product={p} onAddToCart={handleAddToCart} />
          ))}
        </div>
      </section>

      {/* Footer & Compliance Notice */}
      <footer className="border-t border-cellar-800 bg-cellar-950 text-alabaster-muted py-14 px-4 sm:px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          <div className="md:col-span-2 space-y-4">
            <span className="font-serif text-2xl font-bold text-alabaster tracking-widest block">VINEYARD</span>
            <p className="text-xs leading-relaxed max-w-sm">
              Đơn vị nhập khẩu và phân phối độc quyền các dòng rượu vang và đồ uống cao cấp chính hãng từ các nhà làm vang hàng đầu thế giới.
            </p>
            <div className="text-xs text-cellar-700 font-mono">
              © 2026 VINEYARD.VN • Hệ thống khảo sát & hiện đại hóa VINEYARD 2.0
            </div>
          </div>

          <div className="space-y-2 text-xs">
            <h5 className="font-serif text-sm font-semibold text-alabaster uppercase tracking-wider mb-3">Danh Mục</h5>
            <Link href="/danh-muc/vang-do" className="block hover:text-champagne transition">Rượu Vang Đỏ</Link>
            <Link href="/danh-muc/vang-trang" className="block hover:text-champagne transition">Rượu Vang Trắng</Link>
            <Link href="/danh-muc/vang-cao-cap" className="block hover:text-champagne transition">Vang Thượng Hạng</Link>
            <Link href="/danh-muc/ruou-manh" className="block hover:text-champagne transition">Rượu Mạnh & Spirits</Link>
          </div>

          <div className="space-y-2 text-xs">
            <h5 className="font-serif text-sm font-semibold text-alabaster uppercase tracking-wider mb-3">Liên Hệ Showroom</h5>
            <p>Hotline: 0969.843.286</p>
            <p>Website gốc: https://vineyard.vn/</p>
            <p>Trạng thái kiểm toán: Hoàn thành 100% cục bộ</p>
          </div>
        </div>

        {/* Legal Disclaimer */}
        <div className="max-w-7xl mx-auto pt-8 border-t border-cellar-800 text-center text-[11px] text-cellar-700 leading-relaxed font-sans">
          CẢNH BÁO: Rượu bia có thể gây nghiện và có hại cho sức khỏe. Uống có trách nhiệm. Không lái xe sau khi sử dụng đồ uống có cồn. Sản phẩm chỉ dành cho người đủ 18 tuổi trở lên.
        </div>
      </footer>

      {/* Cart Slide-Over Drawer */}
      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        items={cartItems}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveItem}
        onClearCart={() => setCartItems([])}
      />
    </div>
  );
}
