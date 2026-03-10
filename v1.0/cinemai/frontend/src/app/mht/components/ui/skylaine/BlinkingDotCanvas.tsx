"use client"

import React, { useMemo, useRef } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import * as THREE from "three"

function BlinkingDot({ size = 14, speed = 4 }) {
  const mat = useRef<THREE.PointsMaterial>(null)

  // géométrie avec 1 point
  const geom = useMemo(() => {
    const g = new THREE.BufferGeometry()
    g.setFromPoints([new THREE.Vector3(0, 0, 0)])
    return g
  }, [])

  useFrame(({ clock }) => {
    const a = (Math.sin(clock.getElapsedTime() * speed) + 1) / 2
    if (mat.current) mat.current.opacity = a
  })

  return (
    <points geometry={geom}>
      <pointsMaterial
        ref={mat}
        color="lime"
        size={size}
        sizeAttenuation={false}
        transparent
        depthWrite={false}
      />
    </points>
  )
}

export default function BlinkingDotCanvas() {
  return (
    <div style={{ width: "100%", height: 300 }}>
      <Canvas camera={{ position: [0, 0, 3], fov: 50 }}>
        <BlinkingDot />
      </Canvas>
    </div>
  )
}