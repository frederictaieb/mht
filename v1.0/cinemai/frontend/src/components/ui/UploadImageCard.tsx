"use client"

import { useEffect, useRef, useState } from "react"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

type UploadResponse = { filename: string }

type Props = {
  onUploaded?: (filename: string) => void
}

export default function UploadImageCard({ onUploaded }: Props) {
  const [preview, setPreview] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const inputRef = useRef<HTMLInputElement | null>(null)

  /**
   * Ouvre le file picker
   */
  const pickFile = () => inputRef.current?.click()

  /**
   * Upload automatique dès sélection
   */
  const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setError(null)

    // preview immédiat
    const url = URL.createObjectURL(file)
    setPreview(url)

    setUploading(true)

    try {
      const form = new FormData()
      form.append("f", file)

      const res = await fetch(`${API_BASE}/faceswap/img/upload`, {
        method: "POST",
        body: form,
      })

      if (!res.ok) {
        const txt = await res.text()
        throw new Error(txt || `Upload failed (${res.status})`)
      }

      const data = (await res.json()) as UploadResponse

      onUploaded?.(data.filename)
    } catch (e: any) {
      setError(e?.message ?? "Erreur upload")
    } finally {
      setUploading(false)
    }
  }

  /**
   * Nettoyage mémoire du preview
   */
  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview)
    }
  }, [preview])

  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">

      {/* input file caché */}
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg"
        onChange={onFileChange}
        className="hidden"
      />

      {/* zone cliquable */}
      <div
  className="w-full aspect-video bg-gray-200 rounded overflow-hidden relative cursor-pointer hover:bg-gray-100 transition"
  onClick={pickFile}
>
  {preview ? (
    <img
      src={preview}
      alt="Preview"
      className="absolute inset-0 w-full h-full object-contain"
      // ou object-contain si tu veux voir toute l'image sans crop
    />
  ) : (
    <div className="absolute inset-0 grid place-items-center">
      <span className="text-sm text-muted-foreground">
        Cliquer pour uploader une image
      </span>
    </div>
  )}

  {uploading && (
    <div className="absolute inset-0 bg-black/40 grid place-items-center text-white text-sm">
      Upload...
    </div>
  )}
</div>

      {/* erreur */}
      {error && (
        <div className="text-xs text-red-600 p-2">
          {error}
        </div>
      )}
    </div>
  )
}