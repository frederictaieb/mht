//GeneratedVideoCard.tsx
"use client"

type Props = {
  generating: boolean
  resultUrl: string | null
  error: string | null
  hasInput: boolean
  onDoubleClick?: () => void
  onVideoCanPlay?: () => void
}

export default function GeneratedVideoCard({
  generating,
  resultUrl,
  error,
  hasInput,
  onDoubleClick,
  onVideoCanPlay,
}: Props) {
  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">
      <div
        className="w-full aspect-video bg-gray-200 rounded overflow-hidden grid place-items-center cursor-pointer hover:bg-gray-200 transition"
        onDoubleClick={() => {
            console.log("DOUBLE CLICK ✅", { hasInput, generating, resultUrl })
            onDoubleClick?.()
          }}
        title={hasInput ? "Double-clic pour générer" : "Choisis une image d'abord"}
      >
        {generating ? (
          <div className="text-sm text-muted-foreground">Génération en cours…</div>
        ) : resultUrl ? (
          <video
            src={resultUrl}
            className="w-full h-full object-cover"
            autoPlay
            muted
            playsInline
            loop
            onCanPlay={onVideoCanPlay}
          />
        ) : hasInput ? (
          <div className="text-sm text-muted-foreground">
            Double-clic pour générer
          </div>
        ) : (
          <div className="text-sm text-muted-foreground">En attente d'image ...</div>
        )}
      </div>

      {error && (
        <div className="text-sm text-red-600 whitespace-pre-wrap">{error}</div>
      )}
    </div>
  )
}