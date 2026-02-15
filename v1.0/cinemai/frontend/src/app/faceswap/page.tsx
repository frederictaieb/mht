export default async function Page() {

  const res_available = await fetch("http://localhost:8000/faceswap/available/list", { cache: "no-store" })
  const data_available = await res_available.json()

  const res_output = await fetch("http://localhost:8000/faceswap/output/list", { cache: "no-store" })
  const data_output= await res_output.json()

  const clean = (files: string[]) => (files ?? []).filter(f => !f.startsWith("."))

  return (
    <div>
      <h1>Vidéos disponibles</h1>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, 200px)",
        gap: "10px"
      }}>

        {clean(data_available.files).map((f: string) => (

          <div key={f}>

            <video
              src={`http://localhost:8000/faceswap/available/video/${encodeURIComponent(f)}`}
              width={200}
              autoPlay
              muted
              playsInline
              loop
            />

            <div>{f}</div>

          </div>

        ))}
      </div>

      <h1>Vidéos générées</h1>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, 200px)",
        gap: "10px"
      }}>

        {clean(data_output.files).map((f: string) => (

          <div key={f}>

            <video
              src={`http://localhost:8000/faceswap/output/video/${encodeURIComponent(f)}`}
              width={200}
              autoPlay
              muted
              playsInline
              loop
            />

            <div>{f}</div>

          </div>

        ))}

      </div>
    </div>
  )
}
