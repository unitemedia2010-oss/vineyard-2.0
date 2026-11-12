"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Search, ShoppingBag, Menu, X, Phone, Wine, Sparkles } from "lucide-react";

interface HeaderProps {
  cartCount?: number;
  onOpenCart?: () => void;
}

export function Header({ cartCount = 0, onOpenCart }: HeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 bg-cellar-950/90 backdrop-blur-md border-b border-cellar-800 text-alabaster transition-all">
      {/* Top Banner Alert / 18+ Notification */}
      <div className="bg-bordeaux px-4 py-1.5 text-center text-xs tracking-wider font-medium text-champagne-light flex items-center justify-center gap-2">
        <Sparkles className="w-3.5 h-3.5 text-champagne" />
        <span>VINEYARD 2.0 • TUYỂN CHỌN RƯỢU VANG CAO CẤP NHẬP KHẨU NGUYÊN CHAI CHÍNH HÃNG</span>
        <span className="hidden md:inline font-mono opacity-80">(Chỉ dành cho người trên 18 tuổi)</span>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Mobile menu trigger */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="lg:hidden p-2 text-alabaster hover:text-champagne transition"
          aria-label="Open menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>

        {/* Brand Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-full border border-champagne/40 bg-cellar-900 flex items-center justify-center group-hover:border-champagne transition-colors">
            <Wine className="w-5 h-5 text-champagne" />
          </div>
          <div>
            <span className="font-serif text-2xl font-bold tracking-widest text-alabaster block leading-none">
              VINEYARD
            </span>
            <span className="text-[10px] tracking-[0.25em] text-champagne uppercase font-sans">
              Grand Cru Cellar
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden lg:flex items-center gap-8 font-sans text-sm tracking-wide">
          <Link href="/danh-muc/ruou-vang" className="hover:text-champagne transition-colors py-2">
            Rượu Vang
          </Link>
          <Link href="/danh-muc/vang-do" className="hover:text-champagne transition-colors py-2">
            Vang Đỏ
          </Link>
          <Link href="/danh-muc/vang-trang" className="hover:text-champagne transition-colors py-2">
            Vang Trắng
          </Link>
          <Link href="/danh-muc/vang-cao-cap" className="hover:text-champagne transition-colors py-2 text-champagne flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5" /> Vang Thượng Hạng
          </Link>
          <Link href="/danh-muc/ruou-manh" className="hover:text-champagne transition-colors py-2">
            Rượu Mạnh
          </Link>
          <Link href="/ve-chung-toi" className="hover:text-champagne transition-colors py-2">
            Về Vineyard
          </Link>
        </nav>

        {/* Right Actions: Hotline, Search & Cart Drawer Trigger */}
        <div className="flex items-center gap-4">
          <a
            href="tel:0969843286"
            className="hidden sm:flex items-center gap-2 text-xs font-medium text-alabaster-muted hover:text-champagne transition border border-cellar-800 rounded-full px-3 py-1.5 bg-cellar-900"
          >
            <Phone className="w-3.5 h-3.5 text-champagne" />
            <span>0969.843.286</span>
          </a>

          <button
            onClick={onOpenCart}
            className="relative p-2.5 rounded-full bg-cellar-900 border border-cellar-800 hover:border-champagne/60 text-alabaster transition-all group"
            aria-label="Xem giỏ hàng"
          >
            <ShoppingBag className="w-5 h-5 group-hover:text-champagne transition-colors" />
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-bordeaux text-champagne-light text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center border border-cellar-950">
                {cartCount}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-cellar-900 border-b border-cellar-800 px-6 py-4 space-y-3 font-sans">
          <Link
            href="/danh-muc/ruou-vang"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-alabaster hover:text-champagne py-2 text-base"
          >
            Tất Cả Rượu Vang
          </Link>
          <Link
            href="/danh-muc/vang-do"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-alabaster hover:text-champagne py-2 text-base"
          >
            Vang Đỏ (Red Wine)
          </Link>
          <Link
            href="/danh-muc/vang-trang"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-alabaster hover:text-champagne py-2 text-base"
          >
            Vang Trắng (White Wine)
          </Link>
          <Link
            href="/danh-muc/vang-cao-cap"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-champagne hover:underline py-2 text-base font-medium"
          >
            Vang Thượng Hạng (Icon Wines)
          </Link>
        </div>
      )}
    </header>
  );
}
