//src/app/components/mht/Header.tsx
import Link from "next/link";
import { Button } from "@/app/mht/components/ui/button";
import { Logo } from "@/app/mht/components/ui/Logo";
import { TopNav } from "@/app/mht/components/ui/TopNav";
import { Login } from "@/app/mht/components/ui/Login";


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
