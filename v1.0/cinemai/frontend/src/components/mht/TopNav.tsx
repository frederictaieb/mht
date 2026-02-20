//src/app/components/mht/TopNav.tsx
"use client";

import Link from "next/link";

export function TopNav() {
  return (
    <nav className="flex items-center justify-center gap-12">
      <div className="relative">
        <Link 
          href="/cinemai"
          className="flex items-center gap-1 text-[18px] font-black tracking-wide text-[#141018]/90 hover:text-[#141018]"
          >
            CINEMAI
        </Link>
      </div>

      <div className="relative">
        <Link 
          href="/skylaine"
          className="flex items-center gap-1 text-[18px] font-black tracking-wide text-[#141018]/90 hover:text-[#141018]"
          >
            SKYLAINE
        </Link>
      </div>

      <div className="relative">
        <Link 
          href="/telepai"
          className="flex items-center gap-1 text-[18px] font-black tracking-wide text-[#141018]/90 hover:text-[#141018]"
          >
            TELEPAI
        </Link>
      </div>
    </nav>
  );
}