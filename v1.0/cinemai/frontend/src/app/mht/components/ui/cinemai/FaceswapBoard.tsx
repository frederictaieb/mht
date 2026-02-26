// src/app/mht/components/ui/cinemai/FaceswapBoard.tsx
"use client"

import FaceswapRow from "@/app/mht/components/ui/cinemai/FaceswapRow"
import { useCinemai } from "@/app/mht/contexts/CinemaiContext"
import ButtonsPanel   from "@/app/mht/components/ui/cinemai/ButtonsPanel"

export default function FaceswapBoard() {
  const { rows, isLoading} = useCinemai()

  return (
    <div className="container mx-auto p-6 space-y-6">
      <ButtonsPanel />

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

