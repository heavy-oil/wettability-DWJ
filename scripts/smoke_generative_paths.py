#!/usr/bin/env python3
"""License and syntax smoke check for vendored generative-model trees.

This does not download weights, allocate a GPU, or run training.
It confirms each upstream LICENSE file is present and that the
training/inference entry points parse under the current Python.
"""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LICENSE_MARKERS = {
    "stylegan2-ada-pytorch/LICENSE.txt": "NVIDIA Source Code License",
    "multiscale-drpnet/LICENSE": "MIT License",
    "multiscale-drpnet/stylegan2-ada/LICENSE.txt": "NVIDIA Source Code License",
    "p3t-net/LICENSE": "MIT License",
    "sr3/LICENSE": "Apache License",
    "stablesr/LICENSE.txt": "S-Lab License",
    "resshift/LICENSE": "S-Lab License",
    "pytorch-CycleGAN-and-pix2pix/LICENSE": "Jun-Yan Zhu",
    "CycleGAN/LICENSE": "Jun-Yan Zhu",
}

OMISSION_NOTES = (
    "sr3/dataset/NOT_VENDORED.txt",
    "resshift/assets/NOT_VENDORED.txt",
    "resshift/testdata/NOT_VENDORED.txt",
)

ENTRY_POINTS = (
    "stylegan2-ada-pytorch/train.py",
    "stylegan2-ada-pytorch/generate.py",
    "stylegan2-ada-pytorch/dataset_tool.py",
    "multiscale-drpnet/cyclegan/train.py",
    "multiscale-drpnet/cyclegan/test.py",
    "multiscale-drpnet/cyclegan/recons3d.py",
    "multiscale-drpnet/stylegan2-ada/train.py",
    "multiscale-drpnet/stylegan2-ada/gen_imgs.py",
    "p3t-net/TrainingDataPrepare.py",
    "p3t-net/Semantic_Indication_Modules.py",
    "p3t-net/Domain_Transfer_and_Semantic_Consistency_Module.py",
    "p3t-net/Misalignment_Fixing_Module.py",
    "p3t-net/Inference.py",
    "p3t-net/models.py",
    "sr3/sr.py",
    "sr3/infer.py",
    "sr3/sample.py",
    "stablesr/main.py",
    "stablesr/scripts/sr_val_ddpm_text_T_vqganfin_old.py",
    "resshift/inference_resshift.py",
    "resshift/main.py",
    "pytorch-CycleGAN-and-pix2pix/train.py",
    "pytorch-CycleGAN-and-pix2pix/test.py",
)


def main() -> int:
    failures: list[str] = []

    for rel, marker in LICENSE_MARKERS.items():
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"missing license: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if marker not in text:
            failures.append(f"license marker {marker!r} not in {rel}")
        if len(text) < 200:
            failures.append(f"license file looks truncated: {rel}")

    for rel in OMISSION_NOTES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing omission note: {rel}")

    for rel in ENTRY_POINTS:
        path = ROOT / rel
        if not path.is_file():
            failures.append(f"missing entry point: {rel}")
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"syntax error in {rel}: {exc.msg}")

    if failures:
        print("smoke failed:")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(f"smoke ok: {len(LICENSE_MARKERS)} license files, {len(ENTRY_POINTS)} entry points")
    print("weights, GPU, and training were not required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
