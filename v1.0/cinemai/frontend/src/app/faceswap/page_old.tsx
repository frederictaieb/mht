import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default async function Page() {
  const res_available = await fetch("http://localhost:8000/faceswap/available/list", { cache: "no-store" })
  const data_available = await res_available.json()

  const res_output = await fetch("http://localhost:8000/faceswap/output/list", { cache: "no-store" })
  const data_output = await res_output.json()

  const clean = (files: string[]) => (files ?? []).filter((f) => !f.startsWith("."))

  return (
    <div className="container mx-auto p-6 space-y-8">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold">Vidéos disponibles</h1>
        <p className="text-sm text-muted-foreground">
          Aperçu en boucle. Clique pour ouvrir (on ajoutera ça après).
        </p>
      </div>

      <div className="grid gap-4 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {clean(data_available.files).map((f: string) => (
          <Card key={f} className="overflow-hidden">
            <CardContent className="p-0">
              <video
                src={`http://localhost:8000/faceswap/available/video/${encodeURIComponent(f)}`}
                className="w-full aspect-video object-cover"
                autoPlay
                muted
                playsInline
                loop
              />
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="space-y-2">
        <h2 className="text-2xl font-semibold">Vidéos générées</h2>
      </div>

      <div className="grid gap-4 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {clean(data_output.files).map((f: string) => (
          <Card key={f} className="overflow-hidden">
            <CardContent className="p-0">
              <video
                src={`http://localhost:8000/faceswap/output/video/${encodeURIComponent(f)}`}
                className="w-full aspect-video object-cover"
                autoPlay
                muted
                playsInline
                loop
              />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
