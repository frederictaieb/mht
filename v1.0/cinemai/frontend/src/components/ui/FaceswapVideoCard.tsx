//GeneratedVideoCard.tsx
"use client"

import { useState } from "react"

type Props = {
  isReady: boolean; // si tu veux garder cette casse (pas recommandé)
  img: string;
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
      console.log("vid:" + vid)
      console.log("img" + img)
      form.append("video_name", vid)
      form.append("image_name", img)

      const res = await fetch(`${API_BASE}/cinemai/generate_faceswap`, {
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
        `${API_BASE}/cinemai/output/fs-`+vid
      )


    } catch (e: any) {
    } finally {
      setIsGenerating(false)
    };
  }

  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">
      <div
        className="w-full aspect-video bg-gray-200 rounded overflow-hidden grid place-items-center cursor-pointer hover:bg-gray-100 transition"
        onDoubleClick={handleGenerateFaceswapVideo}
        title={isReady ? "Double-clic pour générer" : "Choisis une image d'abord"}
      >
      
        {isGenerating ? (
          <div className="text-sm text-muted-foreground">Génération en cours…</div>
        ) : faceswapVideoUrl ? (
          <video
            src={faceswapVideoUrl}
            className="w-full h-full object-cover"
            autoPlay
            muted
            playsInline
            loop
          />
        ) : isReady ? (
          <div className="text-sm text-muted-foreground">
            Double-clic pour générer
          </div>
        ) : (
          <div className="text-sm text-muted-foreground">En attente d'image ...</div>
        )}
      </div>
    </div>
  )
}