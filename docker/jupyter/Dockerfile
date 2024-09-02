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

RUN pip install -U apache-flink==1.20.0 
RUN pip install -U pyspark==3.5.0
RUN pip install delta-spark==3.2.0
RUN pip install deltalake==0.19.1
