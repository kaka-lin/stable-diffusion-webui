FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu18.04

# Ubuntu 18.04: tzdata issue
# set noninteractive installation
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    software-properties-common \
    tzdata \
    locales \
    git \
    build-essential \
    ca-certificates \
    cmake \
    cmake-data \
    pkg-config \
    python3-dev python3-pip python3-setuptools \
    libcurl4 \
    libsm6 \
    libxext6 \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libssl1.0-dev \
    zlib1g-dev \
    unzip \
    curl \
    wget \
    ffmpeg \
    nodejs node-gyp nodejs-dev \
    npm

# Upgrade Node.js to v18.x
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    # upgrade GLIBC to 2.28
    echo "deb http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \ 
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A 54404762BBB6E853 && \
    apt-get update && \   
    apt-get install -y libc6 libc6-dev && \
    # install node 18.x
    apt-get install -y nodejs 

RUN apt-get -y autoremove && \
    apt-get -y autoclean && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

# Set timezone
ENV TZ=Etc/UTC

# Install Miniconda in /opt/conda
ENV PYTHON_VERSION="3.10"
ENV CONDA_PATH="/opt/conda"
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p ${CONDA_PATH} && \
    ${CONDA_PATH}/bin/conda update -n base conda && \
    ${CONDA_PATH}/bin/conda install python=${PYTHON_VERSION} && \
    ${CONDA_PATH}/bin/conda clean -y -a && \
    # init conda for bash and reload the environment
    # Because you nedd run 'conda init' before 'conda activate' in the Dockerfile
    #
    # Enable conda for the for all users (conda initialize)
    ln -s ${CONDA_PATH}/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    # Enable conda for the current user (conda initialize)
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate automatic" >> ~/.bashrc && \
    rm ~/miniconda.sh && \
    rm -rf /temp/*

ENV PATH=${CONDA_PATH}/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/cuda-10.0/lib64:/usr/local/cuda-10.0/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Make RUN commands use `bash --login`:
SHELL [ "bin/bash","--login","-c" ]

# The Environment for Stable Diffusion WebUI 
COPY environment-wsl2.yaml environment-wsl2.yaml
COPY requirements_versions.txt requirements_versions.txt
RUN git config --global --add safe.directory "*"

# Activate the environment and install related packages
RUN conda env create -f environment-wsl2.yaml
RUN conda install cuda -c nvidia
RUN conda activate automatic && \
    pip3 --no-cache-dir install --upgrade pip wheel && \
    # for fix error: ImportError: cannot import name 'packaging' from 'pkg_resources'
    pip3 --no-cache-dir install setuptools==69.5.1 && \
    pip3 install transformers diffusers invisible-watermark --prefer-binary && \
    pip3 install opencv-python-headless && \
    pip3 install -U torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && \
    pip3 install tensorflow==2.13.1 && \
    pip3 install -r requirements_versions.txt --prefer-binary

RUN rm environment-wsl2.yaml && rm requirements_versions.txt

# Setting defaule command arguments for sd_webui
ENV COMMANDLINE_ARGS="--disable-safe-unpickle"

VOLUME /stable-diffusion-webui
WORKDIR /stable-diffusion-webui
