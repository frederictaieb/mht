import FaceswapBoard from "@/components/ui/FaceswapBoard"

export default async function Page() {
  const res_available = await fetch("http://localhost:8000/faceswap/available/list", {
    cache: "no-store",
  })
  const data_available = await res_available.json()

  const clean = (files: string[]) => (files ?? []).filter((f) => !f.startsWith("."))
  const first = clean(data_available.files)[0]

  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">MHT</h1>
      <FaceswapBoard firstVideo={first} />
    </div>
  )
}
