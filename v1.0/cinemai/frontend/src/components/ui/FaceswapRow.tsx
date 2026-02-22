// FaceswapRow.tsx
"use client"

import { useRef, useState } from "react"
import UploadImageCard from "./UploadImageCard"
import AvailableVideoCard from "./AvailableVideoCard"
import FaceswapVideoCard from "./FaceswapVideoCard"
import GeneratedVideoCard from "./GeneratedVideoCard copy"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

type Props = {
  vid: string
}

type SubmitResponse =
  | { job_id: string; status: "done"; output_file: string }
  | { job_id: string; status: "waiting_for_video" }

export default function FaceswapRow({ vid }: Props) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const [generating, setGenerating] = useState(false)
  const [resultUrl, setResultUrl] = useState<string | null>(null)
  const [genError, setGenError] = useState<string | null>(null)

  const [isImageReady, setIsImageReady] = useState(false)

  // ref sur la vidéo de gauche (si tu veux la remettre à 0)
  const leftVideoRef = useRef<HTMLVideoElement | null>(null)

  const syncLeftToZero = () => {
    const left = leftVideoRef.current
    if (!left) return
    left.muted = true
    left.currentTime = 0
    left.play().catch(() => {})
  }

  const onGenerate = async () => {
    console.log("onGenerate called ✅", { selectedFile, generating })
    if (!selectedFile || generating) return

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

      console.log("setting resultUrl ✅", data)
      setResultUrl(
        `${API_BASE}/faceswap/output/${encodeURIComponent(data.output_file)}`
      )
    } catch (e: any) {
      setGenError(e?.message ?? "Erreur génération")
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-3 items-stretch">
      {/* Colonne 1 : video available */}
      <AvailableVideoCard vid={vid} videoRef={leftVideoRef} />
      <UploadImageCard onImageUploaded = {
        (image:File) => {
          setIsImageReady(true)
          console.log("FaceswapRow - Image : " + image)
          console.log("FaceswapRow - IsImageReady : " + isImageReady)
        }
      }/>
      
      <FaceswapVideoCard isImageReady={isImageReady} />
      

      {/*
      <UploadImageCard onFileReady={(file: File) => {
        if (!file) return 

        setSelectedFile((prev) => {
          const same =
            prev &&
            prev.name === file.name &&
            prev.size === file.size &&
            prev.lastModified === file.lastModified

            if (!same) {
              setGenError(null)
              setResultUrl(null)
            }

            return file
          })
        }}
      />
      */}

      
    </div>
  )
}