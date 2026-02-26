// src/app/mht/contexts/CinemaiContext.tsx
"use client"

import React, { createContext, useContext, useEffect, useMemo, useState } from "react"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

export type CinemaiRowState = {
  input_vid: string
  input_img: string | null
  output_vid: string | null
}

type CinemaiContextValue = {
  rows: CinemaiRowState[]
  isLoading: boolean
  refresh: () => Promise<void>
  reset: () => Promise<void>
  submit: () => Promise<void>
  setInputImg: (vid: string, imgName: string | null) => void
  setOutputVid: (vid: string, outputVid: string | null) => void
}

const CinemaiContext = createContext<CinemaiContextValue | null>(null)

export function useCinemai() {
  const ctx = useContext(CinemaiContext)
  if (!ctx) throw new Error("useCinemai must be used within CinemaiProvider")
  return ctx
}

async function fetchBoardState(): Promise<CinemaiRowState[]> {
  const res = await fetch(`${API_BASE}/cinemai/board_state`, { cache: "no-store" })
  if (!res.ok) throw new Error(await res.text())
  const data = await res.json()
  return data.rows ?? []
}

export function CinemaiProvider({ children }: { children: React.ReactNode }) {
  const [rows, setRows] = useState<CinemaiRowState[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const refresh = async () => {
    setIsLoading(true)
    try {
      const serverRows = await fetchBoardState()
      setRows(serverRows.slice(0, 10))
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  const reset = async () => {
    await fetch(`${API_BASE}/cinemai/reset`, { method: "DELETE" })
    await refresh()
  }

  const submit = async () => {
    await fetch(`${API_BASE}/cinemai/submit`, { method: "GET" })
    await refresh()
  }

  const setInputImg = (vid: string, imgName: string | null) => {
    setRows(prev => prev.map(r => (r.input_vid === vid ? { ...r, input_img: imgName } : r)))
  }

  const setOutputVid = (vid: string, outputVid: string | null) => {
    setRows(prev => prev.map(r => (r.input_vid === vid ? { ...r, output_vid: outputVid } : r)))
  }

  const value = useMemo(() => ({
    rows,
    isLoading,
    refresh,
    reset,
    submit,
    setInputImg,
    setOutputVid,
  }), [rows, isLoading])

  return <CinemaiContext.Provider value={value}>{children}</CinemaiContext.Provider>
}