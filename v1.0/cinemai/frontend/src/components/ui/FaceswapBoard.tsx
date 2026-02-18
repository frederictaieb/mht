"use client"

import { useRef, useState } from "react"
import UploadCard from "@/components/ui/UploadCard"
import { Button } from "@/components/ui/button"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

type Props = {
  firstVideo?: string
}

type SubmitResponse =
  | { job_id: string; status: "done"; output_file: string }
  | { job_id: string; status: "waiting_for_video" }

export default function FaceswapBoard({ firstVideo }: Props) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const [generating, setGenerating] = useState(false)
  const [resultUrl, setResultUrl] = useState<string | null>(null)
  const [genError, setGenError] = useState<string | null>(null)

  // ✅ ref sur la vidéo de gauche
  const leftVideoRef = useRef<HTMLVideoElement | null>(null)

  const canGenerate = !!selectedFile && !generating

  const onGenerate = async () => {
    if (!selectedFile) return

    setGenerating(true)
    setGenError(null)
    setResultUrl(null)

    try {
      const form = new FormData()
      form.append("f", selectedFile)

      const res = await fetch(`${API_BASE}/faceswap/submit`, {
        method: "POST",
        body: form,
      })

      if (!res.ok) {
        const txt = await res.text()
        throw new Error(txt || `Generate failed (${res.status})`)
      }

      const data = (await res.json()) as SubmitResponse

      if (data.status === "waiting_for_video") {
        setGenError("Plus de vidéos disponibles pour le moment.")
        return
      }

      // ⚠️ ton backend expose /output/{filename} (FileResponse ou StaticFiles)
      // Dans tes messages précédents tu avais /faceswap/output/{filename}
      // Garde l’URL qui correspond à TON backend.
      setResultUrl(`${API_BASE}/faceswap/output/${encodeURIComponent(data.output_file)}`)
    } catch (e: any) {
      setGenError(e?.message ?? "Erreur génération")
    } finally {
      setGenerating(false)
    }
  }

  // ✅ quand la vidéo générée démarre, on reset la vidéo de gauche à 0
  const syncLeftToZero = () => {
    const left = leftVideoRef.current
    if (!left) return

    // important pour éviter blocage autoplay
    left.muted = true
    left.currentTime = 0
    left.play().catch(() => {})
  }

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-3 items-stretch">
      {/* Colonne 1 : video available */}
      <div className="border border-black h-full overflow-hidden rounded-lg">
        {firstVideo ? (
          <video
            ref={leftVideoRef}
            src={`${API_BASE}/faceswap/available/video/${encodeURIComponent(firstVideo)}`}
            className="w-full aspect-video object-cover"
            autoPlay
            muted
            playsInline
            loop
          />
        ) : (
          <div className="w-full aspect-video grid place-items-center text-sm text-muted-foreground">
            Aucune vidéo available
          </div>
        )}
      </div>

      {/* Colonne 2 : upload */}
      <UploadCard onFileReady={setSelectedFile} />

      {/* Colonne 3 : result + generate */}
      <div className="border border-black h-full rounded-lg p-4 flex flex-col gap-4">
        <div className="w-full aspect-video bg-gray-100 rounded overflow-hidden grid place-items-center">
          {generating ? (
            <div className="text-sm text-muted-foreground">Génération en cours…</div>
          ) : resultUrl ? (
            <video
              src={resultUrl}
              className="w-full h-full object-cover"
              autoPlay
              muted
              playsInline
              loop
              // ✅ au démarrage de lecture de la vidéo générée
              onPlay={syncLeftToZero}
            />
          ) : (
            <div className="text-sm text-muted-foreground">Aucune vidéo générée</div>
          )}
        </div>

        {genError && (
          <div className="text-sm text-red-600 whitespace-pre-wrap">{genError}</div>
        )}

        <Button className="w-full mt-auto" onClick={onGenerate} disabled={!canGenerate}>
          {generating ? "Generate..." : "Generate"}
        </Button>
      </div>
    </div>
  )
}
