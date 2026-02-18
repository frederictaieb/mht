"use client"

import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

type UploadResponse = {
  directory: string
  type: "upload"
  filename: string
}

export default function UploadCard() {
  const inputRef = useRef<HTMLInputElement>(null)

  const [open, setOpen] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [uploadedName, setUploadedName] = useState<string | null>(null)

  // Preview local
  useEffect(() => {
    if (!file) {
      setPreview(null)
      return
    }

    const url = URL.createObjectURL(file)
    setPreview(url)

    return () => URL.revokeObjectURL(url)
  }, [file])

  const pickFile = () => inputRef.current?.click()

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] ?? null
    setError(null)
    setUploadedName(null)
    setFile(f)
  }

  const uploadToApi = async () => {
    if (!file) {
      setError("Choisis une image d'abord.")
      return
    }

    setUploading(true)
    setError(null)

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
      setUploadedName(data.filename)
      setOpen(false)
    } catch (e: any) {
      setError(e?.message ?? "Erreur upload")
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="border border-black h-full rounded-lg p-4 flex flex-col gap-4">

      {/* IMAGE PREVIEW (plus petite mais cadre conservé) */}
      <div className="w-full aspect-video bg-gray-100 flex items-center justify-center rounded overflow-hidden">
        {preview ? (
          <img
            src={preview}
            alt="Preview"
            className="max-h-[220px] max-w-full object-contain"
          />
        ) : (
          <span className="text-sm text-muted-foreground">
            Aucune image sélectionnée
          </span>
        )}
      </div>

      {/* Status */}
      <div className="text-xs text-muted-foreground">
        {uploadedName ? `Uploadé: ${uploadedName}` : "\u00A0"}
      </div>

      {/* Upload button */}
      <Button className="w-full mt-auto" onClick={() => setOpen(true)}>
        Upload
      </Button>

      {/* Modal */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Choisir une image</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">

            <input
              ref={inputRef}
              type="file"
              accept="image/png,image/jpeg"
              onChange={onFileChange}
              className="hidden"
            />

            <div className="border rounded-lg p-4 flex items-center justify-between">
              {file ? (
                <>
                  <div className="text-sm">
                    <div className="font-medium">{file.name}</div>
                    <div className="text-xs text-muted-foreground">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </div>
                  </div>
                  <Button variant="secondary" onClick={pickFile}>
                    Changer
                  </Button>
                </>
              ) : (
                <>
                  <span className="text-sm text-muted-foreground">
                    PNG / JPG uniquement
                  </span>
                  <Button onClick={pickFile}>
                    Choisir un fichier
                  </Button>
                </>
              )}
            </div>

            {error && (
              <div className="text-sm text-red-600 whitespace-pre-wrap">
                {error}
              </div>
            )}

          </div>

          <DialogFooter className="gap-2">
            <Button
              variant="secondary"
              onClick={() => setOpen(false)}
              disabled={uploading}
            >
              Annuler
            </Button>

            <Button
              onClick={uploadToApi}
              disabled={!file || uploading}
            >
              {uploading ? "Upload..." : "Uploader"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

    </div>
  )
}
