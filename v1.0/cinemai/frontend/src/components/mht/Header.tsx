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
        <Logo />
        <TopNav />
        <Login />
      </div>
    </header>
  );
}
