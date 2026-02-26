import Link from "next/link";
import { Button } from "@/app/mht/components/ui/button";

export function Login() {
    return (
        <div className="flex items-center gap-2 justify-self-end">
          <Button
            asChild
            className="ml-3 h-[40px] rounded-[6px] bg-[#f0b429] px-6 text-[14px] font-black tracking-[0.2em] text-black hover:bg-[#f3c24d]"
          >
            <Link href="/buy">LOGIN</Link>
          </Button>
        </div>
    );
  }