FROM python:3.10 as build
ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PATH="/usr/src/app/scripts:${PATH}"

WORKDIR /usr/src/app

RUN apt-get update -y && \
    apt install libgl1-mesa-glx -y && \
    apt-get install ffmpeg libsm6 libxext6 -y

RUN pip install -U pip poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /usr/src/app/
RUN poetry install -n --only main && \
    poetry run poe autoinstall-torch-cuda

COPY /scripts /usr/src/app/scripts
RUN chmod +x /usr/src/app/scripts/*

COPY /app /usr/src/app/app
COPY /weights /usr/src/app/weights

ENTRYPOINT [ "start.sh" ]