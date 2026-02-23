// FaceswapRow.tsx
"use client"

import { useRef, useState, useEffect } from "react"
import UploadImageCard from "./UploadImageCard"
import AvailableVideoCard from "./AvailableVideoCard"
import FaceswapVideoCard from "./FaceswapVideoCard"
import GeneratedVideoCard from "./GeneratedVideoCard copy"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

type Props = {
  vid: string
}

export default function FaceswapRow({ vid }: Props) {

  //const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [img, setImg] = useState("")
  const isImgReady = !!img


  useEffect(() => {
    console.log("FaceswapRow - selectedImage changed:", img)
  }, [img])

  // ref sur la vidéo de gauche (si tu veux la remettre à 0)
  const leftVideoRef = useRef<HTMLVideoElement | null>(null)

  const syncLeftToZero = () => {
    const left = leftVideoRef.current
    if (!left) return
    left.muted = true
    left.currentTime = 0
    left.play().catch(() => {})
  }

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-3 items-stretch">

      <AvailableVideoCard vid={vid} />

      <UploadImageCard 
        vid={vid} 
        onImgUploaded = {
          (img:string) => {
            setImg(img)
          }
        }
      />

      <FaceswapVideoCard 
        isReady={isImgReady}
        vid={vid}
        img={img} 
      />
    </div>
  )
}