//app/components/mht/Logo.tsx

import Image from "next/image";

export function Logo() {
  return (
    <div className="relative h-16 w-[180px]">
      <Image
        src="/images/mht_logo.png"
        alt="Logo"
        fill
        className="object-contain"
      />
    </div>
  );
}