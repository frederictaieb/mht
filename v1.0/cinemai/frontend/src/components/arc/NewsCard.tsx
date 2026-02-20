import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import type { Post } from "@/components/arc/types";

export function NewsCard({ post }: { post: Post }) {
  return (
    <Link href={post.href} className="block">
      <article
        className="
          overflow-hidden rounded-[18px] bg-white
          ring-1 ring-[#63b1d3]
          transition
          hover:ring-2 hover:ring-[#f0b429]
          focus-within:ring-2 focus-within:ring-[#f0b429]
        "
      >
        <div className="relative h-[230px] w-full overflow-hidden bg-neutral-200">
          <img
            src={post.imageUrl}
            alt=""
            className="h-full w-full object-cover"
            loading="lazy"
          />

          {/* bande arc-en-ciel */}
          <div className="pointer-events-none absolute inset-0">
            <div className="absolute left-0 top-0 h-full w-[120px] bg-gradient-to-tr from-cyan-400 via-emerald-400 to-red-500 opacity-90 [clip-path:polygon(0_0,100%_0,0_100%)]" />
            <div className="absolute left-0 top-0 h-full w-[108px] bg-gradient-to-tr from-cyan-300 via-yellow-300 to-red-400 opacity-80 [clip-path:polygon(0_0,100%_0,0_100%)]" />
          </div>

          {/* texte ARC Raiders */}
          <div className="pointer-events-none absolute left-6 top-7">
            <div className="text-[58px] font-black leading-[0.9] tracking-tight text-white drop-shadow">
              ARC
              <br />
              Raiders
            </div>
          </div>
        </div>

        <div className="bg-white px-6 pb-5 pt-4">
          {/* SLOT FIXE (important!) */}
          {/* 22px badge + ~12px d'espace = 34px => titres alignés partout */}
          <div className="h-[34px]">
            {post.tag ? (
              <Badge
                className="
                  inline-flex items-center justify-center
                  h-[22px] px-3
                  rounded-[6px]
                  bg-[#1a131c] text-white
                  text-[11px] font-semibold
                  leading-none
                  hover:bg-[#1a131c]
                "
              >
                {post.tag}
              </Badge>
            ) : null}
          </div>

          <h3 className="text-[20px] font-black leading-snug text-[#141018]">
            {post.title}
          </h3>

          <p className="mt-2 text-[13px] font-semibold text-[#141018]/60">
            {post.date}
          </p>
        </div>
      </article>
    </Link>
  );
}