#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import math
import urllib.request
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


# -----------------------------
# Config
# -----------------------------
IMAGE_PATH = "skyline.jpeg"  # <-- mets ici ton fichier (ou un chemin)
OUT_DIR = Path("out")

# Proxy "Dow volume" : ETF DIA (SPDR Dow Jones Industrial Average ETF)
# Stooq CSV daily: Date,Open,High,Low,Close,Volume
STOOQ_CSV_URL = "https://stooq.com/q/d/l/?s=dia.us&i=d"

# Extraction ciel/bâtiment (adapté à ta photo : ciel clair + faible saturation)
HSV_S_MAX = 70
HSV_V_MIN = 150

# Lissage
SMOOTH_WINDOW = 21  # impair, plus grand = plus lisse

# Animation
CANVAS_BG = "#05060A"
LINE_COLOR = "#9AFBFF"
GLOW_COLOR = "rgba(154,251,255,0.25)"


# -----------------------------
# Utils
# -----------------------------
def moving_average(y: np.ndarray, window: int) -> np.ndarray:
    if window < 3:
        return y
    if window % 2 == 0:
        window += 1
    pad = window // 2
    ypad = np.pad(y, (pad, pad), mode="edge")
    kernel = np.ones(window, dtype=np.float32) / window
    return np.convolve(ypad, kernel, mode="valid")


def rdp_simplify(points, epsilon=1.5):
    """
    Simplification Ramer-Douglas-Peucker (optionnel mais utile).
    points: list[(x,y)]
    """
    if len(points) < 3:
        return points

    def perp_dist(pt, a, b):
        (x, y), (x1, y1), (x2, y2) = pt, a, b
        if x1 == x2 and y1 == y2:
            return math.hypot(x - x1, y - y1)
        num = abs((y2 - y1)*x - (x2 - x1)*y + x2*y1 - y2*x1)
        den = math.hypot(y2 - y1, x2 - x1)
        return num / den

    def recurse(pts):
        a = pts[0]
        b = pts[-1]
        max_d = -1.0
        idx = -1
        for i in range(1, len(pts) - 1):
            d = perp_dist(pts[i], a, b)
            if d > max_d:
                max_d = d
                idx = i
        if max_d > epsilon:
            left = recurse(pts[:idx+1])
            right = recurse(pts[idx:])
            return left[:-1] + right
        return [a, b]

    return recurse(points)


def download_stooq_csv(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_stooq_volume_series(csv_text: str, max_points=365):
    """
    Retourne une liste de dict: [{date, volume, v_norm}, ...]
    Normalisation log pour avoir un rendu stable.
    """
    lines = [l.strip() for l in csv_text.splitlines() if l.strip()]
    if len(lines) < 3 or "Volume" not in lines[0]:
        raise ValueError("CSV Stooq invalide / inattendu")

    # Skip header, parse from oldest->newest
    rows = []
    for l in lines[1:]:
        parts = l.split(",")
        if len(parts) < 6:
            continue
        date_s, vol_s = parts[0], parts[5]
        try:
            vol = float(vol_s)
        except:
            continue
        rows.append((date_s, vol))

    # Limiter aux derniers max_points (et garder ordre chronologique)
    rows = rows[-max_points:]

    vols = np.array([v for _, v in rows], dtype=np.float64)
    # log-normalisation robuste
    vols_clipped = np.clip(vols, 1.0, None)
    logs = np.log(vols_clipped)
    lo, hi = float(np.min(logs)), float(np.max(logs))
    if hi - lo < 1e-9:
        norms = np.zeros_like(logs)
    else:
        norms = (logs - lo) / (hi - lo)

    series = []
    for (date_s, vol), vn in zip(rows, norms):
        series.append({"date": date_s, "volume": vol, "v_norm": float(vn)})

    return series


def generate_html(out_path: Path):
    html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>NYC Skyline ECG — volume (proxy DIA)</title>
  <style>
    html, body {{
      margin: 0; padding: 0;
      background: {CANVAS_BG};
      color: #d7d7d7;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      height: 100%;
      overflow: hidden;
    }}
    #wrap {{
      display: grid;
      grid-template-rows: auto 1fr;
      height: 100%;
    }}
    header {{
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      display: flex;
      align-items: baseline;
      gap: 12px;
      flex-wrap: wrap;
    }}
    header strong {{
      color: {LINE_COLOR};
      letter-spacing: 0.4px;
    }}
    header small {{
      opacity: 0.75;
    }}
    #hud {{
      margin-left: auto;
      display: flex;
      gap: 14px;
      align-items: baseline;
      flex-wrap: wrap;
      opacity: 0.9;
    }}
    #canvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}
    .pill {{
      padding: 4px 10px;
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 999px;
      background: rgba(255,255,255,0.03);
    }}
  </style>
</head>
<body>
<div id="wrap">
  <header>
    <strong>NYC Skyline → “ECG électronique”</strong>
    <small>Amplitude pilotée par le volume (proxy Dow : DIA, daily)</small>
    <div id="hud">
      <div class="pill">Date: <span id="date">—</span></div>
      <div class="pill">Vol: <span id="vol">—</span></div>
      <div class="pill">Amp: <span id="amp">—</span></div>
    </div>
  </header>
  <canvas id="canvas"></canvas>
</div>

<script>
(async function() {{
  const skyline = await fetch("skyline.json").then(r => r.json());
  const series = await fetch("volume_series.json").then(r => r.json());

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  const hudDate = document.getElementById("date");
  const hudVol  = document.getElementById("vol");
  const hudAmp  = document.getElementById("amp");

  // Resize canvas to device pixels
  function resize() {{
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.floor(rect.width * dpr);
    canvas.height = Math.floor(rect.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // draw in CSS pixels
  }}
  window.addEventListener("resize", resize);
  resize();

  // Skyline points (x,y) from extraction: original image width & half-height.
  // We'll normalize to [0..1] for scaling to canvas.
  const xs = skyline.map(p => p[0]);
  const ys = skyline.map(p => p[1]);
  const maxX = Math.max(...xs);
  const maxY = Math.max(...ys);
  const minY = Math.min(...ys);

  const pts = skyline.map(([x,y]) => {{
    return {{
      x: x / maxX,
      y: (y - minY) / (maxY - minY + 1e-9)  // 0..1
    }};
  }});

  // ECG-like deformation field
  function pseudoNoise(i, t) {{
    // Mix de sinusoïdes + micro-variation
    const a = Math.sin(i*0.035 + t*4.0);
    const b = Math.sin(i*0.12  + t*1.8);
    const c = Math.sin(i*0.007 + t*7.0);
    return (a*0.55 + b*0.35 + c*0.10);
  }}

  // Add sharp "spikes" like ECG (rare peaks)
  function spike(i, t) {{
    // A moving spike window
    const speed = 0.9; // how fast the spike travels along skyline
    const center = (t * speed) % 1.0; // 0..1
    const xi = pts[i].x;
    const d = Math.abs(xi - center);
    const width = 0.018;
    if (d > width) return 0;
    // narrow peak shape
    const u = 1 - (d / width);
    // asymmetric spike: rise fast, fall slower
    return Math.pow(u, 3) * (xi < center ? 1.2 : 0.8);
  }}

  // Map volume norm (0..1) -> amplitude pixels
  function ampFromV(vn, height) {{
    // Base amplitude + exponential feel
    const base = 10;
    const maxA = Math.max(18, height * 0.22);
    const eased = Math.pow(vn, 0.65);
    return base + eased * (maxA - base);
  }}

  // Soft glow pass
  function drawGlowPath(pathFn) {{
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.strokeStyle = "{GLOW_COLOR}";
    ctx.lineWidth = 10;
    ctx.shadowBlur = 18;
    ctx.shadowColor = "{LINE_COLOR}";
    pathFn();
    ctx.stroke();
    ctx.restore();
  }}

  function drawMainPath(pathFn) {{
    ctx.save();
    ctx.strokeStyle = "{LINE_COLOR}";
    ctx.lineWidth = 2.2;
    ctx.shadowBlur = 0;
    pathFn();
    ctx.stroke();
    ctx.restore();
  }}

  // Animation timeline:
  // We iterate through daily volumes but animate continuously.
  let t0 = performance.now();
  let idx = 0;

  function frame(now) {{
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;
    ctx.clearRect(0, 0, w, h);

    // advance idx at fixed rate
    const elapsed = (now - t0) / 1000;
    const stepEvery = 0.20; // seconds per sample (speed of time)
    const newIdx = Math.floor(elapsed / stepEvery) % series.length;
    idx = newIdx;

    const s = series[idx];
    const vn = s.v_norm;
    const amp = ampFromV(vn, h);

    hudDate.textContent = s.date;
    hudVol.textContent  = (s.volume || 0).toLocaleString("en-US");
    hudAmp.textContent  = amp.toFixed(1) + "px";

    // draw baseline grid (subtle)
    ctx.save();
    ctx.globalAlpha = 0.16;
    ctx.strokeStyle = "rgba(255,255,255,0.10)";
    ctx.lineWidth = 1;
    const gridY = 6;
    for (let i = 1; i < gridY; i++) {{
      const yy = (h * i / gridY);
      ctx.beginPath();
      ctx.moveTo(0, yy);
      ctx.lineTo(w, yy);
      ctx.stroke();
    }}
    ctx.restore();

    // Skyline ECG path
    const time = now / 1000;

    const pathFn = () => {{
      ctx.beginPath();
      for (let i = 0; i < pts.length; i++) {{
        const p = pts[i];

        // base position
        const x = p.x * w;
        // put skyline in upper half, with margin
        const baseY = (0.18*h) + p.y * (0.42*h);

        // deformation: noise + spike, controlled by amp
        const n = pseudoNoise(i, time);
        const sp = spike(i, time) * 2.4;
        const dy = (n + sp) * amp;

        const y = baseY - dy;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }}
    }};

    drawGlowPath(pathFn);
    drawMainPath(pathFn);

    // footer pulse / scanline
    ctx.save();
    ctx.globalAlpha = 0.22;
    ctx.fillStyle = "rgba(154,251,255,0.10)";
    const scan = (time * 120) % w;
    ctx.fillRect(scan, 0, 2, h);
    ctx.restore();

    requestAnimationFrame(frame);
  }}

  requestAnimationFrame(frame);
}})();
</script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")


# -----------------------------
# Main pipeline
# -----------------------------
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img_path = Path(IMAGE_PATH)
    if not img_path.exists():
        raise FileNotFoundError(f"Image introuvable: {img_path.resolve()}")

    # 1) Load
    img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError("Impossible de lire l'image (format non supporté ?)")

    h, w = img.shape[:2]

    # 2) Keep top half (ignore reflection)
    top = img[: h // 2, :, :]

    # 3) Sky mask using HSV thresholds
    hsv = cv2.cvtColor(top, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    sky_mask = (s < HSV_S_MAX) & (v > HSV_V_MIN)  # True where sky

    # 4) For each column, find first non-sky pixel from top
    points = []
    th = top.shape[0]
    for x in range(w):
        col = sky_mask[:, x]
        ys = np.where(~col)[0]  # non-sky
        y = int(ys[0]) if len(ys) else 0
        points.append((x, y))

    # 5) Smooth
    ys = np.array([p[1] for p in points], dtype=np.float32)
    ys_sm = moving_average(ys, SMOOTH_WINDOW)

    points_sm = [(int(points[i][0]), float(ys_sm[i])) for i in range(len(points))]

    # 6) Simplify a bit (optional)
    points_simpl = rdp_simplify(points_sm, epsilon=1.2)

    # 7) Export JSON
    skyline_json = OUT_DIR / "skyline.json"
    skyline_json.write_text(json.dumps(points_simpl), encoding="utf-8")

    # 8) Export SVG
    svg_path = OUT_DIR / "skyline.svg"
    # SVG path
    d = []
    for i, (x, y) in enumerate(points_simpl):
        cmd = "M" if i == 0 else "L"
        d.append(f"{cmd}{x:.2f},{y:.2f}")
    path_d = " ".join(d)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h//2}">
  <path d="{path_d}" fill="none" stroke="black" stroke-width="2"/>
</svg>
"""
    svg_path.write_text(svg, encoding="utf-8")

    # 9) Download volumes
    series = None
    try:
        csv_text = download_stooq_csv(STOOQ_CSV_URL)
        series = parse_stooq_volume_series(csv_text, max_points=520)
    except Exception as e:
        # Fallback: synthetic series
        print("⚠️  Download volumes failed, using synthetic series. Reason:", e)
        series = []
        for i in range(520):
            vn = (math.sin(i * 0.07) * 0.5 + 0.5)
            series.append({"date": f"synthetic-{i}", "volume": int(1e7 + vn*2e7), "v_norm": float(vn)})

    (OUT_DIR / "volume_series.json").write_text(json.dumps(series), encoding="utf-8")

    # 10) Generate HTML
    generate_html(OUT_DIR / "index.html")

    # 11) Small report
    print("✅ Done.")
    print("   -", skyline_json)
    print("   -", svg_path)
    print("   -", OUT_DIR / "volume_series.json")
    print("   -", OUT_DIR / "index.html")
    print("\nNext:")
    print("  cd out")
    print("  python -m http.server 8000")
    print("  open http://localhost:8000/index.html")


if __name__ == "__main__":
    main()

