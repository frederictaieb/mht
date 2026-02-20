"use client";

import Link from "next/link";
import { useState, useRef, useEffect } from "react";

export function TopNav() {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // 👉 Fermer si clic en dehors
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <nav className="flex items-center justify-center gap-12">
      {/* ABOUT dropdown (CLICK) */}
      <div ref={ref} className="relative">
        <button
          onClick={() => setOpen((prev) => !prev)}
          className="flex items-center gap-1 text-[18px] font-black tracking-wide text-[#141018]/90 hover:text-[#141018]"
          type="button"
        >
          ABOUT
          <span className="inline-block">
            {open ? "▾" : "▴"}
          </span>
        </button>

        {open && (
          <div
            className="
              absolute left-0 top-[42px] z-30 w-[140px]
              rounded-[4px] border border-black/15 bg-[#efe8d8]
              shadow-[0_8px_20px_rgba(0,0,0,0.15)]
            "
          >
            <Link
              href="/news"
              className="block px-4 py-3 text-[16px] font-black text-[#141018] hover:bg-black/5"
              onClick={() => setOpen(false)}
            >
              NEWS
            </Link>

            <div className="h-px bg-black/10" />

            <Link
              href="/media"
              className="block px-4 py-3 text-[16px] font-black text-[#141018] hover:bg-black/5"
              onClick={() => setOpen(false)}
            >
              MEDIA
            </Link>

            <div className="h-px bg-black/10" />

            <Link
              href="/features"
              className="block px-4 py-3 text-[16px] font-black text-[#141018] hover:bg-black/5"
              onClick={() => setOpen(false)}
            >
              FEATURES
            </Link>
          </div>
        )}
      </div>

      {/* autres items */}
      <Link
        href="/community"
        className="text-[18px] font-black tracking-wide text-[#141018]/90 hover:text-[#141018]"
      >
        NEWS & COMMUNITY{" "}
        <span className="inline-block -translate-y-[1px]">▾</span>
      </Link>

      <Link
        href="/embark"
        className="text-[18px] font-black tracking-wide text-[#141018]/90 hover:text-[#141018]"
      >
        EMBARK <span className="inline-block -translate-y-[1px]">▾</span>
      </Link>
    </nav>
  );
}