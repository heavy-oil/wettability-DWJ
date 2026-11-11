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

Liang, Wang, Feng et al. (SPE Journal 2024, SPE 218397, https://doi.org/10.2118/218397-PA) reconstruct shale FIB-SEM in two steps: DBPI on each xy slice, then a VDSR-style 3D CNN along z so that pores below about 10 nm enter the pore network. The mapping, citations, and license notes are in `docs/liang2024-fibsem-sr.md`.

- xy-plane DBPI (Kim, Jung, Kim, IEEE Signal Processing Letters 2020, https://doi.org/10.1109/LSP.2020.3005043) is the official tree https://github.com/prote376/DBPI-BlindSR at `5c7702c`, copied under `DBPI-BlindSR/`. That repository has no LICENSE file. `imresize.py` matches KernelGAN; the Weizmann / Yeda academic non-commercial license is in `DBPI-BlindSR/KERNELGAN_LICENSE.txt`.
- The authors' 10-layer z-direction 3D CNN was not released. `pytorch-vdsr/` is https://github.com/twtygqyy/pytorch-vdsr at `514b021` (MIT), a public 2D VDSR reimplementation of Kim, Lee, and Lee, CVPR 2016 (https://doi.org/10.1109/CVPR.2016.182). It is not Liang et al. code. The upstream checkpoint, HDF5 sample, and Set5 binaries are omitted; see `pytorch-vdsr/NOT_VENDORED.txt`.
- SRCNN (Dong et al., TPAMI 2016, https://doi.org/10.1109/TPAMI.2015.2439281) had no official git repository with a LICENSE. `srcnn/` is https://github.com/Lornatang/SRCNN-PyTorch at `a0a108e` (Apache-2.0). Weights stay on the Drive and Baidu links in that README.
- FSRCNN (Dong, Loy, and Tang, ECCV 2016, https://doi.org/10.1007/978-3-319-46475-6_25) is the same case. `fsrcnn/` is https://github.com/Lornatang/FSRCNN-PyTorch at `e6f8d53` (Apache-2.0), with weights linked out rather than committed.

CinCGAN, SRGAN, EDSR, and CycleGAN are only related work in that paper and are not copied again.
