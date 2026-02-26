// src/app/mht/components/ui/cinemai/FaceswapRow.tsx
"use client"

import UploadImageCard from "../cinemai/UploadImageCard"
import AvailableVideoCard from "./AvailableVideoCard"
import FaceswapVideoCard from "./FaceswapVideoCard"
import { useCinemai } from "@/app/mht/contexts/CinemaiContext"

type Props = { vid: string }

export default function FaceswapRow({ vid }: Props) {
  const { rows, setInputImg } = useCinemai()
  const row = rows.find(r => r.input_vid === vid)

  const imgName = row?.input_img ?? null
  const isImgReady = !!imgName

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-3 items-stretch">
      <AvailableVideoCard vid={vid} />

      <UploadImageCard
        vid={vid}
        imgName={imgName} // ✅ important: contrôle par le context
        onImgUploaded={(name) => setInputImg(vid, name)}
      />

      <FaceswapVideoCard
        isReady={isImgReady}
        vid={vid}
        img={imgName ?? ""}
      />
    </div>
  )
}