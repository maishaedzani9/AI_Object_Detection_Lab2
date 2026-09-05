"""Verify dependencies, CUDA status, sample decoding, and YOLO inference."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


REQUIRED_MODULES = {
    "torch": "torch",
    "torchvision": "torchvision",
    "cv2": "opencv-python",
    "numpy": "numpy",
    "ultralytics": "ultralytics",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "tqdm": "tqdm",
    "PIL": "pillow",
    "albumentations": "albumentations",
    "tensorboard": "tensorboard",
    "onnx": "onnx",
    "onnxruntime": "onnxruntime",
}


def main() -> int:
    failures: list[str] = []
    loaded = {}
    for module_name, package_name in REQUIRED_MODULES.items():
        try:
            loaded[module_name] = importlib.import_module(module_name)
            print(f"[PASS] dependency: {package_name}")
        except Exception as exc:
            failures.append(f"{package_name}: {exc}")
            print(f"[FAIL] dependency: {package_name} ({exc})")

    if failures:
        print("\nInstall dependencies with: python -m pip install -r requirements.txt")
        return 1

    torch = loaded["torch"]
    print(f"[INFO] Python: {sys.version.split()[0]}")
    print(f"[INFO] PyTorch: {torch.__version__}")
    print(f"[INFO] CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"[INFO] CUDA device: {torch.cuda.get_device_name(0)}")

    sample = Path("data") / "sample.jpg"
    image = loaded["cv2"].imread(str(sample)) if sample.is_file() else None
    if image is None:
        print("[FAIL] sample image is missing or unreadable; run the asset download script")
        return 1
    print(f"[PASS] sample image: {sample} ({image.shape[1]}x{image.shape[0]})")

    try:
        model = loaded["ultralytics"].YOLO("yolov8n.pt")
        results = model.predict(source=str(sample), imgsz=640, conf=0.35, verbose=False)
        detections = len(results[0].boxes) if results else 0
    except Exception as exc:
        print(f"[FAIL] model inference: {exc}")
        return 1

    print(f"[PASS] model inference: {detections} detections")
    print("Setup verification completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
