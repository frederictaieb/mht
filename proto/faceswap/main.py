import os
import json

from lib.logging_utils import setup_logger
from lib.cli import build_parser
from lib.insight import init_models, available_ort_providers
from lib.pipeline import process_one
from lib.utils import ensure_dir


def load_batch_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "files" not in data or not isinstance(data["files"], list):
        raise ValueError("JSON invalide: attendu {'files':[...]}")

    for i, item in enumerate(data["files"]):
        for k in ("in_vid", "in_img", "out_vid"):
            if k not in item or not item[k]:
                raise ValueError(f"Entrée files[{i}] invalide: clé '{k}' manquante/vide.")
    return data["files"]


def main():
    logger, log_path = setup_logger()
    logger.info(f"Logs -> {log_path}")

    ap = build_parser()
    args = ap.parse_args()

    if not os.path.isfile(args.swapper):
        raise FileNotFoundError(f"Modèle swapper introuvable: {args.swapper}")

    det_w, det_h = map(int, args.det_size.split(","))
    app, swapper, providers, use_gpu = init_models(
        swapper_path=args.swapper,
        det_size=(det_w, det_h),
        device=args.device,
        logger=logger,
    )

    logger.info(f"Providers ORT dispo: {available_ort_providers(logger)}")
    logger.info(f"Providers utilisés: {providers} | use_gpu={use_gpu}")

    single_mode = bool(args.source and args.video)

    if single_mode:
        out_path = args.out or "out.mp4"
        logger.info(f"[single] video={args.video} source={args.source} -> {out_path}")
        process_one(
            app=app,
            swapper=swapper,
            source_img_path=args.source,
            video_in_path=args.video,
            out_path=out_path,
            max_width=args.max_width,
            every=args.every,
            keep_audio=args.keep_audio,
            logger=logger,
        )
        return

    # batch
    logger.info(f"[batch] json={args.json} input={args.input_dir} output={args.output_dir}")
    jobs = load_batch_json(args.json)
    ensure_dir(args.output_dir)

    for i, item in enumerate(jobs, start=1):
        in_vid = os.path.join(args.input_dir, item["in_vid"])
        in_img = os.path.join(args.input_dir, item["in_img"])
        out_vid = os.path.join(args.output_dir, item["out_vid"])

        logger.info(f"[{i}/{len(jobs)}] START | in_vid={in_vid} in_img={in_img} out={out_vid}")
        try:
            process_one(
                app=app,
                swapper=swapper,
                source_img_path=in_img,
                video_in_path=in_vid,
                out_path=out_vid,
                max_width=args.max_width,
                every=args.every,
                keep_audio=args.keep_audio,
                logger=logger,
            )
            logger.info(f"[{i}/{len(jobs)}] OK | out={out_vid}")
        except Exception as e:
            logger.exception(f"[{i}/{len(jobs)}] FAIL | {e}")


if __name__ == "__main__":
    main()
