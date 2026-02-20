import { Header } from "@/components/arc/Header";
import { NewsCard } from "@/components/arc/NewsCard";
import { posts } from "@/components/arc/news-data";

export default function NewsPage() {
  return (
    <div className="min-h-screen bg-[#efe8d8] text-[#141018]">
      <Header />

      <main>
        {/* Title */}
        <section className="px-6 pt-10">
          <div className="mx-auto max-w-[1120px] text-center">
            <h1 className="text-[44px] font-black tracking-tight">NEWS</h1>
            <p className="mt-2 text-[22px] font-black tracking-wide">
              FOLLOW THE LATEST NEWS ABOUT ARC RAIDERS.
            </p>
          </div>

          {/* Yellow line full width */}
          <div className="mt-8 h-[2px] w-full bg-[#f0b429]" />
        </section>

        {/* Grid */}
        <section className="px-6 pb-20 pt-10">
          <div className="mx-auto max-w-[1120px]">
            <div className="grid gap-x-10 gap-y-12 md:grid-cols-3">
              {posts.map((p) => (
                <NewsCard key={p.href} post={p} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}