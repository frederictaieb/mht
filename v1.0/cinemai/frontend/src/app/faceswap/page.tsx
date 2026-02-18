import UploadCard from "@/components/ui/UploadCard"

export default async function Page() {
  const res_available = await fetch(
    "http://localhost:8000/faceswap/available/list",
    { cache: "no-store" }
  )

  const data_available = await res_available.json()

  const clean = (files: string[]) => (files ?? []).filter((f) => !f.startsWith("."))
  const first = clean(data_available.files)[0]

  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">MHT</h1>

      <div className="grid gap-4 grid-cols-1 md:grid-cols-3 items-stretch">
        {/* colonne 1 : video */}
        <div className="border border-black h-full overflow-hidden rounded-lg">
          {first ? (
            <video
              src={`http://localhost:8000/faceswap/available/video/${encodeURIComponent(first)}`}
              className="w-full aspect-video object-cover"
              autoPlay
              muted
              playsInline
              loop
            />
          ) : (
            <div className="w-full aspect-video grid place-items-center text-sm text-muted-foreground">
              Aucune vidéo available
            </div>
          )}
        </div>

        {/* colonne 2 : upload */}
        <UploadCard />

        {/* colonne 3 : placeholder */}
        <div className="border border-black h-full overflow-hidden rounded-lg">
          <img
            src="/placeholder-face.jpg"
            alt="Placeholder"
            className="w-full aspect-video object-cover"
          />
        </div>
      </div>
    </div>
  )
}
