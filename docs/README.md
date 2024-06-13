# Stable Diffusion web UI Docs

## Quick Start

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