FROM python:3.11-slim AS base

USER root

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# # Add a new user with useradd
RUN useradd -m -s /bin/bash -g ${NB_GID} -u $NB_UID $NB_USER

WORKDIR /home/${NB_USER}

# Create folders
RUN mkdir -p datasets notebooks

# Optional: Set permissions if needed
RUN chown -R ${NB_UID}:${NB_GID} datasets notebooks

ENV PATH="/home/${NB_USER}/.local/bin:$PATH"

# install required libs
RUN apt-get update && apt-get install -y --no-install-recommends curl && \ 
    curl -sL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y ca-certificates-java && \
    apt-get install -y openjdk-17-jdk-headless && \
    apt-get install -y gcc && \
    apt-get install -y graphviz && \
    rm -rf /var/lib/apt/lists/* && \
    java -version       

# set java_home
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH="${PATH}:${JAVA_HOME}/bin"

ENV SCALA_VERSION=2.13.10
ENV ALMOND_VERSION=0.13.14

RUN \
    curl -L -o coursier https://git.io/coursier-cli && \
    chmod +x coursier && \
    ./coursier \
        bootstrap \
        -r jitpack \
        sh.almond:scala-kernel_$SCALA_VERSION:$ALMOND_VERSION \
        --sources \
        --default=true \
        -o almond && \
    ./almond --install --global && \
    rm -rf almond couriser 

USER ${NB_USER}

# Install python requirements
RUN pip install -U apache-flink==1.20.0
RUN pip install -U pyspark==3.5.2
RUN pip install -U delta-spark
RUN pip install -U deltalake
RUN pip install -U graphviz
RUN pip install -U ipykernel
RUN pip install -U ipywidgets
RUN pip install -U jupyterhub
RUN pip install -U jupyterlab
RUN pip install -U nbclassic
RUN pip install -U notebook
RUN pip install -U graphviz
RUN pip install -U widgetsnbextension
RUN jupyter server --generate-config

EXPOSE 8888

ENTRYPOINT [ "jupyter", "lab" ]

CMD ["--port=8888", "--no-browser", "--ip=0.0.0.0", "--NotebookApp.token=" ]