FROM gcr.io/oss-fuzz-base/base-builder-python:v1

# The base image ships Python 3.11 (Ubuntu focal), but Argenta
# requires >=3.12 (PEP 695 generics/type statements). Install a
# standalone CPython via a pinned uv binary and a seeded venv.
ARG UV_VERSION=0.13.0
RUN curl -LsSf "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz" \
      | tar -xz --strip-components=1 -C /usr/local/bin \
    && uv python install 3.12.11 \
    && uv venv --seed --python 3.12.11 /opt/fuzz-venv \
    && /opt/fuzz-venv/bin/pip install atheris==3.1.0 pyinstaller==6.22.3

COPY . $SRC/argenta
WORKDIR $SRC/argenta
RUN /opt/fuzz-venv/bin/pip install .

COPY .clusterfuzzlite/build.sh $SRC/
