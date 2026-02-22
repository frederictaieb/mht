// UploadImageCard.tsx

import { useRef, useState } from "react";

type Props = {
  onImageUploaded: (image: File) => void;
};

export default function UploadImageCard({ onImageUploaded }: Props) {
  // 👉 ton "pickle" (state local)
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [selectedImageUrl, setSelectedImageUrl] =  useState<string | null>(null) //
  const inputRef = useRef<HTMLInputElement | null>(null) //
  const  selectImage = () => inputRef.current?.click()
  

  const handleChangeImage = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const file = e.target.files[0];

    // stocker dans le state (pickle)
    setSelectedImage(file);
    setSelectedImageUrl(URL.createObjectURL(file))

    // envoyer au parent
    onImageUploaded(file);
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