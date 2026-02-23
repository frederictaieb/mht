// UploadImageCard.tsx

import { useEffect, useRef, useState } from "react";

type Props = {
  vid: string;
  onImgUploaded: (img: string) => void;
};

type UploadResponse = {
  img_name: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

export default function UploadImageCard({ vid, onImgUploaded }: Props) {
  // 👉 ton "pickle" (state local)
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [selectedImageUrl, setSelectedImageUrl] =  useState<string | null>(null) //
  const inputRef = useRef<HTMLInputElement | null>(null) //
  const  selectImage = () => inputRef.current?.click()

  useEffect(() => {
    console.log("*** UploadImageCard - selectedImage", selectedImage)
  }, [selectedImage])

  const handleChangeImage = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const file = e.target.files[0];
    if (!file) 
      return

    try {

      const form = new FormData()
      form.append("image", file)
      form.append("name", vid )

      const res = await fetch(`${API_BASE}/faceswap/upload/image`, {
        method: "POST",
        body: form,
      })

      if (!res.ok) {
        const txt = await res.text()
        throw new Error(txt || `Upload failed (${res.status})`)
      }

      const data = (await res.json()) as UploadResponse;

      if (!data?.img_name) {
        throw new Error("Réponse API invalide: img_name manquant");
      }

      onImgUploaded(data.img_name);

    } catch (e: any) {
      console.error(e);
    } finally {
      e.target.value = "";
    }
      
    // stocker dans le state (pickle)
    setSelectedImage(file);
    setSelectedImageUrl(URL.createObjectURL(file))

  };

  function renderImageContent() {
    if (selectedImageUrl) {
      return (
        <img
          src={selectedImageUrl}
          className="absolute inset-0 w-full h-full object-contain"
        />
      );
    }
  
    return (
      <div className="absolute inset-0 grid place-items-center">
        <span className="text-sm text-muted-foreground">
          Cliquer pour uploader une image
        </span>
      </div>
    );
  }

  return (
    <div className="border border-black rounded-lg overflow-hidden flex flex-col">
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg"
        onChange={handleChangeImage}
        className="hidden"
      />

      <div 
        className="w-full aspect-video bg-gray-200 rounded overflow-hidden relative cursor-pointer hover:bg-gray-100 transition"
        onClick={selectImage}
      >
        {renderImageContent()}
      </div>
    </div>
  );
}