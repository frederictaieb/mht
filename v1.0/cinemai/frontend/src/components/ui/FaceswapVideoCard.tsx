//GeneratedVideoCard.tsx
"use client"

type Props = {
  isImageReady: boolean; // si tu veux garder cette casse (pas recommandé)
};

export default function FaceswapVideoCard({ isImageReady }: Props) { 
  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">

      {isImageReady ? (
        <div
          className="w-full aspect-video bg-gray-200 rounded overflow-hidden grid place-items-center cursor-pointer hover:bg-gray-100 transition"
          onDoubleClick={() => console.log("FaceswapVideoCard")}
        >
          <div className="text-sm text-muted-foreground">Cliquer pour générer la vidéo</div>
        </div>
      ) : (
        <div
          className="w-full aspect-video bg-gray-200 rounded overflow-hidden grid place-items-center cursor-pointer hover:bg-gray-200 transition"
        />
      )}
    </div>
  )
}