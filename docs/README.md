# 数字岩心生成式路径 / Generative paths for digital rock

μ-CT 提供大视场、较低分辨率的三维灰度；SEM 或 cryo-EM 提供小视场、较高分辨率的二维细节。两套图像经常来自样品的不同位置，只有弱配准，甚至完全不成对。本仓库把几条公开实现放在一起，供润湿性 / 数字岩心流程按这个设定选用。已有的 EDSR、SRGAN、ESRGAN 目录保持原样，作为有监督超分参考。

μ-CT supplies a large field of view at coarser resolution. SEM and cryo-EM supply fine 2-D detail over a small field of view. The two are often acquired at different locations, so pairs are missing or only weakly registered. The trees below are public implementations for that setting. The existing EDSR, SRGAN, and ESRGAN folders stay as supervised super-resolution references.

## 孔隙拓扑警告 / Pore-topology warning

生成器会补出输入里并不存在的孔喉。被幻觉出来的喉道会改变欧拉数、流体–固体接触面积和界面曲率，从而改写渗透率与润湿性解释。把 CycleGAN、StyleGAN2-ADA、P3T-Net、SR3、StableSR、ResShift 的输出当作外观假设：保留原始 μ-CT 几何作为约束，并用孔隙度、两点相关、比表面积或渗透率做独立核对。扩散超分是次级增强，适合已经有一张低分辨率观测的切片；它不能单独充当 μ-CT 与 SEM/cryo-EM 之间的拓扑真值。

Generators fill in pore throats that are not in the measurement. Invented throats change the Euler number, fluid–solid contact area, and interfacial curvature, and they move permeability and wettability interpretations. Treat CycleGAN, StyleGAN2-ADA, P3T-Net, SR3, StableSR, and ResShift outputs as appearance hypotheses. Keep the measured μ-CT geometry as the constraint, and check porosity, two-point correlation, specific surface, or permeability separately. Diffusion super-resolution is a secondary enhancement for a slice that already has a low-resolution observation. It is not a standalone topology measurement for unpaired μ-CT versus SEM/cryo-EM.

许可证与引用见 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)。不下载权重、不启动训练的检查：

```bash
python scripts/smoke_generative_paths.py
```

## 1. CycleGAN + StyleGAN2-ADA（Liu & Mukerji 式多尺度融合）

论文：Liu and Mukerji, Geophysical Research Letters, 2022. https://doi.org/10.1029/2022GL098342

流程是两步。先用 StyleGAN2-ADA 在稀缺的高分辨率 SEM（或 cryo-EM）切片上学习纹理并扩充样本；再用 CycleGAN 把低分辨率 μ-CT 切片和无配对的高分辨率切片互相翻译。循环一致只约束外观往返，不保证孔喉连通。

The workflow has two steps. StyleGAN2-ADA learns texture from scarce high-resolution SEM or cryo-EM patches and draws extra samples. CycleGAN then translates low-resolution μ-CT patches and those high-resolution patches without pairs. Cycle consistency constrains a round trip of appearance. It does not guarantee throat connectivity.

### 官方 StyleGAN2-ADA（首选训练入口）

目录 `stylegan2-ada-pytorch/`，NVIDIA Source Code License，仅限非商业研究或评估。依赖见上游 `README.md`（PyTorch、click、numpy、pillow、scipy、tqdm、requests、imageio、psutil、ninja，以及可选 CUDA 自定义算子）。

```bash
cd stylegan2-ada-pytorch
python dataset_tool.py --source /path/to/sem_or_cryoem_pngs --dest /path/to/sem.zip
python train.py --outdir /path/to/training-runs --data /path/to/sem.zip \
  --gpus 1 --cfg paper256 --mirror 1 --aug ada --kimg 2000 --snap 10 --metrics none
python generate.py --outdir /path/to/stylegan_samples --trunc 1 --seeds 0-99 \
  --network /path/to/network-snapshot.pkl
```

灰度岩心图在送入 `dataset_tool.py` 之前整理成 PNG。官方仓库的 FFHQ 等预训练权重说明写在该目录 `README.md`。Liu & Mukerji 训练好的 SEM StyleGAN 快照在 https://doi.org/10.5281/zenodo.6420099 （`network-snapshot-stylegan.pkl`，与 372 张 1024×1024 SEM 和 24 万张 64×64 μ-CT 子图放在一起）。不要把这些权重提交回 git。

### 通用 CycleGAN（junyanz）

目录 `pytorch-CycleGAN-and-pix2pix/` 已在仓库中。无配对数据布局：

```text
datasets/ct_to_em/
  trainA/   # μ-CT patches
  trainB/   # SEM, cryo-EM, or StyleGAN samples
  testA/
  testB/
```

```bash
cd pytorch-CycleGAN-and-pix2pix
python train.py --dataroot ../datasets/ct_to_em --name ct_to_em \
  --model cycle_gan --dataset_mode unaligned
python test.py --dataroot ../datasets/ct_to_em --name ct_to_em \
  --model cycle_gan --dataset_mode unaligned
```

安装说明见该目录 `README.md`。原始 Torch 实现在 `CycleGAN/`。

### 论文配套脚本

目录 `multiscale-drpnet/` 是 Liu 与 Mukerji 的公开代码（MIT）。其中 `stylegan2-ada/` 仍是 NVIDIA 许可证下的 StyleGAN2-ADA 子集，并带有他们的 `gen_imgs.py`（从 pickle 写出灰度图）。`cyclegan/train.py` 默认读取 `./data/carbonates/train/A` 与 `train/B`，低分辨率边长 64、高分辨率边长 1024、单通道。`cyclegan/recons3d.py` 读取 `./data/recons` 和 `./saved_models/netG_A2B_5.pth`。数据集不要从 Zenodo 直接提交进本仓库。

```bash
cd multiscale-drpnet/stylegan2-ada
# edit gen_imgs.py model_path, then:
python gen_imgs.py

cd ../cyclegan
python train.py --dataroot ./data/carbonates --n_epochs 10 --size_LR 64 --size_HR 1024 --cuda
```

他们的 `train.py` 使用 `unaligned=False`，两个文件夹按排序后的下标对齐读取。科学设定仍是不成对成像；若要随机配对，需要改 `ImageDataset` 的调用。此处保持与上游提交一致。

## 2. P3T-Net（Tang et al., Nature Communications 2025）

论文：https://doi.org/10.1038/s41467-025-66449-6  
代码：`p3t-net/`，来自 https://github.com/KunningTang1/P3T-Net-for-3D-large-image-transfer ，MIT。

P3T-Net 用三个二维模块处理三维体：语义指示、带语义一致的域迁移、第三轴错位修正。它把不同扫描条件的材料图像拉到同一灰度/风格/语义域，面向微 CT / 纳米 CT 的无配对三维迁移。SEM 或 cryo-EM 的纹理融合使用上一节的 CycleGAN + StyleGAN 路径。若要把 cryo-EM 或 SEM 当作目标域，需要先整理成这些脚本期望的体数据与分割。

作者给出的顺序是：

```bash
cd p3t-net
python TrainingDataPrepare.py
python Semantic_Indication_Modules.py
python Test_SemanticModule.py
python Domain_Transfer_and_Semantic_Consistency_Module.py
python Misalignment_Fixing_Module.py
python Inference.py
```

`TrainingDataPrepare.py` 从 `../Testingdata` 读取三个体（源域、目标域、目标域分割），并把图块写到 `../Example/...`。该 GitHub 提交在若干 `imwrite` 路径里使用了反斜杠拼接。Linux 上这些路径不会落进预期文件夹。Zenodo 上的 Linux 包（https://doi.org/10.5281/zenodo.15031051 ，约 2.6 GB，含环境）是作者提供的可运行打包；Docker 镜像约 17 GB。两者都没有放进本仓库。示例数据与作者权重见 https://zenodo.org/records/12633623 与 https://zenodo.org/records/12631632 。依赖包括 PyTorch、scikit-image、OpenCV、NumPy、Matplotlib、tqdm。

## 3. SR3（Saharia et al. 扩散超分）

论文：https://arxiv.org/abs/2104.07636  
项目页：https://iterative-refinement.github.io/

检索时没有找到 Google 公开的官方训练仓库。`sr3/` 是使用最广的非官方 PyTorch 复现（Janspiry，Apache-2.0），README 写明结构与论文有差异（ResNet 块、注意力分辨率、γ 嵌入、后验方差）。不要把它当成官方权重或官方结构。

```bash
cd sr3
pip install -r requirement.txt
python data/prepare_data.py --path /path/to/hr_pngs --out /path/to/rock_16_128 --size 16,128
# point config/sr_sr3.json datasets.train.dataroot at that folder
python sr.py -p train -c config/sr_sr3.json
python infer.py -c config/sr_sr3.json
```

人脸演示图未纳入，见 `sr3/dataset/NOT_VENDORED.txt`。预训练权重链接在上游 README（Google Drive / 百度网盘）。SR3 以低分辨率图像为条件做迭代细化，训练需要高分辨率目标（或由高分辨率下采样得到的低分辨率）。对只有弱配准的 CT 与 cryo-EM，它是条件超分，不是无配对域迁移。

## 4. StableSR

论文：https://arxiv.org/abs/2305.07015  
代码：`stablesr/`，https://github.com/IceClear/StableSR ，S-Lab License 1.0（非商业）。

它在 Stable Diffusion 先验上微调时序编码器，并用可控特征包装（CFW）做真实图像超分。安装以 `environment.yaml` / `requirements.txt` 为准（上游写明 PyTorch 1.12.1、pytorch-lightning 1.4.2，以及 taming-transformers 与 CLIP）。权重：

- 模型卡：https://huggingface.co/Iceclear/StableSR
- Turbo 检查点示例：https://huggingface.co/Iceclear/StableSR/resolve/main/stablesr_turbo.ckpt
- 还需要 CFW / VQGAN 检查点（同一模型卡中的 `vqgan_cfw` 文件）
- 训练起点的 Stable Diffusion 底模：https://huggingface.co/stabilityai/stable-diffusion-2-1-base （CreativeML Open RAIL-M）

最小推理（仍需上述权重，默认从 `inputs/test_example/` 一类目录读图）：

```bash
cd stablesr
python scripts/sr_val_ddpm_text_T_vqganfin_old.py \
  --config configs/stableSRNew/v2-finetune_text_T_512.yaml \
  --ckpt ./stablesr_turbo.ckpt \
  --vqgan_ckpt ./vqgan_cfw_00011.ckpt \
  --init-img ./inputs/test_example \
  --outdir /path/to/out \
  --ddpm_steps 4 --dec_w 0.5 --seed 42 --n_samples 1 --colorfix_type wavelet
```

训练入口是 `python main.py --train --base configs/stableSRNew/v2-finetune_text_T_512.yaml ...`，详见该目录 README。扩散先验会改写孔隙边缘；对岩心切片只把它当作视觉增强。

## 5. ResShift

论文：https://arxiv.org/abs/2307.12348  
代码：`resshift/`，https://github.com/zsyOAOA/ResShift 的 `journal` 分支，S-Lab License 1.0（非商业）。

ResShift 在高分辨率与低分辨率之间移动残差，用很少的扩散步数做超分。`inference_resshift.py` 会从 GitHub Release 下载权重（约数百 MB）到本地 `weights/`，这些文件已被 `.gitignore` 排除。

```bash
cd resshift
pip install -r requirements.txt
python inference_resshift.py -i /path/to/ct_slices -o /path/to/out --task realsr --scale 4 --version v3
```

`--task bicsr` 对应 MATLAB 双三次退化；`--version v3` 是期刊版 4 步模型。训练示例：

```bash
python main.py --cfg_path configs/realsr_swinunet_realesrgan256_journal.yaml --save_dir /path/to/log
```

上游 README 还要求预先放入 VQGAN 权重。演示照片与 `testdata/` 未纳入，见对应 `NOT_VENDORED.txt`。该提交里的 `predict.py`（Cog / Replicate 接口）在 `bicsr` 字典项处有语法错误，保持原样；命令行入口是 `inference_resshift.py` 与 `main.py`。和 SR3、StableSR 一样，ResShift 假设低分辨率观测与高分辨率图像之间存在退化关系。弱配准的 cryo-EM 需要另做配准或无配对迁移后，才能当作监督真值。

## 怎么选 / Which path to run

| 目的 | 入口 |
| --- | --- |
| 用少量 SEM/cryo-EM 扩充高分辨率纹理，再与 μ-CT 无配对融合 | `stylegan2-ada-pytorch/`，然后 `pytorch-CycleGAN-and-pix2pix/` 或 `multiscale-drpnet/cyclegan/` |
| 把不同扫描协议的三维 CT 拉到同一域（伪 3D） | `p3t-net/` |
| 已有低分辨率切片、希望扩散模型做 4× 外观增强 | `sr3/`、`stablesr/` 或 `resshift/` |
| 有配对高低分辨率、要可复现的卷积超分基线 | 原有 `edsr-pytorch/`、`esrgan/`、`srgan/` |
