FROM flink:1.20-scala_2.12-java11

# Install required libraries
RUN apt-get update && \
    apt-get install -y libstdc++6 locales dos2unix && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Add Flink dependencies
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.2.0-1.19/flink-connector-kafka-3.2.0-1.19.jar /opt/flink/lib/
ADD https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.8.0/kafka-clients-3.8.0.jar /opt/flink/lib/
ADD https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.20.0/flink-sql-avro-confluent-registry-1.20.0.jar /opt/flink/lib/
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-s3-fs-hadoop/1.20.0/flink-s3-fs-hadoop-1.20.0.jar /opt/flink/lib/
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-table-store-dist/0.2.1/flink-table-store-dist-0.2.1.jar /opt/flink/lib/
ADD https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar /opt/flink/lib/
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-connector-elasticsearch_2.12/1.8.3/flink-connector-elasticsearch_2.12-1.8.3.jar /opt/flink/lib/
ADD https://repo1.maven.org/maven2/com/getindata/flink-http-connector/0.15.0/flink-http-connector-0.15.0.jar /opt/flink/lib/

# configuration file
COPY flink-conf.yaml /opt/flink/conf/flink-conf.yaml

# The Flink image expects dependencies to be owned by the flink user
RUN chown -R flink:flink /opt/flink/lib/