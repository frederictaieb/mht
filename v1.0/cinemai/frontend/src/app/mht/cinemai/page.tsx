//src/app/mht/cinemai/page.tsx

import { Header } from "@/components/mht/Header";
import FaceswapBoard from "@/components/ui/FaceswapBoard";



export default async function CinemaiPage() {

    const res = await fetch("http://localhost:8000/cinemai/available_videos", {cache: "no-store",})
    const available_files =await res.json()

    return (
        <div className="min-h-screen bg-[#efe8d8] text-[#141018]">
            <Header />
            <FaceswapBoard />
        </div>
    )
} 