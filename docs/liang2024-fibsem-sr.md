# FIB-SEM stepwise super-resolution (Liang et al., SPE 218397)

Liang, Y., Wang, S., Feng, Q., Zhang, M., Cao, X., and Wang, X. 2024.
Ultrahigh-Resolution Reconstruction of Shale Digital Rocks from FIB-SEM
Images Using Deep Learning. *SPE Journal* 29 (3): 1434–1450.
Paper SPE 218397. https://doi.org/10.2118/218397-PA

The paper reconstructs shale from the Jiyang Depression (Shengli oil
field) so that pores smaller than about 10 nm can be segmented and
turned into a pore-network model. FIB-SEM volumes are anisotropic:
the two data sets are 6.5 × 6.5 × 10 nm³ (organic-matter stack: 567
slices of 1024 × 1120; inorganic-matter stack: 1000 slices of
1000 × 1000). SEM sets the xy sampling; FIB milling sets the coarser
z sampling. A single 3D network is a poor fit, because the xy/z
difference is an acquisition difference, not only a scale factor.
The published method is therefore two supervised-or-not steps, both
at a scale of about 2 in xy and about 10/3.25 along z, aiming at an
isotropic 3.25 nm voxel.

## What is vendored

| Step in the paper | Model | Tree in this repo | What it is |
| --- | --- | --- | --- |
| xy slices | DBPI (Kim, Jung, Kim, 2020) | `DBPI-BlindSR/` | Official public code |
| z, after xy | 10-layer residual 3D CNN adapted from VDSR | not vendored | Authors did not release it |
| cited basis of that z-network | VDSR (Kim, Lee, Lee, 2016) | `pytorch-vdsr/` | Public 2D reimplementation, MIT |
| cited earlier CNN SR | SRCNN (Dong et al.) | `srcnn/` | Public reimplementation, Apache-2.0 |
| cited with SRCNN for z-interpolation SR | FSRCNN (Dong, Loy, Tang, 2016) | `fsrcnn/` | Public reimplementation, Apache-2.0 |

`pytorch-vdsr/` is the 20-layer 2D VDSR network (input convolution,
18 residual blocks, output convolution, residual added to the
bicubic-upsampled luminance). It is not a 3D network and it is not
Liang et al. code. No from-scratch copy of their z-network is added
here.

CinCGAN, SRGAN, EDSR, and CycleGAN appear only in the paper's related
work. They are already covered by other trees (`srgan/`, `edsr/`,
`edsr-pytorch/`, `CycleGAN/`, `pytorch-CycleGAN-and-pix2pix/`) or by
open pull requests, and they are not part of this pipeline.

## Workflow

1. **Denoise.** Nonlocal-means filtering on every FIB-SEM slice.
   In the paper this beat a Gaussian filter and a median filter on
   NIQE (7.0 vs 8.56 vs 8.72) while keeping pore boundaries. The
   filtered stack is the low-resolution volume, size (X, X, Z).

2. **xy-plane, unsupervised, one slice at a time.** Run 2D DBPI at
   scale 2. Each grayscale SEM slice is the only training image.
   There is no paired high-resolution FIB-SEM target: milling destroys
   the face, so a second scan at 3.25 nm of the same surface does not
   exist. Synthetic downsampling is also a poor teacher, because real
   FIB-SEM blur is not additive noise on a bicubic downsample
   (the paper cites Dong et al. 2016a, Kim et al. 2016, and Kohler
   et al. 2020 for that point). DBPI learns the downscaling kernel and
   the upscaling map together by internal learning.

   The official network, matching Fig. 3 and Fig. 4 of the paper:

   - Downscaler: a strided convolution whose stride is the scale
     factor, then five convolutions and no nonlinearity. Kernels
     7×7×64, 5×5×64, 3×3×64, 1×1×64, 1×1×64, 1×1×1. The residual is
     added to an average-pool of the input.
   - Upscaler: bicubic upsampling plus eight convolutions, ReLU on all
     but the last. The first seven are 3×3×64; the last is 3×3×3.
     The residual is added to the bicubic image. FIB-SEM is one
     channel, so the three-channel output is converted to grayscale.
   - Loss is the dual back-projection L1 in their equation (1):
     the upscaler must invert the downscaler on the given patch, and
     the downscaler must invert the upscaler. Adam, 3000 iterations,
     learning rate 10⁻⁴ divided by 10 every 750 iterations, random
     64×64 crops. Same schedule as Kim et al. 2020.
   - Wall clock in the paper: about 1.5 minutes per slice, about 39
     hours for the 1567 organic-matter and inorganic-matter slices,
     on one NVIDIA RTX 3080. PyTorch 1.1.0. The vendored DBPI README
     pins PyTorch 1.3.0; that pin is the official code's environment,
     not a second training recipe.

   Output of this step: a volume at (X/2, X/2, Z), here
   3.25 × 3.25 × 10 nm³.

3. **z-direction, supervised, anisotropic.** DBPI is 2D. Extending it
   to 3D would keep the cycleGAN-style pair of networks (the paper's
   wording: the DBPI architecture is built upon cycleGAN). The authors
   rejected a 3D DBPI because adversarial training costs more memory
   and was less attractive than a plain CNN for the imaging quality
   they needed. The z-model is their own 10-layer 3D CNN, using the
   residual-learning idea of VDSR rather than VDSR's 20-layer 2D
   layout:

   - 10 convolutional layers, ReLU after each. The paper states the
     first nine as 3×3×64 and the last as 3×3×1. The residual image
     is added to the low-resolution input.
   - Optimizer SGDM, momentum 0.9. They compared Adam: Adam was about
     9 minutes faster per epoch, but SGDM reached NIQE 6.32 against
     Adam's 6.35. Loss is MSE (NIQE 6.32) rather than mean absolute
     error (NIQE 6.38). Learning rate starts at 0.1 and is multiplied
     by 0.1 every 10 epochs. Batch size 36. 15 epochs, about 1.5 hours
     each (22.5 hours).
   - Pairs are built from the xy-super-resolved volume so that the
     degradation looks like coarser FIB milling, not like bicubic
     downsampling of a CT volume. Crop 24×24×24 cubes as the
     high-resolution set {y}. Along z, keep one slice out of every
     three, then cubic-spline those slices back to the cube size.
     That interpolated cube is the low-resolution input {x}. The
     factor of three is the 10 nm to 3.25 nm ratio. Augment by crop,
     rotation, and translation.
   - At test time the xy-super-resolved volume is cut into
     non-overlapping 24³ tiles, passed through the network, and
     written back in order. They do not average overlaps.

   The resulting volume is 3.25 × 3.25 × 3.25 nm³.

   **The 3D z-network, its weights, and the training script were not
   released.** Nothing under `pytorch-vdsr/` should be cited as that
   code. `pytorch-vdsr/` is only the public 2D model whose residual
   formulation the paper says it adapted.

4. **Pore network.** Multilevel Otsu segmentation (three classes on
   organic-matter images, pore threshold 0.249; inorganic-matter pore
   threshold 0.39), then the maximal-ball pore network. On the
   super-resolved connected pores the paper reports radii from 0 nm
   to 40 nm, in line with nitrogen adsorption; pores with radius
   below 10 nm are about half of the connected pores; coordination
   numbers lie mainly between 1 and 4; the pore-throat ratio lies
   between 1 and 3. Isolated pores are fewer than on the original
   FIB-SEM network. That pore-network comparison is the reason for
   the super-resolution, not a visual demo.

## Sources and licenses

### DBPI, xy-plane

Official code, vendored unchanged apart from the two note files in
that directory:

- https://github.com/prote376/DBPI-BlindSR @ `5c7702cfd34018ea93576755afe1b0bbc67e7fd6`
- Kim, J., Jung, C., and Kim, C. 2020. Dual Back-Projection-Based
  Internal Learning for Blind Super-Resolution. *IEEE Signal
  Processing Letters* 27: 1190–1194.
  https://doi.org/10.1109/LSP.2020.3005043

The GitHub repository has no LICENSE file. `DBPI-BlindSR/VENDOR_NOTE.txt`
records that. `imresize.py` is byte-identical to KernelGAN, and the
training modules are adapted from https://github.com/sefibk/KernelGAN.
KernelGAN's Weizmann / Yeda academic non-commercial license is copied
as `DBPI-BlindSR/KERNELGAN_LICENSE.txt`. DBPI does not ship pretrained
weights; each image is trained on itself (`python train.py -i ... -o ...`
for ×2, add `--X4` for ×4).

### VDSR, the cited 2D residual network

Official author code is the MATLAB package linked from
http://cv.snu.ac.kr/research/VDSR/ . That download is not a git
repository and does not carry an SPDX license, so it is not vendored.

Vendored instead, the widely used PyTorch reimplementation:

- https://github.com/twtygqyy/pytorch-vdsr @ `514b021044018baf909e79f48392783daa592888`
- MIT, copyright Jiu Xu, Rakuten, Inc., and Rakuten Institute of
  Technology (`pytorch-vdsr/LICENSE`)
- Kim, J., Lee, J. K., and Lee, K. M. 2016. Accurate Image
  Super-Resolution Using Very Deep Convolutional Networks. CVPR,
  1646–1654. https://doi.org/10.1109/CVPR.2016.182

`model/model_epoch_50.pth`, `data/train.h5`, `Set5/`, and `Set5_mat/`
are not committed. Paths and upstream links are in
`pytorch-vdsr/NOT_VENDORED.txt`. The upstream README also points at
the 291-image training set on Google Drive.

### SRCNN

Dong, C., Loy, C. C., He, K., and Tang, X. 2016. Image Super-Resolution
Using Deep Convolutional Networks. *IEEE Trans. Pattern Anal. Mach.
Intell.* 38 (2): 295–307.
https://doi.org/10.1109/TPAMI.2015.2439281

This is the three-layer CNN the paper cites as the start of CNN
super-resolution, and the model Wang et al. later extended to 3D CT
(3DSRCNN), which Liang et al. say does not transfer to anisotropic
FIB-SEM. Bai et al. (2020) also used SRCNN and FSRCNN ideas to clean
up z-interpolation; this paper's z-step is the VDSR-style CNN instead.

The author Caffe/MATLAB package is
http://mmlab.ie.cuhk.edu.hk/projects/SRCNN.html . It is not a git
repository with a LICENSE file. The often-forked `yjn870/SRCNN-pytorch`
tree also has no LICENSE. Vendored here:

- https://github.com/Lornatang/SRCNN-PyTorch @ `a0a108ea47710118b7a3ba99d72290c409feacff`
- Apache License 2.0 (`srcnn/LICENSE`). Source files name Dakewe
  Biotech Corporation as the copyright holder.
- Weights are not in the repository. The upstream README links a
  Google Drive folder and a Baidu disk
  (https://drive.google.com/drive/folders/17ju2HN7Y6pyPK2CC_AqnAfTOe9_3hCQ8
  and https://pan.baidu.com/s/1yNs4rqIb004-NKEdKBJtYg?pwd=llot).

The network is the standard SRCNN map: 9×9 to 64 channels, 5×5 to 32,
5×5 to 1, ReLU on the first two layers.

### FSRCNN

Dong, C., Loy, C. C., and Tang, X. 2016. Accelerating the
Super-Resolution Convolutional Neural Network. ECCV 2016, 391–407.
https://doi.org/10.1007/978-3-319-46475-6_25
(Liang et al. print the proceedings DOI
https://doi.org/10.1007/978-3-319-46475-6 .)

Author package: http://mmlab.ie.cuhk.edu.hk/projects/FSRCNN.html , again
without a git LICENSE. Vendored here:

- https://github.com/Lornatang/FSRCNN-PyTorch @ `e6f8d53775d93249292fb80eed0af940aa7710c5`
- Apache License 2.0 (`fsrcnn/LICENSE`). Same copyright headers as the
  SRCNN port.
- Same external weight folders as the SRCNN README (Drive and Baidu).
  Nothing under `fsrcnn/results/` is a checkpoint.

The port keeps the paper's hourglass: 5×5 feature extraction to 56
channels, 1×1 shrink to 12, four 3×3 mapping layers, 1×1 expand to 56,
and a 9×9 deconvolution by the scale factor. A more starred TensorFlow
port (https://github.com/Saafke/FSRCNN_Tensorflow) replaces that
deconvolution with a sub-pixel layer and ships frozen graphs; it is
not the architecture cited here, so it is not vendored.
