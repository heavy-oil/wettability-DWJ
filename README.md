# wettability-DWJ

This repository vendors upstream CycleGAN source code from Jun-Yan Zhu (`junyanz`) for unpaired image translation. The linked official repository, https://github.com/junyanz/CycleGAN, is the original Lua/Torch implementation. The PyTorch port the same authors maintain is vendored beside it. Both trees are unmodified snapshots of the commits below. Each keeps its upstream `LICENSE` (copyright Jun-Yan Zhu and Taesung Park) and `README.md`.

- Original Torch CycleGAN: https://github.com/junyanz/CycleGAN at `40b4498526de6b566f94a000d98fe18b9b8921db` (`CycleGAN/`)
- Maintained PyTorch CycleGAN and pix2pix: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix at `2a7afba2895d52556dd5dfe07e8555ef657ced6f` (`pytorch-CycleGAN-and-pix2pix/`)

For new runs, use the PyTorch tree. How the unpaired `trainA` / `trainB` layout maps onto μ-CT versus SEM or cryo-EM slices, including the pore-geometry warning, is in [docs/cyclegan-digital-rock.md](docs/cyclegan-digital-rock.md). A one-channel training entry point is `examples/cyclegan_ct_sem.sh`. Confirm the snapshots with `python scripts/verify_cyclegan_upstream.py`.

Tang Kunning 2025 WRR cascading super-resolution code was intended for the folder `tang-cascading-sr/`, but Zenodo record https://doi.org/10.5281/zenodo.15254020 (10.5281/zenodo.15254020) has restricted file access (403), so that folder was not added yet.

Ledig et al. did not publish an official Twitter or author GitHub for SRGAN. https://github.com/tensorlayer/srgan (`srgan/`) is a popular community reimplementation of the CVPR 2017 paper.

- ESRGAN (Wang et al., ECCV 2018 workshops) is vendored from https://github.com/xinntao/ESRGAN (`esrgan/`).
- Torch EDSR+MDSR (Lim et al., NTIRE 2017) is vendored from https://github.com/limbee/NTIRE2017 (`edsr/`).
- The official PyTorch port, by the same authors and formerly published as thstkdgus35/EDSR-PyTorch, is vendored from https://github.com/sanghyun-son/EDSR-PyTorch (`edsr-pytorch/`).

Ma et al. (TiPM 2025) apply EDSR in a multiphase setting. That paper's code is not included here.
