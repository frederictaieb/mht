// src/app/mht/cinemai/layout.tsx
import { CinemaiProvider } from "@/app/mht/contexts/CinemaiContext"

export default function CinemaiLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <CinemaiProvider>{children}</CinemaiProvider>
}