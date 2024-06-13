# Stable Diffusion web UI - Develop Guide

## 0. Environment

如果要增減所需的套件，則只需修改 [requirements_versions.txt](../requirements_versions.txt) 或是 extension module 各自的 `install.py` 檔案。詳細解說如下:

1. [webui.sh](../webui.sh):

    確認與安裝 Python, torch, torchvision, torchaudio 版本。

2. launch.py -> [launch_utils.prepare_environment](../modules/launch_utils.py#L317):

    再次確認 torch, torchvision 版本及安裝其他所需的套件:

    - clip
    - open_clip
    - xformers
    - ngrok
    - [requirements_versions.txt](../requirements_versions.txt) and [Option] [requirements_npu.txt](../requirements_npu.txt).
    - all of the packages that [extension modules](../extensions/) need:
      [launch_utils.run_extensions_installers](../modules/launch_utils.py#L264)

        > 將會檢查各個 extension module 底下的 `install.py` 檔案

## 1. How to modify UI

- `create_ui()` in modules/ui.py

## 2. Creating new tab (Extension)

> 實際範例請詳見 [extenstions/Segment](../extensions/Segment/)

在 `extensions` floder 新增資料夾，並且新增:
- `install.py`: 這個 tab 所需安裝的相關套件
- `scripts/ui.py`: 
  1. 定義 `on_ui_tab()` 裡面含相關 ui 程式，並返回 `(gradio_component, title, elem_id)
  2. 在最後 call [script_callbacks.on_ui_tabs(on_ui_tabs)](../modules/script_callbacks.py#L473)

    Example:

    ```python
    import gradio as gr

    from modules import shared, paths, script_callbacks


    def on_ui_tabs():
        # <YOUR UI related code, called `gradio component`>

        #  (gradio_component, title, elem_id)
        return [(gradio_component, "New Tab", "new_tab")]


    script_callbacks.on_ui_tabs(on_ui_tabs)
    ```