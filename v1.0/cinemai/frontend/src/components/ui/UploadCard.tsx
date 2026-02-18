"use client"

import { useRef, useState, useEffect } from "react"
import { Button } from "@/components/ui/button"

export default function UploadCard() {
  const inputRef = useRef<HTMLInputElement>(null)
  const [preview, setPreview] = useState<string | null>(null)

  const handleClick = () => {
    inputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const url = URL.createObjectURL(file)
    setPreview(url)
  }

  // libère la mémoire
  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview)
    }
  }, [preview])

  return (
    <div className="border border-black h-full rounded-lg p-4 flex flex-col gap-4">

      {/* preview image */}
      {preview ? (
        <img
          src={preview}
          alt="Preview"
          className="w-full aspect-video object-cover rounded"
        />
      ) : (
        <div className="w-full aspect-video grid place-items-center text-sm text-muted-foreground border rounded">
          Aucune image sélectionnée
        </div>
      )}

      {/* hidden file input */}
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />

      {/* upload button */}
      <Button
        onClick={handleClick}
        className="w-full mt-auto"
      >
        Upload
      </Button>

    </div>
  )
}
