# Stable Diffusion web UI Docs

## Develop Guide

### 0. Environment

1. [webui.sh](../webui.sh):

    確認與安裝 Python, torch, torchvision, torchaudio 版本。

2. launch.py -> [launch_utils.prepare_environment](../modules/launch_utils.py):

    再次確認 torch, torchvision 版本及安裝其他所需的套件:

    - clip
    - open_clip
    - xformers
    - ngrok
    - [requirements_versions.txt](../requirements_versions.txt) and [Option] [requirements_npu.txt](../requirements_npu.txt).
    - all of the packages that [extension modules](../extensions/) need:
      [launch_utils. run_extensions_installers](../modules/launch_utils.py)

        > 將會檢查各個 extension module 底下的 `install.py` 檔案
