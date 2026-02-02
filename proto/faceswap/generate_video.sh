source .venv/bin/activate
python3 main.py \
  --source input/1.jpg \
  --video input/1.mp4 \
  --swapper models/inswapper_128.onnx \
  --out output/1.mp4 \
  --max-width 1280

