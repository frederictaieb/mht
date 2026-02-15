"use client";

import { useState } from "react";

import type { ImgListResponse } from "../types/faceswap";
import { listImages } from "../lib/api";

import { UploadPanel } from "../components/UploadPanel";
import { DeletePanel } from "../components/DeletePanel";
import { ImagesPanel } from "../components/ImagesPanel";

export default function FaceSwapPage() {
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<string[]>([]);
  const [error, setError] = useState<string>("");

  async function refreshImages() {
    setLoading(true);
    setError("");

    try {
      const data = (await listImages()) as ImgListResponse;
      setFiles(data.files);
    } catch (e: any) {
      setError(e?.message ?? "Erreur lors du listing");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: 20 }}>
      <h1>FaceSwap</h1>
      <p style={{ opacity: 0.7 }}>
        Upload / Delete / List — architecture modulaire
      </p>

      <UploadPanel onUploaded={() => refreshImages()} />

      <ImagesPanel
        files={files}
        loading={loading}
        error={error}
        onRefresh={refreshImages}
      />

      <DeletePanel onDeleted={() => refreshImages()} />


    </main>
  );
}
