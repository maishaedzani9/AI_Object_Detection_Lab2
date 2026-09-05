# YOLOv8 Object Detection and Tracking Lab

[![Python 3.10–3.11](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build](https://github.com/maishaedzani9/AI_Object_Detection_Lab2/actions/workflows/ci.yml/badge.svg)](https://github.com/maishaedzani9/AI_Object_Detection_Lab2/actions/workflows/ci.yml)

## Overview

This project demonstrates object detection in images and object tracking in video or webcam streams with a pretrained Ultralytics YOLOv8 model. It provides a reproducible command-line workflow, defensive input validation, optional CUDA acceleration, automated setup verification, and tests.

The repository is an educational inference project. It currently uses pretrained COCO weights and does **not** claim a custom-trained model, custom dataset accuracy, quantization, pruning, or independently measured mAP. Sections for measured results are intentionally marked as placeholders until experiments are run.

## Features

- Image detection with annotated output
- Video and webcam tracking with ByteTrack
- Configurable model, confidence threshold, image size, output path, and device
- Optional YOLO-format label and confidence export
- CPU operation with optional NVIDIA CUDA acceleration
- Automatic download of a small demo image and pretrained weights
- Dependency, image-decoding, CUDA, and inference verification
- Unit tests and GitHub Actions build checks
- Clear separation between tracked source code and ignored datasets, weights, and generated output

## Installation

### Prerequisites

- Python 3.10 or 3.11
- Git
- A webcam only if live tracking is required
- Optional: an NVIDIA GPU with a driver compatible with the selected PyTorch CUDA wheel

OpenCV wheels include the Python OpenCV binaries. Linux desktop environments may additionally need runtime libraries:

```bash
sudo apt-get update
sudo apt-get install -y libgl1 libglib2.0-0
```

No separate system OpenCV installation is normally required on Windows or macOS.

### Option A: `venv`

#### Windows PowerShell

```powershell
git clone https://github.com/maishaedzani9/AI_Object_Detection_Lab2.git
cd AI_Object_Detection_Lab2
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks local activation scripts for the current process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

#### Linux or macOS

```bash
git clone https://github.com/maishaedzani9/AI_Object_Detection_Lab2.git
cd AI_Object_Detection_Lab2
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Option B: Conda

The commands are the same on Windows, Linux, and macOS after Conda is installed:

```bash
git clone https://github.com/maishaedzani9/AI_Object_Detection_Lab2.git
cd AI_Object_Detection_Lab2
conda create --name yolo-lab python=3.11 -y
conda activate yolo-lab
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Optional NVIDIA CUDA installation

The default requirements are suitable for CPU use. For the official PyTorch 2.6.0 CUDA 12.6 wheels, run this after installing `requirements.txt`:

```bash
python -m pip install --force-reinstall torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu126
```

You generally need a compatible NVIDIA driver, not a separate CUDA Toolkit, because the PyTorch wheel supplies its CUDA runtime. Confirm GPU access with:

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

### Download demo assets

Linux or macOS:

```bash
sh download_assets.sh
```

Windows Command Prompt or PowerShell:

```bat
download_assets.bat
```

Cross-platform alternative:

```bash
python scripts/download_assets.py
```

The script downloads `data/sample.jpg` from the public Ultralytics assets and prepares `yolov8n.pt`. Large videos, datasets, and weights are deliberately excluded from Git. To use your own asset host, pass a direct file URL:

```bash
python scripts/download_assets.py --sample-url "https://your-domain.example/sample.jpg" --overwrite
```

Only download and use media for which you have permission.

## Usage

Run all commands from the repository root with the virtual environment activated.

### Basic image detection

```bash
python -m src.cli predict --source data/sample.jpg
```

### Video tracking

```bash
python -m src.cli track --source path/to/input-video.mp4 --output runs/video
```

### Webcam tracking

```bash
python -m src.cli track --source 0 --show --output runs/webcam
```

On systems with multiple webcams, replace `0` with `1`, `2`, or the appropriate device index.

### Demo mode

Demo mode uses `data/sample.jpg` when `--source` is omitted:

```bash
python -m src.cli demo
```

### Advanced usage

```bash
python -m src.cli track \
  --source path/to/input-video.mp4 \
  --model yolov8n.pt \
  --confidence 0.45 \
  --image-size 640 \
  --device 0 \
  --tracker bytetrack.yaml \
  --save-txt \
  --save-conf \
  --output runs/advanced
```

Windows PowerShell uses the backtick for line continuation:

```powershell
python -m src.cli track `
  --source path/to/input-video.mp4 `
  --model yolov8n.pt `
  --confidence 0.45 `
  --image-size 640 `
  --device 0 `
  --save-txt `
  --save-conf `
  --output runs/advanced
```

Use `--device cpu` to force CPU inference. Run `python -m src.cli --help` for the complete argument list.

### Expected output

Annotated images or videos are written beneath the selected output directory. If `--save-txt` is enabled, normalized YOLO labels are written under its `labels/` subdirectory. The terminal prints a machine-readable summary:

```text
mode=predict
source=data/sample.jpg
processed_items=1
elapsed_seconds=1.234
average_fps=0.81
output_directory=/absolute/path/to/runs/inference
```

`average_fps` is an end-to-end project measurement and includes file loading and result handling. It should not be compared directly with model-only benchmark numbers.

## Results

The following placeholders prevent unmeasured values from being presented as facts. Replace them only after running a documented experiment on fixed hardware and a named dataset.

### Sample detection result

<!-- Add docs/results/sample-detection.jpg, then remove this comment and placeholder. -->
> **Image placeholder:** Add an annotated image at `docs/results/sample-detection.jpg`, then insert `![YOLOv8 sample detection](docs/results/sample-detection.jpg)` here.

**Caption:** Sample YOLOv8 inference showing class labels, confidence scores, and bounding boxes around detected objects. State the model checkpoint and confidence threshold used.

### Tracking result

<!-- Add docs/results/tracking-result.gif, then remove this comment and placeholder. -->
> **Media placeholder:** Add a short, compressed GIF at `docs/results/tracking-result.gif`, then insert `![ByteTrack result](docs/results/tracking-result.gif)` here.

**Caption:** Multi-object tracking across consecutive frames. Stable track identifiers demonstrate temporal association by ByteTrack.

### Performance metrics

| Model | Device | Input size | Precision | Recall | mAP@0.50 | mAP@0.50:0.95 | End-to-end FPS |
|---|---|---:|---:|---:|---:|---:|---:|
| YOLOv8n | _Add hardware_ | 640 | _Not measured_ | _Not measured_ | _Not measured_ | _Not measured_ | _Not measured_ |

**Caption:** Report metrics only from a held-out validation or test set. Record the dataset version, sample count, batch size, software versions, and hardware so the result is reproducible.

### Confusion matrix and precision–recall curves

> **Plot placeholders:** After model validation, add `docs/results/confusion-matrix.png` and `docs/results/precision-recall-curve.png`. Embed them with descriptive alt text and identify the dataset split.

**Caption:** The confusion matrix shows class-level prediction errors. Precision–recall curves show the trade-off between false positives and missed detections across confidence thresholds. These plots are not meaningful for an undocumented collection of demo images.

## Technical Approach

### Model architecture

The current implementation uses **YOLOv8n**, the nano-sized member of the Ultralytics YOLO family. YOLO is a one-stage detector: one forward pass predicts object locations and class probabilities. Unlike two-stage detectors such as Faster R-CNN, it does not first generate region proposals. SSD is also a one-stage family, but this repository does not use SSD or Faster R-CNN.

YOLOv8 combines a convolutional feature-extraction backbone, multi-scale feature aggregation, and a decoupled detection head. Non-maximum suppression removes overlapping predictions. A prediction is retained when its confidence exceeds the selected threshold. Intersection over Union is

$$
\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}.
$$

Average precision summarizes the area under a class precision–recall curve, and mean average precision averages AP across classes:

$$
\operatorname{mAP}=\frac{1}{C}\sum_{c=1}^{C}\operatorname{AP}_c.
$$

### Preprocessing

Ultralytics handles inference preprocessing: image decoding, color conversion, aspect-ratio-preserving resize/letterboxing to the selected input size, tensor conversion, and pixel scaling. For an 8-bit channel value $x\in[0,255]$, scaling is represented as

$$
x' = \frac{x}{255}.
$$

Augmentation is not applied during normal inference. `albumentations` is included for future custom-training experiments, where transformations such as horizontal flips, color changes, blur, scale, and crop must be chosen carefully so bounding boxes remain valid.

### Tracking

Video and webcam modes use ByteTrack through Ultralytics. Each frame receives YOLO detections, after which the tracker associates detections with existing tracks across time. This produces stable identifiers and handles some low-confidence detections during association.

### Training strategy

The checked-in project performs **transfer-learning inference** using pretrained COCO weights; it does not currently fine-tune those weights. A defensible future training experiment should:

1. Version and split a labelled dataset into training, validation, and held-out test sets.
2. Initialize from pretrained YOLOv8 weights.
3. Record image size, batch size, epochs, optimizer, learning rate, weight decay, random seed, augmentations, and early-stopping policy.
4. Select checkpoints using validation performance and report final metrics once on the held-out test set.
5. Save TensorBoard logs outside Git and publish only summarized, reproducible results.

No hyperparameter values are claimed here because no custom training run is included in this repository.

### Optimization and export

The project currently uses standard PyTorch inference. Quantization and pruning have not been implemented or benchmarked. ONNX packages are included so an explicitly tested export path can be added later. Any future optimization should compare model size, latency, mAP, and hardware under the same test protocol. A smaller file or faster isolated forward pass must not be described as an overall improvement if accuracy or end-to-end latency worsens.

### Project-specific contribution

This repository's contribution is the engineering around a pretrained detector: a validated multi-source CLI, separate prediction and tracking modes, configurable thresholds and devices, structured output, automatic demo-asset setup, dependency and inference verification, tests, and reproducible documentation. It does not present YOLOv8 or ByteTrack as original algorithms.

## Project Structure

```text
AI_Object_Detection_Lab2/
├── .github/workflows/ci.yml       # tracked: automated build and tests
├── configs/default.yaml           # tracked: documented defaults
├── data/
│   ├── .gitkeep                   # tracked
│   └── sample.jpg                 # tracked after asset download if intentionally committed
├── docs/results/                  # tracked: small result images only
├── models/README.md               # tracked: architecture-extension guidance
├── scripts/download_assets.py     # tracked: cross-platform asset downloader
├── src/
│   ├── __init__.py                # tracked
│   ├── cli.py                     # tracked: command-line entry point
│   └── detector.py                # tracked: inference service
├── tests/test_detector.py         # tracked: unit tests
├── utils/README.md                # tracked: helper-extension guidance
├── .gitignore                     # tracked
├── download_assets.bat            # tracked: Windows wrapper
├── download_assets.sh             # tracked: Linux/macOS wrapper
├── LICENSE                        # tracked
├── MIGRATION.md                   # tracked: cleanup steps for the existing repository
├── pyproject.toml                 # tracked: project and pytest settings
├── README.md                      # tracked
├── requirements.txt              # tracked: pinned environment
└── verify_setup.py                # tracked: end-to-end setup check

Ignored and not committed:
├── datasets/                      # ignored: full datasets
├── checkpoints/                   # ignored: training checkpoints
├── logs/                          # ignored: TensorBoard/training logs
├── runs/                          # ignored: generated inference output
├── *.mp4, *.avi, *.mov            # ignored: raw videos
└── *.pt, *.pth, *.h5, *.onnx      # ignored: weights and exported models
```

## Verification

After installation and asset download, run:

```bash
python verify_setup.py
python -m pytest
python -m src.cli demo
```

The setup script exits with a non-zero status and a clear message if a dependency is unavailable, CUDA cannot be queried, the sample image cannot be decoded, the model cannot load, or inference fails. CUDA being unavailable is informational and does not fail verification because CPU inference is supported.

## Contributing

1. Fork the repository and create a focused branch: `git switch -c feature/short-description`.
2. Keep datasets, raw videos, generated runs, and model weights out of Git.
3. Add or update tests for behavioral changes.
4. Run `python -m pytest` and `python -m compileall src scripts verify_setup.py`.
5. Update the README when commands, outputs, dependencies, or results change.
6. Open a pull request explaining the problem, solution, verification performed, and any performance impact.

Please do not publish private footage, personally identifiable data, or third-party datasets without permission.

## License

This project is available under the [MIT License](LICENSE). Ultralytics and pretrained model usage remain subject to their own applicable licensing terms.
