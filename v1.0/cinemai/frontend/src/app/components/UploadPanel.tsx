"use client";

import { useState } from "react";
import { uploadImage } from "../lib/api";

type Props = {
  onUploaded?: (filename: string) => void;
};

export function UploadPanel({ onUploaded }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  async function handleUpload() {
    if (!file) return;

    setUploading(true);
    setError("");

    try {
      const res = await uploadImage(file);
      onUploaded?.(res.filename);
      setFile(null);
      // (optionnel) reset l’input visuellement en changeant sa key (voir plus bas)
    } catch (e: any) {
      setError(e?.message ?? "Erreur upload");
    } finally {
      setUploading(false);
    }
  }

  return (
    <section style={{ marginTop: 16, padding: 12, border: "1px solid #ddd", borderRadius: 12 }}>
      <h2 style={{ marginTop: 0 }}>Upload</h2>

      <input
        type="file"
        accept="image/png,image/jpeg"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />

      <div style={{ marginTop: 12 }}>
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          style={{ padding: "8px 12px" }}
        >
          {uploading ? "Upload..." : "Uploader"}
        </button>
      </div>

      <div style={{ marginTop: 10, fontSize: 12, opacity: 0.7 }}>
        {file ? (
          <>
            Fichier sélectionné : <span style={{ fontFamily: "monospace" }}>{file.name}</span>
          </>
        ) : (
          "Aucun fichier sélectionné."
        )}
      </div>

      {error ? (
        <pre style={{ marginTop: 10, whiteSpace: "pre-wrap", color: "crimson" }}>{error}</pre>
      ) : null}
    </section>
  );
}
