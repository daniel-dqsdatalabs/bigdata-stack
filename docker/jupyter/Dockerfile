FROM quay.io/jupyter/scipy-notebook:latest

USER root

ARG openjdk_version="17"
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jdk-headless" && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    java -version       


ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH="${PATH}:${JAVA_HOME}/bin"

USER ${NB_UID}

# Install python requirements
RUN pip install -U apache-flink==1.20.0
RUN pip install -U pyspark==3.5.0
RUN pip install -U delta-spark==3.2.0
RUN pip install -U deltalake==0.19.1
RUN pip install graphviz==0.20.3


ENV SCALA_VERSION=2.13.12 
ENV ALMOND_VERSION=0.14.0-RC14

# Install almond kernel (Scala)
RUN curl -Lo coursier https://git.io/coursier-cli && \
    chmod +x coursier && \
    ./coursier launch "almond:$ALMOND_VERSION" --scala $SCALA_VERSION -- \
    --install \
    --id scala213 \
    --display-name "Scala (2.13)" \
    </dev/null 2>&1 | grep -v '^Download'



