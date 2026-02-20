import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/arc/Logo";
import { TopNav } from "@/components/arc/TopNav";

function IconStub({ label }: { label: string }) {
  return (
    <button
      aria-label={label}
      className="grid h-10 w-10 place-items-center rounded-full text-[#141018]/70 hover:bg-black/5 hover:text-[#141018]"
      type="button"
    >
      <span className="block h-4 w-4 rounded-sm border border-current" />
    </button>
  );
}

export function Header() {
  return (
    <header className="border-b border-black/10 bg-[#efe8d8]">
      {/* grid 3 colonnes: logo | nav (container centré) | icons+buy */}
      <div className="grid h-[72px] grid-cols-[auto,1fr,auto] items-center px-6">
        {/* LEFT */}
        <div className="justify-self-start">
          <Logo />
        </div>

        {/* CENTER */}
        <div className="justify-self-center">
          <div className="mx-auto w-full max-w-[760px]">
            <TopNav />
          </div>
        </div>

        {/* RIGHT */}
        <div className="flex items-center gap-2 justify-self-end">
          <div className="hidden items-center gap-1 md:flex">
            <IconStub label="X" />
            <IconStub label="Discord" />
            <IconStub label="Other" />
          </div>

          <Button
            asChild
            className="ml-3 h-[40px] rounded-[6px] bg-[#f0b429] px-6 text-[14px] font-black tracking-[0.2em] text-black hover:bg-[#f3c24d]"
          >
            <Link href="/buy">BUY NOW</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}