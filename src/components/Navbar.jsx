import React, { useState } from 'react';
import { Bell, ChevronDown, Check, SlidersHorizontal, Maximize2, Minimize2 } from 'lucide-react';

export default function Navbar({ activeTab = 'Rent', onTabChange, isFramed, onToggleFramed }) {
  const [hasUnread, setHasUnread] = useState(true);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const navLinks = ['About', 'Buy', 'Sell', 'Rent', 'Contact'];

  return (
    <header className="w-full bg-white px-8 py-4 flex items-center justify-between border-b border-zinc-100/80 select-none z-30">
      {/* Brand Logo */}
      <div className="flex items-center gap-3">
        <a href="#home" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-black flex items-center justify-center text-white shadow-sm transition-transform group-hover:scale-105">
            {/* Custom geometric logo matching screenshot */}
            <svg viewBox="0 0 24 24" className="w-5 h-5 fill-current" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 4h7a4 4 0 0 1 4 4v2H9v-2H6v8h3v-2h6v4a4 4 0 0 1-4 4H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm14 7h2v2h-2v-2z" />
            </svg>
          </div>
          <span className="text-xl font-bold tracking-tight text-zinc-900 font-sans">
            Estates
          </span>
        </a>
      </div>

      {/* Center Nav Links */}
      <nav className="flex items-center gap-8">
        {navLinks.map((item) => {
          const isActive = item === activeTab;
          return (
            <button
              key={item}
              onClick={() => onTabChange?.(item)}
              className={`relative py-1 text-sm transition-all duration-200 cursor-pointer ${
                isActive
                  ? 'font-bold text-zinc-950'
                  : 'font-medium text-zinc-500 hover:text-zinc-900'
              }`}
            >
              {item}
              {isActive && (
                <span className="absolute -bottom-2 left-0 right-0 h-[2px] bg-black rounded-full transition-all" />
              )}
            </button>
          );
        })}
      </nav>

      {/* Right User Controls */}
      <div className="flex items-center gap-5">
        {/* View toggle (Mockup presentation mode vs full screen) */}
        <button
          onClick={onToggleFramed}
          title={isFramed ? "Switch to Full Screen View" : "Switch to Dribbble Mockup Frame View"}
          className="hidden sm:flex items-center gap-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-900 bg-zinc-100/80 hover:bg-zinc-200/80 px-2.5 py-1.5 rounded-full transition-colors cursor-pointer"
        >
          {isFramed ? <Maximize2 className="w-3.5 h-3.5" /> : <Minimize2 className="w-3.5 h-3.5" />}
          <span className="hidden md:inline">{isFramed ? 'Full View' : 'Frame View'}</span>
        </button>

        {/* Profile Pill */}
        <div className="relative">
          <div 
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="flex items-center gap-3 cursor-pointer p-1 rounded-full hover:bg-zinc-50 transition-colors"
          >
            <span className="text-sm font-semibold text-zinc-900">
              Guangming
            </span>
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80"
                alt="Guangming avatar"
                className="w-8 h-8 rounded-full object-cover ring-2 ring-zinc-100 shadow-xs"
              />
            </div>
          </div>

          {/* User popup menu */}
          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-2xl shadow-xl border border-zinc-100 p-2 text-xs z-50 animate-in fade-in zoom-in-95 duration-150">
              <div className="px-3 py-2 border-b border-zinc-100">
                <p className="font-semibold text-zinc-800">Guangming Zhao</p>
                <p className="text-zinc-400 text-[11px]">guangming@estates.io</p>
              </div>
              <div className="py-1">
                <button className="w-full text-left px-3 py-1.5 rounded-lg text-zinc-700 hover:bg-zinc-100">My Bookings</button>
                <button className="w-full text-left px-3 py-1.5 rounded-lg text-zinc-700 hover:bg-zinc-100">Saved Properties (3)</button>
                <button className="w-full text-left px-3 py-1.5 rounded-lg text-zinc-700 hover:bg-zinc-100">Preferences</button>
              </div>
              <div className="pt-1 border-t border-zinc-100">
                <button className="w-full text-left px-3 py-1.5 rounded-lg text-red-600 hover:bg-red-50">Log out</button>
              </div>
            </div>
          )}
        </div>

        {/* Notification Bell */}
        <button
          onClick={() => setHasUnread(!hasUnread)}
          className="relative p-1.5 rounded-full text-zinc-800 hover:bg-zinc-100 transition-colors cursor-pointer"
          aria-label="Notifications"
          title="Notifications"
        >
          <Bell className="w-4 h-4 stroke-[2]" />
          {hasUnread && (
            <span className="absolute top-1 right-1 w-1.5 h-1.5 bg-black rounded-full" />
          )}
        </button>
      </div>
    </header>
  );
}
