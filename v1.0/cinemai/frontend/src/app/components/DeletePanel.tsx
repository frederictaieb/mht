"use client";

import { useState } from "react";
import { deleteAllImages } from "../lib/api";

type Props = {
  onDeleted?: () => void;
};

export function DeletePanel({ onDeleted }: Props) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");

  async function handleDelete() {
    // mini-confirmation (simple et efficace)
    const ok = window.confirm("Supprimer toutes les images ?");
    if (!ok) return;

    setDeleting(true);
    setError("");

    try {
      await deleteAllImages();
      onDeleted?.();
    } catch (e: any) {
      setError(e?.message ?? "Erreur suppression");
    } finally {
      setDeleting(false);
    }
  }

  return (
    <section style={{ marginTop: 16, padding: 12, border: "1px solid #ddd", borderRadius: 12 }}>
      <h2 style={{ marginTop: 0 }}>Suppression</h2>

      <button
        onClick={handleDelete}
        disabled={deleting}
        style={{ padding: "8px 12px" }}
      >
        {deleting ? "Suppression..." : "Supprimer toutes les images"}
      </button>

      {error ? (
        <pre style={{ marginTop: 10, whiteSpace: "pre-wrap", color: "crimson" }}>{error}</pre>
      ) : null}
    </section>
  );
}
