// src/app/mht/components/ui/cinemai/UploadImageCard.tsx
"use client"

import React, { useEffect, useRef, useState } from "react"

type Props = {
  vid: string
  imgName: string | null
  onImgUploaded: (imgName: string) => void
}

type UploadResponse = { img_name: string }

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

const INPUT_IMG_URL = (imgName: string) =>
  `${API_BASE}/cinemai/static/upload_image/${encodeURIComponent(imgName)}`

export default function UploadImageCard({ vid, imgName, onImgUploaded }: Props) {
  const [localPreviewUrl, setLocalPreviewUrl] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const inputRef = useRef<HTMLInputElement | null>(null)

  const selectImage = () => inputRef.current?.click()

  useEffect(() => {
    return () => {
      if (localPreviewUrl) URL.revokeObjectURL(localPreviewUrl)
    }
  }, [localPreviewUrl])

  const handleChangeImage = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const url = URL.createObjectURL(file)
    setLocalPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return url
    })

    setIsUploading(true)
    try {
      const form = new FormData()
      form.append("image", file)
      form.append("name", vid)

      const res = await fetch(`${API_BASE}/cinemai/upload_image`, {
        method: "POST",
        body: form,
      })

      if (!res.ok) throw new Error(await res.text())

      const data = (await res.json()) as UploadResponse
      if (!data?.img_name) throw new Error("Réponse API invalide: img_name manquant")

      onImgUploaded(data.img_name)
    } catch (err) {
      console.error(err)
    } finally {
      setIsUploading(false)
      e.target.value = ""
    }
  }

  // priorité à l’image serveur (persistante)
  const displayUrl = imgName ? INPUT_IMG_URL(imgName) : localPreviewUrl

  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg"
        onChange={handleChangeImage}
        className="hidden"
      />

      <div
        className="w-full aspect-video bg-gray-200 rounded overflow-hidden relative cursor-pointer hover:bg-gray-100 transition"
        onClick={selectImage}
      >
        {displayUrl ? (
          <img
            src={displayUrl}
            alt="input"
            className="absolute inset-0 w-full h-full object-contain"
          />
        ) : (
          <div className="absolute inset-0 grid place-items-center">
            <span className="text-sm text-muted-foreground">Cliquer pour uploader une image</span>
          </div>
        )}

        {isUploading && (
          <div className="absolute inset-0 grid place-items-center bg-white/60">
            <span className="text-sm text-muted-foreground">Upload…</span>
          </div>
        )}
      </div>
    </div>
  )
}