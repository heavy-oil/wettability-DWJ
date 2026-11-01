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
