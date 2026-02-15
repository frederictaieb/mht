"use client";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

type Props = {
  files: string[];
  loading: boolean;
  error: string;
  onRefresh: () => void;
};

export function ImagesPanel({ files, loading, error, onRefresh }: Props) {
  return (
    <section style={{ marginTop: 16, padding: 12, border: "1px solid #ddd", borderRadius: 12 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, justifyContent: "space-between" }}>
        <h2 style={{ margin: 0 }}>Images</h2>
        <button onClick={onRefresh} disabled={loading} style={{ padding: "8px 12px" }}>
          {loading ? "Chargement..." : "Rafraîchir"}
        </button>
      </div>

      <div style={{ marginTop: 12 }}>
        {error ? (
          <pre style={{ whiteSpace: "pre-wrap", color: "crimson" }}>{error}</pre>
        ) : null}

        {files.length === 0 ? (
          <p style={{ opacity: 0.7 }}>Aucune image.</p>
        ) : (
          <div
            style={{
              marginTop: 12,
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))",
              gap: 12,
            }}
          >
            {files.map((f) => {
              const url = `${API_BASE}/img/${encodeURIComponent(f)}`;

              return (
                <div
                  key={f}
                  style={{
                    border: "1px solid #eee",
                    borderRadius: 12,
                    overflow: "hidden",
                    background: "white",
                  }}
                >
                  <div
                    style={{
                      width: "100%",
                      aspectRatio: "1 / 1",
                      background: "#f6f6f6",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    {/* img classique (simple, pas besoin next/image pour commencer) */}
                    <img
                      src={url}
                      alt={f}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                      loading="lazy"
                      onError={(e) => {
                        // Si l’image n’est pas servie correctement, on affiche un placeholder
                        (e.currentTarget as HTMLImageElement).style.display = "none";
                      }}
                    />
                  </div>

                  <div style={{ padding: 8 }}>
                    <div
                      style={{
                        fontFamily: "monospace",
                        fontSize: 12,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                      title={f}
                    >
                      {f}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {!API_BASE ? (
        <p style={{ marginTop: 12, fontSize: 12, color: "crimson" }}>
          NEXT_PUBLIC_API_BASE_URL manquant (.env.local)
        </p>
      ) : null}
    </section>
  );
}
