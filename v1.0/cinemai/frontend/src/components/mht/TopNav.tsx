"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function TopNav() {
  const pathname = usePathname();

  const linkClass = (path: string) =>
    `relative text-[18px] font-black tracking-wide transition-colors
     ${pathname.startsWith(path)
       ? "text-[#141018] after:scale-x-100 after:bg-[#141018]"
       : "text-[#141018]/90 hover:text-[#141018] after:bg-yellow-400"
     }
     after:absolute 
     after:left-1/2 
     after:-translate-x-1/2 
     after:-bottom-1 
     after:h-[2px] 
     after:w-full 
     after:scale-x-0 
     after:origin-center 
     after:transition-transform 
     after:duration-300
     hover:after:scale-x-100`

  return (
    <nav className="flex items-center justify-center gap-24 whitespace-nowrap">
      <Link href="/mht/cinemai" className={linkClass("/mht/cinemai")}>
        CINEMAI
      </Link>

      <Link href="/mht/skylaine" className={linkClass("/mht/skylaine")}>
        SKYLAINE
      </Link>

      <Link href="/mht/telepai" className={linkClass("/mht/telepai")}>
        TELEPAI
      </Link>
    </nav>
  );
}