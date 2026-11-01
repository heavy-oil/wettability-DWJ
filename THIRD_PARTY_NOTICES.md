# Third-party notices

Snapshots below were copied from public Git commits with their license files kept.
`.git` directories, `__pycache__`, and `*.pyc` files were removed. Weights are not included.
Commercial use is restricted for the NVIDIA and S-Lab components; read those licenses before use.

| Path | Upstream | Commit | License |
| --- | --- | --- | --- |
| `pytorch-CycleGAN-and-pix2pix/` | https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix | already on `main` | BSD-style notices in `LICENSE` (Zhu & Park; Isola & Zhu for pix2pix) |
| `CycleGAN/` | https://github.com/junyanz/CycleGAN | already on `main` | BSD-style notice in `LICENSE` |
| `stylegan2-ada-pytorch/` | https://github.com/NVlabs/stylegan2-ada-pytorch | `d72cc7d041b42ec8e806021a205ed9349f87c6a4` | NVIDIA Source Code License for StyleGAN2-ADA (`LICENSE.txt`). Non-commercial research or evaluation only. NVIDIA may use the work commercially. |
| `multiscale-drpnet/` | https://github.com/theanswer003/MultiscaleDRPNet | `6e88d5053ec361722a9ea03bced342d3c76e572e` | MIT, Copyright (c) 2022 Mingliang Liu (`LICENSE`). The nested `stylegan2-ada/` tree keeps NVIDIA's `LICENSE.txt` and stays under the NVIDIA non-commercial terms. PyCharm `.idea/` directories from that snapshot were omitted. |
| `p3t-net/` | https://github.com/KunningTang1/P3T-Net-for-3D-large-image-transfer | `346193d8ca96cb1ab8814c948fb3f27981c0ecae` | MIT, Copyright (c) 2024 KunningTang1 |
| `sr3/` | https://github.com/Janspiry/Image-Super-Resolution-via-Iterative-Refinement | `01d27a7cbfa8502be1d8dbd4ee02fcbd5e44389d` | Apache-2.0. This is an unofficial PyTorch reimplementation of Saharia et al., not a Google release. `dataset/` face crops are omitted; see `sr3/dataset/NOT_VENDORED.txt`. |
| `stablesr/` | https://github.com/IceClear/StableSR | `398ee9383777e255540ea027a704c8ce1f32145b` | S-Lab License 1.0 (`LICENSE.txt`). Non-commercial redistribution. Commercial use needs permission from the contributors. |
| `resshift/` | https://github.com/zsyOAOA/ResShift branch `journal` | `bb03b7d21614cace01787e097c8a6ab6b945227d` | S-Lab License 1.0 (`LICENSE`). Same non-commercial terms. `assets/` and `testdata/` images are omitted; see the `NOT_VENDORED.txt` files. `predict.py` (Cog/Replicate) has an upstream syntax error at the `bicsr` dict entry; use `inference_resshift.py` and `main.py`. |

Papers to cite when you use the corresponding code:

- Zhu et al., Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks, ICCV 2017. https://arxiv.org/abs/1703.10593
- Karras et al., Training Generative Adversarial Networks with Limited Data, NeurIPS 2020. https://arxiv.org/abs/2006.06676
- Liu and Mukerji, Multiscale Fusion of Digital Rock Images Based on Deep Generative Adversarial Networks, Geophysical Research Letters, 2022. https://doi.org/10.1029/2022GL098342
- Tang et al., Scaling deep learning for material imaging with a pseudo 3D model for domain transfer, Nature Communications 16, 11293 (2025). https://doi.org/10.1038/s41467-025-66449-6
- Saharia et al., Image Super-Resolution via Iterative Refinement, 2021. https://arxiv.org/abs/2104.07636
- Wang et al., Exploiting Diffusion Prior for Real-World Image Super-Resolution, IJCV 2024. https://arxiv.org/abs/2305.07015
- Yue, Wang, and Loy, ResShift, NeurIPS 2023 / TPAMI. https://arxiv.org/abs/2307.12348

## Nested code inside StableSR and ResShift

The upstream READMEs state that those trees build on other projects. In-file notices that came with the snapshot are unchanged.

- StableSR: Stable Diffusion (https://github.com/Stability-AI/stablediffusion), Latent Diffusion (https://github.com/CompVis/latent-diffusion), SPADE (https://github.com/NVlabs/SPADE; `stablesr/ldm/modules/spade.py` carries a CC BY-NC-SA 4.0 header), BasicSR (https://github.com/XPixelGroup/BasicSR).
- ResShift: Improved Diffusion (https://github.com/openai/improved-diffusion), Latent Diffusion, BasicSR, and Real-ESRGAN for synthesizing training pairs.

BasicSR is Apache-2.0 upstream. Stable Diffusion weights and code are under the CreativeML Open RAIL-M license when taken from Stability-AI. This repository does not ship those weights.

## Bundles that were not copied

P3T-Net Zenodo records https://doi.org/10.5281/zenodo.15031051 and https://doi.org/10.5281/zenodo.13766393 contain multi-gigabyte Linux/Windows environment zip files and a Docker image (about 17 GB). They were not vendored. Example volumes and author checkpoints are linked from the P3T-Net README (including https://zenodo.org/records/12633623 and https://zenodo.org/records/12631632).

Liu and Mukerji training images and their StyleGAN pickle are at https://doi.org/10.5281/zenodo.6420099.

Pretrained SR weights stay on the upstream hosts named in `docs/README.md`.
