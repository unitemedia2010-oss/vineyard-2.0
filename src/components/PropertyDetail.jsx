import React, { useState } from 'react';
import { 
  Star, 
  Share2, 
  MapPin, 
  Bed, 
  Bath, 
  Armchair, 
  Maximize2, 
  MoreHorizontal, 
  ChevronLeft, 
  ChevronRight,
  Compass,
  Check
} from 'lucide-react';

export default function PropertyDetail({
  property,
  onShowContacts,
  onOpenVirtualTour,
  onShare
}) {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const [copiedToast, setCopiedToast] = useState(false);

  const images = property?.images || [
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80"
  ];

  const handleNextImage = (e) => {
    e.stopPropagation();
    setCurrentImageIndex((prev) => (prev + 1) % images.length);
  };

  const handlePrevImage = (e) => {
    e.stopPropagation();
    setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  const handleShareClick = () => {
    if (onShare) {
      onShare(property);
    } else {
      navigator.clipboard?.writeText(window.location.href);
      setCopiedToast(true);
      setTimeout(() => setCopiedToast(false), 2500);
    }
  };

  return (
    <div className="bg-white rounded-[24px] p-5 shadow-xs border border-zinc-100/80 transition-all duration-300">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-5 items-stretch">
        
        {/* Left Side: Photo Carousel (approx 5 cols) */}
        <div className="md:col-span-6 lg:col-span-5 relative group">
          <div className="relative w-full aspect-[4/3] md:aspect-auto md:h-full min-h-[260px] rounded-[20px] overflow-hidden bg-zinc-100 select-none">
            {/* Active Image */}
            <img
              src={images[currentImageIndex]}
              alt={property.title}
              className="w-full h-full object-cover transition-all duration-500 hover:scale-105"
            />

            {/* Gradient overlay for contrast */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-black/15 pointer-events-none" />

            {/* Top-Left: Rating Badge */}
            <div className="absolute top-3.5 left-3.5 z-10">
              <div className="flex items-center gap-1 bg-white/95 backdrop-blur-md px-2.5 py-1 rounded-full shadow-sm text-zinc-900 text-xs font-bold">
                <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                <span>{property.rating || '4.8'}</span>
              </div>
            </div>

            {/* Top-Right: 360 Virtual Tour Button */}
            <div className="absolute top-3.5 right-3.5 z-10">
              <button
                onClick={onOpenVirtualTour}
                className="w-8 h-8 rounded-full bg-white/95 backdrop-blur-md text-zinc-800 hover:text-black hover:bg-white shadow-sm flex items-center justify-center transition-all hover:scale-110 cursor-pointer"
                title="360° Virtual Tour"
              >
                {/* 360 icon */}
                <svg viewBox="0 0 24 24" className="w-4 h-4 fill-none stroke-current stroke-2">
                  <circle cx="12" cy="12" r="9" />
                  <ellipse cx="12" cy="12" rx="4" ry="9" strokeDasharray="2 2" />
                  <path d="M7 12h10" />
                </svg>
              </button>
            </div>

            {/* Hover Next/Prev Arrows */}
            <button
              onClick={handlePrevImage}
              className="absolute left-2.5 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-white/80 hover:bg-white text-zinc-800 shadow-md opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center cursor-pointer"
              title="Previous image"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={handleNextImage}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-white/80 hover:bg-white text-zinc-800 shadow-md opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center cursor-pointer"
              title="Next image"
            >
              <ChevronRight className="w-4 h-4" />
            </button>

            {/* Bottom Carousel Dots: ◉ ○ ○ ○ ○ */}
            <div className="absolute bottom-3 left-0 right-0 flex items-center justify-center gap-1.5 z-10">
              {images.map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => setCurrentImageIndex(idx)}
                  className={`transition-all duration-200 cursor-pointer ${
                    currentImageIndex === idx
                      ? 'w-2.5 h-2.5 rounded-full border-2 border-white bg-transparent scale-110'
                      : 'w-1.5 h-1.5 rounded-full bg-white/70 hover:bg-white'
                  }`}
                  aria-label={`Go to slide ${idx + 1}`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Right Side: Information & Actions (approx 7 cols) */}
        <div className="md:col-span-6 lg:col-span-7 flex flex-col justify-between py-1">
          <div>
            {/* Top row: Most popular & Share */}
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wide">
                {property.isPopular ? 'Most popular' : 'Featured Listing'}
              </span>

              <div className="relative">
                <button
                  onClick={handleShareClick}
                  className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-900 transition-colors font-medium cursor-pointer"
                >
                  <span>Share</span>
                  <Share2 className="w-3.5 h-3.5" />
                </button>

                {copiedToast && (
                  <div className="absolute right-0 -bottom-8 bg-zinc-900 text-white text-[11px] px-2.5 py-1 rounded-md shadow-lg whitespace-nowrap flex items-center gap-1 animate-in fade-in">
                    <Check className="w-3 h-3 text-emerald-400" />
                    <span>Link copied!</span>
                  </div>
                )}
              </div>
            </div>

            {/* Listing Title */}
            <h2 className="text-xl lg:text-[22px] font-extrabold text-zinc-950 tracking-tight leading-snug mb-1">
              {property.title}
            </h2>

            {/* Address */}
            <div className="flex items-center gap-1.5 text-zinc-400 text-xs mb-4">
              <MapPin className="w-3.5 h-3.5 shrink-0 text-zinc-400 stroke-[2]" />
              <span className="truncate">{property.address}</span>
            </div>

            {/* Amenities Grid/Row */}
            <div className="inline-flex items-center gap-4 bg-zinc-50/80 border border-zinc-100 rounded-xl px-3.5 py-2 mb-4 text-xs font-semibold text-zinc-700">
              {/* Bed */}
              <div className="flex items-center gap-1.5">
                <Bed className="w-4 h-4 text-zinc-400 stroke-[2]" />
                <span>{property.beds}</span>
              </div>

              {/* Bath */}
              <div className="flex items-center gap-1.5">
                <Bath className="w-4 h-4 text-zinc-400 stroke-[2]" />
                <span>{property.baths}</span>
              </div>

              {/* Armchair / Living room */}
              <div className="flex items-center gap-1.5">
                <Armchair className="w-4 h-4 text-zinc-400 stroke-[2]" />
                <span>{property.livingRooms || 1}</span>
              </div>

              {/* Area */}
              <div className="flex items-center gap-1.5">
                <Maximize2 className="w-3.5 h-3.5 text-zinc-400 stroke-[2]" />
                <span className="whitespace-nowrap">{property.area || '1,250 ft²'}</span>
              </div>
            </div>

            {/* Description with "see details" */}
            <p className="text-xs text-zinc-500 leading-relaxed mb-4">
              {isExpanded ? property.fullDescription : property.description}{' '}
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="text-teal-600 font-semibold hover:underline cursor-pointer inline-flex items-center"
              >
                {isExpanded ? 'see less' : 'see details'}
              </button>
            </p>
          </div>

          {/* Bottom Price & CTA */}
          <div className="pt-2 border-t border-zinc-100 flex flex-wrap items-center justify-between gap-3">
            {/* Price */}
            <div className="flex items-baseline gap-1.5">
              <span className="text-xs text-zinc-400 font-medium">Rental price:</span>
              <span className="text-2xl font-black text-zinc-950 tracking-tight">
                {property.priceDisplay}
              </span>
              <span className="text-xs text-zinc-400 font-normal">
                {property.priceUnit || '/ night'}
              </span>
            </div>

            {/* Actions: Show contacts + more */}
            <div className="flex items-center gap-2">
              <button
                onClick={onShowContacts}
                className="bg-black hover:bg-zinc-800 text-white text-xs font-bold px-6 py-2.5 rounded-full shadow-sm hover:shadow-md transition-all cursor-pointer tracking-wide"
              >
                Show contacts
              </button>

              <button
                className="w-9 h-9 rounded-full border border-zinc-200/90 text-zinc-600 hover:text-black hover:bg-zinc-100/60 flex items-center justify-center transition-colors cursor-pointer"
                title="Options"
              >
                <MoreHorizontal className="w-4 h-4" />
              </button>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
