FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.1.3
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:/root/.local/bin:$PATH

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    ffmpeg \
    ca-certificates \
    bzip2 \
    && rm -rf /var/lib/apt/lists/*

# Python 3.12 설치 (PPA 안 씀)
RUN curl -fsSL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o /tmp/miniforge.sh \
    && bash /tmp/miniforge.sh -b -p $CONDA_DIR \
    && rm /tmp/miniforge.sh \
    && conda install -y python=3.12 pip \
    && conda clean -afy

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3

COPY pyproject.toml poetry.lock* ./

RUN poetry env use python3.12 \
    && poetry install --only main --no-root

COPY . .

EXPOSE 8001

CMD ["poetry", "run", "hypercorn", "app.main:app", "--bind", "0.0.0.0:8001"]