import Link from "next/link";
import Image from "next/image";

export function Logo() {
  return (
      <Image
        src="/images/mht_logo.png"
        alt="Moi"
        width={256}
        height={256}
        className="rounded-full"
        priority={false}
    />
  );
}