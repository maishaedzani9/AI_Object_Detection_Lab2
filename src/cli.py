"""Command-line interface for detection, tracking, and demo inference."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.detector import ObjectDetector


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yolo-lab",
        description="Run YOLOv8 object detection or ByteTrack object tracking.",
    )
    parser.add_argument("mode", choices=("predict", "track", "demo"))
    parser.add_argument("--source", help="Image/video path or webcam index, such as 0.")
    parser.add_argument("--model", default="yolov8n.pt", help="Model name or local weights path.")
    parser.add_argument("--confidence", type=float, default=0.35, help="Confidence threshold in (0, 1].")
    parser.add_argument("--image-size", type=int, default=640, help="Square inference size in pixels.")
    parser.add_argument("--device", default=None, help="Inference device, for example cpu, 0, or 0,1.")
    parser.add_argument("--output", type=Path, default=Path("runs") / "inference")
    parser.add_argument("--tracker", default="bytetrack.yaml", help="Ultralytics tracker configuration.")
    parser.add_argument("--show", action="store_true", help="Display results in a GUI window.")
    parser.add_argument("--save-txt", action="store_true", help="Save normalized YOLO label text files.")
    parser.add_argument("--save-conf", action="store_true", help="Include confidence values in label files.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.mode == "demo":
        source = args.source or str(Path("data") / "sample.jpg")
        inference_mode = "predict"
    else:
        if args.source is None:
            print("error: --source is required for predict and track modes", file=sys.stderr)
            return 2
        source = args.source
        inference_mode = args.mode

    try:
        detector = ObjectDetector(model_path=args.model, device=args.device)
        summary = detector.run(
            mode=inference_mode,
            source=source,
            confidence=args.confidence,
            image_size=args.image_size,
            output_directory=args.output,
            show=args.show,
            save_txt=args.save_txt,
            save_conf=args.save_conf,
            tracker=args.tracker,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"mode={summary.mode}")
    print(f"source={summary.source}")
    print(f"processed_items={summary.processed_items}")
    print(f"elapsed_seconds={summary.elapsed_seconds:.3f}")
    print(f"average_fps={summary.average_fps:.2f}")
    print(f"output_directory={summary.output_directory.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
