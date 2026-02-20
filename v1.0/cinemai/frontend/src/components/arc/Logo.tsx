import Link from "next/link";

export function Logo() {
  return (
    <Link href="/" className="flex items-center gap-3">
      <div className="flex items-end gap-0.5">
        <span className="h-4 w-1.5 -skew-x-12 rounded-sm bg-cyan-400" />
        <span className="h-5 w-1.5 -skew-x-12 rounded-sm bg-emerald-400" />
        <span className="h-6 w-1.5 -skew-x-12 rounded-sm bg-yellow-400" />
        <span className="h-7 w-1.5 -skew-x-12 rounded-sm bg-orange-500" />
        <span className="h-8 w-1.5 -skew-x-12 rounded-sm bg-red-500" />
      </div>

      <span className="text-[28px] font-black tracking-tight text-[#141018]">
        ARC<span className="font-black">Raiders</span>
      </span>
    </Link>
  );
}