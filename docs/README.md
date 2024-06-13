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
$ docker-compose -f docker-compose-dev.yml
$ docker exec -it sd_webui bash
$ python launch.py --listen --precision full --no-half --enable-insecure-extension-access --port 7860 --api
```

### Production mode

```sh
$ docker-compose up -d
```

## Develop Guide

[Stable Diffusion web UI - Develop Guide](./develop.md)