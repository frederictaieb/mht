// src/app/mht/components/ui/cinemai/AvailableVideoCard.tsx
"use client"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

export default function AvailableVideoCard({ vid }: { vid?: string }) {
  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">
      {vid ? (
        <video
          src={`${API_BASE}/cinemai/static/available_videos/${encodeURIComponent(vid)}`}
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
  )
}