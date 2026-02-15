export default async function Page() {

  const res_available = await fetch("http://localhost:8000/faceswap/available/list", {cache: "no-store"})
  const res_output = await fetch("http://localhost:8000/faceswap/output/list", {cache: "no-store"})



  const data_avaiable = await res_available.json()
  const data_output = await res_output.json()

  return (
    <div>
      <h1>Vidéos disponibles:</h1>
      <ul>
        {data_avaiable.files?.map((f: string) => (
          <li key={f}>{f}</li>
        ))}
      </ul>

      <h1>Vidéo générées:</h1>
      <ul>
        {data_output.files?.map((f: string) => (
          <li key={f}>{f}</li>
        ))}
      </ul>

    </div>
  )
}