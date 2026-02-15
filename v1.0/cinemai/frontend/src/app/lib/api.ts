const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  if (!API_BASE) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is missing (.env.local).");
  }

  const res = await fetch(`${API_BASE}${path}`, init);

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `HTTP ${res.status}`);
  }

  return (await res.json()) as T;
}

export async function listImages() {
  return apiFetch("/faceswap/img/list", { method: "POST" });
}

export async function deleteAllImages() {
  return apiFetch("/faceswap/img/delete", { method: "DELETE" });
}

export async function uploadImage(file: File) {
  if (!API_BASE) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL est manquant (.env.local).");
  }

  const form = new FormData();
  // ton backend attend un champ "f"
  form.append("f", file);

  const res = await fetch(`${API_BASE}/faceswap/img/upload`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `HTTP ${res.status}`);
  }

  return (await res.json()) as { directory: string; type: "upload"; filename: string };
}