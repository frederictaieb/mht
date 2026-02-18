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
    <section className="mt-4 p-4 border rounded-xl bg-white">

      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Images</h2>

        <button
          onClick={onRefresh}
          disabled={loading}
          className="px-3 py-2 border rounded-md text-sm hover:bg-gray-100 disabled:opacity-50"
        >
          {loading ? "Chargement..." : "Rafraîchir"}
        </button>
      </div>

      <div className="mt-4">

        {/* Error */}
        {error && (
          <pre className="whitespace-pre-wrap text-red-600 text-sm">
            {error}
          </pre>
        )}

        {/* Empty */}
        {files.length === 0 ? (
          <p className="opacity-70 text-sm">Aucune image.</p>
        ) : (
          <div className="mt-4 grid gap-4 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
            {files.map((f) => {
              const url = `${API_BASE}/img/${encodeURIComponent(f)}`;

              return (
                <div
                  key={f}
                  className="border rounded-xl overflow-hidden bg-white shadow-sm hover:shadow-md transition"
                >
                  {/* Image container */}
                  <div className="w-full aspect-square bg-gray-100 flex items-center justify-center">
                    <img
                      src={url}
                      alt={f}
                      className="max-h-full max-w-full object-contain"
                      loading="lazy"
                      onError={(e) => {
                        (e.currentTarget as HTMLImageElement).style.display = "none";
                      }}
                    />
                  </div>

                  {/* Filename */}
                  <div className="p-2">
                    <div
                      className="font-mono text-xs truncate"
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

      {!API_BASE && (
        <p className="mt-4 text-xs text-red-600">
          NEXT_PUBLIC_API_BASE_URL manquant (.env.local)
        </p>
      )}
    </section>
  );
}
