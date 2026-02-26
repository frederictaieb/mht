// src/app/mht/contexts/CinemaiContext.tsx
"use client"

import React, { createContext, useContext, useEffect, useMemo, useState } from "react"

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

export type CinemaiRowState = {
  input_vid: string
  input_img: string | null
  output_vid: string | null
}

type BoardStateResponse = {
  rows: CinemaiRowState[]
  required: number
}

type CinemaiContextValue = {
  rows: CinemaiRowState[]
  isLoading: boolean
  refresh: () => Promise<void>
  reset: () => Promise<void>
  submit: () => Promise<void>
  setInputImg: (vid: string, imgName: string | null) => void
  setOutputVid: (vid: string, outputVid: string | null) => void
  required: number
  canSubmit: boolean
  submitLabel: string
}

const CinemaiContext = createContext<CinemaiContextValue | null>(null)

export function useCinemai() {
  const ctx = useContext(CinemaiContext)
  if (!ctx) throw new Error("useCinemai must be used within CinemaiProvider")
  return ctx
}

async function fetchBoardState(): Promise<BoardStateResponse>{
  const res = await fetch(`${API_BASE}/cinemai/board_state`, { cache: "no-store" })
  if (!res.ok) throw new Error(await res.text())
  const data = await res.json()
  return {
    rows: data.rows ?? [],
    required: Number(data.required ?? 10),
  }
}

export function CinemaiProvider({ children }: { children: React.ReactNode }) {
  const [rows, setRows] = useState<CinemaiRowState[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [required, setRequired] = useState<number>(10)

  const refresh = async () => {
    setIsLoading(true)
    try {
      const { rows: serverRows, required: req } = await fetchBoardState()
      setRequired(req)
      setRows(serverRows.slice(0, req))
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
    await fetch(`${API_BASE}/cinemai/submit`, { method: "DELETE" })
    await refresh()
  }

  const setInputImg = (vid: string, imgName: string | null) => {
    setRows(prev => prev.map(r => (r.input_vid === vid ? { ...r, input_img: imgName } : r)))
  }

  const setOutputVid = (vid: string, outputVid: string | null) => {
    setRows(prev => prev.map(r => (r.input_vid === vid ? { ...r, output_vid: outputVid } : r)))
  }
  
  const filledCount = useMemo(() => rows.filter(r => !!r.output_vid).length, [rows])
  const canSubmit = rows.length === required && filledCount === required
  const submitLabel = canSubmit ? "SUBMIT" : `(${filledCount}/${required})`

  const value = useMemo(() => ({
    rows,
    isLoading,
    refresh,
    reset,
    submit,
    setInputImg,
    setOutputVid,
    required,
    canSubmit,
    submitLabel,
  }), [rows, isLoading, required, canSubmit, submitLabel])

  return <CinemaiContext.Provider value={value}>{children}</CinemaiContext.Provider>
}