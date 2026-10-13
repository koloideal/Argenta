FROM gcr.io/oss-fuzz-base/base-builder-python:v1

# The base image ships Python 3.11, but Argenta requires >=3.12
# (PEP 695 generics/type statements). Install 3.12 into a venv and
# use it for the project and the fuzz tooling.
RUN apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.12 python3.12-venv python3.12-dev \
    && python3.12 -m venv /opt/fuzz-venv \
    && /opt/fuzz-venv/bin/pip install --upgrade pip atheris pyinstaller

COPY . $SRC/argenta
WORKDIR $SRC/argenta
RUN /opt/fuzz-venv/bin/pip install .

COPY .clusterfuzzlite/build.sh $SRC/
