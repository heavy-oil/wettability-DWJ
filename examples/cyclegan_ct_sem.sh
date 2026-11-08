#!/usr/bin/env bash
# Unpaired μ-CT (domain A) ↔ SEM or cryo-EM (domain B) with the vendored
# junyanz PyTorch CycleGAN. See docs/cyclegan-digital-rock.md.
#
# Expected layout (not committed):
#   datasets/ct_sem/trainA  datasets/ct_sem/trainB
#   datasets/ct_sem/testA   datasets/ct_sem/testB
#
# Both domains are cropped to one pixel size. This is appearance translation,
# not super-resolution and not a 3D reconstruction. Resample patches to a
# common physical window before training if pore size must stay meaningful.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATAROOT="${DATAROOT:-${ROOT}/datasets/ct_sem}"
NAME="${NAME:-ct_sem_cyclegan}"

cd "${ROOT}/pytorch-CycleGAN-and-pix2pix"

python train.py \
  --dataroot "${DATAROOT}" \
  --name "${NAME}" \
  --model cycle_gan \
  --dataset_mode unaligned \
  --input_nc 1 \
  --output_nc 1 \
  --no_flip \
  --no_dropout \
  "$@"
