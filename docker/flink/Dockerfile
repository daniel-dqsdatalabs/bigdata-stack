ARG FLINK_VERSION=1.20.0
FROM flink:${FLINK_VERSION}

ARG openjdk_version="17"
ARG FLINK_VERSION=1.20.0

RUN wget -nv -P $FLINK_HOME/lib/ https://repo1.maven.org/maven2/org/apache/flink/flink-python/${FLINK_VERSION}/flink-python-${FLINK_VERSION}.jar

# install python3 and pip3
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip "openjdk-${openjdk_version}-jdk-headless" && \
    rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

# install PyFlink
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH="${PATH}:${JAVA_HOME}/bin"

RUN pip3 install apache-flink==${FLINK_VERSION}
