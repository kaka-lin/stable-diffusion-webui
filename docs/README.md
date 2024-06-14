# Stable Diffusion web UI Docs

## Quick Start

### Prerequisite

1. clone with submodule

    ```
    $ git clone --recursive https://github.com/kaka-lin/stable-diffusion-webui.git
    ```

2. update after clone

    ```
    $ git submodule update --init --recursive
    ```

    ##### Update the submodule to the latest remote commit, as below:

    ```
    $ git submodule update --remote --merge
    ```

### Run on locally

```sh
$ ./webui.sh   
```

### Run with Docker

#### Develop mode

```sh
$ docker-compose -f docker-compose-dev.yml up -d
$ docker exec -it sd_webui bash

# Prerequisite: need to install gradio-image-prompter
$ cd /stable-diffusion-webui/gradio_components/gradio-image-prompter/frontend && npm install
$ cd /stable-diffusion-webui/gradio_components/gradio-image-prompter && npm install && gradio cc install

# Run the server
$ cd /stable-diffusion-webui
$ python launch.py --listen \
    --precision full \
    --no-half \
    --enable-insecure-extension-access \
    --device-id 1 \
    --port 7860 \
    --api
```
- `--device-id <id>`: specify the GPU device id

### Production mode

```sh
# only need run once
$ chmod +x docker-entrypoint.sh 

$ docker-compose up -d
```

> You can use ```$ docker logs sd_webui``` to check the start progress

After running (about one minute), you can access Stable Diffusion WebUI at http://localhost:7860. Enjoy! 😄

## Develop Guide

[Stable Diffusion web UI - Develop Guide](./develop.md)
