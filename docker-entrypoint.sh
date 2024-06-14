#! /bin/bash --login

# start conda environment (because this shell is sub-shell)
conda activate automatic 

# Prerequisite: need to install gradio-image-prompter
cd /stable-diffusion-webui/gradio_components/gradio-image-prompter/frontend && npm install
cd /stable-diffusion-webui/gradio_components/gradio-image-prompter && \
    npm install && \
    /opt/conda/envs/automatic/bin/gradio cc install
cd /stable-diffusion-webui

# Start the  process
# specify the GPU device id: --device-id <id>
python launch.py \
    --listen \
    --precision full \
    --no-half \
    --enable-insecure-extension-access \
    --port 7860 \
    --api
