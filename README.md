# SPOLRE

## Installation

```shell
# Put the dependent tools under the tools folder.
git clone https://github.com/IDEA-Research/OpenSeeD.git
git clone https://github.com/PITI-Synthesis/PITI.git

conda create -n mumo python=3.9 -y
# Install according to your CUDA version
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt

# If there is an issue with the previous pip installation
conda install -c conda-forge mpi4py -y
conda install -c conda-forge pycocotools -y

# If an error is reported after the previous step: ImportError: libmpi.so.12: cannot open shared object file: No such file or directory
conda install -c conda-forge openmpi mpi4py -y

# If CUDA_HOME is None
conda install -c conda-forge cudatoolkit=11.8.0 -y
conda install -c conda-forge cudatoolkit-dev=11.7.0 -y

pip install git+https://github.com/MaureenZOU/detectron2-xyz.git
pip install git+https://github.com/cocodataset/panopticapi.git
cd path/to/OpenSeeD/openseed/body/encoder/ops /home/wgy/multimodal/tools/OpenSeeD/openseed/body/encoder/ops
sh make.sh

# Download checkpoint from the following address and put it under /MuMo/ckpt
https://hkustconnect-my.sharepoint.com/:u:/g/personal/tfwang_connect_ust_hk/EVslpwvzHJxFviyd3bw6KSEBWQ9B9Oqd5xUlemo4BNcHpQ?e=F5450q
https://hkustconnect-my.sharepoint.com/:u:/g/personal/tfwang_connect_ust_hk/ERPFM88nCR5Gna_i81cB_X4BgMyvkVE3uMX7R_w-LcSAEQ?e=EmL4fs
https://github.com/IDEA-Research/OpenSeeD/releases/download/openseed/model_state_dict_swint_51.2ap.pt
```

