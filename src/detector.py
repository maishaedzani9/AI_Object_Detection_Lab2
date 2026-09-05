"""Core detection and tracking services."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

import cv2
from ultralytics import YOLO


@dataclass(frozen=True)
class InferenceSummary:
    mode: str
    source: str
    output_directory: Path
    processed_items: int
    elapsed_seconds: float

    @property
    def average_fps(self) -> float:
        return self.processed_items / self.elapsed_seconds if self.elapsed_seconds else 0.0


class ObjectDetector:
    """Validated wrapper around Ultralytics YOLO prediction and tracking."""

    def __init__(self, model_path: str = "yolov8n.pt", device: str | None = None) -> None:
        self.model_path = model_path
        self.device = device
        try:
            self.model = YOLO(model_path)
        except Exception as exc:
            raise RuntimeError(f"Could not load model '{model_path}': {exc}") from exc

    @staticmethod
    def validate_source(source: str) -> str | int:
        if source.strip().isdigit():
            return int(source)
        path = Path(source).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Input source does not exist or is not a file: {path}")
        return str(path)

    def run(
        self,
        *,
        mode: str,
        source: str,
        confidence: float,
        image_size: int,
        output_directory: Path,
        show: bool = False,
        save_txt: bool = False,
        save_conf: bool = False,
        tracker: str = "bytetrack.yaml",
    ) -> InferenceSummary:
        if not 0.0 < confidence <= 1.0:
            raise ValueError("confidence must be greater than 0 and at most 1")
        if image_size <= 0:
            raise ValueError("image_size must be a positive integer")
        if mode not in {"predict", "track"}:
            raise ValueError("mode must be 'predict' or 'track'")

        validated_source = self.validate_source(source)
        output_directory.mkdir(parents=True, exist_ok=True)
        arguments: dict[str, Any] = {
            "source": validated_source,
            "conf": confidence,
            "imgsz": image_size,
            "device": self.device,
            "project": str(output_directory.parent),
            "name": output_directory.name,
            "exist_ok": True,
            "save": True,
            "show": show,
            "save_txt": save_txt,
            "save_conf": save_conf,
            "verbose": False,
        }
        if arguments["device"] is None:
            arguments.pop("device")

        started = perf_counter()
        try:
            if mode == "track":
                results = self.model.track(tracker=tracker, persist=True, **arguments)
            else:
                results = self.model.predict(**arguments)
        except Exception as exc:
            raise RuntimeError(f"{mode.capitalize()} inference failed: {exc}") from exc

        elapsed = perf_counter() - started
        processed_items = len(results)
        return InferenceSummary(
            mode=mode,
            source=str(validated_source),
            output_directory=output_directory,
            processed_items=processed_items,
            elapsed_seconds=elapsed,
        )


def image_is_readable(path: Path) -> bool:
    """Return True when OpenCV can decode the image."""
    return path.is_file() and cv2.imread(str(path)) is not None
