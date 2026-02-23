//GeneratedVideoCard.tsx
"use client"

import { useState } from "react"

type Props = {
  isReady: boolean; // si tu veux garder cette casse (pas recommandé)
  img: File | null
  vid: string;

};

export default function FaceswapVideoCard({ isReady, img, vid }: Props) { 

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

  const [isGenerating, setIsGenerating] = useState(false)
  const [faceswapVideoUrl, setFaceswapVideoUrl] = useState<string | null>(null)


  const handleGenerateFaceswapVideo = async () => {
    setIsGenerating(true)
    setFaceswapVideoUrl(null)

    try {

      const form = new FormData()
      form.append("video_name", "01.mp4")
      form.append("image_name", "01.jpg" )

      const res = await fetch(`${API_BASE}/faceswap/generate/faceswap`, {
        method: "POST",
        body: form,
      })

      if (!res.ok) {
        const txt = await res.text()
        throw new Error(txt || `Generation failed (${res.status})`)
      }

      //setFaceswapVideoUrl(
      //  `${API_BASE}/faceswap/output/${encodeURIComponent(data.output_file)}`
      //)
      setFaceswapVideoUrl(
        `${API_BASE}/faceswap/output/fs-01.mp4`
      )


    } catch (e: any) {
    } finally {
      setIsGenerating(false)
    };
  }

  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">

      {isReady ? (
        <div
          className="w-full aspect-video bg-gray-200 rounded overflow-hidden grid place-items-center cursor-pointer hover:bg-gray-100 transition"
          onDoubleClick={handleGenerateFaceswapVideo}
        >
          <div className="text-sm text-muted-foreground">Cliquer pour générer la vidéo</div>
        </div>
      ) : (
        <div
          className="w-full aspect-video bg-gray-200 rounded overflow-hidden grid place-items-center cursor-pointer hover:bg-gray-200 transition">
          {
            isGenerating ? (
              <div className="text-sm text-muted-foreground">Génération en cours…</div>
            ):(
              <video
                src={faceswapVideoUrl}
                className="w-full h-full object-cover"
                autoPlay
                muted
                playsInline
                loop
              />
            )
          } 
        </div>
        
      )}
    </div>
  )
}