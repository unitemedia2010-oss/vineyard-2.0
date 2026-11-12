import React, { useState } from 'react';
import { X, RotateCcw, Move, Compass, Eye, Check } from 'lucide-react';

export default function VirtualTourModal({ property, onClose }) {
  const [selectedRoom, setSelectedRoom] = useState(0);

  const rooms = [
    {
      name: "Living Room",
      image: property.images?.[0] || "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1600&q=80",
      description: "Sunlit panoramic view with custom mid-century furnishings."
    },
    {
      name: "Master Suite",
      image: property.images?.[3] || "https://images.unsplash.com/photo-1540518614846-7ede433c4550?auto=format&fit=crop&w=1600&q=80",
      description: "King bed, noise-canceling double glazing, ensuite wardrobe."
    },
    {
      name: "Dining & Kitchen",
      image: property.images?.[2] || "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1600&q=80",
      description: "Fully equipped with induction stove, espresso bar, and dishwasher."
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md animate-in fade-in duration-200">
      <div 
        className="bg-zinc-950 text-white rounded-3xl max-w-4xl w-full shadow-2xl border border-zinc-800 overflow-hidden transform animate-in zoom-in-95 duration-200 flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="px-6 py-4 border-b border-zinc-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-zinc-800 flex items-center justify-center text-teal-400">
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-sm text-zinc-100 flex items-center gap-2">
                360° Virtual Tour • {property.title}
              </h3>
              <p className="text-[11px] text-zinc-400">
                Interactive spatial view • Nice, France
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-zinc-800 hover:bg-zinc-700 text-zinc-400 hover:text-white flex items-center justify-center transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* 360 Viewport Simulation */}
        <div className="relative flex-1 min-h-[380px] bg-black overflow-hidden group">
          <img
            src={rooms[selectedRoom].image}
            alt={rooms[selectedRoom].name}
            className="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
          />

          {/* Compass / Pan Indicator */}
          <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-md rounded-full px-3 py-1.5 flex items-center gap-2 text-xs text-zinc-300">
            <Move className="w-3.5 h-3.5 animate-pulse text-teal-400" />
            <span>Interactive 360° Panorama</span>
          </div>

          {/* Room info overlay */}
          <div className="absolute bottom-4 left-4 right-4 bg-gradient-to-t from-black/80 via-black/40 to-transparent p-4 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h4 className="font-bold text-sm text-white">{rooms[selectedRoom].name}</h4>
              <p className="text-xs text-zinc-300">{rooms[selectedRoom].description}</p>
            </div>

            {/* Room switcher buttons */}
            <div className="flex items-center gap-2">
              {rooms.map((room, idx) => (
                <button
                  key={room.name}
                  onClick={() => setSelectedRoom(idx)}
                  className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                    selectedRoom === idx
                      ? 'bg-white text-zinc-900 shadow-md'
                      : 'bg-zinc-800/80 hover:bg-zinc-700 text-zinc-300'
                  }`}
                >
                  {room.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Footer controls */}
        <div className="px-6 py-3 border-t border-zinc-800/80 bg-zinc-900/60 flex items-center justify-between text-xs text-zinc-400">
          <span>Resolution: Ultra HD 4K Virtual Capture</span>
          <button
            onClick={onClose}
            className="bg-white text-zinc-950 font-bold px-4 py-1.5 rounded-full hover:bg-zinc-200 transition-colors cursor-pointer"
          >
            Close Tour
          </button>
        </div>
      </div>
    </div>
  );
}
