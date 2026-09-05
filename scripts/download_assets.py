"""Download a small public demo image and prepare the default YOLO model."""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path


SAMPLE_URL = "https://ultralytics.com/images/bus.jpg"


def download(url: str, destination: Path, overwrite: bool = False) -> None:
    if destination.exists() and not overwrite:
        print(f"Keeping existing file: {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "AI-Object-Detection-Lab/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output)
        temporary.replace(destination)
    except (OSError, urllib.error.URLError) as exc:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"Could not download {url}: {exc}") from exc
    print(f"Downloaded: {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-url", default=SAMPLE_URL)
    parser.add_argument("--model", default="yolov8n.pt")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    try:
        download(args.sample_url, Path("data") / "sample.jpg", args.overwrite)
        from ultralytics import YOLO

        YOLO(args.model)
    except (ImportError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Model is ready: {args.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
