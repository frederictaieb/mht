"use client";

import { useEffect, useMemo, useState } from "react";

type ImgListResponse = {
  directory: string;
  type: "list";
  count: number;
  files: string[];
};

type UploadResponse = {
  directory: string;
  type: "upload";
  filename: string;
};

type DeleteResponse = {
  directory: string;
  type: "delete";
  count: number;
};

type FaceSwapResponse = {
  output_file: string;
  output_path: string;
  frames: number;
  swapped_frames: number;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    // Important en dev si FastAPI est sur un autre domaine/port
    // (et si tu utilises cookies un jour)
    // credentials: "include",
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `HTTP ${res.status}`);
  }
  return (await res.json()) as T;
}

export default function FaceSwapPage() {
  const [images, setImages] = useState<string[]>([]);
  const [loadingList, setLoadingList] = useState(false);

  const [uploading, setUploading] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);

  const [deleting, setDeleting] = useState(false);

  const [selectedImg, setSelectedImg] = useState<string>("");
  const [vidFilename, setVidFilename] = useState<string>("");

  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<FaceSwapResponse | null>(null);

  const [error, setError] = useState<string>("");

  const canRun = useMemo(() => !!selectedImg && !!vidFilename, [selectedImg, vidFilename]);

  async function refreshImages() {
    setError("");
    setLoadingList(true);
    try {
      const data = await apiFetch<ImgListResponse>("/faceswap/img/list", {
        method: "POST",
      });
      setImages(data.files);
      // auto-select si rien n’est sélectionné
      if (!selectedImg && data.files.length > 0) {
        setSelectedImg(data.files[0]);
      }
    } catch (e: any) {
      setError(e?.message ?? "Erreur lors du listing");
    } finally {
      setLoadingList(false);
    }
  }

  useEffect(() => {
    refreshImages();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleUpload() {
    if (!uploadFile) return;

    setError("");
    setUploading(true);
    try {
      const form = new FormData();
      // ton backend attend param "f"
      form.append("f", uploadFile);

      const res = await fetch(`${API_BASE}/faceswap/img/upload`, {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(text || `HTTP ${res.status}`);
      }

      const data = (await res.json()) as UploadResponse;
      // refresh list
      await refreshImages();
      // sélectionne l’upload automatiquement
      setSelectedImg(data.filename);
      setUploadFile(null);
      // reset input file via state (l’input lui-même ne se reset pas automatiquement partout)
    } catch (e: any) {
      setError(e?.message ?? "Erreur upload");
    } finally {
      setUploading(false);
    }
  }

  async function handleDeleteAll() {
    setError("");
    setDeleting(true);
    setResult(null);

    try {
      const data = await apiFetch<DeleteResponse>("/faceswap/img/delete", {
        method: "DELETE",
      });
      await refreshImages();
      setSelectedImg("");
    } catch (e: any) {
      setError(e?.message ?? "Erreur suppression");
    } finally {
      setDeleting(false);
    }
  }

  async function handleRun() {
    if (!canRun) return;

    setError("");
    setRunning(true);
    setResult(null);

    try {
      const data = await apiFetch<FaceSwapResponse>("/faceswap/single", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ img: selectedImg, vid: vidFilename }),
      });
      setResult(data);
    } catch (e: any) {
      setError(e?.message ?? "Erreur faceswap");
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="min-h-screen p-6">
      <div className="mx-auto max-w-4xl space-y-6">
        <header className="space-y-1">
          <h1 className="text-2xl font-semibold">FaceSwap UI</h1>
          <p className="text-sm opacity-70">
            API: <span className="font-mono">{API_BASE || "(NEXT_PUBLIC_API_BASE_URL manquant)"}</span>
          </p>
        </header>

        {error ? (
          <div className="rounded-2xl border p-4">
            <p className="text-sm font-medium">Erreur</p>
            <pre className="mt-2 whitespace-pre-wrap text-sm opacity-80">{error}</pre>
          </div>
        ) : null}

        {/* Images */}
        <section className="rounded-2xl border p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold">Images</h2>
            <div className="flex gap-2">
              <button
                onClick={refreshImages}
                disabled={loadingList}
                className="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              >
                {loadingList ? "Actualisation..." : "Rafraîchir"}
              </button>
              <button
                onClick={handleDeleteAll}
                disabled={deleting}
                className="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              >
                {deleting ? "Suppression..." : "Supprimer tout"}
              </button>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {/* Upload */}
            <div className="rounded-2xl border p-4 space-y-3">
              <p className="text-sm font-medium">Upload</p>

              <input
                type="file"
                accept="image/png,image/jpeg"
                onChange={(e) => setUploadFile(e.target.files?.[0] ?? null)}
                className="block w-full text-sm"
              />

              <button
                onClick={handleUpload}
                disabled={!uploadFile || uploading}
                className="w-full rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              >
                {uploading ? "Upload..." : "Uploader l’image"}
              </button>

              <p className="text-xs opacity-70">
                Formats acceptés (backend) : jpg / jpeg / png
              </p>
            </div>

            {/* List + select */}
            <div className="rounded-2xl border p-4 space-y-3">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">Liste / sélection</p>
                <p className="text-xs opacity-70">{images.length} fichier(s)</p>
              </div>

              <select
                value={selectedImg}
                onChange={(e) => setSelectedImg(e.target.value)}
                className="w-full rounded-xl border px-3 py-2 text-sm"
              >
                <option value="" disabled>
                  -- Choisir une image --
                </option>
                {images.map((f) => (
                  <option key={f} value={f}>
                    {f}
                  </option>
                ))}
              </select>

              <div className="text-xs opacity-70">
                Image sélectionnée : <span className="font-mono">{selectedImg || "-"}</span>
              </div>
            </div>
          </div>
        </section>

        {/* Run faceswap */}
        <section className="rounded-2xl border p-5 shadow-sm space-y-4">
          <h2 className="text-lg font-semibold">Génération (FaceSwap)</h2>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border p-4 space-y-2">
              <label className="text-sm font-medium">Vidéo (nom de fichier)</label>
              <input
                value={vidFilename}
                onChange={(e) => setVidFilename(e.target.value)}
                placeholder="ex: myvideo.mp4"
                className="w-full rounded-xl border px-3 py-2 text-sm font-mono"
              />
              <p className="text-xs opacity-70">
                Ton backend attend un fichier existant dans <span className="font-mono">VID_DIR</span>.
                (Si tu ajoutes un endpoint /vid/list, on peut faire un select comme pour les images.)
              </p>
            </div>

            <div className="rounded-2xl border p-4 space-y-3">
              <p className="text-sm font-medium">Lancer</p>
              <button
                onClick={handleRun}
                disabled={!canRun || running}
                className="w-full rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              >
                {running ? "Traitement..." : "Générer (faceswap)"}
              </button>

              <div className="text-xs opacity-70 space-y-1">
                <div>
                  img: <span className="font-mono">{selectedImg || "-"}</span>
                </div>
                <div>
                  vid: <span className="font-mono">{vidFilename || "-"}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Result */}
          {result ? (
            <div className="rounded-2xl border p-4 space-y-2">
              <p className="text-sm font-medium">Résultat</p>
              <div className="text-sm">
                <div>
                  output_file: <span className="font-mono">{result.output_file}</span>
                </div>
                <div>
                  frames: <span className="font-mono">{result.frames}</span> — swapped_frames:{" "}
                  <span className="font-mono">{result.swapped_frames}</span>
                </div>
                <div className="opacity-70 text-xs mt-2">
                  output_path (côté serveur) : <span className="font-mono">{result.output_path}</span>
                </div>
              </div>

              <p className="text-xs opacity-70">
                Pour lire la vidéo dans le navigateur, ton backend doit exposer <span className="font-mono">OUTPUT_DIR</span> en statique
                (ex: <span className="font-mono">/static/output/...</span>). Je te montre comment juste dessous.
              </p>
            </div>
          ) : null}
        </section>

        {/* Tips backend */}
        <section className="rounded-2xl border p-5 shadow-sm space-y-2">
          <h2 className="text-lg font-semibold">Pour afficher la vidéo générée dans la page</h2>
          <p className="text-sm opacity-80">
            Actuellement tu renvoies un <span className="font-mono">output_path</span> absolu côté serveur.
            Pour que le frontend puisse lire le fichier, il faut le servir via FastAPI (static files).
          </p>

          <pre className="rounded-xl border p-4 text-xs overflow-auto">
{`# app/main.py (exemple)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings

app = FastAPI()

# Expose le dossier OUTPUT_DIR (ou un sous-dossier)
app.mount("/output", StaticFiles(directory=settings.OUTPUT_DIR), name="output")`}
          </pre>

          <p className="text-sm opacity-80">
            Ensuite, dans la réponse, tu peux retourner aussi une URL lisible :
            <span className="font-mono"> {"{ output_url: `/output/${out_name}` }"} </span>
          </p>
        </section>
      </div>
    </div>
  );
}
