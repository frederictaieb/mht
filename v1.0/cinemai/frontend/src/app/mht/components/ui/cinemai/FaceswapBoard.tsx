// src/app/mht/components/ui/cinemai/FaceswapBoard.tsx
"use client"

import FaceswapRow from "@/app/mht/components/ui/cinemai/FaceswapRow"
import { Button } from "@/app/mht/components/ui/button";
import { useCinemai } from "@/app/mht/contexts/CinemaiContext"
import { useEffect, useState } from "react";

export default function FaceswapBoard() {
  const { rows, isLoading, reset, submit } = useCinemai()

  //const [files, setFiles] = useState<string[]>([])

  //const fetchFiles = async () => {
  //  const res = await fetch("http://localhost:8000/cinemai/available_videos")
  //  const data = await res.json()
  //  setFiles(data.files)
  //}

  //useEffect(() => {
  //  fetchFiles()
  //}, [])

  //const handleReset = async () => {
  //  await fetch("http://localhost:8000/cinemai/reset", {
  //    method: "DELETE",
  //  })

    // refresh après reset
  //  await fetchFiles()
  //}

  //const handleSubmit = async () => {
  //  await fetch("http://localhost:8000/cinemai/submit", {
  //    method: "GET",
  //  })

    // refresh après reset
  //  await fetchFiles()
  //}

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-end gap-2">
        <Button
          onClick={reset}
          className="h-[40px] w-[100px] rounded-[6px] border border-red-500/40 bg-red-600 px-6 text-[14px] font-black tracking-[0.2em] text-white hover:bg-red-700"
        >
          RESET
        </Button>

        <Button
          onClick={submit}
          className="h-[40px] w-[100px] rounded-[6px] border border-blue-500/40 bg-blue-600 px-6 text-[14px] font-black tracking-[0.2em] text-white hover:bg-blue-700"
        >
          SUBMIT
        </Button>
      </div>

      {isLoading ? (
        <div className="text-sm text-muted-foreground">Chargement…</div>
      ) : (
        rows.map((row) => (
          <FaceswapRow key={row.input_vid} vid={row.input_vid} />
        ))
      )}
    </div>
  )
}

