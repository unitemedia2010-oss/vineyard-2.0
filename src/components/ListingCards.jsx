import React, { useState } from 'react';
import { Heart, Bed, Bath, Maximize2 } from 'lucide-react';

export default function ListingCards({
  properties,
  selectedProperty,
  onSelectProperty
}) {
  const [favorites, setFavorites] = useState({});

  const toggleFavorite = (e, propId) => {
    e.stopPropagation();
    setFavorites((prev) => ({
      ...prev,
      [propId]: !prev[propId]
    }));
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 select-none">
      {properties.map((item) => {
        const isSelected = selectedProperty?.id === item.id;
        const isFavorited = favorites[item.id];

        return (
          <div
            key={item.id}
            onClick={() => onSelectProperty?.(item)}
            className={`group bg-white rounded-2xl p-2.5 transition-all duration-200 cursor-pointer flex flex-col justify-between ${
              isSelected
                ? 'ring-2 ring-zinc-950 shadow-md'
                : 'border border-zinc-100 hover:border-zinc-300 shadow-xs hover:shadow-sm'
            }`}
          >
            {/* Top thumbnail image */}
            <div className="relative w-full aspect-[16/10] rounded-xl overflow-hidden bg-zinc-100 mb-2.5">
              <img
                src={item.images?.[0]}
                alt={item.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>

            {/* Price & Favorite row */}
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-baseline gap-1">
                <span className="text-sm font-extrabold text-zinc-950">
                  {item.priceDisplay}
                </span>
                <span className="text-[11px] font-normal text-zinc-400">
                  {item.priceUnit || '/ night'}
                </span>
              </div>

              <button
                onClick={(e) => toggleFavorite(e, item.id)}
                className="p-1 rounded-full text-zinc-300 hover:text-rose-500 transition-colors cursor-pointer"
                aria-label="Add to favorites"
              >
                <Heart
                  className={`w-4 h-4 transition-all ${
                    isFavorited
                      ? 'fill-rose-500 text-rose-500 scale-110'
                      : 'stroke-[2] hover:stroke-rose-500'
                  }`}
                />
              </button>
            </div>

            {/* Address */}
            <div className="text-[11px] text-zinc-400 font-medium truncate mb-2.5">
              {item.shortAddress || item.address}
            </div>

            {/* Amenities icons */}
            <div className="flex items-center gap-3 pt-1 border-t border-zinc-100/80 text-[11px] text-zinc-600 font-semibold">
              <div className="flex items-center gap-1">
                <Bed className="w-3.5 h-3.5 text-zinc-400 stroke-[2]" />
                <span>{item.beds}</span>
              </div>

              <div className="flex items-center gap-1">
                <Bath className="w-3.5 h-3.5 text-zinc-400 stroke-[2]" />
                <span>{item.baths}</span>
              </div>

              <div className="flex items-center gap-1">
                <Maximize2 className="w-3 h-3 text-zinc-400 stroke-[2]" />
                <span>{item.areaMetric || '60 m²'}</span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
