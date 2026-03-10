"use client"

import React, { useMemo } from "react"
import { Canvas } from "@react-three/fiber"
import * as THREE from "three"

function RoundBlinkingDot({ size = 18, speed = 4 }) {
  const geom = useMemo(() => {
    const g = new THREE.BufferGeometry()
    g.setFromPoints([new THREE.Vector3(0, 0, 0)])
    return g
  }, [])

  const material = useMemo(() => {
    return new THREE.ShaderMaterial({
      transparent: true,
      depthWrite: false,
      uniforms: {
        uTime: { value: 0 },
        uSize: { value: size },
        uColor: { value: new THREE.Color("lime") },
        uSpeed: { value: speed },
      },
      vertexShader: `
        uniform float uSize;
        void main() {
          vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
          gl_Position = projectionMatrix * mvPosition;
          gl_PointSize = uSize;
        }
      `,
      fragmentShader: `
        uniform float uTime;
        uniform vec3 uColor;
        uniform float uSpeed;

        void main() {
          // gl_PointCoord : coords dans le carré du point, de 0..1
          vec2 c = gl_PointCoord - vec2(0.5);
          float d = length(c);

          // disque : on jette les pixels hors rayon
          if (d > 0.5) discard;

          // blink (0..1)
          float a = (sin(uTime * uSpeed) + 1.0) * 0.5;

          // petit anti-alias sur le bord
          float edge = smoothstep(0.5, 0.45, d);

          gl_FragColor = vec4(uColor, a * edge);
        }
      `,
    })
  }, [size, speed])

  return (
    <points
      geometry={geom}
      onBeforeRender={(_, __, ___, ____, materialObj) => {
        // On met à jour uTime juste avant rendu
        ;(materialObj as THREE.ShaderMaterial).uniforms.uTime.value =
          performance.now() / 1000
      }}
      material={material}
    />
  )
}

export default function Page() {
  return (
    <div style={{ height: 300 }}>
      <Canvas camera={{ position: [0, 0, 3], fov: 50 }}>
        <RoundBlinkingDot size={22} speed={5} />
      </Canvas>
    </div>
  )
}