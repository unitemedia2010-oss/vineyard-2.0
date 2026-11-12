"use client";

import React, { useState } from "react";
import { CartItem } from "@/types/wine";
import { X, Trash2, Wine, Send, CheckCircle2 } from "lucide-react";

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  items: CartItem[];
  onUpdateQuantity: (id: number, delta: number) => void;
  onRemoveItem: (id: number) => void;
  onClearCart: () => void;
}

export function CartDrawer({
  isOpen,
  onClose,
  items,
  onUpdateQuantity,
  onRemoveItem,
  onClearCart
}: CartDrawerProps) {
  const [submitted, setSubmitted] = useState(false);
  const [customerName, setCustomerName] = useState("");
  const [phone, setPhone] = useState("");
  const [note, setNote] = useState("");

  if (!isOpen) return null;

  const totalCalculated = items.reduce((acc, item) => {
    return acc + (item.product.sale_price || 0) * item.quantity;
  }, 0);

  const handleSubmitInquiry = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customerName || !phone) return;
    setSubmitted(true);
    setTimeout(() => {
      onClearCart();
      setSubmitted(false);
      onClose();
    }, 3000);
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/75 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Drawer content */}
      <div className="relative w-full max-w-md bg-cellar-900 border-l border-cellar-800 text-alabaster shadow-2xl flex flex-col justify-between z-10 h-full font-sans">
        {/* Header */}
        <div className="p-6 border-b border-cellar-800 flex items-center justify-between bg-cellar-950">
          <div className="flex items-center gap-2">
            <Wine className="w-5 h-5 text-champagne" />
            <h2 className="font-serif text-xl font-bold tracking-wide">Danh Sách Tuyển Chọn ({items.length})</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-full hover:bg-cellar-800 text-alabaster-muted hover:text-alabaster transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {items.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center text-alabaster-muted py-12">
              <Wine className="w-16 h-16 stroke-1 text-cellar-700 mb-4" />
              <p className="font-serif text-lg text-alabaster">Hầm rượu của bạn đang trống</p>
              <p className="text-xs text-alabaster-muted mt-1 max-w-xs">
                Hãy khám phá các dòng vang thượng hạng từ Ý, Pháp, Chile và thêm vào danh sách tư vấn.
              </p>
            </div>
          ) : submitted ? (
            <div className="h-full flex flex-col items-center justify-center text-center py-12">
              <CheckCircle2 className="w-16 h-16 text-champagne mb-4 animate-bounce" />
              <h3 className="font-serif text-2xl font-bold text-alabaster">Đã Gửi Yêu Cầu Thành Công</h3>
              <p className="text-sm text-alabaster-muted mt-2 max-w-xs">
                Chuyên viên Sommelier của Vineyard sẽ liên hệ với quý khách trong vòng 15 phút để chuẩn bị rượu và giao hàng tận nơi.
              </p>
            </div>
          ) : (
            items.map((item) => (
              <div
                key={item.product.id}
                className="flex gap-4 p-3 bg-cellar-850 rounded-xl border border-cellar-800 items-center justify-between"
              >
                <div className="w-14 h-16 bg-cellar-950 rounded flex items-center justify-center p-1 border border-cellar-700">
                  {item.product.main_image_url ? (
                    <img
                      src={item.product.main_image_url}
                      alt={item.product.name}
                      className="max-h-full max-w-full object-contain"
                    />
                  ) : (
                    <Wine className="w-6 h-6 text-cellar-700" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <h4 className="font-serif text-sm font-semibold text-alabaster truncate">
                    {item.product.name}
                  </h4>
                  <span className="text-xs text-champagne font-mono block">
                    {item.product.sale_price
                      ? `${item.product.sale_price.toLocaleString("vi-VN")} ₫`
                      : "Liên hệ tư vấn"}
                  </span>
                  <div className="flex items-center gap-3 mt-2">
                    <button
                      onClick={() => onUpdateQuantity(item.product.id, -1)}
                      className="w-6 h-6 rounded bg-cellar-800 hover:bg-cellar-700 text-xs flex items-center justify-center"
                    >
                      -
                    </button>
                    <span className="text-xs font-mono font-bold">{item.quantity}</span>
                    <button
                      onClick={() => onUpdateQuantity(item.product.id, 1)}
                      className="w-6 h-6 rounded bg-cellar-800 hover:bg-cellar-700 text-xs flex items-center justify-center"
                    >
                      +
                    </button>
                  </div>
                </div>

                <button
                  onClick={() => onRemoveItem(item.product.id)}
                  className="p-2 text-cellar-700 hover:text-red-400 transition"
                  title="Xóa khỏi danh sách"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))
          )}
        </div>

        {/* Footer Checkout Simulation */}
        {items.length > 0 && !submitted && (
          <div className="p-6 border-t border-cellar-800 bg-cellar-950 space-y-4">
            <div className="flex justify-between items-center text-sm">
              <span className="text-alabaster-muted">Tạm tính ước tính:</span>
              <span className="font-serif text-lg font-bold text-champagne font-mono">
                {totalCalculated > 0 ? `${totalCalculated.toLocaleString("vi-VN")} ₫` : "Theo báo giá Sommelier"}
              </span>
            </div>

            <form onSubmit={handleSubmitInquiry} className="space-y-3 pt-2">
              <input
                type="text"
                placeholder="Họ và tên quý khách *"
                required
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                className="w-full bg-cellar-900 border border-cellar-800 rounded-lg px-3.5 py-2.5 text-xs text-alabaster placeholder:text-cellar-700 focus:outline-none focus:border-champagne"
              />
              <input
                type="tel"
                placeholder="Số điện thoại / Zalo *"
                required
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full bg-cellar-900 border border-cellar-800 rounded-lg px-3.5 py-2.5 text-xs text-alabaster placeholder:text-cellar-700 focus:outline-none focus:border-champagne"
              />
              <textarea
                placeholder="Ghi chú (yêu cầu ướp lạnh trước, hộp quà...)"
                rows={2}
                value={note}
                onChange={(e) => setNote(e.target.value)}
                className="w-full bg-cellar-900 border border-cellar-800 rounded-lg px-3.5 py-2 text-xs text-alabaster placeholder:text-cellar-700 focus:outline-none focus:border-champagne resize-none"
              />
              <button
                type="submit"
                className="w-full bg-bordeaux hover:bg-bordeaux-hover text-champagne-light py-3 rounded-lg font-serif font-bold tracking-wider text-sm flex items-center justify-center gap-2 transition shadow-lg"
              >
                <Send className="w-4 h-4" />
                <span>YÊU CẦU SOMMELIER TƯ VẤN & GIAO RƯỢU</span>
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
