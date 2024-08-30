# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG REGISTRY=quay.io
ARG OWNER=jupyter
ARG BASE_CONTAINER=$REGISTRY/$OWNER/minimal-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root


ARG openjdk_version="17"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jdk-headless" \
    ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    java -version


ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-arm64
ENV PATH="${PATH}:${JAVA_HOME}/bin"

USER ${NB_UID}

# python packages including IRKernel which gets installed globally.
RUN mamba install --yes -c conda-forge \
    'deltalake' \
    'delta-spark' \
    'pyarrow' \
    'ibis-flink' \
    'ibis-pyspark' \
    'ibis-postgres' \
    'pyspark' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}" && \
    pip install apache-flink \ 
    pip install apache-flink-libraries