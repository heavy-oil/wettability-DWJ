# wettability-DWJ

This repository vendors upstream CycleGAN source code for reference.

- PyTorch CycleGAN and pix2pix: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix (`pytorch-CycleGAN-and-pix2pix/`)
- Original Torch CycleGAN: https://github.com/junyanz/CycleGAN (`CycleGAN/`)

Tang Kunning 2025 WRR cascading super-resolution code was intended for the folder `tang-cascading-sr/`, but Zenodo record https://doi.org/10.5281/zenodo.15254020 (10.5281/zenodo.15254020) has restricted file access (403), so that folder was not added yet.

Ledig et al. did not publish an official Twitter or author GitHub for SRGAN. https://github.com/tensorlayer/srgan (`srgan/`) is a popular community reimplementation of the CVPR 2017 paper.

- ESRGAN (Wang et al., ECCV 2018 workshops) is vendored from https://github.com/xinntao/ESRGAN (`esrgan/`).
- Torch EDSR+MDSR (Lim et al., NTIRE 2017) is vendored from https://github.com/limbee/NTIRE2017 (`edsr/`).
- The official PyTorch port, by the same authors and formerly published as thstkdgus35/EDSR-PyTorch, is vendored from https://github.com/sanghyun-son/EDSR-PyTorch (`edsr-pytorch/`).

Ma et al. (TiPM 2025) apply EDSR in a multiphase setting. That paper's code is not included here.

## Generative paths (μ-CT, SEM, cryo-EM)

Unpaired or weakly registered fusion lives in these added trees. A bilingual map, install and weight notes, and the pore-throat hallucination warning (Euler number, contact area, curvature) are in [docs/README.md](docs/README.md). Licenses are indexed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

- CycleGAN is already in `pytorch-CycleGAN-and-pix2pix/` and `CycleGAN/`.
- StyleGAN2-ADA (NVIDIA non-commercial license): `stylegan2-ada-pytorch/`.
- Liu and Mukerji multiscale fusion scripts: `multiscale-drpnet/` (MIT for their files; nested StyleGAN stays under the NVIDIA license).
- P3T-Net (Tang et al., Nature Communications 2025): `p3t-net/` (MIT GitHub snapshot). The multi-GB Zenodo environment bundles are linked, not vendored.
- SR3 unofficial PyTorch reimplementation (Saharia et al.): `sr3/` (Apache-2.0).
- StableSR: `stablesr/` (S-Lab License 1.0, non-commercial).
- ResShift: `resshift/` (S-Lab License 1.0, non-commercial).

Syntax and license check, without weights or a GPU:

```bash
python scripts/smoke_generative_paths.py
```
