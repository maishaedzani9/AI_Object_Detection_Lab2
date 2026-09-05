from pathlib import Path

import cv2
import numpy as np
import pytest

from src.detector import ObjectDetector, image_is_readable


def test_validate_existing_image(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.jpg"
    cv2.imwrite(str(image_path), np.zeros((16, 16, 3), dtype=np.uint8))
    assert ObjectDetector.validate_source(str(image_path)) == str(image_path)
    assert image_is_readable(image_path)


def test_validate_webcam_index() -> None:
    assert ObjectDetector.validate_source("0") == 0


def test_validate_missing_source() -> None:
    with pytest.raises(FileNotFoundError):
        ObjectDetector.validate_source("missing-image.jpg")
