# Official CycleGAN for unpaired μ-CT, SEM, and cryo-EM

[https://github.com/junyanz/CycleGAN](https://github.com/junyanz/CycleGAN) is the original Lua/Torch implementation of CycleGAN (Zhu, Park, Isola, and Efros, ICCV 2017). That is the repository linked as the official CycleGAN code. The authors' maintained implementation is the PyTorch port [https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix), which also contains pix2pix. Both trees are in this repository, unmodified, with their upstream `LICENSE` and `README.md`.

| Tree | Upstream | Commit | Date | Role |
| --- | --- | --- | --- | --- |
| `CycleGAN/` | [junyanz/CycleGAN](https://github.com/junyanz/CycleGAN) | `40b4498526de6b566f94a000d98fe18b9b8921db` | 2023-09-12 | Original Torch7 code. Use it to match the paper-era software. |
| `pytorch-CycleGAN-and-pix2pix/` | [junyanz/pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) | `2a7afba2895d52556dd5dfe07e8555ef657ced6f` | 2025-08-06 | Maintained PyTorch code (Python 3.11, PyTorch 2.4). Use this for new runs. |

Every file matches the Git blob SHA of those commits. The list is `docs/cyclegan-upstream-manifest.txt`. Check it with:

```bash
python scripts/verify_cyclegan_upstream.py
```

Copyright is Jun-Yan Zhu and Taesung Park, in `CycleGAN/LICENSE` and `pytorch-CycleGAN-and-pix2pix/LICENSE`. Redistribution must keep that notice. Cite the paper if you use the code:

> Jun-Yan Zhu, Taesung Park, Phillip Isola, and Alexei A. Efros. Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks. ICCV 2017. [https://arxiv.org/abs/1703.10593](https://arxiv.org/abs/1703.10593)

Upstream training notes stay in each tree (`CycleGAN/README.md`, `pytorch-CycleGAN-and-pix2pix/README.md`, `pytorch-CycleGAN-and-pix2pix/docs/tips.md`). Pretrained horse2zebra-style weights are downloaded by the upstream scripts. They are not part of this snapshot.

## Where it fits a digital-rock workflow

μ-CT, SEM, and cryo-EM of one rock are often acquired at different locations, fields of view, and pixel sizes. A μ-CT volume is a large field of X-ray attenuation. An SEM or cryo-EM image is a small field of electron contrast. Corresponding pixels are usually missing, so a paired translator such as pix2pix does not apply.

CycleGAN trains two generators, G: A→B and F: B→A, on two unpaired folders. Adversarial losses match each translated image to the target collection. Cycle consistency penalizes ||F(G(A)) − A|| and ||G(F(B)) − B||. That is the right training setup when domain A is a stack of μ-CT slices or patches and domain B is a separate stack of SEM or cryo-EM patches.

Use it as a 2-D appearance model:

- Slice a μ-CT volume yourself. These loaders read ordinary images, not volumes, and they do not read voxel spacing.
- Put μ-CT patches in domain A and SEM or cryo-EM patches in domain B.
- Both domains are resized and cropped to one `crop_size` (PyTorch default 256, Torch example 128). The official code is not a super-resolution model and it is not a 3-D reconstruction. A 64-pixel μ-CT patch and a 1024-pixel SEM patch become the same crop. Resample both to a common physical window before training if pore size has to stay meaningful.

Cycle consistency is a round trip of appearance. It does not preserve pore throats, the Euler number, fluid–solid contact area, or interfacial curvature. A generator can invent a throat that is not in the measurement, and that change moves permeability and wettability. Keep the measured μ-CT geometry when those quantities matter, and check porosity, two-point correlation, or specific surface on any translated image before interpreting it. A texture match between X-ray attenuation and electron contrast is not a calibrated density.

## Dataset layout

```text
datasets/ct_sem/
  trainA/    # μ-CT patches (png or jpg)
  trainB/    # SEM or cryo-EM patches
  testA/
  testB/
```

The PyTorch unaligned loader (`pytorch-CycleGAN-and-pix2pix/data/unaligned_dataset.py`) reads `{phase}A` and `{phase}B` and draws B at random, so the two folders do not need the same length or matching filenames. The Torch loader does the same: `phase` plus `A` or `B` under `DATA_ROOT` (`CycleGAN/data/data_util.lua`).

Grayscale rock images should be trained with one channel. The PyTorch loader opens each file as RGB and then applies `Grayscale(1)` when `--input_nc 1` and `--output_nc 1` are set.

Horizontal flips are on by default. Pass `--no_flip` (PyTorch) or `flip=0` (Torch) when bedding or fabric orientation matters.

## PyTorch training and test

Environment: `pytorch-CycleGAN-and-pix2pix/environment.yml` (Python 3.11, PyTorch 2.4, torchvision 0.19). Install from that file, then run from the PyTorch tree so its imports resolve. Weights and the `datasets/` folder stay outside git.

```bash
bash examples/cyclegan_ct_sem.sh
```

That script calls:

```bash
cd pytorch-CycleGAN-and-pix2pix
python train.py \
  --dataroot ../datasets/ct_sem \
  --name ct_sem_cyclegan \
  --model cycle_gan \
  --dataset_mode unaligned \
  --input_nc 1 \
  --output_nc 1 \
  --no_flip \
  --no_dropout
```

`G_A` maps A→B (μ-CT → SEM or cryo-EM). `G_B` maps B→A. Checkpoints land in `pytorch-CycleGAN-and-pix2pix/checkpoints/ct_sem_cyclegan/` as `latest_net_G_A.pth` and `latest_net_G_B.pth`.

One-direction test on μ-CT slices only, loading `G_A`:

```bash
cd pytorch-CycleGAN-and-pix2pix
python test.py \
  --dataroot ../datasets/ct_sem/testA \
  --name ct_sem_cyclegan \
  --model test \
  --model_suffix _A \
  --input_nc 1 \
  --output_nc 1 \
  --no_dropout \
  --no_flip
```

`--model test` switches the loader to a single folder. `--model_suffix _A` selects `net_G_A`. Use `_B` and point `--dataroot` at SEM or cryo-EM images to run the opposite generator. Results go to `./results/`. To run both directions in one call, pass `--model cycle_gan` and a dataroot that contains `testA` and `testB`.

The original Torch entry point, for a Torch7 install with `nngraph` and `class`, is `CycleGAN/train.lua`:

```bash
cd CycleGAN
DATA_ROOT=../datasets/ct_sem name=ct_sem_cyclegan model=cycle_gan \
  align_data=0 which_direction=AtoB input_nc=1 output_nc=1 flip=0 \
  th train.lua
```

The upstream README says the PyTorch port produces comparable or better results and is the version under active development. Prefer `pytorch-CycleGAN-and-pix2pix/` unless you are reproducing a Torch-only experiment.
