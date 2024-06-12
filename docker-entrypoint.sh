#! /bin/bash

# Start the first process
# docker-compose not specify the GPU device id
# python launch.py \
#     --listen \
#     --precision full \
#     --no-half \
#     --enable-insecure-extension-access \
#     --device-id 1 \
#     --port 7860 \
#     --api

# docker-cpmpose specify the GPU device id
python launch.py \
    --listen \
    --precision full \
    --no-half \
    --enable-insecure-extension-access \
    --port 7860 \
    --api
