"use client";

import React, { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { WineProduct } from "@/types/wine";
import { Header } from "@/components/Header";
import { CartDrawer } from "@/components/CartDrawer";
import { Wine, MapPin, Award, CheckCircle2, Phone, ArrowLeft, ShieldAlert } from "lucide-react";
import Link from "next/link";

export default function ProductDetailPage() {
  const params = useParams();
  const slug = params?.slug as string;
  const [product, setProduct] = useState<WineProduct | null>(null);
  const [cartItems, setCartItems] = useState<any[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  useEffect(() => {
    fetch("/products.json")
      .then((res) => res.json())
      .then((data: WineProduct[]) => {
        const found = data.find((p) => p.slug === slug);
        if (found) setProduct(found);
      })
      .catch((err) => console.error("Error loading product detail:", err));
  }, [slug]);

  if (!product) {
    return (
      <div className="min-h-screen bg-cellar-950 text-alabaster flex flex-col justify-between">
        <Header />
        <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
          <Wine className="w-16 h-16 text-champagne animate-pulse mb-4" />
          <h2 className="font-serif text-2xl font-bold">Đang tải thông tin chai vang...</h2>
          <Link href="/" className="mt-4 text-xs font-mono text-champagne hover:underline">
            ← Quay lại trang chủ
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cellar-950 text-alabaster flex flex-col justify-between">
      <Header
        cartCount={cartItems.reduce((sum, item) => sum + item.quantity, 0)}
        onOpenCart={() => setIsCartOpen(true)}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 flex-1 w-full">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-xs font-mono text-alabaster-muted hover:text-champagne transition mb-8"
        >
          <ArrowLeft className="w-4 h-4" /> Quay lại bộ sưu tập
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16">
          {/* Left: Wine Bottle Image Stage */}
          <div className="relative aspect-[3/4] max-h-[600px] bg-gradient-to-b from-cellar-900 to-cellar-950 rounded-2xl border border-cellar-800 p-8 flex items-center justify-center overflow-hidden shadow-2xl">
            <div className="absolute inset-0 bg-bordeaux/10 rounded-2xl pointer-events-none" />
            {product.main_image_url ? (
              <img
                src={product.main_image_url}
                alt={product.name}
                className="max-h-full max-w-full object-contain drop-shadow-[0_25px_25px_rgba(0,0,0,0.8)]"
              />
            ) : (
              <Wine className="w-24 h-24 text-cellar-700" />
            )}
          </div>

          {/* Right: Wine Specs & Tasting Info */}
          <div className="flex flex-col justify-between space-y-6">
            <div>
              {/* Badges & Provenance */}
              <div className="flex flex-wrap items-center gap-2 text-xs font-mono text-champagne mb-3">
                <span className="uppercase tracking-widest">{product.brand || "Selection"}</span>
                {product.vintage && <span>• Niên vụ {product.vintage}</span>}
                {product.sku && (
                  <span className="text-alabaster-muted bg-cellar-900 border border-cellar-800 px-2.5 py-0.5 rounded-full">
                    SKU: {product.sku}
                  </span>
                )}
              </div>

              {/* Title */}
              <h1 className="font-serif text-3xl sm:text-4xl font-bold text-alabaster leading-tight mb-4">
                {product.name}
              </h1>

              {/* Price & Stock */}
              <div className="p-4 rounded-xl bg-cellar-900 border border-cellar-800 mb-6 flex items-center justify-between">
                <div>
                  <span className="text-xs text-alabaster-muted block font-sans">Giá bán tiêu chuẩn</span>
                  <span className="text-2xl font-bold font-mono text-champagne">
                    {product.sale_price
                      ? `${product.sale_price.toLocaleString("vi-VN")} ₫`
                      : "Liên hệ Sommelier"}
                  </span>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>{product.stock_status || "Còn hàng"}</span>
                </div>
              </div>

              {/* Key Specs Table Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
                {product.origin_country && (
                  <div className="p-3 bg-cellar-900/60 rounded-lg border border-cellar-800">
                    <span className="text-[11px] text-alabaster-muted block">Quốc gia</span>
                    <span className="text-sm font-semibold text-alabaster">{product.origin_country}</span>
                  </div>
                )}
                {product.region && (
                  <div className="p-3 bg-cellar-900/60 rounded-lg border border-cellar-800">
                    <span className="text-[11px] text-alabaster-muted block">Vùng sản xuất</span>
                    <span className="text-sm font-semibold text-alabaster">{product.region}</span>
                  </div>
                )}
                {product.grape_variety && (
                  <div className="p-3 bg-cellar-900/60 rounded-lg border border-cellar-800">
                    <span className="text-[11px] text-alabaster-muted block">Giống nho</span>
                    <span className="text-sm font-semibold text-alabaster">{product.grape_variety}</span>
                  </div>
                )}
                {product.abv && (
                  <div className="p-3 bg-cellar-900/60 rounded-lg border border-cellar-800">
                    <span className="text-[11px] text-alabaster-muted block">Nồng độ cồn</span>
                    <span className="text-sm font-semibold text-alabaster">{product.abv}</span>
                  </div>
                )}
                {product.volume && (
                  <div className="p-3 bg-cellar-900/60 rounded-lg border border-cellar-800">
                    <span className="text-[11px] text-alabaster-muted block">Dung tích</span>
                    <span className="text-sm font-semibold text-alabaster">{product.volume}</span>
                  </div>
                )}
                {product.producer && (
                  <div className="p-3 bg-cellar-900/60 rounded-lg border border-cellar-800">
                    <span className="text-[11px] text-alabaster-muted block">Nhà sản xuất</span>
                    <span className="text-sm font-semibold text-alabaster">{product.producer}</span>
                  </div>
                )}
              </div>

              {/* Tasting Notes */}
              {product.tasting_notes && (
                <div className="p-4 rounded-xl bg-cellar-900 border border-bordeaux/40 mb-6">
                  <h4 className="font-serif text-sm font-semibold text-champagne mb-2 flex items-center gap-1.5">
                    <Award className="w-4 h-4" /> Ghi Chú Thử Nếm (Sommelier Tasting Notes)
                  </h4>
                  <p className="text-xs text-alabaster-muted leading-relaxed whitespace-pre-line font-sans">
                    {product.tasting_notes}
                  </p>
                </div>
              )}
            </div>

            {/* CTA Consultation Button */}
            <div className="space-y-3">
              <button
                onClick={() => {
                  setCartItems([{ product, quantity: 1 }]);
                  setIsCartOpen(true);
                }}
                className="w-full bg-bordeaux hover:bg-bordeaux-hover text-champagne-light py-4 rounded-xl font-serif font-bold text-sm tracking-wider transition-all shadow-xl flex items-center justify-center gap-2"
              >
                <span>THÊM VÀO DANH SÁCH TƯ VẤN THƯỞNG THỨC</span>
              </button>

              <div className="flex items-center justify-center gap-2 text-xs text-cellar-700">
                <ShieldAlert className="w-3.5 h-3.5" />
                <span>Nguồn gốc: {product.source_url}</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        items={cartItems}
        onUpdateQuantity={() => {}}
        onRemoveItem={() => setCartItems([])}
        onClearCart={() => setCartItems([])}
      />
    </div>
  );
}
