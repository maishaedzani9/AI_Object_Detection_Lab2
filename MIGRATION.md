# Migration from the current repository

Perform this cleanup on a branch after copying the upgraded files into the repository.

## 1. Create the branch

```bash
git switch main
git pull --ff-only
git switch -c improve/production-structure
```

## 2. Preserve the small demonstration image

```bash
mkdir -p data
git mv "Asian market.jpg" data/original-sample.jpg
```

If you want `original-sample.jpg` tracked, add this exception directly below `!data/sample.jpg` in `.gitignore`:

```gitignore
!data/original-sample.jpg
```

Otherwise remove it and use the downloadable `data/sample.jpg` demo asset.

## 3. Remove generated and large files from the current Git snapshot

The following commands remove the known raw videos and generated screenshots from the latest repository version. They do not rewrite historical commits.

```bash
git rm --ignore-unmatch "Cars Moving On Road Footage.avi" webcam.avi
git rm --ignore-unmatch image_test.png.png video_test.png.png webcam_test.png.png
git rm --ignore-unmatch lab_1.py
```

Copy the result screenshots you genuinely want to display to `docs/results/`, rename them clearly, and add them again. Do not commit raw video output.

## 4. Add the upgraded files and verify

```bash
python scripts/download_assets.py
python verify_setup.py
python -m pytest
python -m src.cli demo
git status
```

## 5. Commit and open a pull request

```bash
git add .
git commit -m "Refactor object detection lab into tested CLI project"
git push -u origin improve/production-structure
```

Open a pull request into `main`. Confirm the Build workflow passes before merging.

## Optional history cleanup

Deleting a tracked video from the latest snapshot does not remove it from earlier Git history. History rewriting is disruptive for collaborators and is not necessary for this portfolio cleanup. If repository size remains a serious problem, use `git filter-repo` only after making a backup and coordinating with every collaborator.
