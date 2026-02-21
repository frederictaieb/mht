"use client";

type Props = {
  onFileReady: (file: File) => void;
};

export default function FilePicker({ onFileReady }: Props) {
  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) {
      onFileReady(file);
    }
  }
  return <input type="file" onChange={handleChange} />;
}