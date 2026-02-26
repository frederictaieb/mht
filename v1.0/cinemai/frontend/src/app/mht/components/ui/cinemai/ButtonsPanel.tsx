import { useCinemai } from "@/app/mht/contexts/CinemaiContext";
import { Button } from "@/app/mht/components/ui/button";

export default function ButtonsPanel() {

    const { reset, submit } = useCinemai()

    return (
        <div className="flex justify-end gap-2">
            <Button
                onClick={reset}
                className="h-[40px] w-[100px] rounded-[6px] border border-red-500/40 bg-red-600 px-6 text-[14px] font-black tracking-[0.2em] text-white hover:bg-red-700"
            >
                RESET
            </Button>

            <Button
                onClick={submit}
                className="h-[40px] w-[100px] rounded-[6px] border border-blue-500/40 bg-blue-600 px-6 text-[14px] font-black tracking-[0.2em] text-white hover:bg-blue-700"
            >
                SUBMIT
            </Button>
        </div>
    )
}