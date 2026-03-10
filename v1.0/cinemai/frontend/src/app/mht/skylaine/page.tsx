//src/app/mht/skylaine/page.tsx
import { Header } from "@/app/mht/components/ui/Header";
import BlinkingDotCanvas from "@/app/mht/components/ui/skylaine/BlinkingDotCanvas"
import RoundBlinkingDot from "@/app/mht/components/ui/skylaine/RoundBlinkingDot"


export default function SkylainePage() {
    return (
        <div className="min-h-screen bg-[#efe8d8] text-[#141018]">
            <Header />
            <BlinkingDotCanvas />
            <RoundBlinkingDot />
        </div>
    )
}