"use client";

import React from "react";
import Link from "next/link";
import { WineProduct } from "@/types/wine";
import { Wine, Plus, Sparkles, MapPin } from "lucide-react";

interface ProductCardProps {
  product: WineProduct;
  onAddToCart?: (p: WineProduct) => void;
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const priceDisplay = product.sale_price
    ? `${product.sale_price.toLocaleString("vi-VN")} ₫`
    : "Liên hệ tư vấn";

  return (
    <div className="group relative bg-cellar-900 border border-cellar-800 rounded-xl overflow-hidden hover:border-champagne/40 transition-all duration-300 flex flex-col justify-between shadow-lg hover:shadow-2xl hover:-translate-y-1">
      {/* Top badges */}
      <div className="absolute top-3 left-3 right-3 z-10 flex items-center justify-between pointer-events-none">
        {product.origin_country ? (
          <span className="bg-cellar-950/80 backdrop-blur-sm border border-cellar-700 text-alabaster-muted text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1">
            <MapPin className="w-3 h-3 text-champagne" />
            {product.origin_country}
          </span>
        ) : <div />}

        {product.abv && (
          <span className="bg-bordeaux/80 backdrop-blur-sm border border-bordeaux-light text-champagne-light text-[11px] font-bold px-2 py-0.5 rounded-full">
            {product.abv}
          </span>
        )}
      </div>

      {/* Wine Bottle Image Container */}
      <Link
        href={`/san-pham/${product.slug}`}
        className="block relative aspect-[3/4] p-6 bg-gradient-to-b from-cellar-900 to-cellar-950 flex items-center justify-center overflow-hidden"
      >
        {product.main_image_url ? (
          <img
            src={product.main_image_url}
            alt={product.name}
            className="max-h-[85%] max-w-[85%] object-contain drop-shadow-[0_15px_15px_rgba(0,0,0,0.7)] group-hover:scale-105 transition-transform duration-500 ease-out"
            loading="lazy"
          />
        ) : (
          <div className="flex flex-col items-center justify-center text-cellar-700">
            <Wine className="w-16 h-16 stroke-1 mb-2" />
            <span className="text-xs">Chưa có ảnh</span>
          </div>
        )}
      </Link>

      {/* Details Section */}
      <div className="p-5 flex flex-col flex-grow justify-between border-t border-cellar-800/60 bg-cellar-900">
        <div>
          {/* Brand & Vintage */}
          <div className="flex items-center justify-between text-xs text-champagne font-sans tracking-wider mb-1.5 uppercase">
            <span>{product.brand || "Vineyard Selection"}</span>
            {product.vintage && <span className="font-mono text-alabaster-muted">{product.vintage}</span>}
          </div>

          {/* Product Name */}
          <Link href={`/san-pham/${product.slug}`}>
            <h3 className="font-serif text-base font-semibold text-alabaster group-hover:text-champagne transition-colors line-clamp-2 leading-snug mb-2">
              {product.name}
            </h3>
          </Link>

          {/* Grape & Region Subtext */}
          <p className="text-xs text-alabaster-muted font-sans line-clamp-1 mb-4">
            {product.grape_variety ? `${product.grape_variety} • ` : ""}
            {product.region || product.origin_country || "Vang Nhập Khẩu"}
          </p>
        </div>

        {/* Price & Action Button */}
        <div className="flex items-center justify-between pt-3 border-t border-cellar-800">
          <div>
            <span className="text-xs text-alabaster-muted/70 block font-sans">Giá bán</span>
            <span className="text-base font-semibold text-alabaster font-mono">
              {priceDisplay}
            </span>
          </div>

          <button
            onClick={() => onAddToCart && onAddToCart(product)}
            className="p-2.5 rounded-lg bg-bordeaux hover:bg-bordeaux-hover text-alabaster transition-colors flex items-center justify-center shadow"
            title="Thêm vào giỏ hàng"
            aria-label="Thêm vào giỏ hàng"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
