//src/app/components/mht/Header.tsx
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Logo } from "@/components/mht/Logo";
import { TopNav } from "@/components/mht/TopNav";
import { Login } from "@/components/mht/Login";


export function Header() {
  return (
    <header className="border-b border-black/10 bg-[#efe8d8]">
      <div className="flex items-center px-3 py-2">
        <div className="shrink-0"><Logo /></div>
        <div className="flex-1 flex justify-center"><TopNav /></div>
        <div className="shrink-0"><Login /></div>
      </div>
    </header>
  );
}
