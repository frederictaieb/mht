// src/app/mht/components/ui/cinemai/FaceswapVideoCard.tsx
"use client"

import { useMemo, useState } from "react"
import { useCinemai } from "@/app/mht/contexts/CinemaiContext"

type Props = {
  isReady: boolean
  img: string
  vid: string
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"
const OUTPUT_URL = (name: string) =>
  `${API_BASE}/cinemai/static/output_video/${encodeURIComponent(name)}`

export default function FaceswapVideoCard({ isReady, img, vid }: Props) {
  const { rows, setOutputVid } = useCinemai()
  const row = rows.find(r => r.input_vid === vid)
  const [isGenerating, setIsGenerating] = useState(false)

  const outputUrl = useMemo(() => {
    const out = row?.output_vid
    return out ? OUTPUT_URL(out) : null
  }, [row?.output_vid])

  const handleGenerateFaceswapVideo = async () => {
    if (!isReady) return

    setIsGenerating(true)
    try {
      // vider pendant génération
      setOutputVid(vid, null)

      const form = new FormData()
      form.append("video_name", vid)
      form.append("image_name", img)

      const res = await fetch(`${API_BASE}/cinemai/generate_faceswap`, {
        method: "POST",
        body: form,
      })

      if (!res.ok) throw new Error(await res.text())

      // ✅ règle exacte
      setOutputVid(vid, `fs-${vid}`)
    } catch (err) {
      console.error(err)
    } finally {
      setIsGenerating(false)
    }
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
        ) : outputUrl ? (
          <video
            src={outputUrl}
            className="w-full h-full object-cover"
            autoPlay
            muted
            playsInline
            loop
          />
        ) : isReady ? (
          <div className="text-sm text-muted-foreground">Double-clic pour générer</div>
        ) : (
          <div className="text-sm text-muted-foreground">En attente d'image ...</div>
        )}
      </div>
    </div>
  )
}