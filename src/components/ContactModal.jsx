import React, { useState } from 'react';
import { X, Phone, Mail, MessageSquare, Calendar, ShieldCheck, Check } from 'lucide-react';

export default function ContactModal({ property, onClose }) {
  const [sent, setSent] = useState(false);
  const [formData, setFormData] = useState({
    name: 'Guangming Guest',
    email: '',
    phone: '',
    message: `Hello, I am interested in booking "${property.title}" in Nice. Could you please confirm availability?`
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => {
      setSent(false);
      onClose();
    }, 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs animate-in fade-in duration-200">
      <div 
        className="bg-white rounded-3xl max-w-lg w-full shadow-2xl border border-zinc-100 overflow-hidden transform animate-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 pb-4 border-b border-zinc-100 flex items-start justify-between">
          <div className="flex items-center gap-3">
            <img
              src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80"
              alt={property.host?.name || "Host"}
              className="w-12 h-12 rounded-full object-cover ring-2 ring-zinc-100"
            />
            <div>
              <div className="flex items-center gap-1.5">
                <h3 className="font-bold text-zinc-950 text-base">{property.host?.name || 'Guangming'}</h3>
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
              </div>
              <p className="text-xs text-zinc-400">
                {property.host?.title || 'Premier Verified Host'} • Responds {property.host?.responseTime || 'within 1h'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-zinc-100 hover:bg-zinc-200 text-zinc-500 hover:text-zinc-900 flex items-center justify-center transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {sent ? (
            <div className="py-8 flex flex-col items-center text-center">
              <div className="w-14 h-14 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mb-3">
                <Check className="w-7 h-7" />
              </div>
              <h4 className="text-lg font-bold text-zinc-900 mb-1">Message Sent!</h4>
              <p className="text-xs text-zinc-500 max-w-xs">
                The host has received your inquiry and will contact you back via phone or email shortly.
              </p>
            </div>
          ) : (
            <>
              {/* Quick Contact Buttons */}
              <div className="grid grid-cols-2 gap-3 mb-5">
                <a
                  href={`tel:${property.host?.phone || '+33493123456'}`}
                  className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-2xl bg-zinc-50 hover:bg-zinc-100 border border-zinc-200/80 text-xs font-semibold text-zinc-800 transition-colors"
                >
                  <Phone className="w-3.5 h-3.5 text-zinc-700" />
                  <span>Call {property.host?.phone || '+33 4 93...'}</span>
                </a>

                <a
                  href={`mailto:${property.host?.email || 'contact@estates.io'}?subject=Inquiry for ${property.title}`}
                  className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-2xl bg-zinc-50 hover:bg-zinc-100 border border-zinc-200/80 text-xs font-semibold text-zinc-800 transition-colors"
                >
                  <Mail className="w-3.5 h-3.5 text-zinc-700" />
                  <span>Send Email</span>
                </a>
              </div>

              {/* Message Form */}
              <form onSubmit={handleSubmit} className="space-y-3">
                <div>
                  <label className="block text-[11px] font-semibold text-zinc-600 mb-1">Your Contact Details</label>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="text"
                      placeholder="Your name"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full text-xs px-3 py-2 rounded-xl border border-zinc-200 focus:outline-none focus:ring-2 focus:ring-zinc-900"
                    />
                    <input
                      type="email"
                      placeholder="Your email / phone"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      className="w-full text-xs px-3 py-2 rounded-xl border border-zinc-200 focus:outline-none focus:ring-2 focus:ring-zinc-900"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-zinc-600 mb-1">Message to Host</label>
                  <textarea
                    rows={3}
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    className="w-full text-xs p-3 rounded-xl border border-zinc-200 focus:outline-none focus:ring-2 focus:ring-zinc-900 resize-none"
                  />
                </div>

                <div className="pt-2 flex items-center justify-between">
                  <div className="text-[11px] text-zinc-400">
                    Estates Verified Guarantee
                  </div>
                  <button
                    type="submit"
                    className="bg-black hover:bg-zinc-800 text-white text-xs font-bold px-6 py-2.5 rounded-full transition-all cursor-pointer shadow-sm"
                  >
                    Send Direct Message
                  </button>
                </div>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
