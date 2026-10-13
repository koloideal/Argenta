FROM gcr.io/oss-fuzz-base/base-builder-python:v1

# The base image ships Python 3.11 (Ubuntu focal), but Argenta
# requires >=3.12 (PEP 695 generics/type statements). Install a
# standalone CPython via uv — no apt packages needed.
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh \
    && uv python install 3.12 \
    && uv venv --seed --python 3.12 /opt/fuzz-venv \
    && /opt/fuzz-venv/bin/pip install --upgrade pip atheris pyinstaller

COPY . $SRC/argenta
WORKDIR $SRC/argenta
RUN /opt/fuzz-venv/bin/pip install .

COPY .clusterfuzzlite/build.sh $SRC/
