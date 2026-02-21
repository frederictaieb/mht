"use client";
import FilePicker from "@/components/test/FilePicker";

export default function Page() {
  function handleFileReady(file: File) {
    console.log("Fichier choisi :", file.name);
  }

  return (
    <div>
      <FilePicker onFileReady={handleFileReady} />
    </div>
  );
}