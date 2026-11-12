import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import { Search, X, ChevronDown, MoreHorizontal, Edit3, Plus, Minus, Check } from 'lucide-react';

export default function MapExplorer({
  properties,
  selectedProperty,
  onSelectProperty,
  searchQuery,
  onSearchChange,
  activeFilters,
  onFilterToggle,
  onOpenFilterModal
}) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef({});
  const polygonRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [showAreaDropdown, setShowAreaDropdown] = useState(false);
  const [showFloorDropdown, setShowFloorDropdown] = useState(false);
  const [showMoreMenu, setShowMoreMenu] = useState(false);

  // Approximate coordinate boundary for the organic shape in Nice, France
  const boundaryCoords = [
    [43.7360, 7.2710],
    [43.7350, 7.2830],
    [43.7310, 7.2910],
    [43.7250, 7.2950],
    [43.7170, 7.2940],
    [43.7110, 7.2870],
    [43.7070, 7.2780],
    [43.7060, 7.2680],
    [43.7120, 7.2610],
    [43.7200, 7.2640],
    [43.7250, 7.2590],
    [43.7310, 7.2620],
  ];

  // Specific visual markers matching the screenshot layout
  const markerConfigs = [
    {
      id: "nice-cosy-1",
      lat: 43.7310,
      lng: 7.2720,
      label: "€80",
      subLabel: "/ night",
      hasClusterBadge: false,
    },
    {
      id: "nice-loft-3",
      lat: 43.7240,
      lng: 7.2820,
      label: "from €69",
      subLabel: "/ night",
      hasClusterBadge: true,
      clusterCount: 2,
    },
    {
      id: "nice-loft-3-side",
      propertyRefId: "nice-loft-3",
      lat: 43.7210,
      lng: 7.2940,
      label: "€69",
      subLabel: "/ night",
      hasClusterBadge: false,
    },
    {
      id: "nice-studio-2",
      lat: 43.7110,
      lng: 7.2740,
      label: "€55",
      subLabel: "/ night",
      hasClusterBadge: false,
    }
  ];

  useEffect(() => {
    if (!mapContainerRef.current) return;

    // Check if map is already initialized
    if (!mapInstanceRef.current) {
      // Nice center: 43.722, 7.278
      const map = L.map(mapContainerRef.current, {
        center: [43.722, 7.278],
        zoom: 14,
        zoomControl: false,
        attributionControl: false,
        scrollWheelZoom: true,
      });

      // CartoDB Positron monochrome light tiles
      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        subdomains: 'abcd',
      }).addTo(map);

      // Add the organic boundary polygon
      const polygon = L.polygon(boundaryCoords, {
        color: '#18181b', // bold black outline
        weight: 2,
        dashArray: null,
        fillColor: '#18181b',
        fillOpacity: 0.04,
        smoothFactor: 2.5,
        lineCap: 'round',
        lineJoin: 'round',
      }).addTo(map);

      polygonRef.current = polygon;
      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;

    // Remove existing markers
    Object.values(markersRef.current).forEach((m) => map.removeLayer(m));
    markersRef.current = {};

    // Render price markers
    markerConfigs.forEach((cfg) => {
      const isSelected =
        selectedProperty?.id === cfg.id ||
        (cfg.propertyRefId && selectedProperty?.id === cfg.propertyRefId);

      const html = `
        <div class="group relative flex flex-col items-center cursor-pointer transition-transform duration-200 ${
          isSelected ? 'scale-110 z-50' : 'hover:scale-105 z-20'
        }">
          <div class="px-3.5 py-1.5 rounded-full shadow-[0_4px_12px_rgba(0,0,0,0.12)] border transition-all duration-200 flex items-center gap-1 whitespace-nowrap ${
            isSelected
              ? 'bg-zinc-900 text-white border-zinc-900 shadow-[0_6px_20px_rgba(0,0,0,0.25)]'
              : 'bg-white text-zinc-900 border-zinc-200/80 hover:border-zinc-400'
          }">
            <span class="text-xs font-bold tracking-tight">${cfg.label}</span>
            <span class="text-[10px] font-normal opacity-70">${cfg.subLabel}</span>
          </div>
          ${
            cfg.hasClusterBadge
              ? `
              <div class="w-5 h-5 -mt-1.5 rounded-full bg-zinc-950 text-white text-[10px] font-bold flex items-center justify-center ring-2 ring-white shadow-md">
                ${cfg.clusterCount}
              </div>
            `
              : `
              <div class="w-2.5 h-2.5 -mt-1 rounded-full ${
                isSelected ? 'bg-zinc-950 ring-2 ring-white' : 'bg-zinc-900 ring-2 ring-white'
              } shadow-xs"></div>
            `
          }
        </div>
      `;

      const icon = L.divIcon({
        className: 'custom-price-pin',
        html: html,
        iconSize: [80, 40],
        iconAnchor: [40, 36],
      });

      const marker = L.marker([cfg.lat, cfg.lng], { icon }).addTo(map);

      marker.on('click', () => {
        const targetId = cfg.propertyRefId || cfg.id;
        const targetProp = properties.find((p) => p.id === targetId);
        if (targetProp) {
          onSelectProperty(targetProp);
        }
      });

      markersRef.current[cfg.id] = marker;
    });

    return () => {
      // cleanup on unmount
    };
  }, [selectedProperty, properties]);

  // Handle zoom in / out
  const handleZoomIn = () => {
    mapInstanceRef.current?.zoomIn();
  };

  const handleZoomOut = () => {
    mapInstanceRef.current?.zoomOut();
  };

  const toggleDrawing = () => {
    setIsDrawing(!isDrawing);
  };

  return (
    <div className="relative w-full h-full min-h-[580px] overflow-hidden select-none bg-[#f1f3f5]">
      {/* Real Map Canvas */}
      <div ref={mapContainerRef} className="w-full h-full absolute inset-0 z-0" />

      {/* Floating Top Filters Row */}
      <div className="absolute top-5 left-6 right-6 z-20 flex flex-wrap items-center gap-2 pointer-events-auto">
        {/* Type: Apartment [X] */}
        {activeFilters?.type && (
          <div className="flex items-center gap-1.5 bg-zinc-950 text-white text-xs font-semibold px-3.5 py-2 rounded-full shadow-md hover:bg-zinc-800 transition-all">
            <span>Type: {activeFilters.type}</span>
            <button
              onClick={() => onFilterToggle?.('type')}
              className="p-0.5 rounded-full hover:bg-zinc-700 transition-colors ml-1 cursor-pointer"
              title="Remove filter"
            >
              <X className="w-3.5 h-3.5 stroke-[2.5]" />
            </button>
          </div>
        )}

        {/* Price: €150-530 [X] */}
        {activeFilters?.price && (
          <div className="flex items-center gap-1.5 bg-zinc-950 text-white text-xs font-semibold px-3.5 py-2 rounded-full shadow-md hover:bg-zinc-800 transition-all">
            <span>Price: {activeFilters.price}</span>
            <button
              onClick={() => onFilterToggle?.('price')}
              className="p-0.5 rounded-full hover:bg-zinc-700 transition-colors ml-1 cursor-pointer"
              title="Remove filter"
            >
              <X className="w-3.5 h-3.5 stroke-[2.5]" />
            </button>
          </div>
        )}

        {/* Area dropdown */}
        <div className="relative">
          <button
            onClick={() => {
              setShowAreaDropdown(!showAreaDropdown);
              setShowFloorDropdown(false);
              setShowMoreMenu(false);
            }}
            className="flex items-center gap-1.5 bg-white/95 backdrop-blur-md text-zinc-700 hover:text-zinc-900 text-xs font-semibold px-3.5 py-2 rounded-full shadow-sm border border-zinc-200/70 hover:bg-white transition-all cursor-pointer"
          >
            <span>Area</span>
            <ChevronDown className="w-3.5 h-3.5 opacity-60" />
          </button>

          {showAreaDropdown && (
            <div className="absolute left-0 mt-2 w-44 bg-white rounded-2xl shadow-xl border border-zinc-100 p-2 text-xs z-50 animate-in fade-in zoom-in-95 duration-100">
              <div className="px-2 py-1.5 font-semibold text-zinc-400 text-[10px] uppercase tracking-wider">Surface Area</div>
              {['Any size', '40 - 70 m²', '70 - 100 m²', '100+ m²'].map((item) => (
                <button
                  key={item}
                  onClick={() => setShowAreaDropdown(false)}
                  className="w-full text-left px-2.5 py-1.5 rounded-lg text-zinc-700 hover:bg-zinc-100 flex items-center justify-between"
                >
                  <span>{item}</span>
                  {item === '40 - 70 m²' && <Check className="w-3.5 h-3.5 text-zinc-900" />}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Floor dropdown */}
        <div className="relative">
          <button
            onClick={() => {
              setShowFloorDropdown(!showFloorDropdown);
              setShowAreaDropdown(false);
              setShowMoreMenu(false);
            }}
            className="flex items-center gap-1.5 bg-white/95 backdrop-blur-md text-zinc-700 hover:text-zinc-900 text-xs font-semibold px-3.5 py-2 rounded-full shadow-sm border border-zinc-200/70 hover:bg-white transition-all cursor-pointer"
          >
            <span>Floor</span>
            <ChevronDown className="w-3.5 h-3.5 opacity-60" />
          </button>

          {showFloorDropdown && (
            <div className="absolute left-0 mt-2 w-40 bg-white rounded-2xl shadow-xl border border-zinc-100 p-2 text-xs z-50 animate-in fade-in zoom-in-95 duration-100">
              <div className="px-2 py-1.5 font-semibold text-zinc-400 text-[10px] uppercase tracking-wider">Floor Level</div>
              {['Ground floor', '1st - 3rd floor', 'High floor', 'Penthouse'].map((f) => (
                <button
                  key={f}
                  onClick={() => setShowFloorDropdown(false)}
                  className="w-full text-left px-2.5 py-1.5 rounded-lg text-zinc-700 hover:bg-zinc-100"
                >
                  {f}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* More options button */}
        <div className="relative">
          <button
            onClick={() => {
              setShowMoreMenu(!showMoreMenu);
              setShowAreaDropdown(false);
              setShowFloorDropdown(false);
            }}
            className="flex items-center justify-center w-8 h-8 bg-white/95 backdrop-blur-md text-zinc-700 hover:text-zinc-900 rounded-full shadow-sm border border-zinc-200/70 hover:bg-white transition-all cursor-pointer"
            title="More filters"
          >
            <MoreHorizontal className="w-4 h-4" />
          </button>

          {showMoreMenu && (
            <div className="absolute left-0 mt-2 w-48 bg-white rounded-2xl shadow-xl border border-zinc-100 p-2 text-xs z-50 animate-in fade-in zoom-in-95 duration-100">
              <div className="px-2 py-1.5 font-semibold text-zinc-400 text-[10px] uppercase tracking-wider">Amenities</div>
              {['Balcony / Terrace', 'Air conditioning', 'Parking space', 'Elevator', 'Pet friendly'].map((opt) => (
                <label key={opt} className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg hover:bg-zinc-50 cursor-pointer">
                  <input type="checkbox" defaultChecked={opt.includes('Balcony')} className="rounded accent-zinc-900" />
                  <span className="text-zinc-700">{opt}</span>
                </label>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Floating Region Search Input */}
      <div className="absolute top-18 left-6 z-20 pointer-events-auto">
        <div className="bg-white rounded-full shadow-[0_6px_20px_rgba(0,0,0,0.08)] border border-zinc-100 px-4 py-2 flex items-center gap-3 w-64 md:w-72 transition-all focus-within:ring-2 focus-within:ring-zinc-900/20">
          <Search className="w-4 h-4 text-zinc-400 shrink-0" />
          <div className="flex flex-col flex-1 leading-tight">
            <span className="text-[10px] font-medium text-zinc-400">Region</span>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => onSearchChange?.(e.target.value)}
              placeholder="France, Nice"
              className="text-xs font-bold text-zinc-900 bg-transparent outline-none p-0 border-none w-full"
            />
          </div>
          {searchQuery && (
            <button
              onClick={() => onSearchChange?.('')}
              className="w-5 h-5 rounded-full bg-zinc-100 hover:bg-zinc-200 flex items-center justify-center text-zinc-500 hover:text-zinc-800 transition-colors cursor-pointer"
            >
              <X className="w-3 h-3 stroke-[2]" />
            </button>
          )}
        </div>
      </div>

      {/* Bottom-Left Map Tools */}
      <div className="absolute bottom-6 left-6 z-20 flex flex-col items-center gap-2 pointer-events-auto">
        {/* Draw tool */}
        <button
          onClick={toggleDrawing}
          className={`w-9 h-9 rounded-full shadow-md flex items-center justify-center transition-all cursor-pointer ${
            isDrawing
              ? 'bg-zinc-950 text-white ring-2 ring-zinc-900/40'
              : 'bg-white text-zinc-700 hover:text-zinc-950 hover:bg-zinc-50 border border-zinc-200/60'
          }`}
          title={isDrawing ? 'Drawing active: Drag on map to adjust area' : 'Draw custom search boundary'}
        >
          <Edit3 className="w-4 h-4" />
        </button>

        {/* Zoom In */}
        <button
          onClick={handleZoomIn}
          className="w-9 h-9 rounded-full bg-white text-zinc-700 hover:text-zinc-950 hover:bg-zinc-50 shadow-md border border-zinc-200/60 flex items-center justify-center transition-all cursor-pointer"
          title="Zoom in"
        >
          <Plus className="w-4 h-4" />
        </button>

        {/* Zoom Out */}
        <button
          onClick={handleZoomOut}
          className="w-9 h-9 rounded-full bg-white text-zinc-700 hover:text-zinc-950 hover:bg-zinc-50 shadow-md border border-zinc-200/60 flex items-center justify-center transition-all cursor-pointer"
          title="Zoom out"
        >
          <Minus className="w-4 h-4" />
        </button>
      </div>

      {/* Hint for drawing tool */}
      {isDrawing && (
        <div className="absolute bottom-6 left-20 z-20 bg-zinc-900 text-white text-xs px-3.5 py-2 rounded-xl shadow-lg border border-zinc-800 flex items-center gap-2 animate-in fade-in slide-in-from-left duration-200">
          <span>Boundary mode active</span>
          <button
            onClick={() => setIsDrawing(false)}
            className="text-zinc-400 hover:text-white underline text-[11px] ml-1"
          >
            Done
          </button>
        </div>
      )}
    </div>
  );
}
