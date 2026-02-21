import FaceswapRow from "@/components/ui/FaceswapRow"

export default async function FaceswapBoard() {

    const res = await fetch("http://localhost:8000/faceswap/available/list", {cache: "no-store",})
    const available_files =await res.json()

    return (
        <div className="container mx-auto p-6 space-y-6">
            {available_files.files.map((file: string, index: number) => (
                <FaceswapRow key={index} vid={file} />
            ))}
        </div>
    )
}